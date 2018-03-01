# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def PrintRunGrapth(currentRun, excpectedRun):
    # Data
    df=pd.DataFrame({'x': range(1,11), 'currentRun': currentRun, 'excpectedRun': excpectedRun })
     
    # multiple line plot
    plt.plot( 'x', 'currentRun', data=df, marker='', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)
    plt.plot( 'x', 'excpectedRun', data=df, marker='', color='red', linewidth=2)
#     plt.plot( 'x', 'y3', data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
    plt.legend()
    
    print "finish"
#     current = np.random.randn(10)+range(11,21)

#test:
if __name__ == '__main__':
    x = np.random.randn(10)
    x = [1,2,3,4,5,6,7,8,9,0]    
    y = np.random.randn(10)

PrintRunGrapth(x, y)