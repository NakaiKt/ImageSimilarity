"""
参考 : https://www.pc-koubou.jp/magazine/43855
"""
import glob
import cv2
import os
import time

from image_imgsim import write_csv

file_inou_figre = glob.glob("./images/inou_figre/*.png")
file_inou_home = glob.glob("./images/inou_home/*.png")
file_other = glob.glob("./images/other/*.png")
csv_folder = ""

IMG_SIZE = (224, 224) #200



def img_sim_folder(files1, files2, write_csv_file_name = None):
    dist_matrix = []
    max_dist = 0
    min_dist = 10000

    for file1 in files1:
        file_name1 = os.path.basename(file1)[0]
        dist_row = [file_name1]
        for file2 in files2:
            # ファイル読み込み（グレースケール）
            img1 = cv2.imread(file1, cv2.IMREAD_GRAYSCALE)
            img2 = cv2.imread(file2, cv2.IMREAD_GRAYSCALE)
            # 画像リサイズ
            img1 = cv2.resize(img1, IMG_SIZE)
            img2 = cv2.resize(img2, IMG_SIZE)

            # Brute-Foce Matcherによる総当たりマッチングで距離の平均を出す
            bf = cv2.BFMatcher(cv2.NORM_HAMMING)

            # AKAZEを適用して特徴点検出
            detector = cv2.AKAZE_create()
            kernel_point1, distance1 = detector.detectAndCompute(img1, None)
            kernel_point2, distance2 = detector.detectAndCompute(img2, None)

            # BF matchで総当りマッチング
            matches = bf.match(distance1, distance2)
            # 距離の和を取り平均を算出
            dist = [m.distance for m in matches]
            ret = sum(dist) / len(dist)

            if max_dist < ret:
                max_dist = ret
            if min_dist > ret:
                min_dist = ret

            dist_row.append(ret)
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
