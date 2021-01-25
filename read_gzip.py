# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:18:35 2021

@author: bruceyu1113
"""

import pandas as pd
def tmp_read(filename):
    path = "C:\\Users\\Public\\version_control\\tmp\\"
    tmp = pd.read_parquet(path + filename + ".gzip", engine='fastparquet')
    return tmp