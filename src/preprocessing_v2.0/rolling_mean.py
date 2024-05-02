import pandas as pd
import os
import numpy as np


def create_moving_average(path, name, save_path, window, compositeness):
    df = pd.read_csv(path + name)
    if name == "INF.csv":
        col = df.columns[1]
        df[col] = df[col].rolling(window).mean()
    elif name == "PR.csv":
        col = df.columns[1]
        df[col] = df[col].rolling(window).mean()
    elif compositeness == 1:
        col = df.columns[1]
        df[col] = df[col].rolling(window).mean()
    else:
        for col in ['cb privatbank', 'credit agricole bank', 'fuib', 'kredobank', 'oschadbank', 'otp bank',
                    'pivdennyi bank', 'raiffeisen bank', 'sense bank', 'ukrsibbank', 'universal bank']:
            df[col] = df[col].rolling(window).mean()
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv(save_path + name, index=False)


for file in ["CDR.csv", "CR.csv", "INF.csv", "LAS.csv", "NIA.csv", "NIM.csv", "OE.csv", "PR.csv", "RA.csv", "ROA.csv",
             "SCTA.csv", "SIZE.csv"]:
    create_moving_average('./../../data/10_detrend/pct/', file, './../../data/13_mov_aver/pct/', 3, 0)
    create_moving_average('./../../data/9_c_detrend/pct/', file, './../../data/12_c_mov_aver/pct/', 3, 1)
