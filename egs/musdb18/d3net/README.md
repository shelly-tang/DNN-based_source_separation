# D3Net
Reference: [D3Net: Densely connected multidilated DenseNet for music source separation](https://arxiv.org/abs/2010.01733)

## How to Run
### 0. Preparation
Build environment by pip
```
cd <REPOSITORY_ROOT>/egs/musdb18/
pip install -r requirements.txt
```
or by conda.
```
cd <REPOSITORY_ROOT>/egs/musdb18/
conda env create -f environment-gpu.yaml
```

Download MUSDB18 dataset and convert to `.wav`.
```
cd <REPOSITORY_ROOT>/egs/musdb18/common/
. ./prepare_musdb18.sh \
--musdb18_root <MUSDB18_ROOT> \
--is_hq 0 \
--to_wav 1
```
If you want to download MUSDB18-HQ dataset, 
```
cd <REPOSITORY_ROOT>/egs/musdb18/common/
. ./prepare_musdb18.sh \
--musdb18_root <MUSDB18HQ_ROOT> \
--is_hq 1
```

### 1. Training
```
cd <REPOSITORY_ROOT>/egs/musdb18/d3net/
. ./train.sh \
--exp_dir <OUTPUT_DIR> \
--target <TARGET> \
--config_path <CONFIG_PATH>
```

If you want to resume training,
```
. ./train.sh \
--exp_dir <OUTPUT_DIR> \
--continue_from <MODEL_PATH> \
--target <TARGET> \
--config_path <CONFIG_PATH>
```

### 2. Evaluation
```
cd <REPOSITORY_ROOT>/egs/musdb18/d3net/
. ./test.sh --exp_dir <OUTPUT_DIR>
```

## Results
- SDR [dB] (median of median SDR of each song computed by `museval`)
- You can check example in `exp/paper`.

| Model | Vocals | Drums | Bass | Other | Accompaniment | Average | Note |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| D3Net w/o dilation | - | - | - | - | - | - | - |
| D3Net standard dilation | - | - | - | - | - | - | - |
| D3Net | 6.58 | 6.46 | 5.12 | 4.54 | 13.06 | 5.68 | Epoch is chosen by validation loss. |
| D3Net | 6.63 | 6.40 | 5.24 | 4.58 | 13.24 | 5.71 | After 50 epochs. |
| D3Net | 7.24 | 7.01 | 5.25 | 4.53 | 13.52 | 6.01 | Official report. |

- You can separate your audio using these pretrained models. See `egs/tutorials/d3net/separate.ipynb` or click [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/d3net/separate.ipynb).