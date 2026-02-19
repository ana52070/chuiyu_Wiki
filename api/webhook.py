"""
webhook.py
企业微信消息回调入口（Vercel Serverless Function）
"""

import os
import time
import random
import string
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# 导入同目录模块
import sys
sys.path.insert(0, os.path.dirname(__file__))
from wxwork import WXBizMsgCrypt
from rag import query as rag_query


# ── 从环境变量读取配置 ─────────────────────────────────
CORP_ID      = os.environ["WXWORK_CORP_ID"]       # ww85c7eda8f9ffd53c
AGENT_ID     = os.environ["WXWORK_AGENT_ID"]       # 1000002
CORP_SECRET  = os.environ["WXWORK_SECRET"]
WX_TOKEN     = os.environ["WXWORK_TOKEN"]          # 自己设置的 Token
WX_AES_KEY   = os.environ["WXWORK_AES_KEY"]        # 自己设置的 EncodingAESKey
# ──────────────────────────────────────────────────────

crypt = WXBizMsgCrypt(WX_TOKEN, WX_AES_KEY, CORP_ID)


def get_access_token() -> str:
    """获取企业微信 access_token"""
    import requests
    url = (
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        f"?corpid={CORP_ID}&corpsecret={CORP_SECRET}"
    )
    resp = requests.get(url, timeout=10)
    return resp.json()["access_token"]


def send_message(to_user: str, content: str):
    """发送文本消息给用户"""
    import requests
    token = get_access_token()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
    payload = {
        "touser": to_user,
        "msgtype": "text",
        "agentid": int(AGENT_ID),
        "text": {"content": content},
    }
    requests.post(url, json=payload, timeout=15)


def parse_message(xml_str: str) -> dict:
    """解析企业微信消息 XML"""
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """企业微信回调 URL 验证"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        msg_signature = params.get("msg_signature", [""])[0]
        timestamp     = params.get("timestamp", [""])[0]
        nonce         = params.get("nonce", [""])[0]
        echostr       = params.get("echostr", [""])[0]

        if crypt.verify_signature(msg_signature, timestamp, nonce, echostr):
            decrypted = crypt.decrypt(echostr)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(decrypted.encode())
        else:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")

    def do_POST(self):
        """接收并处理企业微信消息"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        msg_signature = params.get("msg_signature", [""])[0]
        timestamp     = params.get("timestamp", [""])[0]
        nonce         = params.get("nonce", [""])[0]

        # 读取请求体
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        # 从 XML 中取出加密消息
        root = ET.fromstring(body)
        encrypted = root.find("Encrypt").text

        # 验证签名
        if not crypt.verify_signature(msg_signature, timestamp, nonce, encrypted):
            self.send_response(403)
            self.end_headers()
            return

        # 解密
        xml_str = crypt.decrypt(encrypted)
        msg = parse_message(xml_str)

        # 只处理文本消息
        if msg.get("MsgType") == "text":
            user_id  = msg.get("FromUserName", "")
            question = msg.get("Content", "").strip()

            # 异步思路：先回复"正在思考"，再主动推送结果
            # 受限于 Vercel Serverless 超时，直接在这里同步处理
            answer = rag_query(question)
            send_message(user_id, answer)

        # 企业微信要求回复 "success"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"success")

    def log_message(self, format, *args):
        pass  # 关闭默认日志输出