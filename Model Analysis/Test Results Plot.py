import matplotlib.pyplot as pl

model_id = "1662209768"

rf = open("./test_results/ground_truth/test_gt_model_" + model_id + ".txt", 'r')
gt = eval(rf.readline())
rf.close()

rf = open("./test_results/output_value/test_output_model_" + model_id + ".txt", 'r')
output = eval(rf.readline())
rf.close()

gt = [x * 10 for x in gt]
output = [x * 10 for x in output]

data_n = range(1, len(gt) + 1)

over_x, under_x, over_y, under_y = [], [], [], []
for i in range(len(gt)):
    if output[i] - gt[i] > 0:
        over_x.append(data_n[i])
        over_y.append(output[i] - gt[i])
    else:
        under_x.append(data_n[i])
        under_y.append(output[i] - gt[i])

pl.plot(data_n, gt, color='tab:cyan', linestyle='-', label="Ground Truth")
pl.plot(data_n, output, color='tab:pink', linestyle='-', label="Output Value")
pl.title("Test Result of Model " + model_id)
pl.ylabel("Heart Rate")
pl.legend()
pl.tight_layout()
pl.show()

pl.vlines(over_x, 0, over_y, color='tab:green', label="Overestimated")
pl.vlines(under_x, under_y, 0, color='tab:red', label="Underestimated")
pl.ylabel("Heart Rate")
pl.legend()
pl.tight_layout()
pl.show()
