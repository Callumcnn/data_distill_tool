# -*- coding: utf-8 -*-

from GenerateConfig import *

'''此处修改为自己的url'''
li_gpt4o_url = 'https://chennuo5.fc.chj.cloud/gpt4o/conversation'
# li_gpt4o_url = 'https://llm-app-wangze8.fc.chj.cloud/gpt4o/conversation'

'''若使用vllm 在此处配置参数'''
api_key = "test"
llm_url = "http://10.80.11.174:1688/v1/"

generate_config: GenerateConfig = {
    "model": "qwen",
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 100000,
    "stop": ['<|endoftext|>'],
}