import pandas as pd

def transpose_resample(name):
    file_name = name
    name = 'data/' + name
    df = pd.read_csv(name)
    df = df.transpose()
    df.columns = df.iloc[0]
    df = df[1:]
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d').strftime('%m/%Y')
    new_name = 'improved_data/' + file_name
    df.to_csv(new_name)


for name in ['AE.csv', 'C.csv', 'C.csv', 'D.csv', 'L.csv', 'LA.csv', 'NI.csv', 'NII.csv', 'TA.csv', 'TI.csv']:
    transpose_resample(name)
