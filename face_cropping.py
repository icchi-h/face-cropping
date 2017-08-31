#!/usr/bin/env python
# coding: utf-8

"""
__doc__
画像ファイルに写っている顔部分を特定して切り取り&保存するスクリプト
"""

__author__ = "Haruyuki Ichino"
__version__ = "1.7"
__date__ = "2017/08/31"

print(__doc__)

import sys
import glob
import cv2
import os.path
import argparse
import numpy as np
from datetime import datetime


def get_largest_face(faces):

    # サイズが1ならそれを返却
    if (len(faces) == 1):
        return faces[0]

    largest_face = faces[0];

    for i in range(1, len(faces)):
        width = faces[i][2]
        if width > largest_face[2]:
            largest_face = faces[i]

    return largest_face


# 切り抜いた画像の保存先ディレクトリ
output_dir = "./output/" # 出力ディレクトリの存在確認
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

# ログの出力先
log_dir = "./log/"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
# ログファイルの準備
now_str = datetime.now().strftime('%Y%m%d%H%M%S')
f = open(log_dir+'faild-files'+now_str+'.txt', 'w') # 書き込みモードで開く

# 基本的なモデルパラメータ
FLAGS = None

# 学習済モデルの種類
cascade = ["default","alt","alt2","tree","profile","nose"]

# オプションの設定
parser = argparse.ArgumentParser()
parser.add_argument(
    "--cascade",
    type=str,
    default="default",
    choices=cascade,
    help="cascade file."
)
parser.add_argument(
    "--scale",
    type=float,
    default=1.3,
    help="scaleFactor value of detectMultiScale."
)
parser.add_argument(
    "--neighbors",
    type=int,
    default=2,
    help="minNeighbors value of detectMultiScale."
)
parser.add_argument(
    "--min",
    type=int,
    default=100,
    help="minSize value of detectMultiScale."
)
parser.add_argument(
    "--detectedscale",
    type=float,
    default=1.1,
    help="Rectangle scale detected face."
)
parser.add_argument(
    "--resize",
    type=int,
    default=0,
    help="Output image size."
)
parser.add_argument(
    "-input",
    "--input_dir",
    type=str,
    default="./input/",
    help="The path of input directory."
)

# パラメータ取得と実行
FLAGS, unparsed = parser.parse_known_args()

# 分類器ディレクトリ(以下から取得)
# https://github.com/opencv/opencv/blob/master/data/haarcascades/
# https://github.com/opencv/opencv_contrib/blob/master/modules/face/data/cascades/

# 学習済モデルファイル
if   FLAGS.cascade == cascade[0]:#"default":
    cascade_path = "./models/haarcascade_frontalface_default.xml"
elif FLAGS.cascade == cascade[1]:#"alt":
    cascade_path = "./models/haarcascade_frontalface_alt.xml"
elif FLAGS.cascade == cascade[2]:#"alt2":
    cascade_path = "./models/haarcascade_frontalface_alt2.xml"
elif FLAGS.cascade == cascade[3]:#"tree":
    cascade_path = "./models/haarcascade_frontalface_alt_tree.xml"
elif FLAGS.cascade == cascade[4]:#"profile":
    cascade_path = "./models/haarcascade_profileface.xml"
elif FLAGS.cascade == cascade[5]:#"nose":
    cascade_path = "./models/haarcascade_mcs_nose.xml"

#カスケード分類器の特徴量を取得する
faceCascade = cv2.CascadeClassifier(cascade_path)

# 読み込んだ画像数
total_image_count = 0

# 顔検知に成功した数(デフォルトで0を指定)
face_detect_count = 0

# 入力ディレクトリパスのフォーマット確認
if (FLAGS.input_dir[-1] != "/"):
    FLAGS.input_dir += "/"

# 入力ディレクトリの存在確認
if not os.path.isdir(FLAGS.input_dir):
    print("Error: Not found input directory")
    sys.exit(1)

print("Processing...")

# 各クラスディレクトリ
classes = np.sort(os.listdir(FLAGS.input_dir))
for tclass in classes:

    # .DS_Storeのチェック
    if tclass == ".DS_Store":
        continue

    class_path = FLAGS.input_dir + tclass + '/'

    # ディレクトリじゃない場合はスキップ
    if not os.path.isdir(class_path):
        continue

    # 出力用のクラスディレクトリを作成
    output_class_path = output_dir + tclass + "/"
    if not os.path.exists(output_class_path):
        os.mkdir(output_class_path)

    print("Class: " + tclass + " ---------------------------------")
    files = np.sort(glob.glob(class_path + '*.*g'))
    total_image_count += len(files)
    count = 1
    for file in files:
        # 集めた画像データから顔が検知されたら、切り取り、保存する。
        if os.path.isfile(file):
            print("["+str(count)+"/"+str(len(files))+"] " + file)

            img = cv2.imread(file)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, scaleFactor=FLAGS.scale, minNeighbors=FLAGS.neighbors, minSize=(FLAGS.min, FLAGS.min))


            if len(faces) > 0:
                print("\tDetected face count: ", len(faces))

                largest_face = get_largest_face(faces)

                # 顔の中心点
                center_x = largest_face[0] + largest_face[2] / 2
                center_y = largest_face[1] + largest_face[3] / 2
                offset = largest_face[3] / 2 * FLAGS.detectedscale

                left = int(center_x - offset)
                top = int(center_y - offset)
                right = int(center_x + offset)
                bottom = int(center_y + offset)

                # 画像の切り出し
                cropped_img = img[top:bottom, left:right]

                # 画像のりサイズ
                if (FLAGS.resize):
                    try:
                        cropped_img = cv2.resize(cropped_img, (FLAGS.resize, FLAGS.resize))
                    except:
                        print("Error: Faild to resize cropped image")
                        continue

                #切り取った画像出力
                filename = file.split("/")[-1]
                cv2.imwrite(output_class_path + filename, cropped_img)
                print("\tSucceed: saved face image")
                face_detect_count = face_detect_count + 1
            else:
                f.writelines(file+"\n")
                print("\tError: Not found face")
        else:
            print("Error: Not found " + file)

        count += 1

f.close()

print()
try:
    print("Success Rate: " + str(round(face_detect_count/total_image_count*100, 2)) + "% (" + str(face_detect_count) + "/" + str(total_image_count) + ")")
except:
    print("Success Rate: 0% (0/0)")

print("Completed")
