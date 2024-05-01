import pandas as pd
from datetime import datetime
import os


def flatten_variables(data_folder, save_path):
    """
    Creates flatten version af all variables existent in data_folder
    Creates dummies for all banks listed in bank_names
    Args:
        data_folder (str): path to folder with .csv variables
        save_path (_type_): path to desired saving location
    """
    bank_names = {
        "cb privatbank": "Privat_Bank",
        "credit agricole bank": "Credit_Agricole",
        "fuib": "FUIB",
        "kredobank": "Kredobank",
        "oschadbank": "Oschadbank",
        "otp bank": "OTP",
        "pivdennyi bank": "Pivdennyi",
        "raiffeisen bank": "Raiffeisen",
        "sense bank": "Sense",
        "ukrsibbank": "Ukrsibbank",
        "universal bank": "Universal",
    }

    inf_df = pd.read_csv(data_folder + "/INF.csv", index_col=0)
    inf_df.index = pd.to_datetime(inf_df.index, format="%m/%Y")
    pol_r_df = pd.read_csv(data_folder + "/PR.csv", index_col=0)
    pol_r_df.index = pd.to_datetime(pol_r_df.index, format="%m/%Y")

    stacked = {"Bank": [], "Date": [], "INF": [], "PR": []}
    a = True
    for i in [j for j in os.listdir(data_folder) if j not in ["INF.csv", "PR.csv"]]:
        var = i[:-4]
        stacked[var] = []
        df = pd.read_csv(f"{data_folder}/{i}", index_col=0)
        for date in df.index:
            for bank in df.columns:
                if a:
                    stacked["Bank"].append(bank)
                    stacked["Date"].append(date)
                    stacked["INF"].append(inf_df[inf_df.index == date]["INF"].iloc[0])
                    stacked["PR"].append(pol_r_df[pol_r_df.index == date]["PR"].iloc[0])
                stacked[var].append(df.loc[date][bank])
        a = False

    # print(stacked)
    # for i in stacked.keys():
    #     print(i, len(stacked[i]))

    resulting_df = pd.DataFrame(stacked).replace(bank_names)
    dummies = pd.get_dummies(resulting_df.Bank, dtype=int)
    dummies.columns = [f"is_{i}" for i in dummies]
    for i in dummies:
        resulting_df[i] = dummies[i]

    resulting_df.to_csv(save_path)


def add_dummy_for_year(file_path, dummy_year, dummy_name):
    dummy_year = datetime.strptime(dummy_year, "%Y")
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%Y")
    df[dummy_year] = 1 if dummy_year < df["Date"] else 0
    return df


if __name__ == "__main__":
    data_folder = "./../../data/10_detrend/"
    save_folder = "./../../data/11_flattenned/"
    for methods in ["decomposition", "pct", "wavelet"]:
        if methods == "decomposition":
            flatten_variables(
                data_folder + methods + "/detrended",
                save_folder
                + "flatten_variables_"
                + methods
                + "_"
                + "detrended"
                + ".csv",
            )
            flatten_variables(
                data_folder + methods + "/deseasoned",
                save_folder
                + "flatten_variables_"
                + methods
                + "_"
                + "detrended_and_deseasoned"
                + ".csv",
            )
        else:
            flatten_variables(
                data_folder + methods,
                save_folder + "flatten_variables_" + methods + ".csv",
            )
