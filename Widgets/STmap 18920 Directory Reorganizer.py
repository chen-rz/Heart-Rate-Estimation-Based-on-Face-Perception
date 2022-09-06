import os.path
import random
import shutil

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]

train_cnt = 1
eval_cnt = 1

stmap_root = "../STmap/"
train_dir = "../Datasets/STmap 18920 Training and Evaluation/STmap 18920 Training/"
eval_dir = "../Datasets/STmap 18920 Training and Evaluation/STmap 18920 Evaluation/"
for i in range(1, data_dir_num + 1):
    stmap_pre = stmap_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
                ("0" + str(i) if i < 10 else str(i)) + "_"

    for sce in scenarios:
        stmap_name = stmap_pre + sce + "/"
        if not os.path.exists(stmap_name):
            continue

        c_list = os.listdir(stmap_name)
        c_list.sort(key=lambda x: int(x))

        for c in c_list:
            dice = random.random()

            # 20% for Evaluation
            if dice < 0.175:
                shutil.copytree(stmap_name + str(c) + "/", eval_dir + str(eval_cnt) + "/")
                print("Copied " + stmap_name + str(c) + "/" + " to " + eval_dir + str(eval_cnt) + "/")
                eval_cnt += 1
            else:
                shutil.copytree(stmap_name + str(c) + "/", train_dir + str(train_cnt) + "/")
                print("Copied " + stmap_name + str(c) + "/" + " to " + train_dir + str(train_cnt) + "/")
                train_cnt += 1
