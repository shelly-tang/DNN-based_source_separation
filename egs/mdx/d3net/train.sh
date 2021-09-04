#!/bin/bash

exp_dir="./exp"
continue_from=""
tag=""

sources="[drums,bass,other,vocals]"
target='vocals'
patch=256
valid_duration=100

musdb18_root="../../../dataset/musdb18hq"
sr=44100

window_fn='hann'
fft_size=4096
hop_size=1024

# model
config_path="./config/sample/${target}.yaml"

# Criterion
criterion='mse'

# Optimizer
optimizer='adam'
lr=1e-3
anneal_lr=1e-4
weight_decay=0
max_norm=0 # 0 is handled as no clipping

batch_size=6
samples_per_epoch=7726 # If you specified samples_per_epoch=-1, samples_per_epoch is computed as 3863, which corresponds to total duration of training data. 7726 = 3863 x 2.
epochs=50
anneal_epoch=40

use_cuda=1
overwrite=0
num_workers=2
seed=111
gpu_id="0"

. ./path.sh
. parse_options.sh || exit 1

if [ -z "${tag}" ]; then
    save_dir="${exp_dir}/sr${sr}/${sources}/patch${patch}/${criterion}/stft${fft_size}-${hop_size}_${window_fn}-window"
    if [ ${samples_per_epoch} -gt 0 ]; then
        save_dir="${save_dir}/b${batch_size}_e${epochs}-${anneal_epoch}-s${samples_per_epoch}_${optimizer}-lr${lr}-${anneal_lr}-decay${weight_decay}_clip${max_norm}/seed${seed}"
    else
        save_dir="${save_dir}/b${batch_size}_e${epochs}-${anneal_epoch}_${optimizer}-lr${lr}-${anneal_lr}-decay${weight_decay}_clip${max_norm}/seed${seed}"
    fi
else
    save_dir="${exp_dir}/${tag}"
fi

model_dir="${save_dir}/model/${target}"
loss_dir="${save_dir}/loss/${target}"
sample_dir="${save_dir}/sample/${target}"
config_dir="${save_dir}/config"
log_dir="${save_dir}/log/${target}"

if [ ! -e "${config_dir}" ]; then
    mkdir -p "${config_dir}"
fi

config_name=`basename ${config_path}`

if [ ! -e "${config_dir}/${config_name}" ]; then
    cp "${config_path}" "${config_dir}/${config_name}"
fi

if [ ! -e "${log_dir}" ]; then
    mkdir -p "${log_dir}"
fi

time_stamp=`TZ=UTC-9 date "+%Y%m%d-%H%M%S"`

export CUDA_VISIBLE_DEVICES="${gpu_id}"

train.py \
--musdb18_root ${musdb18_root} \
--config_path "${config_path}" \
--sr ${sr} \
--patch_size ${patch} \
--valid_duration ${valid_duration} \
--window_fn "${window_fn}" \
--fft_size ${fft_size} \
--hop_size ${hop_size} \
--sources ${sources} \
--target ${target} \
--criterion ${criterion} \
--optimizer ${optimizer} \
--lr ${lr} \
--anneal_lr ${anneal_lr} \
--weight_decay ${weight_decay} \
--max_norm ${max_norm} \
--batch_size ${batch_size} \
--samples_per_epoch ${samples_per_epoch} \
--epochs ${epochs} \
--anneal_epoch ${anneal_epoch} \
--model_dir "${model_dir}" \
--loss_dir "${loss_dir}" \
--sample_dir "${sample_dir}" \
--continue_from "${continue_from}" \
--use_cuda ${use_cuda} \
--overwrite ${overwrite} \
--num_workers ${num_workers} \
--seed ${seed} | tee "${log_dir}/train_${time_stamp}.log"
