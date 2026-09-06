"""Validate the v86 room heap with candidate-compiled ABI offsets.

Unloaded rooms are not successes just because a picture appeared: every required
room must have completed its texture/geometry warmup; visible rooms must be
resident, all resident allocations/batches must be owned, and every bank byte
must belong to exactly one live allocation or free span.
"""
V4_KEYS = ('cache_room_size cache_room_loadsize cache_room_lastuse '
           'cache_room_batches cache_room_warmed cache_heap_size cache_heap_free '
           'cache_heap_starts cache_heap_sizes cache_heap_banks cache_heap_faults '
           'cache_block_size cache_block_next cache_block_bytes room_flags '
           'room_loaded room_onscreen_mask').split()


def validate_partition(banks, spans):
    """Pure interval check; no tolerance for holes, overlaps or inter-bank gaps."""
    if not banks or len(banks) > 2:
        raise ValueError('Invalid room-cache banks')
    ordered_banks = sorted(banks)
    for (start, size), following in zip(ordered_banks, ordered_banks[1:] + [(0xffffffff, 0)]):
        if not size or start & 15 or size & 15 or start + size > following[0]:
            raise ValueError('Invalid/overlapping room-cache bank')
    grouped = [[] for _ in banks]
    for start, size, label in spans:
        if not size or start & 15 or size & 15:
            raise ValueError(f'Invalid cache span {label}')
        owners = [i for i, (base, length) in enumerate(banks)
                  if base <= start and start + size <= base + length]
        if len(owners) != 1:
            raise ValueError(f'Cache span outside owned bank: {label}')
        grouped[owners[0]].append((start, size, label))
    for (base, length), group in zip(banks, grouped):
        position = base
        for start, size, label in sorted(group):
            if start != position:
                raise ValueError(f'Cache hole/overlap before {label}')
            position += size
        if position != base + length:
            raise ValueError('Unaccounted room-cache bytes')


def inspect_cache(result, offsets, elf, address, word, half, physical, count, rooms):
    if elf.symbols['g_BgCacheHeap'][1] != offsets['cache_heap_size']:
        raise ValueError('Room-cache heap ABI mismatch')
    cache = {name: word(address('g_BgCache' + symbol)) for name, symbol in (
        ('mode','Mode'), ('epoch','Epoch'), ('misses','Misses'), ('evictions','Evictions'),
        ('load_failures','LoadFailures'), ('preload_skipped','PreloadSkipped'))}
    result['room_cache'] = cache
    if 'g_BgCacheIdleEvictions' in elf.symbols:
        cache['idle_reuse_evictions'] = word(address('g_BgCacheIdleEvictions'))
    if cache['mode'] != 3:
        return
    heap = address('g_BgCacheHeap')
    bankcount = word(heap + offsets['cache_heap_banks'])
    if not 1 <= bankcount <= 2 or not 0 < count < 4096:
        raise ValueError('Invalid active room cache')
    banks = [(word(heap + offsets['cache_heap_starts'] + i * 4),
              word(heap + offsets['cache_heap_sizes'] + i * 4)) for i in range(bankcount)]
    for base, length in banks:
        physical(base, length)
    cache['banks'] = [{'start':hex(base),'bytes':length} for base,length in banks]
    cache['allocator_faults'] = word(heap + offsets['cache_heap_faults'])
    cache['rooms'] = []
    cache['missing_visible_rooms'] = []
    metadata = word(address('g_BgCacheRooms'))
    physical(metadata, count * offsets['cache_room_size'])
    byroom = {item['room']: item for item in result['room_allocations']}
    spans = []
    result['rooms_missing_vertex_batches'] = []
    for i in range(1, count):
        record = metadata + i * offsets['cache_room_size']
        room = rooms + i * offsets['room_size']
        expected = word(record + offsets['cache_room_batches'])
        flags = half(room + offsets['room_flags'])
        loaded = half(room + offsets['room_loaded'])
        allocation = byroom.get(i)
        if bool(loaded) != bool(allocation):
            raise ValueError(f'Room {i} residency flag/pointer mismatch')
        if flags & offsets['room_onscreen_mask'] and not allocation:
            cache['missing_visible_rooms'].append(i)
        cache['rooms'].append(dict(room=i, loadsize=word(record + offsets['cache_room_loadsize']),
            lastuse=word(record + offsets['cache_room_lastuse']), expected_batches=expected,
            warmed=word(record + offsets['cache_room_warmed']), visible=bool(flags & offsets['room_onscreen_mask'])))
        if allocation:
            spans.append((int(allocation['gfxdata'],16),allocation['gfx_bytes'],f'room{i}/gfx'))
            actual = allocation['numvtxbatches'] or 0
            if actual != expected:
                result['rooms_missing_vertex_batches'].append(i)
            if allocation['vtxbatches']:
                spans.append((int(allocation['vtxbatches'],16),
                    (actual * offsets['batch_size'] + 15) & ~15,f'room{i}/batches'))
        elif word(room + offsets['room_batches']):
            raise ValueError(f'Unloaded room {i} retains vertex batches')
    node = word(heap + offsets['cache_heap_free'])
    seen = set()
    previous = 0
    free = 0
    free_spans = []
    while node:
        if node in seen or len(seen) > count * 2 + 4 or node <= previous:
            raise ValueError('Cyclic/unsorted cache free list')
        physical(node, offsets['cache_block_size'])
        seen.add(node)
        size = word(node + offsets['cache_block_bytes'])
        spans.append((node,size,'free'))
        free_spans.append({'start':hex(node),'bytes':size})
        free += size
        previous = node
        node = word(node + offsets['cache_block_next'])
    validate_partition(banks,spans)
    cache['free_bytes'] = free
    cache['free_spans'] = free_spans
    cache['largest_free_span'] = max((span['bytes'] for span in free_spans), default=0)
    cache['partition_valid'] = True
