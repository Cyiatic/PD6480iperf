// Bounded ED64 X-series volatile-ROM transport experiment. Protocol derived
// from the local ed64-x-pub CommandProcessor.cs (cmdW/cmdR/cmdt/cmds, BE words,
// lengths in 512-byte sectors). Does not flash FPGA/firmware or write N64 RAM.
// Unlike a successful host write, matching readback proves cart data arrived.
using System;
using System.Diagnostics;
using System.IO;
using System.IO.Ports;
using System.Security.Cryptography;
using System.Text;
using System.Threading;

internal static class VerifiedEd64
{
    static SerialPort port;
    static Stopwatch clock = Stopwatch.StartNew();
    static Timer deadline;

    static void Log(string message) { Console.WriteLine(clock.ElapsedMilliseconds + "ms " + message); Console.Out.Flush(); }
    static void PutBE(byte[] data, int offset, uint value) {
        data[offset] = (byte)(value >> 24); data[offset+1] = (byte)(value >> 16);
        data[offset+2] = (byte)(value >> 8); data[offset+3] = (byte)value;
    }
    static byte[] Packet(char command, uint address, int bytes) {
        if (bytes < 0 || bytes % 512 != 0) throw new ArgumentException("Sector-aligned length required");
        byte[] packet = new byte[16];
        packet[0] = (byte)'c'; packet[1] = (byte)'m'; packet[2] = (byte)'d'; packet[3] = (byte)command;
        PutBE(packet,4,address); PutBE(packet,8,(uint)(bytes/512));
        return packet;
    }
    static void Send(char command, uint address, int bytes) {
        byte[] packet = Packet(command,address,bytes);
        port.Write(packet,0,packet.Length);
    }
    static byte[] ReadExactly(int count) {
        byte[] data = new byte[count]; int done = 0;
        while (done < count) {
            int received = port.Read(data,done,Math.Min(4096,count-done));
            if (received <= 0) throw new IOException("No read progress at " + done);
            done += received;
        }
        return data;
    }
    static void Ping() {
        Send('t',0,0);
        byte[] response = ReadExactly(16);
        string prefix = Encoding.ASCII.GetString(response,0,3);
        if (!((prefix == "cmd" || prefix == "CMD" || prefix == "RSP" || prefix == "rsp")
                && response[3] == (byte)'r')) throw new IOException("Unexpected test reply " + BitConverter.ToString(response));
    }
    static void CheckBlock(byte[] rom, int offset, int length) {
        uint address = 0x10000000u+(uint)offset;
        Log("WRITE begin offset="+offset+" bytes="+length);
        Send('W',address,length);
        for (int done=0; done<length;) {
            int count=Math.Min(4096,length-done);
            port.Write(rom,offset+done,count);
            done += count;
            Thread.Sleep(1);
        }
        Log("READBACK begin offset="+offset);
        Send('R',address,length);
        byte[] actual = ReadExactly(length);
        for (int i=0;i<length;i++) if (actual[i]!=rom[offset+i])
            throw new IOException("Readback mismatch at ROM byte "+(offset+i));
        Ping();
        Log("MATCH offset="+offset+" bytes="+length);
    }
    static string Hash(byte[] data) {
        using (SHA256 sha=SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(data)).Replace("-","").ToLowerInvariant();
    }
    static void SelfTest() {
        string actual=BitConverter.ToString(Packet('W',0x10004000u,65536));
        if (actual!="63-6D-64-57-10-00-40-00-00-00-00-80-00-00-00-00") throw new Exception("Packet encoding failed");
        try { Packet('R',0,513); throw new Exception("Bad alignment accepted"); } catch (ArgumentException) {}
        if (Hash(new byte[0])!="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855") throw new Exception("SHA failed");
        Console.WriteLine("PASS packet bytes, alignment rejection, SHA256; no device accessed");
    }
    static int Main(string[] args) {
        if (args.Length==1 && args[0]=="self-test") { SelfTest(); return 0; }
        if (args.Length!=4 || (args[0]!="probe" && args[0]!="upload-start") || args[1]!="COM3") {
            Console.Error.WriteLine("Use: probe|upload-start COM3 <32MiB ROM> <expected SHA256>, or self-test"); return 2;
        }
        byte[] rom=File.ReadAllBytes(args[2]);
        if (rom.Length!=33554432 || rom[0]!=0x80 || rom[1]!=0x37 || rom[2]!=0x12 || rom[3]!=0x40
                || Hash(rom)!=args[3].ToLowerInvariant()) { Console.Error.WriteLine("ROM identity mismatch"); return 2; }
        bool upload=args[0]=="upload-start";
        // Last-resort process bound includes hung SerialPort.Dispose/driver I/O.
        deadline=new Timer(delegate { Console.Error.WriteLine("DEADLINE: transport/close not complete"); Console.Error.Flush(); Environment.Exit(124); },null,upload?300000:30000,Timeout.Infinite);
        int result=1;
        try {
            Log("ROM SHA256 "+Hash(rom)+" mode="+args[0]);
            port=new SerialPort("COM3"); port.ReadTimeout=3000; port.WriteTimeout=3000;
            port.Open(); Log("OPEN COM3");
            // Cold menu startup can outlast the fixed power-on dwell. Retry
            // only the read-only handshake before issuing any volatile write.
            for (int attempt=1;;attempt++) {
                try { Ping(); Log("PING matched attempt="+attempt); break; }
                catch (TimeoutException) {
                    Log("PING timeout attempt="+attempt);
                    if (attempt==4) throw;
                    Thread.Sleep(250);
                }
            }
            if (!upload) {
                CheckBlock(rom,0,512); CheckBlock(rom,512,4096);
                CheckBlock(rom,65536,65536); CheckBlock(rom,131072,131072);
                Log("PROBE_ALL_MATCHED; no start command sent");
            } else {
                for (int offset=0;offset<rom.Length;offset+=65536) CheckBlock(rom,offset,65536);
                Log("ALL_33554432_BYTES_READBACK_MATCHED SHA256 "+Hash(rom));
                // Protocol's zero-argument cmd-s matches saved UNFLoader path;
                // no save filename packet or save-type/header modification.
                Send('s',0,0); Log("START_COMMAND_SENT; inspect video for actual boot");
            }
            result=0;
        } catch (Exception error) { Console.Error.WriteLine(clock.ElapsedMilliseconds+"ms FAILED "+error); }
        finally {
            if (port!=null) { Log("CLOSE begin"); port.Dispose(); Log("CLOSE returned"); }
            deadline.Dispose();
        }
        Log("EXIT "+result);
        return result;
    }
}
