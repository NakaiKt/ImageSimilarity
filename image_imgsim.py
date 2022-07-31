import cv2
import imgsim
import glob
import os
import numpy as np
import csv

"""
imgsimを使った画像類似度計算
参考：https://qiita.com/john-rocky/items/12949f1408cb703df081
公式：https://libraries.io/pypi/imgsim
AugNet：https://arxiv.org/abs/2106.06250
"""

file_inou_figre = glob.glob("./images/inou_figre/*.png")
file_inou_home = glob.glob("./images/inou_home/*.png")
file_other = glob.glob("./images/other/*.png")

vtr = imgsim.Vectorizer()


class DistanceList:
    """
    ベクトル間の距離を測るクラス
    """
    def __init__(self, dist_mode = "default"):
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
        l2 = np.linalg.norm(v, ord = order, axis=axis, keepdims=True)
        l2[l2==0] = 1
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

def write_csv(file_name, matrix):
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(matrix)
    f.close()

def img_sim_folder(files1, files2, write = False):
    """
    フォルダ内の画像に対して，距離を走査によって取得する関数
    距離は最大距離と最小距離が表示され，write optionによって
    すべての距離を表示できる

    Args:
        files1 (glob): _description_
        files2 (glob): _description_
        write (bool, optional): _description_. Defaults to False.

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

            vec1 = vtr.vectorize(img1)
            vec2 = vtr.vectorize(img2)
            dist = distance.dist(vec1, vec2)

            file_name2 = os.path.basename(file2)[0]

            if write:
                print("{} : {} = {}".format(file_name1, file_name2, dist))

            if max_dist < dist:
                max_dist = dist
            if min_dist > dist:
                min_dist = dist

            dist_row.append(dist)
        dist_matrix.append(dist_row)
    print("最大類似距離 : {}\n最小類似距離 : {}".format(max_dist, min_dist))

    dist_column = [ i for i in range(len(dist_row))]
    dist_matrix.insert(0, dist_column)
    return dist_matrix

if __name__ == '__main__':
    table_name = "inou_figre"
    print(table_name)
    matrix = img_sim_folder(file_inou_figre, file_inou_figre)
    write_csv(table_name + ".csv", matrix)

    table_name = "inou_home"
    print("\n", table_name)
    matrix = img_sim_folder(file_inou_home, file_inou_home)
    write_csv(table_name + ".csv", matrix)

    table_name = "inou_figre_other"
    print("\n", table_name)
    matrix = img_sim_folder(file_inou_figre, file_other)
    write_csv(table_name + ".csv", matrix)

    table_name = "inou_home_other"
    print("\n", table_name)
    matrix = img_sim_folder(file_inou_home, file_other)
    write_csv(table_name + ".csv", matrix)
