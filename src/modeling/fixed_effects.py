import pandas as pd
import os
import statsmodels.api as sm
import statsmodels.formula.api as smf
from datetime import datetime


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def add_dummy_for_date(file_path, dummy_dates, dummy_names):
    dummy_dates = [datetime.strptime(i, "%m/%Y") for i in dummy_dates]
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    for i, name in enumerate(dummy_names):
        df[name] = (df["Date"] > dummy_dates[i]).astype(int)
    return df


def run_fixed_effects_on_flattened(
    file_path: str,
    X_var_names=["PR", "CDR", "LAS", "CR", "NIA", "OE", "RA", "ROA", "SCTA", "SIZE"],
    dummy_dates=[],
    dummy_names=[],
):

    resulting_df = add_dummy_for_date(file_path, dummy_dates, dummy_names)

    regression_string = "NIM ~ "
    for i in X_var_names:
        regression_string = regression_string + i + "+ "
    for i in dummy_names:
        regression_string = regression_string + i + "+ "

    dummies_str = "is_Credit_Agricole + is_FUIB + is_Kredobank + is_OTP + is_Oschadbank + is_Pivdennyi + \
            is_Privat_Bank + is_Raiffeisen + is_Sense + is_Ukrsibbank + is_Universal"
    regression_string = regression_string + dummies_str

    mod3 = smf.ols(formula=regression_string, data=resulting_df)
    res3 = mod3.fit()
    print(
        bcolors.OKBLUE
        + "==============================================================================="
        + bcolors.ENDC
    )
    print(
        bcolors.OKBLUE
        + "=============================== Fixed Effects ================================="
        + bcolors.ENDC
    )
    print(res3.summary())

    return res3
