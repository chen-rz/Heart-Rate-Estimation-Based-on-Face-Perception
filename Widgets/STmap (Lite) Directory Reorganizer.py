import os
import shutil

rf = open("./Chosen STmaps for Lite Dataset.txt", 'r')
chosen = eval(rf.readline())
rf.close()

new_dir_root = "../STmap Dataset Lite/"
newid = 1

for c in chosen:
    items = os.listdir(c)
    items.sort(key=lambda x:int(x))

    for i in items:
        shutil.copytree(c + i + "/", new_dir_root + str(newid) + "/")
        print("Copied " + c + i + "/" + " to " + new_dir_root + str(newid) + "/")
        newid += 1
