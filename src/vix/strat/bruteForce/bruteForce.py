import pandas as pd
from multiprocessing import Pool
import numpy as np

CSV_LOCATION = "../../vixData/cleanVixData.csv"
MULTIPLIER = 100
TIME_INTERVAL = 5
INCRAMENT = 0.1 * MULTIPLIER 
B_PRIME = 0.4 * MULTIPLIER 


def main():

	##DATA CLEANING
	df = pd.read_csv(CSV_LOCATION)
	#set the interval to 5 minutes 
	df = df.iloc[::TIME_INTERVAL, :]
	#remove the extra unnamed column
	df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	df['Last'] = df['Last'].apply(lambda x: x*MULTIPLIER)
	df['Last']= df['Last'].astype(str).astype(int)
	print(df.head())
	max_vix = df['Last'].max()
	min_vix = df['Last'].min()

	for a in np.arange(min_vix - (INCRAMENT*2), max_vix , INCRAMENT):
		for b in np.arange(min_vix - (INCRAMENT*1), max_vix - (INCRAMENT*1), INCRAMENT):
			for c in np.arange(min_vix, max_vix - (INCRAMENT*2) , INCRAMENT):
				print("a: "+str(a)+" b: "+str(b)+" c: " +str(c))

#def run_test(a,b,c,df)
	
	



if __name__ == '__main__':
	main()


