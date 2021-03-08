# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 16:18:35 2021

@author: bruceyu1113
"""

import pandas as pd
def tmp_read(filename,domain):
    domain = domain.capitalize()
    path = "C:\\Users\\Public\\version_control\\tmp\\"
    tmp = pd.read_parquet(f"{path}{filename}_{domain}.gzip", engine='fastparquet')
    return tmp