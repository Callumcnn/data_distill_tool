# #!/bin/bash

# export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
# # export NCCL_IB_GID_INDEX=3
# # export NCCL_IB_HCA=^mlx5_0
# stamp=$(date +%Y-%m-%d-%H-%M-%S)

# # to work path by scripts path
# PATH_ORI=${0%/*}
# WORK_PATH=$(echo ${PATH_ORI} | sed -r 's/\/{2,}/\//')
# WORKDIR=$(echo ${PATH_ORI} | sed -r 's/\/{2,}/\//')
# cd ${WORK_PATH}

# # WORKDIR=$1
# # CONFIG_PATH=$2
# # echo $WORKDIR
# # echo $CONFIG_PATH

# MASTER_PORT=12344
# MASTER_IP=""
# if [ "${RANK}" == "0" ];then
#   while [[ "$MASTER_IP" == "" ]]
#   do
#     MASTER_IP=`ping ${MASTER_ADDR} -c 3 | sed '1{s/[^(]*(//;s/).*//;q}'`
#     sleep 1
#   done
# else
#   sleep 60
#   MASTER_IP=`getent hosts ${MASTER_ADDR} | awk '{print $1}'` # Ethernet
# fi
# export MASTER_NAME=$MASTER_ADDR
# echo WORLD_SIZE=${WORLD_SIZE}
# echo RANK=${RANK}

# if [ ${WORLD_SIZE} -gt 1 ]
# then
#   NODEINFO='"mindgpt-n'${WORLD_SIZE}'-lisft-master-0":[0,1,2,3,4,5,6,7],';
#   WORKER=`expr ${WORLD_SIZE} - 1`

#   if [ ${WORLD_SIZE} -gt 2 ]
#   then
#     COUNT=0
#     while (( COUNT<${WORKER} ))
#     do
#       NODEINFO="${NODEINFO}"' "mindgpt-n'${WORLD_SIZE}'-lisft-worker-'"${COUNT}"'":[0,1,2,3,4,5,6,7],';
#       ((COUNT++))
#     done
#   fi
#   NODEINFO='{'"${NODEINFO}"'"mindgpt-n'${WORLD_SIZE}'-lisft-worker-'`expr ${WORLD_SIZE} - 2`'":[0,1,2,3,4,5,6,7]}'

#   echo "${NODEINFO}"
#   WORLD_INFO=`echo "${NODEINFO}" | base64`
#   WORLD_INFO=$(echo $WORLD_INFO | sed 's/ //g') #去掉空格
#   echo ${WORLD_INFO}
# fi

# echo $WORKDIR

# TOTAL_GPU=$(expr $WORLD_SIZE \* 8)

# # echo "[global]" > ~/.pip/pip.conf && \
# # echo "trusted-host = pypi.mirrors.ustc.edu.cn" >> ~/.pip/pip.conf && \
# # echo "index-url = https://pypi.mirrors.ustc.edu.cn/simple" >> ~/.pip/pip.conf

# # pip install "sglang[all]>=0.4.2.post4" --trusted-host pypi.mirrors.ustc.edu.cn -i http://pypi.mirrors.ustc.edu.cn/simple/

# echo "[global]" > ~/.pip/pip.conf && \
# echo "trusted-host = artifactory.ep.chehejia.com" >> ~/.pip/pip.conf && \
# echo "index-url = https://artifactory.ep.chehejia.com/artifactory/api/pypi/pypi-remote/simple" >> ~/.pip/pip.conf

# pip install "sglang[all]>=0.4.2.post4" --trusted-host artifactory.ep.chehejia.com -i https://artifactory.ep.chehejia.com/artifactory/api/pypi/pypi-remote/simple

# # MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/DeepSeek-V3-bf16
# # MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/DeepSeek-R1-bf16
# # MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-32B-Instruct
# MODEL_PATH=/lpai/volumes/ss-cv-my/wangze8/models/Qwen2.5-72B-Instruct
# MAX_LEN=32000

# if [ "${RANK}" == "0" ];then
#   python -m sglang.launch_server \
#     --model-path ${MODEL_PATH} \
#     --tp ${TOTAL_GPU} \
#     --dist-init-addr ${MASTER_IP}:${MASTER_PORT} \
#     --nnodes ${WORLD_SIZE} \
#     --node-rank ${RANK} \
#     --trust-remote-code \
#     --max-running-requests 1000 \
#     --context-length ${MAX_LEN} \
#     --host 0.0.0.0 \
#     --port 8012
# else
#   python -m sglang.launch_server \
#     --model-path ${MODEL_PATH} \
#     --tp ${TOTAL_GPU} \
#     --dist-init-addr ${MASTER_IP}:${MASTER_PORT} \
#     --nnodes ${WORLD_SIZE} \
#     --node-rank ${RANK} \
#     --max-running-requests 1000 \
#     --trust-remote-code \
#     --context-length ${MAX_LEN}
# fi

#!/bin/bash

export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7
# export NCCL_IB_GID_INDEX=3
# export NCCL_IB_HCA=^mlx5_0
stamp=$(date +%Y-%m-%d-%H-%M-%S)

# to work path by scripts path
PATH_ORI=${0%/*}
WORK_PATH=$(echo ${PATH_ORI} | sed -r 's/\/{2,}/\//')
WORKDIR=$(echo ${PATH_ORI} | sed -r 's/\/{2,}/\//')
cd ${WORK_PATH}

# WORKDIR=$1
# CONFIG_PATH=$2
# echo $WORKDIR
# echo $CONFIG_PATH

MASTER_PORT=12344
MASTER_IP=""
if [ "${RANK}" == "0" ];then
  while [[ "$MASTER_IP" == "" ]]
  do
    MASTER_IP=`ping ${MASTER_ADDR} -c 3 | sed '1{s/[^(]*(//;s/).*//;q}'`
    sleep 1
  done
else
  sleep 60
  MASTER_IP=`getent hosts ${MASTER_ADDR} | awk '{print $1}'` # Ethernet
fi
export MASTER_NAME=$MASTER_ADDR
echo WORLD_SIZE=${WORLD_SIZE}
echo RANK=${RANK}

if [ ${WORLD_SIZE} -gt 1 ]
then
  NODEINFO='"mindgpt-n'${WORLD_SIZE}'-lisft-master-0":[0,1,2,3,4,5,6,7],';
  WORKER=`expr ${WORLD_SIZE} - 1`

  if [ ${WORLD_SIZE} -gt 2 ]
  then
    COUNT=0
    while (( COUNT<${WORKER} ))
    do
      NODEINFO="${NODEINFO}"' "mindgpt-n'${WORLD_SIZE}'-lisft-worker-'"${COUNT}"'":[0,1,2,3,4,5,6,7],';
      ((COUNT++))
    done
  fi
  NODEINFO='{'"${NODEINFO}"'"mindgpt-n'${WORLD_SIZE}'-lisft-worker-'`expr ${WORLD_SIZE} - 2`'":[0,1,2,3,4,5,6,7]}'

  echo "${NODEINFO}"
  WORLD_INFO=`echo "${NODEINFO}" | base64`
  WORLD_INFO=$(echo $WORLD_INFO | sed 's/ //g') #去掉空格
  echo ${WORLD_INFO}
fi

echo $WORKDIR

TOTAL_GPU=$(expr $WORLD_SIZE \* 8)

# echo "[global]" > ~/.pip/pip.conf && \
# echo "trusted-host = pypi.mirrors.ustc.edu.cn" >> ~/.pip/pip.conf && \
# echo "index-url = https://pypi.mirrors.ustc.edu.cn/simple" >> ~/.pip/pip.conf

# pip install "sglang[all]>=0.4.2.post4" --trusted-host pypi.mirrors.ustc.edu.cn -i http://pypi.mirrors.ustc.edu.cn/simple/


echo "[global]" > ~/.pip/pip.conf && \
echo "trusted-host = artifactory.ep.chehejia.com" >> ~/.pip/pip.conf && \
echo "index-url = https://artifactory.ep.chehejia.com/artifactory/api/pypi/pypi-remote/simple" >> ~/.pip/pip.conf

pip install "sglang[all]>=0.4.2.post4" --trusted-host artifactory.ep.chehejia.com -i https://artifactory.ep.chehejia.com/artifactory/api/pypi/pypi-remote/simple



# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/DeepSeek-V3-bf16
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/DeepSeek-R1-bf16
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-72B-Instruct
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-32B-Instruct
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen1.5-32B-Chat
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-72B-Instruct
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/penghuiling/model/Qwen/Qwen2.5-1.5B-Instruct
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-7B-Instruct
# MODEL_PATH=/mnt/pfs-guan-ssai/nlu/lizr/models/DeepSeek-R1-Distill-Qwen-7B
MODEL_PATH=/mnt/volumes/base-cv-ali-sh/wangze8/models/Qwen3-32B
# /mnt/pfs-gv8sxa/nlu/app/penghuiling/model/Qwen/Qwen2.5-0.5B
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/wangze8/model_output/vla-sft-0411/checkpoint-765
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/wangze8/model_output/vla-sft-6w-0411-ep2/checkpoint-510
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/wangze8/model_output/vla-sft-6w-0411-ep3/checkpoint-765
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/wangze8/model_output/vla-sft-6w-0412-10w-1p1-ep4-2/checkpoint-528
# MODEL_PATH=/mnt/pfs-gv8sxa/nlu/app/wangze8/model_output/vla-sft-0415-42w-ep4/checkpoint-4448
# /mnt/pfs-guan-ssai/nlu/lizr/models/Qwen2.5-32B-Instruct
MAX_LEN=131072

TOTAL_GPU=8

if [ "${RANK}" == "0" ];then
  python -m sglang.launch_server \
    --model-path ${MODEL_PATH} \
    --tp ${TOTAL_GPU} \
    --dist-init-addr ${MASTER_IP}:${MASTER_PORT} \
    --nnodes ${WORLD_SIZE} \
    --node-rank ${RANK} \
    --trust-remote-code \
    --max-running-requests 1000 \
    --context-length ${MAX_LEN} \
    --host 0.0.0.0 \
    --port 1688 \
    --json-model-override-args '{"rope_scaling":{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}}'
else
  python -m sglang.launch_server \
    --model-path ${MODEL_PATH} \
    --tp ${TOTAL_GPU} \
    --dist-init-addr ${MASTER_IP}:${MASTER_PORT} \
    --nnodes ${WORLD_SIZE} \
    --node-rank ${RANK} \
    --max-running-requests 1000 \
    --trust-remote-code \
    --context-length ${MAX_LEN} \
    --json-model-override-args '{"rope_scaling":{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}}'
fi
# --json-model-override-args '{"rope_scaling":{"rope_type":"yarn","factor":4.0,"original_max_position_embeddings":32768}}'

