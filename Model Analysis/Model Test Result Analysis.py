import numpy as np
import pandas as pd

rf = open("./model_test_results/model_test_cuda_1661906413.txt")
rslt = eval(rf.readline())
rf.close()

intervals = pd.cut(pd.Series(rslt), np.arange(0, 5.0, 0.1)).value_counts()

average = np.average(rslt)

print(average)
