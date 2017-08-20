# Face Cropping Script with Python
画像ファイルに写っている顔部分を特定して切り取り&保存するスクリプト

[FukuharaYohei](http://qiita.com/FukuharaYohei)さんが以下のQiitaサイト上で公開されているコードを自分用に改良。  
<http://qiita.com/FukuharaYohei/items/457737530264572f5a5b>

* 入力ディレクトリの指定
* 入力ディレクトリ内の画像ファイル(jpg,png)をすべて取得して処理
* 顔検出エリアの倍率指定
* 出力画像のリサイズオプション


## 使い方
**pythonパッケージをインストール**

* python-opencv

```bash
pip install opencv-python
```

**以下のようなディレクトリ構造に**
> 分類器ディレクトリ(以下から取得)
> https://github.com/opencv/opencv/blob/master/data/haarcascades/
> https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades>/

```
.
├── README.md
├── face_cropping.py
├── input
│   ├── class1
│   │   ├── class1_1.jpg
│   │   ├── class1_10.jpg
│   │   ├── class1_11.jpg
│   ├── class2
│   │   ├── class2_1.jpg
│   │   ├── class2_10.jpg
│   │   ├── class2_11.jpg
│   ├── class3
│   │   ├── class3_1.jpg
│   │   ├── class3_10.jpg
│   │   └── class3_11.jpg
├── models
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_alt2.xml
│   ├── haarcascade_frontalface_alt_tree.xml
│   └── haarcascade_frontalface_default.xml
└── output
```

**実行**
顔検出の各種パラメータによって顔の検出率が変化するので、対象画像に合わせて調節してください。

```bash
# sample
python face_cropping.py --input_dir "./input/" --resize 224 --min 100
```
