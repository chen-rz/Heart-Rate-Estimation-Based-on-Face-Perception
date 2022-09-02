import os
import pandas as pd

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]

for i in range(1, data_dir_num + 1):
    strNo = "0" + str(i) if i < 10 else str(i)
    for sce in scenarios:
        file_dir = "./PFFdatabase/" + strNo + "/" + strNo + "_" + sce + "_f.txt"
        if not os.path.exists(file_dir):
            continue

        gt_HR = []
        file = open(file_dir, mode='r')
        file.readline()  # 去除第一行
        line = file.readline()
        while line:
            gt_HR.append(line.split(sep=',')[1])
            line = file.readline()
        file.close()

        out_csv_dir = "./gt_HR/" + strNo + "/" + strNo + "_" + sce + "_gt_HR.csv"
        df = pd.DataFrame(gt_HR)
        df.to_csv(out_csv_dir, index=False, header=False)
