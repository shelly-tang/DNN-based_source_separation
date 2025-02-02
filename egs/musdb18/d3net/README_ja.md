# D3Net
参考文献: [D3Net: Densely connected multidilated DenseNet for music source separation](https://arxiv.org/abs/2010.01733)

## 実行方法
### 0. データセットの準備
pipによる環境構築
```
cd <REPOSITORY_ROOT>/egs/musdb18/
pip install -r requirements.txt
```
or condaによる環境構築
```
cd <REPOSITORY_ROOT>/egs/musdb18/
conda env create -f environment-gpu.yaml
```

MUSDB18データセットのダウンロードと`.wav`への変換
```
cd <REPOSITORY_ROOT>/egs/musdb18/common/
. ./prepare_musdb18.sh \
--musdb18_root <MUSDB18_ROOT> \
--is_hq 0 \
--to_wav 1
```
MUSDB18-HQデータセットを用いる場合，
```
cd <REPOSITORY_ROOT>/egs/musdb18/common/
. ./prepare_musdb18.sh \
--musdb18_root <MUSDB18HQ_ROOT> \
--is_hq 1
```

### 1. 学習
```
cd <REPOSITORY_ROOT>/egs/musdb18/d3net/
. ./train.sh \
--exp_dir <OUTPUT_DIR> \
--target <TARGET> \
--config_path <CONFIG_PATH>
```

学習を途中から再開したい場合，
```
. ./train.sh \
--exp_dir <OUTPUT_DIR> \
--continue_from <MODEL_PATH> \
--target <TARGET> \
--config_path <CONFIG_PATH>
```

### 2. 評価
```
cd <REPOSITORY_ROOT>/egs/musdb18/d3net/
. ./test.sh --exp_dir <OUTPUT_DIR>
```

## 実験結果
- SDR [dB] (`museval`によって計算された各曲のSDRの中央値の中央値)
- 実験結果の例を`exp/paper`で確認可能．

| Model | Vocals | Drums | Bass | Other | Accompaniment | Average | Note |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| D3Net w/o dilation | - | - | - | - | - | - | - |
| D3Net standard dilation | - | - | - | - | - | - | - |
| D3Net | 6.58 | 6.46 | 5.12 | 4.54 | 13.06 | 5.68 | 検証ロスが最小となるエポックで学習を止めた場合． |
| D3Net | 6.63 | 6.40 | 5.24 | 4.58 | 13.24 | 5.71 | 50エポック学習後 |
| D3Net | 7.24 | 7.01 | 5.25 | 4.53 | 13.52 | 6.01 | 公式実装 |

- 学習済みモデルを使って分離を試すことができます．`egs/tutorials/d3net/separate_ja.ipynb`を見るか， [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tky823/DNN-based_source_separation/blob/main/egs/tutorials/d3net/separate_ja.ipynb)にとんでください．