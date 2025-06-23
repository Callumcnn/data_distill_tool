# 设置每次的时间戳
stamp=$(date +%Y-%m-%d-%H-%M-%S)
# job_name="qwen1p5b-guan-api"
job_name="sft-qwen3"
pool="base-4o-ali-sh"
# pool="base"
node_num=1

echo "job_name:${job_name}"
lizrun lpai start -c "bash /mnt/volumes/base-cv-ali-sh/chennuo5/tools/model_deploymeny/sglang_server_qwen32b.sh" \
   -j ${job_name}-${stamp} \
   -i reg-ai.chehejia.com/ssai/lizr/cu124/py310/pytorch:2.5.1-multinode-flashattn-2.7.3-vllm0.7.1-liktoken1.0.6 \
   -p ${pool} \
   -n ${node_num} 


# lizrun lpai start -c "bash /mnt/volumes/base-cv-ali-sh/wangze8/model_deploymeny/sglang_server_qwen72b.sh" \
# -j qwen72b-instruct-api \
# -i reg-ai.chehejia.com/ssai/lizr/cu124/py310/pytorch:2.5.1-multinode-flashattn-2.7.3-vllm0.7.1-liktoken1.0.6 \
# -p base-4o-ali-sh \
# -n 1