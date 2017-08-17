# Face Trimming Script with Python
画像ファイルに写っている顔部分を特定して切り取り&保存するスクリプト

[FukuharaYohei](http://qiita.com/FukuharaYohei)さんが以下のQiitaサイト上で公開されているコードを自分用に改良。  
<http://qiita.com/FukuharaYohei/items/457737530264572f5a5b>

* 入力ディレクトリの指定
* 入力ディレクトリ内のjpgファイルをすべて取得して処理
* 顔検出エリアの倍率指定
* 出力画像のリサイズオプション


## 使い方
**pythonパッケージをインストール**

* python-opencv

```bash
pip install python-opencv
```

**以下のようなディレクトリ構造に**
> 分類器ディレクトリ(以下から取得)
> https://github.com/opencv/opencv/blob/master/data/haarcascades/
> https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades>/

```
.
├── face_crop.py
├── input
│   └── 1.jpg
├── models
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_alt2.xml
│   ├── haarcascade_frontalface_alt_tree.xml
│   └── haarcascade_frontalface_default.xml
└── output
```

**実行**

```bash
# sample
python face_crop.py --input_path "./input/" --resize 224
```
