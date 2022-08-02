"""
参考：https://qiita.com/john-rocky/items/12949f1408cb703df081
公式：https://libraries.io/pypi/imgsim
AugNet：https://arxiv.org/abs/2106.06250

imgsimを使った画像類似度計算
"""
import glob
import os
import time

import cv2
import imgsim
import numpy as np

from utils import write_csv

file_inou_figre = glob.glob("./images/inou_figre/*.png")
file_inou_home = glob.glob("./images/inou_home/*.png")
file_other = glob.glob("./images/other/*.png")

vtr = imgsim.Vectorizer()

# csv保存先のフォルダ
csv_folder = ""  # r'./result/imgsim_gray/'
# 画像のグレイスケール変換
grayscale = False


class DistanceList:
    """
    ベクトル間の距離を測るクラス
    """

    def __init__(self, dist_mode="default"):
        if dist_mode == "default":
            self.dist = self.dist_default
        elif dist_mode == "norm":
            self.dist = self.dist_default_norm
        elif dist_mode == "cos":
            self.dist = self.dist_cos
        else:
            print("error : Not a proper dist_mode")
            exit()

    def normalize(self, v, axis=-1, order=2):
        """
        ベクトルの正規化を行う
        入力ベクトルvはlistでもndarrayでも

        Args:
            v (ndarray): vector
            axis (int, optional): axis of process. Defaults to -1.
            order (int, optional): l_n norm oder. Defaults to 2.

        Returns:
            ndarray: normalized v
        """
        l2 = np.linalg.norm(v, ord=order, axis=axis, keepdims=True)
        l2[l2 == 0] = 1
        v = v / l2
        return v

    def dist_cos(self, vec1, vec2):
        """
        cos類似度

        Args:
            vec1 (ndarray): vector1
            vec2 (ndarray): vector2

        Returns:
            double: 類似度
        """
        vec1 = self.normalize(vec1)
        vec2 = self.normalize(vec2)

        return abs(np.dot(vec1, vec2) - 1.0)

    def dist_default(self, vec1, vec2):
        """
        ベクトル1，2の類似度を返す

        Args:
            vec1 (ndarray): vector1
            vec2 (ndarray): vector2

        Returns:
            double: 類似度
        """
        return imgsim.distance(vec1, vec2)

    def dist_default_norm(self, vec1, vec2):
        """
        正規化したベクトルを用いて類似度を算出する

        Args:
            vec1 (ndarray): vector1
            vec2 (ndarray): vector2

        Returns:
            double: 類似度
        """
        vec1 = self.normalize(np.array(vec1))
        vec2 = self.normalize(np.array(vec2))

        return self.dist_default(vec1, vec2)


def convert_grayscale_3channel(img):
    """
    カラー画像をgrayscale画像に変換し
    （無理やり）3チャンネルにする

    Args:
        img (cv2image): cv2.imreadで読み込んだ画像

    Returns:
        cv2image: 各チャンネルすべての値が同じcv2image
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.merge([img, img, img])


def img_sim_folder(files1, files2, write_csv_file_name=None):
    """
    フォルダ内の画像に対して，距離を走査によって取得する関数
    距離は最大距離と最小距離が表示され，write optionによって
    すべての距離を表示できる

    Args:
        files1 (glob): 1つ目の画像郡
        files2 (glob): 2つ目の画像郡


    Return:
        list : 距離
    """
    # default, norm, cos
    dist_mode = "default"
    print("dist mode : {}".format(dist_mode))
    distance = DistanceList(dist_mode)

    max_dist = 0
    min_dist = 100
    dist_matrix = []

    for file1 in files1:
        file_name1 = os.path.basename(file1)[0]
        dist_row = [file_name1]
        for file2 in files2:
            img1 = cv2.imread(file1)
            img2 = cv2.imread(file2)
            if grayscale:
                img1 = convert_grayscale_3channel(img1)
                img2 = convert_grayscale_3channel(img2)

            vec1 = vtr.vectorize(img1)
            vec2 = vtr.vectorize(img2)
            dist = distance.dist(vec1, vec2)

            #print("{} : {} = {}".format(file_name1, file_name2, dist))

            if max_dist < dist:
                max_dist = dist
            if min_dist > dist:
                min_dist = dist

            dist_row.append(dist)
        dist_matrix.append(dist_row)
    print("最大類似距離 : {}\n最小類似距離 : {}".format(max_dist, min_dist))

    dist_column = [i for i in range(len(dist_row))]
    dist_matrix.insert(0, dist_column)

    if write_csv_file_name is not None:
        write_csv(csv_folder + write_csv_file_name + ".csv", dist_matrix)

    return dist_matrix


if __name__ == '__main__':
    time_start = time.time()
    img_sim_folder(file_inou_figre, file_inou_figre)
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_home, file_inou_home)
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_figre, file_other)
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_home, file_other)
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))
