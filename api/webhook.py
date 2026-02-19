"""
webhook.py - Vercel Serverless Function
企业微信消息回调入口，使用 BaseHTTPRequestHandler 格式
"""

import os
import sys
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(__file__))
from wxwork import WXBizMsgCrypt
from rag import query as rag_query

CORP_ID     = os.environ.get("WXWORK_CORP_ID", "")
AGENT_ID    = os.environ.get("WXWORK_AGENT_ID", "")
CORP_SECRET = os.environ.get("WXWORK_SECRET", "")
WX_TOKEN    = os.environ.get("WXWORK_TOKEN", "")
WX_AES_KEY  = os.environ.get("WXWORK_AES_KEY", "")

crypt = WXBizMsgCrypt(WX_TOKEN, WX_AES_KEY, CORP_ID)


def get_access_token() -> str:
    import requests
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={CORP_ID}&corpsecret={CORP_SECRET}"
    resp = requests.get(url, timeout=10)
    return resp.json()["access_token"]


def send_message(to_user: str, content: str):
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


def parse_xml(xml_str: str) -> dict:
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        msg_signature = params.get("msg_signature", [""])[0]
        timestamp     = params.get("timestamp", [""])[0]
        nonce         = params.get("nonce", [""])[0]
        echostr       = params.get("echostr", [""])[0]

        if crypt.verify_signature(msg_signature, timestamp, nonce, echostr):
            decrypted = crypt.decrypt(echostr)
            self._respond(200, decrypted)
        else:
            self._respond(403, "Forbidden")

    def do_POST(self):
        params = parse_qs(urlparse(self.path).query)
        msg_signature = params.get("msg_signature", [""])[0]
        timestamp     = params.get("timestamp", [""])[0]
        nonce         = params.get("nonce", [""])[0]

        length = int(self.headers.get("Content-Length", 0))
        body   = self.rfile.read(length).decode("utf-8")

        try:
            root      = ET.fromstring(body)
            encrypted = root.find("Encrypt").text
        except Exception:
            self._respond(400, "Bad Request")
            return

        if not crypt.verify_signature(msg_signature, timestamp, nonce, encrypted):
            self._respond(403, "Forbidden")
            return

        xml_str = crypt.decrypt(encrypted)
        msg     = parse_xml(xml_str)

        if msg.get("MsgType") == "text":
            user_id  = msg.get("FromUserName", "")
            question = msg.get("Content", "").strip()
            answer   = rag_query(question)
            send_message(user_id, answer)

        self._respond(200, "success")

    def _respond(self, code: int, body: str):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format, *args):
        pass