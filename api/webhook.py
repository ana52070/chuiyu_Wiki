"""
webhook.py - Vercel Serverless Function
企业微信消息回调，使用被动回复 XML 模式
"""

import os
import sys
import time
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


def make_text_reply(to_user: str, from_user: str, content: str) -> str:
    """构造被动回复的明文 XML"""
    return (
        f"<xml>"
        f"<ToUserName><![CDATA[{to_user}]]></ToUserName>"
        f"<FromUserName><![CDATA[{from_user}]]></FromUserName>"
        f"<CreateTime>{int(time.time())}</CreateTime>"
        f"<MsgType><![CDATA[text]]></MsgType>"
        f"<Content><![CDATA[{content}]]></Content>"
        f"</xml>"
    )


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
            user_id    = msg.get("FromUserName", "")
            to_user    = msg.get("ToUserName", "")
            question   = msg.get("Content", "").strip()

            # RAG 查询
            answer = rag_query(question)

            # 构造加密被动回复
            reply_xml  = make_text_reply(user_id, to_user, answer)
            encrypted_reply = crypt.encrypt(reply_xml)
            response_xml    = crypt.make_reply_xml(
                encrypted_reply,
                str(int(time.time())),
                nonce
            )
            self._respond(200, response_xml, content_type="application/xml")
        else:
            self._respond(200, "success")

    def _respond(self, code: int, body: str, content_type: str = "text/plain"):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format, *args):
        pass