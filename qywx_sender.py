import config
import requests
import json
import re
from googletrans import Translator

class QywxSender:
    def __init__(self):
        self.webhook_url_list = config.get_qywx_webhook_url_list()
        self.translator = Translator()

    def send_and_recv(self, url, headers, data):
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            result = response.json()
            if result.get("errcode") == 0:
                print("消息发送成功!")
            else:
                print(f"消息发送失败: {result.get('errcode')} , {result.get('errmsg')}")
        except requests.exceptions.RequestException as e:
            print(f"请求发送失败: {e}")
        except json.JSONDecodeError:
            print(f"无法解析服务器响应: {response.text}")

    def send_content_to_all_bot(self, content):
        payload = {
                    "msgtype": "markdown",
                    "markdown": {
                        "content": content
                    }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }

        for webhook_url in self.webhook_url_list:
            self.send_and_recv(webhook_url, headers, json.dumps(payload))

    def transform_content_to_zh(self, content) -> str:
        result = self.translator.translate(content, src='en', dest='zh-cn')
        text = re.sub(r'（', '(', result.text)
        text = re.sub(r'）', ')', text)
        return text

    def solve_trump_msg_with_link(self, raw_content):
        pattern = r'(https?://[^\s,?!]+)'
        return re.sub(pattern, r'[link](\1)', raw_content)

    def send_trump_msg_to_all_bot(self, raw_content):
        raw_content = self.solve_trump_msg_with_link(raw_content)
        content = "# **特朗普发布内容**\n" + "## 原文:\n" + raw_content + "\n## 翻译:\n" + self.transform_content_to_zh(raw_content)
        print(content)
        self.send_content_to_all_bot(content)
