# ImageSimilarity
伊能忠敬像および旧伊能忠敬邸と他の画像との類似度を検証
行った検証は
* imgsim
* opencv AKAZA
* ImageHash

## imgsim
[github](https://github.com/chenmingxiang110/AugNet)
[paper](https://arxiv.org/abs/2106.06250)
AugNet[^1] というモデルによる画像分類手法．（AugはAugmentationから）
画像の一部のみ切り出す水増し手法によって，同じ画像の異なる領域に類似性を見出そうとした手法．
画像を192次元のベクトルに落とし込み，l2normなどで類似度を出す．
**背景寄与が大きい**（論文いわく）

|-|-|
|------|-----|
|dataset|ImageNet (minibarch 1024)
|augment|回転，ガウシアンノイズ，クロップ，リサイズ，色相，彩度，明度，cutout
|aug rate|8倍
|crop size|32 x 32
|architecture| NIN(Network In Network[^2]) 軽量モデル


[^1]: Mingxiang Chen, Zhanguo Chang, Haonan Lu, Bitao Yang, Zhuang Li, Liufang Guo, Zhecheng Wang
"AugNet: End-to-End Unsupervised Visual Representation Learning with Image Augmentation"
arXiv:2106.06250, 11 jun 2021
[^2]: Min Lin, Qiang Chen, Shuicheng Yan, "Network In Network", 10 pages, 4 figures, for iclr2014

## openCV AKAZE
[参考](https://miyashinblog.com/opencvakaze-knn/)
（日本語の「風」が由来らしい）
特許がなく，商用 / 非商用どちらでも．
類似手法のSIFTやSURFは特許があるとのこと．
**背景寄与が大きい**
k-meansがベース．．．？？

## ImageHash
[公式](https://pypi.org/project/ImageHash/)
元ネタは[hacherfactor](https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)というものらしい．
暗号化ハッシュとは異なり，似た画像ほど近いハッシュ値になる．
画像サイズ，アスペクト比，明度彩度に左右されにくいが，
**背景寄与が大きい**


### result
[imgsim](https://docs.google.com/spreadsheets/d/1AfFsY0MBBPsuoY6UXMPSBAcimj3Dx2OeJbljOpNNv-E/edit?usp=sharing)
[imgsim grayscale](https://docs.google.com/spreadsheets/d/1OJKaNU1Snu0cZ-YROBK7s4_LnJdj-KwV8PrTceQrpXM/edit?usp=sharing)
[opencv_AKAZE](https://docs.google.com/spreadsheets/d/1m0ezvB1kHl9bUtQ712vXakJxpDjSlkqAbh3YHJTUAtw/edit?usp=sharing)
[ImageHash](https://docs.google.com/spreadsheets/d/1zt39OlvDaAteIf3u6aLK3i8LvTwBWJxdt8i9FIOabac/edit?usp=sharing)

### 結論・今後
**背景寄与が大きい**ことが難点．
imagesimのような深層モデルは学習データがおそらくImageNet（一般画像）なので，
ランドマークを集めたデータセットなどを見つけられれば再学習できるかも．
また画像はカラーよりも白黒画像が良さそう．
とにかくこれらだけで伊能忠敬像などを判別するのは難しそう．

他の可能性として，GoogleのVisionAPI（有料）にある[LANDMARK_DETECTION](https://cloud.google.com/vision/docs/detecting-landmarks?hl=ja)や，案内板のようなもののテキスト検出などがあるのではないか．

### env
Cuda compilation tools, release 11.7, V11.7.64
Build cuda_11.7.r11.7/compiler.31294372_0
|-|spec|
|-------|----------|
|cpu| Ryzen 7 1700X|
|RAM| 8GB
|GPU|GeForce GTX 1060 3G

#####version
Python 3.10.5


|Package|            Version|
|------------------| ---------|
|autopep8           |1.6.0
|certifi            |2022.6.15
|charset-normalizer |2.1.0
|cycler             |0.11.0
|fonttools          |4.34.4
|idna               |3.3
|ImageHash          |4.2.1
|imgsim             |0.1.2
|kiwisolver         |1.4.4
|matplotlib         |3.5.2
|numpy              |1.23.1
|opencv-python      |4.6.0.66
|packaging          |21.3
|Pillow             |9.2.0
|pip                |22.2.1
|pycodestyle        |2.9.0
|pyparsing          |3.0.9
|python-dateutil    |2.8.2
|PyWavelets         |1.3.0
|requests           |2.28.1
|scipy              |1.9.0
|setuptools         |58.1.0
|six                |1.16.0
|toml               |0.10.2
|torch              |1.12.0
|torchinfo          |1.7.0
|torchvision        |0.13.0
|typing_extensions  |4.3.0
|urllib3            |1.26.11