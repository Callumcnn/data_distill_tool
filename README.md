# 数据合成工具
- 文件结构

    |——distill_account.py       #在此文件中配置llm_url为自己部署的api

    |——distill_prompts.py       #在此文件中配置prompt

    |——GenerateConfig.py

    |——muti_distill_tool_v2_think.py      #程序主入口，生产带<think></think>格式数据

    |——muti_distill_tool_v2.py            #程序主入口，生产cot数据

    |——requirements.txt

    |—— model_deploymeny |——lizrun_lpai_sglang_api_qwen3_32b.sh #api部署脚本，使用yarn，支持上下文长度13w
                         |——sglang_server_qwen32b.sh
 