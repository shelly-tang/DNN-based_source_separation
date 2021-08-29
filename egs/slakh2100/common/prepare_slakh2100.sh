#!/bin/bash

slakh2100_root="../../../dataset/slakh2100"
is_tiny=0

. ./parse_options.sh || exit 1

mkdir -p "${slakh2100_root}"

if [ ${is_tiny} -eq 0 ]; then
    file="slakh2100_flac_redux.tar.gz"
    wget "https://zenodo.org/record/4599666/files/${file}" -P "/tmp"
    unzip "/tmp/${file}" -d "${slakh2100_root}"
    rm "/tmp/${file}"
else
    file="babyslakh_16k.tar.gz"
    wget "https://zenodo.org/record/4603870/files/${file}" -P "/tmp"
    unzip "/tmp/${file}" -d "${slakh2100_root}"
    rm "/tmp/${file}"
fi
