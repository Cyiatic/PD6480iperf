"""Inventory reachable Git payloads for publication; never print file contents."""
import argparse
import collections
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROM_MAGIC = (bytes.fromhex("80371240"), bytes.fromhex("37804012"), bytes.fromhex("40123780"))
BAD_EXT = {".z64", ".n64", ".v64", ".rom", ".iso", ".mp4", ".ts", ".m2ts", ".mkv", ".avi", ".mov", ".wmv", ".webm", ".state", ".savestate"}
SOURCE_EXT = {".c", ".h", ".s", ".ld", ".md", ".txt", ".json", ".csv", ".py", ".ps1", ".sh", ".xml", ".yml", ".yaml", ".toml", ".html", ".rst", ".patch", ".diff"}

def git(repo, *args, data=None):
    return subprocess.check_output(["git", "-C", str(repo), *args], input=data)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    raw = git(args.repo, "rev-list", "--objects", "--all")
    meta = git(args.repo, "cat-file", "--batch-check=%(objecttype) %(objectname) %(objectsize) %(rest)", data=raw)
    blobs = []
    for line in meta.decode("utf-8", "replace").splitlines():
        kind, oid, size, *name = line.split(" ", 3)
        if kind == "blob":
            blobs.append({"oid": oid, "bytes": int(size), "path": name[0] if name else ""})
    print(json.dumps({"reachable_blobs": len(blobs), "phase": "payload inspection"}), flush=True)
    batch = subprocess.Popen(["git", "-C", str(args.repo), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    def blob_body(oid):
        batch.stdin.write(oid.encode() + b"\n")
        batch.stdin.flush()
        header = batch.stdout.readline().split()
        if len(header) != 3 or header[1] != b"blob":
            raise RuntimeError("Invalid blob response")
        size = int(header[2])
        chunks = []
        remaining = size
        while remaining:
            part = batch.stdout.read(remaining)
            if not part:
                raise RuntimeError("Truncated blob")
            chunks.append(part)
            remaining -= len(part)
        if batch.stdout.read(1) != b"\n":
            raise RuntimeError("Invalid blob delimiter")
        return b"".join(chunks)
    ext_counts = collections.Counter()
    remove, review, archives = [], [], []
    for entry in blobs:
        path = entry["path"]
        lower = path.lower()
        ext = Path(path).suffix.lower()
        ext_counts[ext] += 1
        reason = None
        if ext in BAD_EXT:
            reason = "ROM/capture/state filename"
        elif re.search(r"(^|/)(\.env(?:\..+)?|credentials(?:\..+)?|secrets?(?:\..+)?)$", lower):
            reason = "local credential/config filename"
        elif ext in {".pem", ".pfx", ".p12", ".key"}:
            reason = "key-material filename needs exclusion/review"
        if reason:
            remove.append({**entry, "reason": reason})
        # Inspect every non-source payload, plus ROM-sized suspicious source.
        if ext in SOURCE_EXT and entry["bytes"] < 32 * 1024 * 1024:
            continue
        body = blob_body(entry["oid"])
        if body[:4] in ROM_MAGIC and len(body) >= 1024 * 1024:
            if not reason:
                remove.append({**entry, "reason": "N64 ROM magic"})
        if body.startswith((b"MZ", b"\x7fELF")):
            review.append({**entry, "kind": "host/object executable"})
        if ext in {".bin", ".eep", ".fla", ".sra"}:
            review.append({**entry, "kind": "binary/save payload"})
        if body.startswith(b"PK\x03\x04"):
            members = []
            with zipfile.ZipFile(io.BytesIO(body)) as zf:
                for info in zf.infolist():
                    record = {"name": info.filename, "bytes": info.file_size}
                    if info.is_dir():
                        members.append(record)
                        continue
                    with zf.open(info) as stream:
                        prefix = stream.read(4)
                    record["blocked_payload"] = Path(info.filename).suffix.lower() in BAD_EXT or prefix in ROM_MAGIC
                    if info.file_size <= 64 * 1024 * 1024:
                        record["sha256"] = hashlib.sha256(zf.read(info)).hexdigest()
                    if record["blocked_payload"]:
                        remove.append({**entry, "reason": "archive contains ROM/capture/state", "member": info.filename})
                    members.append(record)
            archives.append({**entry, "members": members})
    batch.stdin.close()
    batch.stdout.close()
    if batch.wait() != 0:
        raise RuntimeError("Blob batch reader failed")
    report = {
        "scope": "All reachable refs; blob filenames, non-source payload magic, ZIP member inspection. Separate credential scanner required.",
        "refs": git(args.repo, "for-each-ref", "--format=%(refname) %(objectname)").decode().splitlines(),
        "blob_count": len(blobs),
        "blob_uncompressed_bytes": sum(x["bytes"] for x in blobs),
        "extensions": dict(ext_counts.most_common()),
        "remove": remove,
        "review": review,
        "archives": archives,
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("blob_count", "blob_uncompressed_bytes")}))
    print(json.dumps({"remove": remove, "review": review, "archives": [{"path": x["path"], "members": [m["name"] for m in x["members"]]} for x in archives]}, indent=2))

if __name__ == "__main__":
    main()
