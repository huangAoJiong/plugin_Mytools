## 一个基于[ChatGPT-on-Wechat](https://github.com/zhayujie/chatgpt-on-wechat)**项目的简单插件，目前功能简单，想增加新功能可自行DIY**
[TOC]

### 安装
#### 理想安装步骤

```
#installp https://github.com/huangAoJiong/plugin_Mytools.git
```

安装成功后，根据提示使用`#scanp`命令来扫描新插件，再使用`#enablep mytools`开启插件
**大功告成**

#### 实际上

在使用#installp安装后，扫描若不出现该插件的话，需要到后台安装。

1. 进入plugin_Mytools文件夹
2. pip3 install -r requirement.txt
3. 再扫描插件，查看是否存在该插件
4. 若还是不行就重启python app.py 该服务


### 配置
* 无需配置，尽情DIY

### 功能
* base64加密功能：enbase64 【需要加密的内容】
* base64解码功能：debase64 【需要解码的内容】
* 获取QQ号头像   ：qq 12345678 【12345678部分填写8-10位QQ号】
* 获取动漫壁纸     ：关键字【MC酱、风景、汽车、二次元、动漫、美女】
* 图像增强             ：直接发送一幅图像，返回增强后的图像文件
* 发送QQ消息       ：添加了QQ机器人服务器，具体信息查看帮助



### 扩展
* 可以根据自己兴趣/需求，自行添加关键字查询功能。

