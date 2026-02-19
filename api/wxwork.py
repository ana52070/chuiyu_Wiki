"""
wxwork.py - 企业微信加解密（纯 Python 标准库实现，无需 pycryptodome）
"""

import hashlib
import base64
import struct
import time
import random
import string
import xml.etree.ElementTree as ET

# ── 纯 Python AES 实现 ─────────────────────────────────────────────────────

SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]

SBOX_INV = [0] * 256
for i, v in enumerate(SBOX):
    SBOX_INV[v] = i

RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36]

def _xtime(a):
    return ((a << 1) ^ 0x1b) & 0xff if a & 0x80 else (a << 1) & 0xff

def _gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1: p ^= a
        a = _xtime(a)
        b >>= 1
    return p

def _key_expand(key: bytes):
    w = [list(key[i*4:(i+1)*4]) for i in range(len(key)//4)]
    n = len(w)
    r = (n + 6 + 1) * 4
    for i in range(n, r):
        t = w[i-1][:]
        if i % n == 0:
            t = [SBOX[t[1]]^RCON[i//n-1], SBOX[t[2]], SBOX[t[3]], SBOX[t[0]]]
        elif n > 6 and i % n == 4:
            t = [SBOX[x] for x in t]
        w.append([w[i-n][j]^t[j] for j in range(4)])
    return [bytes(w[i*4]+ w[i*4+1]+ w[i*4+2]+ w[i*4+3]) for i in range(r//4)]

def _add_round_key(state, rk):
    return bytes(state[i] ^ rk[i] for i in range(16))

def _sub_bytes(state):
    return bytes(SBOX[b] for b in state)

def _shift_rows(s):
    return bytes([s[0],s[5],s[10],s[15], s[4],s[9],s[14],s[3],
                  s[8],s[13],s[2],s[7],  s[12],s[1],s[6],s[11]])

def _mix_columns(s):
    def col(a,b,c,d):
        return (_xtime(a)^_xtime(b)^b^c^d,
                a^_xtime(b)^_xtime(c)^c^d,
                a^b^_xtime(c)^_xtime(d)^d,
                _xtime(a)^a^b^c^_xtime(d))
    out=[]
    for i in range(4):
        out+=list(col(s[i],s[i+4],s[i+8],s[i+12]))
    r=[0]*16
    for i in range(4):
        for j in range(4):
            r[j*4+i]=out[i*4+j]
    return bytes(r)

def _inv_shift_rows(s):
    return bytes([s[0],s[13],s[10],s[7], s[4],s[1],s[14],s[11],
                  s[8],s[5],s[2],s[15],  s[12],s[9],s[6],s[3]])

def _inv_sub_bytes(state):
    return bytes(SBOX_INV[b] for b in state)

def _inv_mix_columns(s):
    def col(a,b,c,d):
        return (_gmul(a,14)^_gmul(b,11)^_gmul(c,13)^_gmul(d,9),
                _gmul(a,9)^_gmul(b,14)^_gmul(c,11)^_gmul(d,13),
                _gmul(a,13)^_gmul(b,9)^_gmul(c,14)^_gmul(d,11),
                _gmul(a,11)^_gmul(b,13)^_gmul(c,9)^_gmul(d,14))
    t=[]
    for i in range(4):
        t+=list(col(s[i],s[i+4],s[i+8],s[i+12]))
    r=[0]*16
    for i in range(4):
        for j in range(4):
            r[j*4+i]=t[i*4+j]
    return bytes(r)

def _aes_encrypt_block(block: bytes, round_keys) -> bytes:
    nr = len(round_keys) - 1
    state = _add_round_key(block, round_keys[0])
    for r in range(1, nr):
        state = _mix_columns(_shift_rows(_sub_bytes(state)))
        state = _add_round_key(state, round_keys[r])
    state = _add_round_key(_shift_rows(_sub_bytes(state)), round_keys[nr])
    return state

def _aes_decrypt_block(block: bytes, round_keys) -> bytes:
    nr = len(round_keys) - 1
    state = _add_round_key(block, round_keys[nr])
    for r in range(nr-1, 0, -1):
        state = _inv_mix_columns(_add_round_key(_inv_sub_bytes(_inv_shift_rows(state)), round_keys[r]))
    state = _add_round_key(_inv_sub_bytes(_inv_shift_rows(state)), round_keys[0])
    return state

def _aes_cbc_encrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    rk = _key_expand(key)
    out = b""
    prev = iv
    for i in range(0, len(data), 16):
        block = bytes(data[i+j] ^ prev[j] for j in range(16))
        prev = _aes_encrypt_block(block, rk)
        out += prev
    return out

def _aes_cbc_decrypt(key: bytes, iv: bytes, data: bytes) -> bytes:
    rk = _key_expand(key)
    out = b""
    prev = iv
    for i in range(0, len(data), 16):
        block = data[i:i+16]
        dec = _aes_decrypt_block(block, rk)
        out += bytes(dec[j] ^ prev[j] for j in range(16))
        prev = block
    return out

# ── 企业微信加解密 ──────────────────────────────────────────────────────────

class WXBizMsgCrypt:
    def __init__(self, token: str, encoding_aes_key: str, corp_id: str):
        self.token = token
        self.key = base64.b64decode(encoding_aes_key + "=")
        self.corp_id = corp_id

    def _pkcs7_decode(self, data: bytes) -> bytes:
        pad = data[-1]
        return data[:-pad]

    def _pkcs7_encode(self, data: bytes) -> bytes:
        pad = 32 - len(data) % 32
        return data + bytes([pad] * pad)

    def verify_signature(self, signature: str, timestamp: str, nonce: str, data: str = "") -> bool:
        items = sorted([self.token, timestamp, nonce, data])
        s = hashlib.sha1("".join(items).encode()).hexdigest()
        return s == signature

    def decrypt(self, encrypted: str) -> str:
        data = base64.b64decode(encrypted)
        iv = self.key[:16]
        decrypted = _aes_cbc_decrypt(self.key, iv, data)
        decrypted = self._pkcs7_decode(decrypted)
        content = decrypted[16:]
        msg_len = struct.unpack(">I", content[:4])[0]
        return content[4:4 + msg_len].decode("utf-8")

    def encrypt(self, reply_msg: str) -> str:
        random_str = "".join(random.choices(string.ascii_letters, k=16)).encode()
        msg = reply_msg.encode()
        msg_len = struct.pack(">I", len(msg))
        corp_id = self.corp_id.encode()
        plain = self._pkcs7_encode(random_str + msg_len + msg + corp_id)
        iv = self.key[:16]
        encrypted = _aes_cbc_encrypt(self.key, iv, plain)
        return base64.b64encode(encrypted).decode()

    def make_reply_xml(self, encrypted: str, timestamp: str, nonce: str) -> str:
        sign_items = sorted([self.token, timestamp, nonce, encrypted])
        signature = hashlib.sha1("".join(sign_items).encode()).hexdigest()
        return (
            f"<xml>"
            f"<Encrypt><![CDATA[{encrypted}]]></Encrypt>"
            f"<MsgSignature><![CDATA[{signature}]]></MsgSignature>"
            f"<TimeStamp>{timestamp}</TimeStamp>"
            f"<Nonce><![CDATA[{nonce}]]></Nonce>"
            f"</xml>"
        )