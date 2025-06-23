import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from distill_prompts import all_prompt_dict
from tqdm import tqdm
from typing import Dict, List
from distill_account import *
from openai import OpenAI
import argparse
import ast
import random


MAX_THREAD_NUM = 512
use_vllm = True

# MAX_THREAD_NUM = 6
# use_vllm = False

client = OpenAI(base_url=llm_url, api_key=api_key, max_retries=10)

def create_body_json_only_text(prompt_instruct):
    data_entry = {
        "messages": [
            {"role": "user",
             "contents": [
                 {
                     "type": "text",
                     "text": f"{prompt_instruct}"
                 }
             ]
             }
        ]
    }
    return data_entry

headers = {
    "content-type": "application/json"
}
def request_process(headers, data_entry):
    try:
        response = requests.post(li_gpt4o_url, headers=headers, json=data_entry, timeout=180)
        response_data = json.loads(response.text)
        cnt_ass = response_data['data']['choices'][0]['content']
        return cnt_ass
    except Exception as e:
        print(f'[ERR]外部api调用失败：{e}/n')
        return None

def complete_response(messages: list, stream: bool = False, **kwargs):
    """
    完成响应并返回结果。

    :param messages: 消息列表
    :param stream: 是否流式响应
    :param kwargs: 其他参数
    :return: 响应内容
    """
    if stream:
        completion = client.chat.completions.create(messages=messages, stream=stream, **kwargs)
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content") and chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    else:
        try:
            completion = client.chat.completions.create(messages=messages, **kwargs)
            yield completion.choices[0].message.content
        except Exception as e:
            print('=' * 25)
            print(e)
            print('=' * 25)
            yield '<|wrong data|>'

def request_process_vllm(data_entry: list[dict]):
    """
    处理请求并返回响应文本。
    :param data_entry: 请求体
    :return: 响应文本
    """
    try:
        response_text = ''.join(chunk for chunk in complete_response(messages=data_entry, stream=False, **generate_config))
        return response_text.strip()
    except Exception as e:
        print(e)
        return None

def fill_with_prompt(prompt_instruct=''):
    if use_vllm:
        data = [
            {"role": "system", "content": "你叫理想同学，你是一个有用的助手。"},
            {"role": "user", "content": prompt_instruct}
        ]
        cnt_ass = request_process_vllm(data)
    else:
        request_body_json = create_body_json_only_text(prompt_instruct=prompt_instruct)
        cnt_ass = request_process(headers=headers, data_entry=request_body_json)
    return cnt_ass

def process_entry(data_row, prompt_name, input_keys, dis_res_num, max_retries: int = 5):
    prompt = all_prompt_dict[prompt_name][0]
    num_vals = all_prompt_dict[prompt_name][1]
    entry = {}
    for k in input_keys:
        try:
            entry[k] = data_row[k]
        except Exception as e:
            print(e)


    assert len(entry) == num_vals, '指定key的数量与prompt中key的数量不一致'
    for index, key in enumerate(entry):
        prompt = prompt.replace(f'{{text{index + 1}}}', str(entry[key]))

    distill_results_num = data_row.get('distill_results_num', dis_res_num)
    # data_row['distill_results'] = []
    # data_row['distill_prompt'] = []
    cur_retry = 0
    for i in range(distill_results_num):
        while cur_retry < max_retries: 
            prompt_res_val = fill_with_prompt(prompt_instruct=prompt)
            if not prompt_res_val:
                cur_retry += 1
                continue
            # prompt_res_val = prompt_res_val.split('</think>')[-1]
            try:
                prompt_res_val = prompt_res_val.strip('\n').strip('```json\n').strip('```')
                prompt_res_val = json.loads(prompt_res_val)
                break
            except Exception as e:
                cur_retry += 1
                # print(e)
                continue
            
        if prompt_res_val:
            data_row['distill_results'][0][0]["think_answer"] = prompt_res_val

    return data_row


def produce_data(data_rows, input_keys, prompt_name, output_path, pbar, dis_res_num):
    with ThreadPoolExecutor(max_workers=MAX_THREAD_NUM) as executor:
        futures = [executor.submit(process_entry, data_row, prompt_name, input_keys, dis_res_num) for data_row in data_rows]

        with open(output_path, "a", encoding="utf-8") as f:
            for id, future in enumerate(as_completed(futures)):
                try:
                    pbar.update(1)
                    data_row = future.result()
                    if not data_row:
                        print(f'[ERR] prompt_result is None')
                        continue          
                    if not data_row.get('distill_results'):
                        print(f'[ERR] prompt_result is None')
                        continue
                    if data_row.get('distill_results') == [] or data_row.get('distill_prompt') == []:
                        continue
                    if '<|wrong data|>' in str(data_row.get('distill_results')):
                        print(f'[ERR] distill_results is <|wrong data|>, id{id}')
                        continue


                    f.write(json.dumps(data_row, ensure_ascii=False) + "\n") 
                except Exception as ex:
                    print('[ERR] produce_dcata ! {}'.format(ex))
                    continue
            
def load_jsonl(file_path, batch_size=1000):
    batch = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                batch.append(data)
                if len(batch) == batch_size:
                    yield batch
                    batch = []
            except json.JSONDecodeError as e:
                continue
    if batch:  # 处理最后一批剩余数据
        yield batch

def get_file_line_nums(file_path: str):
        import subprocess
        out = subprocess.getoutput("wc -l {}".format(file_path))
        all_nums = int(out.split()[0])
        return all_nums

def main_entry(input_path, output_path, input_keys, prompt_name, batch_size, dis_res_num=1):
    #处理文件夹
    if os.path.isdir(input_path):
        files = os.listdir(input_path)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
    
        for idx, file in enumerate(files):     
            file_path = os.path.join(input_path, file)
            in_all_nums = get_file_line_nums(file_path)
            if len(file)==0 or file[0] == '.' or file[0] == '~' or not os.path.isfile(file_path):
                continue
            output_path = file.replace('.jsonl', '_output.jsonl')
            output_path = os.path.join(output_path, output_path)
            # if os.path.isfile(output_path):
            #     os.remove(output_path)
            print(f'开始处理文件：{file_path}, id:{idx}')
            pbar = tqdm(desc="proc->{}".format(file), total=in_all_nums, ncols=170)
            
            for data_rows in load_jsonl(file_path, batch_size=batch_size):
                if len(data_rows) == 0:
                    print('[ERR] josn load err !')
                    continue            
                produce_data(data_rows, input_keys, prompt_name, output_path, pbar, dis_res_num)
    #处理文件
    elif os.path.isfile(input_path) and input_path.lower().endswith('.jsonl'):
        file_path = input_path
        in_all_nums = get_file_line_nums(file_path)
        print(f'开始处理文件：{file_path}')
        pbar = tqdm(desc="proc->{}".format(file_path), total=in_all_nums, ncols=150)
        for data_rows in load_jsonl(file_path, batch_size=batch_size):
                if len(data_rows) == 0:
                    print('[ERR] josn load err !')
                    continue            
                produce_data(data_rows, input_keys, prompt_name, output_path, pbar, dis_res_num)
    else:
        raise ValueError("输入路径需要为文件夹或jsonl文件")
 
    


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="muti_distill_tool_v2")
    # parser.add_argument('--input_path', type=str,
    #                    default="/mnt/pfs-guan-ssai/nlu/chennuo5/week2/instruction_align_technology/llm_distill_tool/checker_in",
    #                    help='输入文件夹路径')
    # parser.add_argument('--output_path', type=str,
    #                    default="/mnt/pfs-guan-ssai/nlu/chennuo5/week2/instruction_align_technology/llm_distill_tool/checker_out",
    #                    help='输出文件夹路径')
    # parser.add_argument('--input_keys', type=lambda s: s.split(','),
    #                    default=["source", "query"],
    #                    help='输入键列表')
    # parser.add_argument('--prompt_name', type=str,
    #                    default="冲突检测",
    #                    help='提示词名称')
    # parser.add_argument('--batch_size', type=int,
    #                    default=10,
    #                    help='批次大小')
    # parser.add_argument('--distill_results_num', type=int,
    #                    default=1,
    #                    help='蒸馏结果数量')

    # args = parser.parse_args()
    # main_entry(args.input_path, args.output_path, args.input_keys, args.prompt_name, args.batch_size, args.distill_results_num)
    
    input_path = "/mnt/volumes/base-cv-ali-sh/chennuo5/data/data_paper/exp_data/bbh_exp_data.jsonl"
    output_path = "/mnt/volumes/base-cv-ali-sh/chennuo5/data/data_paper/exp_data_res/bbh_exp_data2.jsonl"
    input_keys = ["query"]
    prompt_name = "simple_cot"
    batch_size = 5000
    distill_results_num = 1
    import time
    start = time.time()
    main_entry(input_path, output_path, input_keys, prompt_name, batch_size, distill_results_num)
    end = time.time()
    print(f'总用时{end-start}s')