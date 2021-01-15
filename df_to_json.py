# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 18:17:29 2021

@author: bruceyu1113
"""
import numpy as np

def dataframe_to_json(dataframe):
    temp_list = []
    nrows = dataframe.shape[0]
    for i in range(nrows):
        ser = dataframe.loc[i, :]
        row_dict = {}
        for idx, val in zip(ser.index, ser.values):
            if type(val) is str:
                row_dict[idx] = val
            elif type(val) is np.int64:
                row_dict[idx] = int(val)
            elif type(val) is np.float64:
                row_dict[idx] = float(val)
        temp_list.append(row_dict)
    return(temp_list)