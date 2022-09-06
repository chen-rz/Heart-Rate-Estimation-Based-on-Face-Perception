import os.path

import pandas as pd

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]
chosen = []

dir_root = "../gt_HR/"
stmap_root = "../STmap/"
for i in range(1, data_dir_num + 1):
    dir_pre = dir_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
              ("0" + str(i) if i < 10 else str(i)) + "_"
    stmap_pre = stmap_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
                ("0" + str(i) if i < 10 else str(i)) + "_"

    for sce in scenarios:
        dir_name = dir_pre + sce + "_gt_HR.csv"
        stmap_name = stmap_pre + sce + "/"
        if not os.path.exists(stmap_name):
            continue
        if not os.path.exists(dir_name):
            continue

        df = pd.read_csv(dir_name)

        if 175 <= df.shape[0] <= 185:
            print(str(df.shape[0]) + " lines in " + dir_name)
            chosen.append(stmap_name)

wf = open("./Chosen STmaps for Lite Dataset.txt", 'w')
wf.write(str(chosen))
wf.close()

stmap_count = 0
dm, ds, nm, ns = 0, 0, 0, 0
for cd in chosen:
    stmap_count += len(os.listdir(cd))
    if "DM" in cd:
        dm += 1
    elif "DS" in cd:
        ds += 1
    elif "NM" in cd:
        nm += 1
    elif "NS" in cd:
        ns += 1

print(stmap_count)
print("DM:{0} DS:{1} NM:{2} NS:{3}".format(dm, ds, nm, ns))
