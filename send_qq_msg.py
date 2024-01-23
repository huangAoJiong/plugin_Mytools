'''
import sys
import requests
import re
import json

def get_qq(input_str):
    ret = "-1"
    pattern = re.compile(r"-q\s*(\d+)+(\s\s*)")
    matches = re.search(pattern, input_str)
    
    if matches and len(matches.groups()) > 0:
        matched_part = matches.group(1)
        rest_part = re.sub(pattern, "", input_str)
        return matched_part, rest_part
    
    return ret, input_str

def qq_send_main():
    url = "http://cqhttp.aoj.lol:20008/send_private_msg"
    error_msg = "用法：./qq-send-server [消息内容]\n发送给某个人的QQ个人消息。\n\n如果没有消息，只能查看帮助。\n"
    error_msg += "  -h, --help\t显示此帮助信息并退出\n  -v, --version\t版本信息\n"
    error_msg += "  -p\t指定接收消息的QQ号\n\n"
    error_msg += "示例：\n  ./qq-send-server Hello world!\t发送QQ消息“Hello World!”\n"
    error_msg += "  ./qq-send-server -h\t显示此帮助信息并退出\n"
    error_msg += "  ./qq-send-server -q12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    error_msg += "  ./qq-send-server -q 12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    
    if len(sys.argv) > 1:
        all_args = " ".join(sys.argv[1:])
        
        if all_args == "-h" or all_args == "--help":
            print("\033[32m" + error_msg + "\033[0m")
            return
        elif all_args == "-v" or all_args == "--version":
            print("\033[33m" + "0.2.1\n个人开发\n" + "\033[0m")
            return
        else:
            # 自定义发送给的qq号
            qq = get_qq(all_args)
            if qq[0] != "-1":
                url_msg = f"{url}?user_id={qq[0]}&message={qq[1]}"
                res = requests.get(url_msg)
                try:
                    json_data = res.json()
                    status_value = json_data.get("status", "")
                    if status_value != "ok":
                        print("\033[31m" + "Failed to send message\n可能原因："
                              + "\n指定接收消息的QQ未添加服务QQ号【2622587578】，检查并添加好友后重试.\n" + "\033[0m")
                except Exception as e:
                    print(f"JSON parsing error: {e}")
            # 默认qq号
            else:
                res = requests.get(f"{url}?user_id=1587555900&message={all_args}")

    else:
        print("\033[31m" + "./qq-send-server: 缺少参数\n请尝试执行 \"./qq-send-server --help\" 来获取更多信息。" + "\033[0m")

if __name__ == "__main__":
    qq_send_main()
'''

import requests
import re
import json

def get_qq(input_str):
    ret = "-1"
    pattern = re.compile(r"-q\s*(\d+)+(\s\s*)")
    matches = re.search(pattern, input_str)
    
    if matches and len(matches.groups()) > 0:
        matched_part = matches.group(1)
        rest_part = re.sub(pattern, "", input_str)
        return matched_part, rest_part
    
    return ret, input_str

def main(all_args):
    url = "http://cqhttp.aoj.lol:20008/send_private_msg"
    error_msg = "用法：./qq-send-server [消息内容]\n发送给某个人的QQ个人消息。\n\n如果没有消息，只能查看帮助。\n"
    error_msg += "  -h, --help\t显示此帮助信息并退出\n  -v, --version\t版本信息\n"
    error_msg += "  -p\t指定接收消息的QQ号\n\n"
    error_msg += "示例：\n  ./qq-send-server Hello world!\t发送QQ消息“Hello World!”\n"
    error_msg += "  ./qq-send-server -h\t显示此帮助信息并退出\n"
    error_msg += "  ./qq-send-server -q12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    error_msg += "  ./qq-send-server -q 12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    
    if all_args:
        if all_args == "-h" or all_args == "--help":
            return("\033[32m" + error_msg + "\033[0m")
            
        elif all_args == "-v" or all_args == "--version":
            return("\033[33m" + "0.2.1\n个人开发\n" + "\033[0m")
        else:
            # 自定义发送给的qq号
            qq = get_qq(all_args)
            if qq[0] != "-1":
                url_msg = f"{url}?user_id={qq[0]}&message={qq[1]}"
                res = requests.get(url_msg)
                try:
                    json_data = res.json()
                    status_value = json_data.get("status", "")
                    if status_value != "ok":
                        print("\033[31m" + "Failed to send message\n可能原因："
                              + "\n指定接收消息的QQ未添加服务QQ号【2622587578】，检查并添加好友后重试.\n" + "\033[0m")
                    else:
                        return '发送成功'
                except Exception as e:
                    return(f"JSON parsing error: {e}")
            # 默认qq号
            else:
                res = requests.get(f"{url}?user_id=1587555900&message={all_args}")
                return '发送成功'
                

    else:
        return("\033[31m" + "./qq-send-server: 缺少参数\n请尝试执行 \"./qq-send-server --help\" 来获取更多信息。" + "\033[0m")

if __name__ == "__main__":
    print(main("-q 2622587578 asd"))
