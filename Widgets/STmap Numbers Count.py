import os.path

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]

dir_root = "../STmap/"
for i in range(1, data_dir_num + 1):
    dir_pre = dir_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
              ("0" + str(i) if i < 10 else str(i)) + "_"
    for sce in scenarios:
        dir_name = dir_pre + sce + "/"
        if not os.path.exists(dir_name):
            continue

        num_itm = len(os.listdir(dir_name))
        if num_itm == 0:
            os.rmdir(dir_name)
        else:
            print(str(num_itm) + " items in " + dir_name)
