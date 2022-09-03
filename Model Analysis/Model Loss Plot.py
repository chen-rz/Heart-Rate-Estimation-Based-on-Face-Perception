import time
import matplotlib.pyplot as pl

time_str = "1662170218"
time_stamp = time.ctime(float(time_str))

rf = open("./model_loss/loss/model_loss_cuda_" + time_str + ".txt", 'r')
loss = eval(rf.readline())
rf.close()

rf = open("./model_loss/eval_loss/model_eval_loss_cuda_" + time_str + ".txt", 'r')
eval_loss = eval(rf.readline())
rf.close()

rf = open("./model_loss/loss_hr/model_loss_hr_cuda_" + time_str + ".txt", 'r')
loss_hr = eval(rf.readline())
rf.close()

# # 8100
# len_train_loader = 3211
# len_eval_loader = 336
#
# # 5665
# # len_train_loader = 2264
# # len_eval_loader = 228
#
# loss = [x / len_train_loader for x in loss]
# eval_loss = [x / len_eval_loader for x in eval_loss]
# loss_hr = [x / len_train_loader for x in loss_hr]

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
