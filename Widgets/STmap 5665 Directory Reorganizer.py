import os
import shutil
import random

rf = open("./Chosen STmaps for Lite Dataset.txt", 'r')
chosen = eval(rf.readline())
rf.close()

train_dir_root = "../Datasets/STmap 5665 Training and Evaluation/STmap 5665 Training/"
eval_dir_root = "../Datasets/STmap 5665 Training and Evaluation/STmap 5665 Evaluation/"

train_id = 1
eval_id = 1

for c in chosen:
    items = os.listdir(c)
    items.sort(key=lambda x: int(x))

    for i in items:
        dice = random.random()

        # 20% for Evaluation
        if dice < 0.2:
            shutil.copytree(c + i + "/", eval_dir_root + str(eval_id) + "/")
            print("Copied " + c + i + "/" + " to " + eval_dir_root + str(eval_id) + "/")
            eval_id += 1
        else:
            shutil.copytree(c + i + "/", train_dir_root + str(train_id) + "/")
            print("Copied " + c + i + "/" + " to " + train_dir_root + str(train_id) + "/")
            train_id += 1
