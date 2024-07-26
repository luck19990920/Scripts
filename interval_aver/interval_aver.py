import numpy as np
import math
from typing import Union

class interval_aver:
    """
    ### 用于进行区间平均的类
    #### 输入：
    * data: 需要进行的数据 (np.ndarray)
    * ref: 以第一行还是第一列的数据作为需要进行划分区间的数据来源,默认为"col",即以第一列的数据进行区间划分 ("col" | "row")
    * bin: 划分的小区间的个数,默认值为10 (int)
    * data_min: 需要进行区间平均的数据的最小值,默认值为data第一行或第一列的最小值 (float)
    * data_max: 需要进行区间平均的数据的最大值,默认值为data第一行或第一列的最大值 (float)

    注意: ref/bin/data_min/data_max都为关键词参数

    #### 输出：
    若i为类interval_aver的一个实例,则
    * i.num返回在每一个小区间中数据出现的次数 (np.ndarray)
    * i.avg返回在每一个小区间中数据的平均值 (np.ndarray)
    * i.max返回在每一个小区间中数据的最大值 (np.ndarray)
    * i.min返回在每一个小区间中数据的最小值 (np.ndarray)

    """
    def __init__(self, 
                 data: np.ndarray,
                 *,
                 ref: str = "col",
                 bin: int = 10,
                 data_min: float | None = None,
                 data_max: float | None = None,
                 ) -> None:
        self.__data = data

        if ref != "col" and ref != "row":
            raise ValueError("ref must be 'col' or 'row'")
        self.__ref = ref

        try:
            bin = int(bin)
        except:
            raise ValueError(f"{bin} could not convert to int")
        self.__bin = bin
        
        if data_min is None or not isinstance(data_min, Union[float, int]):
            data_min = np.min(data[:,0]) if ref == "col" else np.min(data[0,:])
        self.__data_min = float(data_min) # type: ignore

        if data_max is None or not isinstance(data_max, Union[float, int]):
            data_max = np.max(data[:,0]) if ref == "col" else np.max(data[0,:])
        self.__data_max = float(data_max) # type: ignore

        if self.__data_min >= self.__data_max:
            raise ValueError("data_max must be larger than data_min")
        
        self.__number_in_interval = None
        self.__sum_in_interval = None
        self.__max_in_interval = None
        self.__min_in_interval = None
        self.__averge_in_interval = None

        self.__interval = (self.__data_max - self.__data_min) /(self.__bin - 1) # type: ignore


    @property
    def num(self) -> np.ndarray:
        # 计算每一行数据或每一列数据在每一个小区间中的次数
        if self.__number_in_interval is None:
            self.calculate()
        return self.__number_in_interval # type: ignore
    
    @property
    def avg(self) -> np.ndarray:
        # 计算每一行数据或每一列数据在每一个小区间中的平均值
        if self.__averge_in_interval is None:  
            self.calculate()
        return self.__averge_in_interval # type: ignore
        
    
    @property
    def max(self) -> np.ndarray:
        # 计算每一行数据或每一列数据在每一个小区间中的最大值
        if self.__max_in_interval is None:
            self.calculate()
        return self.__max_in_interval # type: ignore
    
    @property
    def min(self) -> np.ndarray:
        # 计算每一行数据或每一列数据在每一个小区间中的最小值
        if self.__min_in_interval is None:
            self.calculate()
        return self.__min_in_interval # type: ignore
    
    @property
    def sum(self) -> np.ndarray:
        # 计算每一行数据或每一列数据在每一个小区间中的和
        if self.__sum_in_interval is None:
            self.calculate()
        return self.__sum_in_interval # type: ignore

    def calculate(self) -> None:
        # 进行相关计算的类
        """
        cal_data为存储着每个小区间的数据的np.ndarray数组
        * cal_data[:,:,0]为self.__number_in_interval
        * cal_data[:,:,1]为self.__sum_in_interval
        * cal_data[:,:,2]为self.__max_in_interval
        * cal_data[:,:,3]为self.__min_in_interval
        """
        d = {}
        if self.__ref == "col":
            cal_data = np.zeros((self.__bin , np.shape(self.__data)[1], 5))
            for m in range(5):
                cal_data[:, 0, int(m)] = np.arange(self.__data_min, self.__data_max + self.__interval, self.__interval) # type: ignore
            for i in range(1, np.shape(self.__data)[1]):    #  i为列索引
                for j in range(np.shape(self.__data)[0]):   #  j为行索引
                    if self.__data[j,0] >= self.__data_min and self.__data[j,0] <= self.__data_max:
                            if not (math.floor((self.__data[j,0]-self.__data_min)/self.__interval),i) in list(d.keys()):
                                d[(math.floor((self.__data[j,0]-self.__data_min)/self.__interval),i)] = np.array([])
                            d[(math.floor((self.__data[j,0]-self.__data_min)/self.__interval),i)] = np.append(d[(math.floor((self.__data[j,0]-self.__data_min)/self.__interval),i)], self.__data[j, i])


            for i in range(1, np.shape(self.__data)[1]):    #  i为列索引
                for j in range(self.__bin):   #  j为行索引
                    if not (j, i) in list(d.keys()):
                        cal_data[int(j), int(i), 0] = 0
                        cal_data[int(j), int(i), 1] = 0
                        cal_data[int(j), int(i), 2] = np.nan
                        cal_data[int(j), int(i), 3] = np.nan
                        cal_data[int(j), int(i), 4] = np.nan
                    else:
                        cal_data[int(j), int(i), 0] = np.size(d[(j,i)])
                        cal_data[int(j), int(i), 1] = np.sum(d[(j,i)])
                        cal_data[int(j), int(i), 2] = np.max(d[(j,i)])
                        cal_data[int(j), int(i), 3] = np.min(d[(j,i)])
                        cal_data[int(j), int(i), 4] = np.average(d[(j,i)])

        else:
            cal_data = np.zeros((np.shape(self.__data)[0], self.__bin, 5))
            for m in range(5):
                cal_data[0, :, int(m)] = np.arange(self.__data_min, self.__data_max + self.__interval, self.__interval) # type: ignore
            for i in range(1, np.shape(self.__data)[0]):    # i为行索引
                for j in range(np.shape(self.__data)[1]):   # j为列索引
                    if self.__data[0,j] >= self.__data_min and self.__data[0,j] <= self.__data_max:
                        if not (i, math.floor((self.__data[0,j]-self.__data_min)/self.__interval)) in list(d.keys()): 
                            d[(i, math.floor((self.__data[0,j]-self.__data_min)/self.__interval))] = np.array([])
                        d[(i, math.floor((self.__data[0,j]-self.__data_min)/self.__interval))] = np.append(d[(i, math.floor((self.__data[0,j]-self.__data_min)/self.__interval))], self.__data[i,j])

            for i in range(1, np.shape(self.__data)[0]):    # i为行索引
                for j in range(self.__bin):   # j为列索引
                    if not (i, j) in list(d.keys()):
                        cal_data[int(i), int(j), 0] = 0
                        cal_data[int(i), int(j), 1] = 0
                        cal_data[int(i), int(j), 2] = np.nan
                        cal_data[int(i), int(j), 3] = np.nan
                        cal_data[int(i), int(j), 4] = np.nan

                    else:
                        cal_data[int(i), int(j), 0] = np.size(d[(i,j)])
                        cal_data[int(i), int(j), 1] = np.sum(d[(i,j)])
                        cal_data[int(i), int(j), 2] = np.max(d[(i,j)])
                        cal_data[int(i), int(j), 3] = np.min(d[(i,j)])
                        cal_data[int(i), int(j), 4] = np.average(d[(i,j)])
        
        self.__number_in_interval = cal_data[:, :, 0]
        self.__sum_in_interval = cal_data[:, :, 1]
        self.__max_in_interval = cal_data[:, :, 2]
        self.__min_in_interval = cal_data[:, :, 3]
        self.__averge_in_interval = cal_data[:, :, 4]

    def __repr__(self):
        return f"class {self.__class__.__name__}"
