from pathlib import Path
import sys, json, importlib.util, random, hashlib, argparse, subprocess, importlib.metadata
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
spec = importlib.util.spec_from_file_location('cipher', ROOT / 'symmetric_cipher.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)

# Independent string/list implementation of the complete block algorithm.
KEY_SBOX = [9, 4, 10, 11, 13, 1, 8, 5, 6, 2, 0, 3, 12, 14, 15, 7]
def reference_keys(key):
    words = [int(f'{key:016b}'[:8], 2), int(f'{key:016b}'[8:], 2)]
    for rcon in [128, 48, 128, 48]:
        bits = f'{words[-1]:08b}'
        rotated = bits[4:] + bits[:4]
        substituted = KEY_SBOX[int(rotated[:4], 2)] * 16 + KEY_SBOX[int(rotated[4:], 2)]
        first = words[-2] ^ rcon ^ substituted
        words.extend([first, first ^ words[-1]])
    return [words[i] * 256 + words[i + 1] for i in [2, 4, 6, 8]]

def reference_encrypt(p, k):
    for r, subkey in enumerate(reference_keys(k)):
        a = subkey % 10
        b = int(f'{subkey:016b}'[::-1], 2) % 10
        replaced = int(c.SBOXES[a][p // 256]) * 256 + int(c.SBOXES[b][p % 256])
        bits = f'{replaced:016b}'
        shuffled = int(''.join(bits[pos] for pos in c.PATTERNS[r]), 2)
        p = shuffled ^ subkey
    return p

assert c.expand_key(0x2D55)[:2] == [0xBCE9, 0xA34A]  # published S-AES example
assert c.box_indices(3) == (3, 2)  # handout example: reversed 3 = 49152
for box, inv in zip(c.SBOXES, c.INVERSES):
    assert sorted(box.tolist()) == list(range(256))
    assert np.array_equal(inv[box], np.arange(256))
assert len({tuple(box.tolist()) for box in c.SBOXES}) == 10
for pattern in c.PATTERNS:
    assert sorted(pattern) == list(range(16))

rng = random.Random(310)
for _ in range(512):
    p, k = rng.randrange(65536), rng.randrange(65536)
    assert c.expand_key(k) == reference_keys(k)
    encrypted = c.encrypt_block(p, k)
    assert encrypted == reference_encrypt(p, k)
    assert c.decrypt_block(encrypted, k) == p

# Exhaustively check that all plaintext blocks map to distinct outputs for the demo key.
blocks = np.arange(65536, dtype=np.uint32)
for r, subkey in enumerate(c.expand_key(0x2D55)):
    a, b = c.box_indices(subkey)
    replaced = ((c.SBOXES[a][blocks >> 8] << 8) | c.SBOXES[b][blocks & 255]).astype(np.uint32)
    shuffled = np.zeros(65536, dtype=np.uint32)
    for destination, source in enumerate(c.PATTERNS[r]):
        shuffled |= ((replaced >> (15 - source)) & 1) << (15 - destination)
    blocks = shuffled ^ subkey
assert len(np.unique(blocks)) == 65536
for p in [0, 1, 0x3130, 0xFFFF]:
    assert int(blocks[p]) == c.encrypt_block(p, 0x2D55)

key, plaintext = 0x2D55, 0x3130
trace, state = [], plaintext
key_trace = []
left, right = key >> 8, key & 255
for r, (subkey, constant) in enumerate(zip(c.expand_key(key), [0x80, 0x30, 0x80, 0x30])):
    rotated = ((right & 15) << 4) | (right >> 4)
    sub = KEY_SBOX[rotated >> 4] * 16 + KEY_SBOX[rotated & 15]
    key_trace.append(dict(round=r+1, left=left, right=right, rotated=rotated,
                          substituted=sub, constant=constant, g=sub ^ constant, key=subkey))
    left, right = subkey >> 8, subkey & 255
    a, b = c.box_indices(subkey)
    replaced = c.substitute(state, c.SBOXES, a, b)
    bits = f'{replaced:016b}'
    shuffled_bits = ''.join(bits[pos] for pos in c.PATTERNS[r])
    shuffled = int(shuffled_bits, 2)
    result = shuffled ^ subkey
    trace.append(dict(round=r+1, subkey=subkey, reverse=int(f'{subkey:016b}'[::-1],2), a=a, b=b,
        input=state, left_input=state>>8, right_input=state&255, left_output=replaced>>8,
        right_output=replaced&255, substituted=replaced, permuted=shuffled, output=result,
        sub_bits=bits, perm_bits=shuffled_bits))
    state=result

ids=[]
for name, student_id in [('Wahab Yaseen Dawod','1098271'),('Faisal Saud Al Maamari','1075075')]:
    encrypted = c.encrypt_id(student_id, key)
    data = student_id.encode('ascii') + b'\x01'
    previous, rows, recovered = 0, [], b''
    for i, output in enumerate(encrypted):
        p = int.from_bytes(data[i*2:i*2+2], 'big')
        assert output == reference_encrypt(p ^ previous, key)
        recovered += (c.decrypt_block(output, key) ^ previous).to_bytes(2,'big')
        rows.append(dict(block=i+1, plaintext=p, previous=previous, input=p ^ previous, ciphertext=output))
        previous=output
    assert recovered == data
    ids.append(dict(name=name,id=student_id,blocks=rows,ciphertext=encrypted))

base=c.encrypt_block(plaintext,key)
tests=[]
for label,p,k in [('Original',plaintext,key),('Plaintext bit 0',plaintext^1,key),('Key bit 0',plaintext,key^1)]:
    out=c.encrypt_block(p,k)
    tests.append(dict(label=label,plaintext=p,key=k,ciphertext=out,difference=base^out,
                      changed=(base^out).bit_count(),percent=100*(base^out).bit_count()/16))

summary=dict(key=key,plaintext=plaintext,keys=c.expand_key(key),key_trace=key_trace,trace=trace,ids=ids,tests=tests,
    versions=dict(numpy=np.__version__,BitVector='3.5.0'),checks=dict(random_pairs=512,exhaustive_plaintexts=65536,
    sboxes=10,inverse_entries=2560),source_sha256=hashlib.sha256((ROOT/'symmetric_cipher.py').read_bytes()).hexdigest())

# Check the bundled source against the pinned upstream file.
provenance = json.loads((ROOT / 'docs/saes_provenance.json').read_text())
assert hashlib.sha256((ROOT / 'saes.py').read_bytes()).hexdigest() == provenance['sha256']
assert importlib.metadata.version('BitVector') == '3.5.0'

parser = argparse.ArgumentParser(description='Verify the cipher and reproduce the archived results.')
mode = parser.add_mutually_exclusive_group()
mode.add_argument('--check', action='store_true', help='Compare with the archived results (the default).')
mode.add_argument('--write-results', action='store_true', help='Regenerate JSON and console output after the math checks pass.')
args = parser.parse_args()
record = ROOT / 'results/results.json'
output = ROOT / 'results/expected_output.txt'
demo = subprocess.run([sys.executable, str(ROOT / 'symmetric_cipher.py')], cwd=ROOT,
                      capture_output=True, text=True, check=True).stdout
if args.write_results:
    record.write_text(json.dumps(summary, indent=2) + '\n')
    output.write_text(demo)
    print('Regenerated results/results.json and results/expected_output.txt.')
else:
    assert summary == json.loads(record.read_text()), 'Recorded results differ from this source/runtime.'
    assert demo.splitlines() == output.read_text().splitlines(), 'Console output differs from the archive.'
    from zipfile import ZipFile
    files = ['Symmetric_Algorithm_Report.docx', 'symmetric_cipher.py', 'requirements.txt', 'saes.py', 'SAES_LICENSE.txt']
    with ZipFile(ROOT / 'submission/Symmetric_Project_Files.zip') as archive:
        assert archive.namelist() == files
        assert archive.testzip() is None
        for name in files:
            path = ROOT / 'report' / name if name.endswith('.docx') else ROOT / name
            assert archive.read(name) == path.read_bytes(), 'Student package is out of sync: ' + name
    print('Verified recorded results, console output, third-party source and student package.')
print('PASS: 10 S-boxes, 2,560 inverse entries, 4 permutations, 512 independent reference cases,')
print('65,536 distinct plaintext outputs under the example key, both IDs, and both one-bit tests.')
