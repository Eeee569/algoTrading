import pandas as pd
import time
import datetime

df = pd.read_csv("./vixData/VIX_intraday-1min_2009-2019.csv",names=['Time','Open','High','Low','Last','Change','Volume','Open Int'])

df = df.iloc[1:]

df.drop('Open Int', axis=1, inplace=True)
df.drop('Volume',axis=1,inplace=True)
df.drop('High',axis=1,inplace=True)
df.drop('Low',axis=1,inplace=True)
df.drop('Change',axis=1,inplace=True)
df.drop('Open',axis=1,inplace=True)
print(df.head())

df['Time'] = df.index

print(df.head())
print(df['Last'].head())

def toFloat(x):
    try:
        return float(x)
    except:
        print("could not convert "+str(x)+" to float\n")
        return 0.000

    return 0.00

df['Last'] = df['Last'].apply(toFloat)

print (df.head())
#df['Last'] = df['Last'].astype(float)

print(df.dtypes)


df.to_csv(r'./vixData/cleanVixData.csv')


df= pd.read_csv('./vixData/cleanVixData.csv')

print(df.dtypes)