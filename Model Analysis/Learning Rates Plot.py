import time
import matplotlib.pyplot as pl

time_str = "1662433109"
time_stamp = time.ctime(float(time_str))

rf = open("./learning_rates/model_learning_rates_cuda_" + time_str + ".txt", 'r')
lr = eval(rf.readline())
rf.close()

epoch = range(1, len(lr) + 1)

pl.plot(epoch, lr, marker='.', color='C4', linestyle='-')
pl.title("Learning Rates of Model @ " + time_stamp)
pl.xlabel("Epoch")
pl.ylabel("Learning Rate")

pl.tight_layout()
pl.show()
