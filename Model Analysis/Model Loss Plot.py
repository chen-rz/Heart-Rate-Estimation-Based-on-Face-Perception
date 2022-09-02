import time
import matplotlib.pyplot as pl

time_str = "1662080288"
time_stamp = time.ctime(float(time_str))

rf = open("./model_loss/model_loss_cuda_" + time_str + ".txt", 'r')
loss = eval(rf.readline())
rf.close()

rf = open("./model_loss/model_eval_loss_cuda_" + time_str + ".txt", 'r')
eval_loss = eval(rf.readline())
rf.close()

rf = open("./model_loss/model_loss_hr_cuda_" + time_str + ".txt", 'r')
loss_hr = eval(rf.readline())
rf.close()


epoch = range(1, len(loss) + 1)

pl.plot(epoch, loss, marker='.', color='C0', linestyle='-')
pl.title("Loss of Model @ " + time_stamp)
pl.xlabel("Epoch")
pl.ylabel("Loss")
pl.show()

pl.plot(epoch, eval_loss, marker='.', color='C1', linestyle='-', label="Validation")
pl.plot(epoch, loss_hr, marker='.', color='C2', linestyle='-', label="Training")
pl.title("Loss_HR of Model @ " + time_stamp)
pl.xlabel("Epoch")
pl.ylabel("Loss_HR")

pl.legend()
pl.tight_layout()
pl.show()
