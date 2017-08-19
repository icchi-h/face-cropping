import sys
import glob
import cv2
import os.path
import argparse


# 切り抜いた画像の保存先ディレクトリ
output_path = "./output/"
# 出力ディレクトリの存在確認
if not os.path.isdir(output_path):
    os.mkdir(output_path)

# 基本的なモデルパラメータ
FLAGS = None

# 学習済モデルの種類
cascade = ["default","alt","alt2","tree","profile","nose"]

# 直接実行されている場合に通る(importされて実行時は通らない)
if __name__ == "__main__":
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
        "--input_path",
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

# 顔検知に成功した数(デフォルトで0を指定)
face_detect_count = 0


# dataディレクトリの存在確認
if not os.path.isdir(FLAGS.input_path):
    print("Error: Not found input directory")
    sys.exit(1)

print("Processing...")

files = glob.glob(FLAGS.input_path + '*.jpg')
count = 0
for file in files:
    # 集めた画像データから顔が検知されたら、切り取り、保存する。
    if os.path.isfile(file):
        print("["+str(count)+"/"+str(len(files))+"]\t" + file)

        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(gray, scaleFactor=FLAGS.scale, minNeighbors=FLAGS.neighbors, minSize=(FLAGS.min, FLAGS.min))


        if len(face) > 0:
            for rect in face:
                center_x = rect[0] + rect[2] / 2
                center_y = rect[1] + rect[3] / 2
                offset = rect[3] / 2 * FLAGS.detectedscale

                left = int(center_x - offset)
                top = int(center_y - offset)
                right = int(center_x + offset)
                bottom = int(center_y + offset)

                # 画像の切り出し
                cropped_img = img[top:bottom, left:right]

                # 画像のりサイズ
                if (FLAGS.resize):
                    cropped_img = cv2.resize(cropped_img, (FLAGS.resize, FLAGS.resize))

                #切り取った画像出力
                filename = file.split("/")[-1]
                cv2.imwrite(output_path + filename, img[top:bottom, left:right])
                face_detect_count = face_detect_count + 1
        else:
            print("Not found: " + file)
    else:
        print("Not found: " + file)

    count += 1

print("Completed")
