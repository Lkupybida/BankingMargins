import pandas as pd
import os

def transpose_resample(name):
    file_name = name
    name = 'original_data/' + name
    df = pd.read_csv(name)
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%m/%Y')
    new_name = 'improved_data/' + file_name
    df.to_csv(new_name)

# for name in ['AE.csv', 'C.csv', 'C.csv', 'D.csv', 'L.csv', 'LA.csv', 'NI.csv', 'NII.csv', 'TA.csv', 'TI.csv']:
#     transpose_resample(name)

for name in ['TE.csv']:
    transpose_resample(name)

def select_banks(banks_list, file):
    file_name, file_extension = os.path.splitext(file)
    file = 'improved_data/' + file
    df = pd.read_csv(file)
    df.index = pd.to_datetime(df.iloc[:, 0], format='%m/%Y')
    df = df[banks_list].set_index(df.index)
    output_file = 'selected_banks/' + file_name + '_sel' + file_extension
    df.to_csv(output_file)

banks_list = ['cb privatbank', 'credit agricole bank', 'fuib', 'kredobank', 'oschadbank', 'otp bank', 'pivdennyi bank', 'raiffeisen bank', 'sense bank', 'ukrsibbank', 'universal bank']
# for file in ['AE.csv', 'C.csv', 'C.csv', 'D.csv', 'L.csv', 'LA.csv', 'NI.csv', 'NII.csv', 'TA.csv', 'TI.csv', 'NPL.csv', 'CL.csv']:
#     select_banks(banks_list, file)

for name in ['TE.csv']:
    select_banks(banks_list, name)

def divide(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    for i in range(1, len(df1)):
        for j in range(1, len(df1.columns)):
            df1.iloc[i, j] /= df2.iloc[i, j]

    return df1

#
# output_file = 'only_sophomores/CR.csv'
# divide('selected_banks/NPL_sel.csv', 'selected_banks/CL_sel.csv').to_csv(output_file)