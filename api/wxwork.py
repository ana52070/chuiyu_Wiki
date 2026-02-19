"""
wxwork.py
企业微信消息加解密工具
"""

import hashlib
import base64
import struct
import socket
import time
import random
import string
from Crypto.Cipher import AES
import xml.etree.ElementTree as ET


class WXBizMsgCrypt:
    def __init__(self, token: str, encoding_aes_key: str, corp_id: str):
        self.token = token
        self.key = base64.b64decode(encoding_aes_key + "=")
        self.corp_id = corp_id

    def _pkcs7_decode(self, data: bytes) -> bytes:
        pad = data[-1]
        return data[:-pad]

    def _pkcs7_encode(self, data: bytes) -> bytes:
        block_size = 32
        pad = block_size - len(data) % block_size
        return data + bytes([pad] * pad)

    def verify_signature(self, signature: str, timestamp: str, nonce: str, data: str = "") -> bool:
        items = sorted([self.token, timestamp, nonce, data])
        s = hashlib.sha1("".join(items).encode()).hexdigest()
        return s == signature

    def decrypt(self, encrypted: str) -> str:
        data = base64.b64decode(encrypted)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key[:16])
        decrypted = self._pkcs7_decode(cipher.decrypt(data))
        # 去掉前16字节随机串，读4字节消息长度
        content = decrypted[16:]
        msg_len = struct.unpack(">I", content[:4])[0]
        return content[4:4 + msg_len].decode("utf-8")

    def encrypt(self, reply_msg: str) -> str:
        random_str = "".join(random.choices(string.ascii_letters, k=16)).encode()
        msg = reply_msg.encode()
        msg_len = struct.pack(">I", len(msg))
        corp_id = self.corp_id.encode()
        plain = random_str + msg_len + msg + corp_id
        data = self._pkcs7_encode(plain)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key[:16])
        return base64.b64encode(cipher.encrypt(data)).decode()

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