"""
webhook.py - Vercel Serverless Function
企业微信消息回调入口
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from urllib.parse import parse_qs

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


def parse_message(xml_str: str) -> dict:
    root = ET.fromstring(xml_str)
    return {child.tag: child.text for child in root}


def handler(request, response):
    method = request.method
    query  = request.query or {}

    # GET：企业微信验证回调 URL
    if method == "GET":
        msg_signature = query.get("msg_signature", "")
        timestamp     = query.get("timestamp", "")
        nonce         = query.get("nonce", "")
        echostr       = query.get("echostr", "")

        if crypt.verify_signature(msg_signature, timestamp, nonce, echostr):
            decrypted = crypt.decrypt(echostr)
            response.status_code = 200
            response.body = decrypted
        else:
            response.status_code = 403
            response.body = "Forbidden"
        return response

    # POST：接收消息
    if method == "POST":
        msg_signature = query.get("msg_signature", "")
        timestamp     = query.get("timestamp", "")
        nonce         = query.get("nonce", "")

        body = request.body or ""
        if isinstance(body, bytes):
            body = body.decode("utf-8")

        try:
            root      = ET.fromstring(body)
            encrypted = root.find("Encrypt").text
        except Exception:
            response.status_code = 400
            response.body = "Bad Request"
            return response

        if not crypt.verify_signature(msg_signature, timestamp, nonce, encrypted):
            response.status_code = 403
            response.body = "Forbidden"
            return response

        xml_str = crypt.decrypt(encrypted)
        msg     = parse_message(xml_str)

        if msg.get("MsgType") == "text":
            user_id  = msg.get("FromUserName", "")
            question = msg.get("Content", "").strip()
            answer   = rag_query(question)
            send_message(user_id, answer)

        response.status_code = 200
        response.body = "success"
        return response

    response.status_code = 405
    response.body = "Method Not Allowed"
    return response