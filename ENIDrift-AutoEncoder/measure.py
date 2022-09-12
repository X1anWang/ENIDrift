from numpy import *
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

def evaluate(x, y, window=10000):
    
    try:
        num = x.shape[0]
    except:
        num = len(x)
    
    # tp, fp, tn, fn, precision, recall, f1, gmean
    result = zeros((num, 8))
        
    result[window-1, 0] = sum([1 for i in range(window) if x[i] == 1 and y[i] == 1])
    result[window-1, 1] = sum([1 for i in range(window) if x[i] == 1 and y[i] == 0])
    result[window-1, 2] = sum([1 for i in range(window) if x[i] == 0 and y[i] == 0])
    result[window-1, 3] = sum([1 for i in range(window) if x[i] == 0 and y[i] == 1])
    
    if result[window-1, 0] + result[window-1, 1] == 0:
        result[window-1, 4] = 0
    else:
        result[window-1, 4] = result[window-1, 0]/(result[window-1, 0] + result[window-1, 1]) 

    if result[window-1, 0] + result[window-1, 3] == 0:
        result[window-1, 5] = 0
    else:
        result[window-1, 5] = result[window-1, 0]/(result[window-1, 0] + result[window-1, 3]) 

    if result[window-1, 4] == 0 and result[window-1, 5] == 0:
        result[window-1, 6] = 0
    else:
        result[window-1, 6] = 2 * result[window-1, 4] * result[window-1, 5]/(result[window-1, 4] + result[window-1, 5]) 

    if result[window-1, 5] == 0 or result[window-1, 2]+result[window-1, 1] == 0:
        result[window-1, 7] = 0
    else:
        result[window-1, 7] = sqrt(result[window-1, 5] * result[window-1, 2] / (result[window-1, 2]+result[window-1, 1]))
       
    for i in range(window, num):
        
        result[i, :] = result[i-1, :]
        if x[i] == 1:
            if y[i] == 1:
                result[i, 0] = result[i, 0] + 1
            else:
                result[i, 1] = result[i, 1] + 1
        else:
            if y[i] == 1:
                result[i, 3] = result[i, 3] + 1
            else:
                result[i, 2] = result[i, 2] + 1

        if x[i-window] == 1:
            if y[i-window] == 1:
                result[i, 0] = result[i, 0] - 1
            else:
                result[i, 1] = result[i, 1] - 1
        else:
            if y[i-window] == 1:
                result[i, 3] = result[i, 3] - 1
            else:
                result[i, 2] = result[i, 2] - 1
        
        if result[i, 0] + result[i, 1] == 0:
            result[i, 4] = 0
        else:
            result[i, 4] = result[i, 0]/(result[i, 0] + result[i, 1]) 
    
        if result[i, 0] + result[i, 3] == 0:
            result[i, 5] = 0
        else:
            result[i, 5] = result[i, 0]/(result[i, 0] + result[i, 3]) 
    
        if result[i, 4] == 0 and result[i, 5] == 0:
            result[i, 6] = 0
        else:
            result[i, 6] = 2 * result[i, 4] * result[i, 5]/(result[i, 4] + result[i, 5]) 
    
        if result[i, 5] == 0 or result[i, 2]+result[i, 1] == 0:
            result[i, 7] = 0
        else:
            result[i, 7] = sqrt(result[i, 5] * result[i, 2] / (result[i, 2]+result[i, 1]))
    
    """
    plt.plot(arange(num), result[:, 0], label="tp")
    plt.plot(arange(num), result[:, 1], label="fp")
    plt.plot(arange(num), result[:, 2], label="tn")
    plt.plot(arange(num), result[:, 3], label="fn")
    
    plt.legend()
    plt.savefig('result_performance_realtime1.png')
    plt.cla()
    plt.clf()
    plt.close()
    
    plt.plot(arange(num), result[:, 4], label="precision")
    plt.plot(arange(num), result[:, 5], label="recall")
    plt.plot(arange(num), result[:, 6], label="f1")
    plt.plot(arange(num), result[:, 7], label="g-mean")
    
    plt.legend()
    plt.savefig('result_performance_realtime2.png')
    plt.cla()
    plt.clf()
    plt.close()
    """
        
    
    return result

def Err1(x):
    e = sum(ones(x.shape)-x)
    return e

def Err2():    
    return 1

def overall(x, y):
    try:
        num = x.shape[0]
    except:
        num = len(x)
    
    
    temp1 = sum([1 for i in range(num) if x[i]==y[i]==1])
    print("True Positive"+str(temp1))
    temp2 = sum([1 for i in range(num) if x[i]==1 and y[i]==0])
    print("False Positive"+str(temp2))
    temp3 = sum([1 for i in range(num) if x[i]==y[i]==0])
    print("True Negative"+str(temp3))
    temp4 = sum([1 for i in range(num) if x[i]==0 and y[i]==1])
    print("False Negative"+str(temp4))
    temp5 = (temp1/(temp1+temp4)) if (temp1+temp4)!=0 else 0
    print("Recall: "+str(temp5))
    temp6 = (temp1/(temp1+temp2)) if (temp1+temp2)!=0 else 0
    print("Precision: "+str(temp6))
    temp7 = (temp1+temp3)/(temp1+temp2+temp3+temp4)
    print("Accuracy: "+str(temp7))
    temp8 = 2*temp5*temp6/(temp5+temp6) if (temp5+temp6)!=0 else 0
    print("F1: "+str(temp8))
    temp_9 = temp3/(temp3+temp2) if (temp3+temp2) != 0 else 0
    print("Specity: "+str(temp_9))
    temp9 = sqrt(temp_9*temp5)
    print("G-mean: "+str(temp9))
    
    save("result_overall_result.npy", [temp1, temp2, temp3, temp4, temp5, temp6, temp7, temp8, temp_9, temp9])