tmp = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现。
现在需要提高的能力维度为'多任务语言理解'；参考的评估集为'MMLU'；MMLU（Massive Multitask Language Understanding，大规模多任务语言理解）是一个专门用于评估语言模型多领域知识理解与推理能力的综合性测试集；

# 数据领域
参考如下领域domain: {text1}

# 任务要求
1.参考MMLU评测集中的一个真实query：{text2}
2.语种：参考第1点中的语种
3.参考第1点中的query生成训练query；确保query逻辑完整；确保query中题型与参考query一致，题目难度应与MMLU相当；
4.生成query对应答案cot_answer，确保cot_answer是对query的正确回答，确保包含必要的推理过程和最终正确选项先生成推理过程，再生成答案；
5.生成query对应答案raw_answer，raw_answer应该尽量简洁；
6.循环步骤1到5，生成3组不一样的数据；
7.输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "query":"",
        "cot_answer":"",
  "raw_answer": ""
    },
    ...
]
你的答案："""


ifeval = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现。
现在需要提高的能力维度为'指令遵循'；参考的评估集为'IFEval (Instruction Following Eval)'；

# 任务知识
指令遵循的任务参考如下的instruction_follow_dict:
{
    "num_sentences": "",
    "relation": "",
    "section_spliter": "",
    "num_sections": "",
    "keywords": "",
    "num_keywords": "",
    "case_match": "",
    "num_words": "",
    "num_bullets": "",
    "forbidden_words": "",
    "end_phrase": "",
    "num_paragraphs": "",
    "paragraph_separator": "",
    "nth_paragraph": "",
    "first_word": "",
    "postscript_marker": "",
    "prompt_to_repeat": ""
}

# 任务要求
IFEval（Instruction Following Eval） 是一个专门用于评估大模型在指令遵循能力上的基准数据集。
1.语种：与大模型IFEval评测集语种保持一致，优先英文，其次中文；
2.遵循kwargs，在instruction_follow_dict中随机选取遵循任务，选取的指令遵循任务要清晰无歧义，不能自相矛盾；
3.遵循任务说明；
4.IFEval完整query；
5.参考大模型IFEval典型query生成训练query；query逻辑正确完整；
6.生成query对应答案all_answer，all_answer中包含关键内容，确保all_answer逻辑完整，内容正确；
7.生成query对应答案raw_answer,raw_answer应该简洁明了；
8.循环步骤1到7，生成3组不一样的数据；
9.输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "遵循kwargs": "",
        "遵循任务说明": "",
        "IFEval完整query":"",
        "query":"",
        "all_answer":"",
        "raw_answer":""
    },
    ..
]
你的答案："""


simple_cot = """# question
{text1}
# requirements
Ensure that the thinking process within the <think> tag must be controlled less then 100 words, must be concise. The response content following </think> should be a correct answer to the question. It should include a brief explanation of the correct answer and the final correct answer. The explanation should be presented first, followed by the correct answer.
Your answer is:"""

GPQA = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现。
现在需要提高的能力维度为'复杂推理与专业领域深度理解'；参考的评估集为'GPQA'；GPQA（全称 Graduate-Level Google-Proof Q&A Benchmark）是一个专注于评估大模型在研究生级别科学问题上的深度推理与专业知识整合能力的高难度测试集；

# 数据领域
参考如下领域domain_list：[生物学, 物理学, 化学]

# 任务要求
1.语种：与大模型GPQA评测集语种保持一致；
2.在domain_list中随机选取一个领域；
3.参考GPQA，确定题目难度；
4.在选取的领域内给出GPQA的一个完整且真实的query，题型为多选题，确保题目描述和选项完整，题目难度参照第三步的题目难度；
5.参考第三步中选取的GPQA的query生成训练query；确保选取的训练query与参考query题型、题目难度保持一致；
6.按照如下格式拼接得到query："Answer the following multiple choice question. The last line of your response should be of the following format: 'Answer: $LETTER' (without quotes) where LETTER is one of ABCD." + "第五步中生成的query" ；
7.生成query对应包含推理的答案all_answer；确保all_answer是对query的正确回答，确保包含必要推理过程和最终正确选项，应该先输出推理过程，再根据推理过程给出正确答案；
8.生成query对应包直接的答案raw_answer；确保raw_answer是对query的正确回答，确保包含最终正确选项，给出正确答案；
9.循环步骤1到8，生成3组不一样的数据；
10.输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "domain": "",
        "难度"："",
        "GPQA完整query": "",
        "query":"",
        "all_answer":"",
        "raw_answer":""
    },
    ...
]
你的答案："""

gsm8k = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现。
现在需要提高的能力维度为'数学推理能力'；参考的评估集为'GSM8k'；GSM8K (Grade School Math 8K)是一个专门用于评估大模型在数学推理和多步逻辑推理能力的数据集；

# 任务要求
1.语种：与大模型GSM8K评测集语种保持一致；
2.参考GSM8K评测集，确定题目题型和题目难度；
3.参考GSM8K评测集，确定回答格式和思维链长度；
4.给出一个GSM8K完整且真实的query，题型、难度参照第2步；
5.参照第4步中的GSM8K的query给出一个适用于大模型SFT训练的query，确保query题型、难度与参看query一致；
6.给出第5步中query的正确解答cot_answer，cot_answer回答参照第3点，确保回答中包含必要的推理过程和最终正确答案，应该先生成推理过程，再根据推理过程生成答案；
7.给出第5步中query的正确解答raw_answer，raw_answer应该尽量简洁，保证包含正确答案，并与第6步中给出的答案一致；
7.循环步骤1到6，生成3组不一样的数据；
输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "题目题型和难度": "",
        "回答格式"："",
        "GSM8K完整query": "",
        "query":"",
        "cot_answer":"",
        "raw_answer":""
    },
    ...
]
你的答案：
"""

HumanEval = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现;
现在需要提高的能力维度为'代码生成'；参考的评估集为'HumanEval'；HumanEval是一个专门用于评估大模型代码生成能力的基准评测集。

# 任务要求
1.语种：与大模型HumanEval评测集语种保持一致；
2.参考HumanEval评测集，确定题目题型和题目难度；
3.参考HumanEval评测集，确定回答格式；
4.给出一个HumanEval完整且真实的query，题型、难度参照第2步；
5.参照第4步中的HumanEval的query给出一个适用于大模型SFT训练的query，确保query题型、难度与参看query一致；
6.给出第5步中query的正确解答cot_answer，cot_answer回答格式参照第3点，答案应该包含对代码逻辑的简单梳理和代码实现，先输出代码逻辑梳理，再给出实现的代码；
7.给出第5步中query的正确解答raw_answer，raw_answer是直接给出代码实现，代码实现参考第5步；
7.循环步骤1到6，生成3组不一样的数据；
输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "题目题型和难度": "",
        "回答格式"："",
        "HumanEval完整query": "",
        "query":"",
        "cot_answer":"",
        "raw_answer":""
    },
    ...
]
你的答案："""

CMMLU = """# 你的身份
你是大模型训练数据构建和指标Benchmark评估专家。

# 你的任务
你需要根据大模型训练的能力维度，生成对应维度的高质量训练数据，用于sft后训练，以提高大模型在对应维度的表现。
现在需要提高的能力维度为'多任务语言理解'；参考的评估集为'CMMLU'；CMMLU（Chinese Massive Multitask Language Understanding，大规模多任务语言理解）是一个专门用于评估语言模型多领域知识理解与推理能力的综合性测试集；

# 数据领域
参考如下领域domain_list：
['agronomy', 'anatomy', 'ancient_chinese', 'arts', 'astronomy', 'business_ethics', 'chinese_civil_service_exam', 'chinese_driving_rule', 'chinese_food_culture', 'chinese_foreign_policy', 'chinese_history', 'chinese_literature', 'chinese_teacher_qualification', 'clinical_knowledge', 'college_actuarial_science', 'college_education', 'college_engineering_hydrology', 'college_law', 'college_mathematics', 'college_medical_statistics', 'college_medicine', 'computer_science', 'computer_security', 'conceptual_physics', 'construction_project_management', 'economics', 'education', 'electrical_engineering', 'elementary_chinese', 'elementary_commonsense', 'elementary_information_and_technology', 'elementary_mathematics', 'ethnology', 'food_science', 'genetics', 'global_facts', 'high_school_biology', 'high_school_chemistry', 'high_school_geography', 'high_school_mathematics', 'high_school_physics', 'high_school_politics', 'human_sexuality', 'international_law', 'journalism', 'jurisprudence', 'legal_and_moral_basis', 'logical', 'machine_learning', 'management', 'marketing', 'marxist_theory', 'modern_chinese', 'nutrition', 'philosophy', 'professional_accounting', 'professional_law', 'professional_medicine', 'professional_psychology', 'public_relations', 'security_study', 'sociology', 'sports_science', 'traditional_chinese_medicine', 'virology', 'world_history', 'world_religions']

# 任务要求
1.语种：与大模型CMMLU评测集语种保持一致；
2.在domain_list中随机选取一个领域；
3.在选取的领域内给出CMMLU的一个真实且完整query，题型为单选题或者多选题，确保query中包含题干和4个选项；
4.参考第3步中的query生成训练query；确保query逻辑完整；确保query中题型与参考query一致，难度相当，包含题目和选项；
5.生成query对应答案cot_answer；确保cot_answer是对query的正确回答，确保包含正确答案的简略解释和最终正确结果，应该先输出简略解释，再输出正确答案；
6.生成query对应答案raw_answer；确保raw_answer是对query的正确回答，回答应该简洁，确保raw_answer和cot_answer答案一致；
7.循环步骤1到6，生成3组不一样的数据；
8.输出内容严格按照如下json结构:
[
    {
        "语种":"",
        "domain": "",
        "MMLU完整query": "",
        "query":"",
        "cot_answer":"",
     "raw_answer":""
    },
    ...
]
你的答案："""

better_answer_gen = PROMPT ="""
# 你的身份
你是一个专业的数据生产专家，擅长生成高质量的回答。你的目标是生成比当前回答更好的回答。

# 你的任务
你需要对输入的对话内容进行深入分析，理解当前回答的优点和不足，生成一个更专业、更全面的回答。

# 上下文对话
'''
{text1}
'''

# 当前回答
'''
{text2}
'''

# 分析步骤
请按照以下步骤进行思考和分析：
1. 理解上下文对话，分析当前回答的不足；
2. 输出当前回答可以改进的具体方面；
3. 输出当前回答改进的具体方式和内容；
4. 生成更高质量的回答，确保回答内容是对用户问题的正确回答，确保包含必要推理过程和最终正确选项，应该先输出推理过程，再根据推理过程给出正确答案；
5. 执行上述1-4步骤，生成一个更好的回答，严格遵守如下JSON格式：

```json
[
    {
        "当前回答分析": "分析当前回答的不足",
        "改进方向": "说明改进的具体方面",
        "改进说明": "说明改进的具体方式和内容",
        "高质量回答": "生成更好的回答"
    }
]
```
你的回答：
"""
all_prompt_dict = {               
                   'ifeval': [ifeval, 0],
                   'simple_cot': [simple_cot, 1],
                   'GPQA': [GPQA, 0],
                   'gsm8k':[gsm8k, 0],
                   'HumanEval':[HumanEval, 0],
                   'CMMLU':[CMMLU, 0],
                   'tmp':[tmp, 2],
                   'better_answer_gen': [better_answer_gen, 2]
                   }