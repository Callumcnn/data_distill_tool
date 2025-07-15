# -*- coding: utf-8 -*-

from GenerateConfig import *

'''此处修改为自己的url'''
li_gpt4o_url = ''
# li_gpt4o_url = ''

'''若使用vllm 在此处配置参数'''
api_key = "test"
llm_url = ""

generate_config: GenerateConfig = {
    "model": "qwen",
    "temperature": 0.6,
    "top_p": 0.95,
    "max_tokens": 100000,
    "stop": ['<|endoftext|>'],
}
