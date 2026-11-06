"""Minimal ISO9660 patcher: copy the original ISO, then replace files.
A file that still fits in its original sector allocation is written in place;
a larger one is appended at the end of the volume and its directory record
(and the PVD volume size) is updated.  UDF is not touched (PS2 reads ISO9660)."""
import struct, os, shutil

SECT = 2048

def walk(f):
    """yield (path, rec_abs_offset, lba, size) for every file."""
    f.seek(16 * SECT); pvd = f.read(SECT); assert pvd[1:6] == b'CD001'
    root = pvd[156:156 + 34]
    stack = [('', struct.unpack_from('<I', root, 2)[0], struct.unpack_from('<I', root, 10)[0])]
    while stack:
        base, lba, size = stack.pop()
        f.seek(lba * SECT); d = f.read(size); i = 0
        while i < len(d):
            L = d[i]
            if L == 0:
                i = (i // SECT + 1) * SECT; continue
            nl = d[i + 32]; name = d[i + 33:i + 33 + nl]
            flags = d[i + 25]
            rl, rs = struct.unpack_from('<I', d, i + 2)[0], struct.unpack_from('<I', d, i + 10)[0]
            if name not in (b'\0', b'\1'):
                nm = name.decode('ascii')
                if flags & 2: stack.append((base + '/' + nm, rl, rs))
                else: yield (base + '/' + nm.split(';')[0], lba * SECT + i, rl, rs)
            i += L

def patch(src_iso, dst_iso, files, log=print):
    """files: dict iso_path (e.g. '/DATACMN/E0_010.BIN') -> bytes"""
    if not os.path.exists(dst_iso) or os.path.getsize(dst_iso) < os.path.getsize(src_iso)\
            or open(dst_iso, 'rb').read(SECT * 17) != open(src_iso, 'rb').read(SECT * 17):
        shutil.copyfile(src_iso, dst_iso)
    orig_size = os.path.getsize(src_iso)
    with open(src_iso, 'rb') as s:
        recs = {p: (o, l, z) for p, o, l, z in walk(s)}
    with open(dst_iso, 'r+b') as f:
        f.truncate(orig_size)
        # restore every touched record/data region from the original first (idempotent rebuilds)
        with open(src_iso, 'rb') as s:
            for p in files:
                o, l, z = recs[p]
                s.seek(o); rec = s.read(34); f.seek(o); f.write(rec)
        end = orig_size // SECT
        moved = 0
        for p in sorted(files):
            data = files[p]; o, lba, size = recs[p]
            alloc = (size + SECT - 1) // SECT
            if (len(data) + SECT - 1) // SECT <= alloc:
                f.seek(lba * SECT); f.write(data + bytes(alloc * SECT - len(data)))
                nl = lba
            else:
                nl = end; f.seek(nl * SECT); f.write(data + bytes((-len(data)) % SECT))
                end += (len(data) + SECT - 1) // SECT; moved += 1
            f.seek(o + 2); f.write(struct.pack('<I', nl) + struct.pack('>I', nl)
                                   + struct.pack('<I', len(data)) + struct.pack('>I', len(data)))
        f.seek(16 * SECT); pvd = bytearray(f.read(SECT))
        struct.pack_into('<I', pvd, 80, end); struct.pack_into('>I', pvd, 84, end)
        f.seek(16 * SECT); f.write(pvd)
        f.truncate(end * SECT)
    log('ISO: %d files replaced (%d appended), %d sectors' % (len(files), moved, end))
