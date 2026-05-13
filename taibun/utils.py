import msgpack
from pathlib import Path

data_dir = Path(__file__).parent / "data"
with open(data_dir / "traditional.msgpack", 'rb') as f:
    trad_dict = msgpack.unpackb(f.read(), raw=False)
with open(data_dir / "simplified.msgpack", 'rb') as f:
    simp_dict = {**{v: k for k, v in trad_dict.items() if len(k) == 1}, **msgpack.unpackb(f.read(), raw=False)}
with open(data_dir / "vars.msgpack", 'rb') as f:
    vars_dict = msgpack.unpackb(f.read(), raw=False)

# Convert Traditional to Simplified characters
def to_simplified(input):
    return ''.join(simp_dict.get(c, c) for c in input)

# Convert Simplified to Traditional characters
def to_traditional(input):
    input = ''.join(vars_dict.get(c, c) for c in input)
    traditional = []
    while input:
        for j in range(4, 0, -1):
            if len(input) < j:
                continue
            word = input[:j]
            if word in trad_dict or j == 1:
                traditional.append(trad_dict.get(word, word))
                input = input[j:]
                break
    return "".join(traditional)

# Helper to check if the character is a Chinese character
def is_cjk(input):
    return all(
        0x4E00 <= ord(char) <= 0x9FFF or  # BASIC
        0x3400 <= ord(char) <= 0x4DBF or  # Ext A
        0x20000 <= ord(char) <= 0x2A6DF or  # Ext B
        0x2A700 <= ord(char) <= 0x2EBEF or  # Ext C,D,E,F
        0x30000 <= ord(char) <= 0x323AF or  # Ext G,H
        0x2EBF0 <= ord(char) <= 0x2EE5F  # Ext I
        for char in input
    )