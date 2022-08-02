"""
参考：https://self-development.info/%E3%80%90python%E3%80%91%E7%94%BB%E5%83%8F%E3%81%AE%E9%A1%9E%E4%BC%BC%E5%BA%A6%E6%AF%94%E8%BC%83%E3%81%8C%E5%8F%AF%E8%83%BD%E3%81%AAimagehash%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC/

ImageHashを使った類似度
"""

import glob
import os
import time

import imagehash
from PIL import Image

from utils import write_csv

file_inou_figre = glob.glob("./images/inou_figre/*.png")
file_inou_home = glob.glob("./images/inou_home/*.png")
file_other = glob.glob("./images/other/*.png")

csv_folder = ""


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

    dist_matrix = []
    max_dist = 0
    min_dist = 10000

    for file1 in files1:
        file_name1 = os.path.basename(file1)[0]
        dist_row = [file_name1]
        for file2 in files2:
            # ハッシュ値計算
            hash = imagehash.average_hash(Image.open(file1))
            otherhash = imagehash.average_hash(Image.open(file2))

            dist = hash - otherhash

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
    img_sim_folder(file_inou_figre, file_inou_figre,
                   write_csv_file_name="inou_figre")
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_home, file_inou_home,
                   write_csv_file_name="inou_home")
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_figre, file_other,
                   write_csv_file_name="inou_figre_other")
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))

    time_start = time.time()
    img_sim_folder(file_inou_home, file_other,
                   write_csv_file_name="inou_home_other")
    time_end = time.time()
    print("実行時間(s) {}\n".format(time_end - time_start))
