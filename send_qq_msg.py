

import requests
import re
import json

RED = ""
GREED = ""
YELLOW = ""
RESET = ""

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
    url = "https://cqhttp.haoj.xyz/send_private_msg"
    error_msg = "用法：sendqq  [消息内容]\n发送给某个人的QQ个人消息。\n\n如果没有消息，只能查看帮助。\n"
    error_msg += "  -h, --help\t显示此帮助信息并退出\n  -v, --version\t版本信息\n"
    error_msg += "  -p\t指定接收消息的QQ号\n\n"
    error_msg += "示例：\n  sendqq  Hello world!\t发送QQ消息“Hello World!”\n"
    error_msg += "  sendqq  -h\t显示此帮助信息并退出\n"
    error_msg += "  sendqq  -q12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    error_msg += "  sendqq  -q 12345678 你好！\t指定QQ号【12345678】接收消息【你好！】\n"
    
    if all_args:
        if all_args == "-h" or all_args == "--help":
            return(GREED + error_msg + RESET)
            
        elif all_args == "-V" or all_args == "--version"or all_args == "-v":
            return(YELLOW + "0.3.1\n个人开发\n" + RESET)
        else:
            # 自定义发送给的qq号
            qq = get_qq(all_args)
            if qq[0] != "-1":
                url_msg = f"{url}?user_id={qq[0]}&message={qq[1]}"
                try:
                    res = requests.get(url_msg)
                except:
                    return "服务器错误，请检查网络连接。"
                try:
                    json_data = res.json()
                    status_value = json_data.get("status", "")
                    if status_value != "ok":
                        print(RED + "Failed to send message\n可能原因："
                              + "\n指定接收消息的QQ未添加服务QQ号【2622587578】，检查并添加好友后重试.\n" + RESET)
                    else:
                        return '发送成功'
                except Exception as e:
                    return(f"JSON parsing error: {e}")
            # 默认qq号
            else:
                res = requests.get(f"{url}?user_id=1587555900&message={all_args}")
                return '发送成功'
                

    else:
        return(RED + "sendqq : 缺少参数\n请尝试执行 \"sendqq  --help\" 来获取更多信息。" + RESET)

if __name__ == "__main__":
    RED = "\033[31m" 
    GREED  = "\033[32m" 
    YELLOW  = "\033[33m" 
    RESET  = "\033[0m" 
    print(main("-v"))
