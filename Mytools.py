import plugins
import requests
import re
import json
from urllib.parse import urlparse
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel import channel
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *
from datetime import datetime, timedelta

import urllib.parse
import urllib.request

import io
# from PIL import Image
#from . import enhance_img
from . import send_qq_msg
# import cv2


@plugins.register(
    name="Mytools",
    desire_priority=940,
    hidden=False,
    desc="自定义工具，想用什么功能自己添加进去",
    version="0.6.1",
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

        # #base64工具使用
        # if content[:len('enbase64')] == 'enbase64' or content[:len('debase64')] == 'debase64':
        #     content = self.get_base64_operator(content)
        #     reply = self.create_reply(ReplyType.TEXT, content)
        #     e_context["reply"] = reply
        #     e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        # #查询时间戳
             # weather_match = re.match(r'^(?:(.{2,7}?)(?:市|县|区|镇)?|(\d{7,9}))(?:的)?天气$', content)
        time_match = re.search(r'现在|目前|此刻|当前.*时间|日期|时间戳', content)
        if time_match:
            content = self.get_timestamp()
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        
        # 查询QQ头像
        qq_format_match = re.search(r'qq\s+\d{8,10}', content)
        if qq_format_match:
            qq_image = self.get_QQ_photo(content)
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(qq_image) else ReplyType.TEXT
            reply = self.create_reply(reply_type, qq_image or "查询错误")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        if content == "二次元" or content == "动漫"  or content == "美女"  or content == "风景"  or content == "汽车"  or content == "MC酱":
            Dm_image = self.get_gm_Img(content)
            print(f"======{Dm_image}=======")
            reply_type = ReplyType.IMAGE_URL if self.is_valid_url(Dm_image) else ReplyType.TEXT
            reply = self.create_reply(reply_type, Dm_image or "查询错误")
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        # 发送QQ消息
        if content[:len('sendqq')] == 'sendqq' or content[:len('sendQQ')] == 'sendQQ':
            content = self.get_QQ_msg(content)
            reply = self.create_reply(ReplyType.TEXT, content)
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        # # 尝试接受图片
        # if e_context["context"].type == ContextType.IMAGE :
        #     msg: ChatMessage = e_context["context"]["msg"]
        #     m_flag = False
        #     try:
        #         msg.prepare()
        #         with open(content, 'rb') as file:
        #             try:
        #                 image_data = file.read()
        #                 logger.info("图片读取成功")
        #                 image = Image.open(io.BytesIO(image_data))
        #                 if not os.path.exists('./tmp/'):
        #                     os.mkdir('./tmp/')
        #                 image.save('./tmp/new_image.bmp')
        #                 m_flag = True
        #                 # 检查文件是否存在
        #                 if os.path.exists('./tmp/new_image.bmp'):
        #                     try:
        #                         # 尝试打开图像
        #                         imageA = Image.open('./tmp/new_image.bmp')
        #                         # 调用CLAHE函数处理图像
        #                         output_image = enhance_img.clahe_color(imageA)  if str(imageA.getbands()) == r"('R', 'G', 'B')" else enhance_img.clahe(imageA) 
                                
        #                         # 保存处理后的图像
        #                         output_image.save("./tmp/output_image_clahe.bmp")
        #                         if os.path.exists('./tmp/output_image_clahe.bmp'):
        #                             try:
        #                                 m_flag = False
        #                                 reply = self.create_reply(ReplyType.FILE, './tmp/output_image_clahe.bmp')
        #                                 e_context["reply"] = reply
        #                                 e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
        #                             except Exception as e:
        #                                 m_flag = True
        #                         # 图像成功打开
        #                     except Exception as e:
        #                         # 图像打开失败
        #                         print(f"无法打开图像：{e}")
        #                         m_flag = True
        #             except Exception as e:
        #                 logger.error(f"发送图片错误：{e}")
        #                 m_flag = True
        #     except Exception as e:
        #         logger.error(f"读取图片数据时出现错误：{e}")
        #         m_flag = True
        #     if m_flag:
        #         content = "测试接受图片"
        #         reply = self.create_reply(ReplyType.TEXT, content)
        #         e_context["reply"] = reply
        #         e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑




    def get_help_text(self, verbose=False, **kwargs):
        short_help_text = " 发送特定指令来获取相关信息！"

        if not verbose:
            return short_help_text

        help_text = "📚 发送关键词获取特定信息！\n"

        # 娱乐和信息类
        help_text += "\n🎉 娱乐与资讯：\n"
        help_text += "    🕉获取动漫壁纸：关键字【MC酱、风景、汽车、二次元、动漫、美女】\n"
        
        
        # 查询类
        help_text += "\n🔍 查询工具：\n"
        help_text += "    🎯 现在时间：返回当前机器时间\n"
        help_text += "    🎯 QQ头像 : 【qq 12345678】获取QQ号为12345678的头像\n"
        help_text += "    🎯 发送QQ消息 : sendqq -h\n"




        return help_text


    
     # base64加密解密操作
    
    def get_base64_operator(self,message):
        import base64
        # 加密操作
        try:
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
        except Exception as e:
            logger.error(f"发生了异常:{e}\n")
            return f"发生了异常:{e}\n输入错误，请查看帮助再进行操作。\n"
    
    #返回当前时间戳
    def get_timestamp(self):
        import time

        result = ""
        result += f"🕐︎当前时间：{datetime.now()}\n"
        result += f"  时间戳-秒级(s)：{int(time.time()) }\n"
        result += f"  时间戳-毫秒级(ms)：{time.time_ns() // 1000000 }\n"
        result += "\n------------\n本次回答由Mytools插件提供😁😁😁\n"
        return  result

    #获取QQ头像
    def get_QQ_photo(self,contents):
        import urllib3
        try:
            # 创建一个连接池
            # http = urllib3.PoolManager()
            qq = contents.replace(" ","").replace("qq","")
            return f"https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640"
        except Exception as e:
            logger.error(f"查询QQ头像出错：{e}")
            return self.handle_error(e, "except里QQ头像获取失败")
    
    # 随机获取二次元图片
    def get_gm_Img(self, content):
         # 二次元壁纸
        def Dm_Image():
            url = 'https://api.gumengya.com/Api/DmImg'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取二次元请求失败%s" % res)
                        return self.handle_error( f"{res}",f"请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取二次元接口异常")
                return self.handle_error("接口异常--","随机获取二次元接口异常")
        
        def Dm2_Image():
            url = 'https://api.gumengya.com/Api/DmImgS'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取二次元请求失败%s" % res)
                        return self.handle_error( f"{res}",f"请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取二次元接口异常")
                return self.handle_error("接口异常--","随机获取二次元接口异常")
        def Mv_Image():
            url = 'https://api.gumengya.com/Api/MvImg'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取美女请求失败%s" % res)
                        return self.handle_error( f"{res}",f"美女接口请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取美女接口异常")
                return self.handle_error("接口异常--","随机获取美女接口异常")
        def Fj_Image():
            url = 'https://api.gumengya.com/Api/FjImg'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取风景请求失败%s" % res)
                        return self.handle_error( f"{res}",f"风景接口请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取风景接口异常")
                return self.handle_error("接口异常--","随机获取风景接口异常")
        def Qc_Image():
            url = 'https://api.gumengya.com/Api/QcImg'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取汽车请求失败%s" % res)
                        return self.handle_error( f"{res}",f"汽车请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取汽车接口异常")
                return self.handle_error("接口异常--","随机获取汽车接口异常")
        def MC_Image():
            url = 'https://api.gumengya.com/Api/McImg'
            params = {
                'format': 'json',
            }
            querys = urllib.parse.urlencode(params)
            querys = querys.encode('utf-8')  # Encode the query string to bytes
            request = urllib.request.Request(url, data=querys)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8')  # Decode the response to a string

            if content:
                try:
                    res = json.loads(content)
                    # 状态码 200 表示请求成功
                    if res['code'] == '200' or res['code'] == 200:
                        logger.info("请求成功%s" % res)
                        return res['data']['url']
                    else:
                        logger.error("随机获取MC酱请求失败%s" % res)
                        return self.handle_error( f"{res}",f"MC酱请求失败")
                except Exception as e:
                    print("解析结果异常：%s" % e)
                    return self.handle_error("解析结果异常--","随机获取美女接口异常")
            else:
                # 无法获取返回内容，请求异常
                logger.error("随机获取MC酱接口异常")
                return self.handle_error("接口异常--","随机获取MC酱接口异常")
        
        key_word_Set = ["二次元", "动漫", "美女", "风景" , "汽车", "MC酱"]
        if content == key_word_Set[0]:
            return Dm_Image()
        elif content == key_word_Set[1]:
            return Dm2_Image()
        elif content == key_word_Set[2]:
            return Mv_Image()
        elif content == key_word_Set[3]:
            return Fj_Image()
        elif content == key_word_Set[4]:
            return Qc_Image()
        elif content == key_word_Set[5]:
            return MC_Image()

    # 获取发送QQ消息的内容
    def get_QQ_msg(self,messages):
        message = messages.split(" ",1)[1]
        return send_qq_msg.main(message)

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
    
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        


#扩展
        



