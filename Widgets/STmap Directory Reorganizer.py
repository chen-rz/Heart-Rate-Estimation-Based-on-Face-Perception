import os
import shutil

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]

old_dir_root = "D:/HR Estimation/STmap/"
new_dir_root = "D:/HR Estimation/STmap Dataset/"
newid = 1

for i in range(1, data_dir_num + 1):
    old_dir_pre = old_dir_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
                  ("0" + str(i) if i < 10 else str(i)) + "_"
    for sce in scenarios:
        old_dir_name = old_dir_pre + sce + "/"
        if not os.path.exists(old_dir_name):
            continue

        items = os.listdir(old_dir_name)
        if not items:
            continue

        items.sort(key=lambda x: int(x))
        for itm in items:
            shutil.copytree(old_dir_name + itm + "/", new_dir_root + str(newid) + "/")

            print("Copied " + old_dir_name + itm + "/ to " + new_dir_root + str(newid) + "/")
            newid += 1
