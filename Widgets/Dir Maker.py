import os

data_dir_num = 13
scenarios = ["DM", "DS", "NM", "NS", "NSE"]

# dir_root = "./face_landmarks_81p/"
dir_root = "./STmap/"
for i in range(1, data_dir_num + 1):
    dir_pre = dir_root + ("0" + str(i) if i < 10 else str(i)) + "/"
    os.mkdir(dir_pre)
    print("Created directory " + dir_pre)

for i in range(1, data_dir_num + 1):
    dir_pre = dir_root + ("0" + str(i) if i < 10 else str(i)) + "/" + \
              ("0" + str(i) if i < 10 else str(i)) + "_"
    for sce in scenarios:
        dir_name = dir_pre + sce + "/"
        os.mkdir(dir_name)
        print("Created directory " + dir_name)
