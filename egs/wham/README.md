# Source separation using WHAM! dataset
## How to create dataset
### 1. Preate wsj0-mix
Download WSJ0 dataset and create wsj0-2mix manually.

### 2. Download WHAM noise and Create WHAM!
```
cd <REPOSITORY_ROOT>/egs/wham/common/
. ./prepare_wham.sh \
--wham_2speakers_root <WHAM_2speakers_ROOT> \
--wham_noise_root <WHAM_NOISE_ROOT> \
--wsjmix_2speakers_8k <WSJ0-MIX_2speakers_8k_ROOT> \
--wsjmix_2speakers_16k <WSJ0-MIX_2speakers_16k_ROOT> \
--create_from "wsjmix"
```
If you want to create from scratch, 
```
cd <REPOSITORY_ROOT>/egs/wham/common/
. ./prepare_wham.sh \
--wham_2speakers_root <WHAM_2speakers_ROOT> \
--wham_noise_root <WHAM_NOISE_ROOT> \
--wsj0_root <WSJ0_ROOT> \
--create_from "scratch"
```

## How to train and evaluate DNN model
See each subdirectory.

## Results