import plugins
import requests
import re
import json
from urllib.parse import urlparse
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel import channel
from common.log import logger
from plugins import *
from datetime import datetime, timedelta



@plugins.register(
    name="Mytools",
    desire_priority=889,
    hidden=True,
    desc="自定义工具，想用什么功能自己添加进去",
    version="0.1",
    author="Haoj",
)
class Mytools(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Mytools] inited")
        self.config = super().load_config()


    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT
        ]:
            return
        content = e_context["context"].content.strip()
        logger.debug("[Mytools] on_handle_context. content: %s" % content)

        #base64工具使用
        if content[:len('enbase64')] == 'enbase64' or content[:len('debase64')] == 'debase64':
            content = self.get_base64_operator(content)
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, verbose=False, **kwargs):
        short_help_text = " 发送特定指令来获取相关信息！"

        if not verbose:
            return short_help_text

        help_text = "📚 发送关键词获取特定信息！\n"

        # 娱乐和信息类
        help_text += "\n🎉 娱乐与资讯：\n"
        help_text += "  ⛓ enbase64:base64加密【enbase64 hello】\ndebase64:base64解密【debase64 aGVsbG8=】"

        # 查询类
        help_text += "\n🔍 查询工具：\n"
        help_text += "  🌦️ 📦 🌌暂无\n"


        return help_text


    
     # base64加密解密操作
    def get_base64_operator(self,message):
        import base64
        # 加密操作
        if message[:len("enbase64")] == "enbase64":
            original_string = message.split(" ", 1)[1]
            encoded_bytes = base64.b64encode(original_string.encode('utf-8'))
            encoded_string = encoded_bytes.decode('utf-8')
            return encoded_string
        # 解密操作
        elif message[:len("debase64")] == "debase64":
            encoded_string = message.split(" ", 1)[1]
            decoded_bytes = base64.b64decode(encoded_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        else:
            return '输入错误，请查看帮助再进行操作。\n'
        

    def make_request(self, url, method="GET", headers=None, params=None, data=None, json_data=None):
        try:
            if method.upper() == "GET":
                response = requests.request(method, url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = requests.request(method, url, headers=headers, data=data, json=json_data)
            else:
                return {"success": False, "message": "Unsupported HTTP method"}

            return response.json()
        except Exception as e:
            return self.handle_error(e, "请求失败")


    def create_reply(self, reply_type, content):
        reply = Reply()
        reply.type = reply_type
        reply.content = content
        return reply

    def handle_error(self, error, message):
        logger.error(f"{message}，错误信息：{error}")
        return message

