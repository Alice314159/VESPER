import sys
import os

path = os.path.abspath('..')
sys.path.extend([path])
print(sys.path)


# from AnalyStock.CapacityAM import CalCapacityStock
from AnalyStock.DownLowest import CalRecentDownLowestStock

if __name__ == '__main__':
    CalRecentDownLowestStock()