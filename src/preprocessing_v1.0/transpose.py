import pandas as pd
import os
import numpy as np
import pywt

from statsmodels.tsa.seasonal import seasonal_decompose


def transpose_resample(name):
    file_name = name
    name = "original_data/" + name
    df = pd.read_csv(name)
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.index = pd.to_datetime(df.index, format="%Y-%m-%d").strftime("%m/%Y")
    new_name = "improved_data/" + file_name
    df.to_csv(new_name)


# for name in ['AE.csv', 'C.csv', 'C.csv', 'D.csv', 'L.csv', 'LA.csv', 'NI.csv', 'NII.csv', 'TA.csv', 'TI.csv']:
#     transpose_resample(name)

# for name in ['TE.csv']:
#     transpose_resample(name)


def select_banks(banks_list, file):
    file_name, file_extension = os.path.splitext(file)
    file = "improved_data/" + file
    df = pd.read_csv(file)
    df.index = pd.to_datetime(df.iloc[:, 0], format="%m/%Y")
    df = df[banks_list].set_index(df.index)
    output_file = "selected_banks/" + file_name + "_sel" + file_extension
    df.to_csv(output_file)


banks_list = [
    "cb privatbank",
    "credit agricole bank",
    "fuib",
    "kredobank",
    "oschadbank",
    "otp bank",
    "pivdennyi bank",
    "raiffeisen bank",
    "sense bank",
    "ukrsibbank",
    "universal bank",
]
# for file in ['AE.csv', 'C.csv', 'C.csv', 'D.csv', 'L.csv', 'LA.csv', 'NI.csv', 'NII.csv', 'TA.csv', 'TI.csv', 'NPL.csv', 'CL.csv']:
#     select_banks(banks_list, file)

# for name in ['TE.csv']:
#     select_banks(banks_list, name)


def divide(file1, file2, name):
    df1 = pd.read_csv("./../../data/5_remove_invalid/" + file1)
    df2 = pd.read_csv("./../../data/5_remove_invalid/" + file2)
    # df1["date"] = pd.to_datetime(df1["date"])
    # df1.set_index("date", inplace=True)
    # df2["date"] = pd.to_datetime(df2["date"])
    # df2.set_index("date", inplace=True)

    for i in range(0, len(df1)):
        for j in range(1, len(df1.columns)):
            df1.iloc[i, j] = float(df1.iloc[i, j]) / float(df2.iloc[i, j])
    df1 = df1.rename(columns={'Unnamed: 0': '', os.path.splitext(file1)[0] : os.path.splitext(name)[0]})
    output_file = "./../../data/8_variables/" + name
    df1.to_csv(output_file, index=False)


# for files in [['NPL_sel.csv', 'CL_sel.csv', 'CR.csv'], ['NII_sel.csv', 'TA_sel.csv', 'NIM.csv'], ['TI_sel.csv', 'TA_sel.csv', 'ROA.csv'],
#               ['NI_sel.csv', 'TI_sel.csv', 'NIA.csv'], ['C_sel.csv', 'TA_sel.csv', 'SCTA.csv'], ['AE_sel.csv', 'TA_sel.csv', 'OE.csv'],
#               ['LA_sel.csv', 'TA_sel.csv', 'LAS.csv'], ['L_sel.csv', 'D_sel.csv', 'CDR.csv'], ['TE_sel.csv', 'TA_sel.csv', 'RA.csv']]:
#     divide(files[0], files[1], files[2])


def divide_composite(file1, file2, name):
    df1 = pd.read_csv("./../../data/6_comp_time_series/" + file1)
    df2 = pd.read_csv("./../../data/6_comp_time_series/" + file2)
    # df1["date"] = pd.to_datetime(df1["date"])
    # df1.set_index("date", inplace=True)
    # df2["date"] = pd.to_datetime(df2["date"])
    # df2.set_index("date", inplace=True)
    old, a = os.path.splitext(file1)
    new, b = os.path.splitext(name)

    for i in range(0, len(df1)):
        for j in range(1, len(df1.columns)):
            df1.iloc[i, j] = float(df1.iloc[i, j]) / float(df2.iloc[i, j])
    df1 = df1.rename(columns={'Unnamed: 0': '', old: new})
    output_file = "./../../data/7_c_variables/" + name
    df1.to_csv(output_file, index=False)

# for files in [['NPL.csv', 'CL.csv', 'CR.csv'], ['NII.csv', 'TA.csv', 'NIM.csv'], ['TI.csv', 'TA.csv', 'ROA.csv'],
#               ['NI.csv', 'TI.csv', 'NIA.csv'], ['C.csv', 'TA.csv', 'SCTA.csv'], ['AE.csv', 'TA.csv', 'OE.csv'],
#               ['LA.csv', 'TA.csv', 'LAS.csv'], ['L.csv', 'D.csv', 'CDR.csv'], ['TE.csv', 'TA.csv', 'RA.csv']]:
#     divide_composite(files[0], files[1], files[2])
#     divide(files[0], files[1], files[2])

# divide('NII_sel.csv', 'TI_sel.csv', 'NIA.csv')
# divide_composite('NII_sel.csv', 'TI_sel.csv', 'NIA.csv')


def remove_row(index_val, file, composite_or_no):
    if composite_or_no == 1:
        file = "./../../data/positive_composite/" + file
    else:
        file = "./../../data/positive_banks/" + file
    df = pd.read_csv(file)
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    # df.drop(df.index[index], inplace=True)
    df = df[df.index != index_val]
    df.to_csv(file)


# for date in [
#     "2019-03-01",
#     "2023-09-01",
#     "2020-08-01",
#     "2023-11-01",
#     "2023-12-01",
#     "2021-06-01",
#     "2021-12-01",
#     "2022-04-01",
#     "2022-05-01",
#     "2020-08-01",
#     "2021-01-01",
# ]:
#     for file in [
#         "CDR.csv",
#         "CR.csv",
#         "INF.csv",
#         "LAS.csv",
#         "NIA.csv",
#         "NIM.csv",
#         "OE.csv",
#         "PR.csv",
#         "RA.csv",
#         "ROA.csv",
#         "SCTA.csv",
#         "SIZE.csv",
#     ]:
#         for compositness in [1]:
#             remove_row(date, file, compositness)

def remove_trend_pct(path, file, save, is_composite, banks):
    df = pd.read_csv(path + file)
    if is_composite == 1:
        df[os.path.splitext(file)[0]] = df[os.path.splitext(file)[0]].pct_change()
    else:
        for bank in banks:
            df[bank] = df[bank].pct_change()
    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv(save + 'pct/' + file, index=False)

def remove_trend_wavelet(path, file, save, is_composite, banks):
    df = pd.read_csv(path + file)
    if is_composite == 1:
        inx = os.path.splitext(file)[0]
        coeffs = pywt.wavedec(df[inx], wavelet='db4', level=2)
        coeffs[1:] = [np.zeros_like(coeff) for coeff in coeffs[1:]]
        trend = pywt.waverec(coeffs, wavelet='db4')[:len(df)]
        df[inx] = df[inx] - trend
    else:
        for bank in banks:
            inx = bank
            coeffs = pywt.wavedec(df[inx], wavelet='db4', level=2)
            coeffs[1:] = [np.zeros_like(coeff) for coeff in coeffs[1:]]
            trend = pywt.waverec(coeffs, wavelet='db4')[:len(df)]
            df[inx] = df[inx] - trend

    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv(save + 'wavelet/' + file, index=False)

def remove_trend_decomposition(path, file, save, is_composite, banks):
    df = pd.read_csv(path + file)
    df1 = pd.read_csv(path + file)
    if is_composite == 1:
        inx = os.path.splitext(file)[0]
        decomposition = seasonal_decompose(df[inx], model='additive', period=12)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        df[inx] = df[inx] - trend
        df1[inx] = residual
    else:
        for bank in banks:
            inx = bank
            decomposition = seasonal_decompose(df[inx], model='additive', period=12)
            trend = decomposition.trend
            seasonal = decomposition.seasonal
            residual = decomposition.resid
            df[inx] = df[inx] - trend
            df1[inx] = residual

    df = df.rename(columns={'Unnamed: 0': ''})
    df.to_csv(save + 'decomposition/' + 'detrended/' + file, index=False)

    df1 = df1.rename(columns={'Unnamed: 0': ''})
    df1.to_csv(save + 'decomposition/' + 'deseasoned/' + file, index=False)

all_banks = ['cb privatbank', 'credit agricole bank', 'fuib', 'kredobank', 'oschadbank', 'otp bank', 'pivdennyi bank', 'raiffeisen bank', 'sense bank', 'ukrsibbank', 'universal bank']
# for file in ["CDR.csv", "CR.csv", "INF.csv",
#              "LAS.csv", "NIA.csv", "NIM.csv",
#              "OE.csv", "PR.csv", "RA.csv",
#              "ROA.csv", "SCTA.csv", "SIZE.csv"]:
#     remove_trend_pct('./../../data/7_c_variables/', file, './../../data/9_c_detrend/wavelet/', 1, all_banks)

for file in ["CDR.csv", "CR.csv", "INF.csv",
             "LAS.csv", "NIA.csv", "NIM.csv",
             "OE.csv", "PR.csv", "RA.csv",
             "ROA.csv", "SCTA.csv", "SIZE.csv"]:
    remove_trend_pct('./../../data/7_c_variables/', file, './../../data/9_c_detrend/', 1, all_banks)
    remove_trend_wavelet('./../../data/7_c_variables/', file, './../../data/9_c_detrend/', 1, all_banks)
    remove_trend_decomposition('./../../data/7_c_variables/', file, './../../data/9_c_detrend/', 1, all_banks)
    if file == "INF.csv":
        compositeness = 1
    elif file == "PR.csv":
        compositeness = 1
    else:
        compositeness = 0
    remove_trend_pct('./../../data/8_variables/', file, './../../data/10_detrend/', compositeness, all_banks)
    remove_trend_wavelet('./../../data/8_variables/', file, './../../data/10_detrend/', compositeness, all_banks)
    remove_trend_decomposition('./../../data/8_variables/', file, './../../data/10_detrend/', compositeness, all_banks)
