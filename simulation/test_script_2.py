import numpy as np


counter_1 = 0
counter_2 = 0
counter_3 = 0

iterator = np.arange(0, 10)

for i in iterator:
    counter_1 += 1
    print('counter 1', counter_1)
    for j in iterator:
        counter_2 += 1
        print('counter_2', counter_2)
        for k in iterator:
            counter_3 += 1
            print('counter 3', counter_3)
            break
            break
            break
    
