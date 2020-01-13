import pandas as pd
from multiprocessing import Pool
import numpy as np

CSV_LOCATION = "../../vixData/cleanVixData.csv"
MULTIPLIER = 100
TIME_INTERVAL = 5
INCRAMENT = int(0.1 * MULTIPLIER) 
B_PRIME = int(0.4 * MULTIPLIER )


def main():

	##DATA CLEANING
	df = pd.read_csv(CSV_LOCATION)
	#set the interval to 5 minutes 
	df = df.iloc[::TIME_INTERVAL, :]
	#remove the extra unnamed column
	df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
	df['Last'] = df['Last'].apply(lambda x: x*MULTIPLIER)
	#set df to int
	df['Last']= df['Last'].astype(np.int64)
	print(df.head())
	max_vix = df['Last'].max()
	min_vix = df['Last'].min()

	procs=[]
	pool = Pool(processes=4)

	for a in np.arange(min_vix , max_vix - (INCRAMENT*2) , INCRAMENT):
		for b in np.arange(a + (INCRAMENT*1), max_vix - (INCRAMENT*1), INCRAMENT):
			for c in np.arange(b + (INCRAMENT*1), max_vix , INCRAMENT):
				pool.apply_async(run_test, args=(a,b,c,df.copy(),)) #df.copy() may not be nesisary

				#print("a: "+str(a)+" b: "+str(b)+" c: " +str(c))

	pool.close()
	pool.join()


def run_test(a,b,c,df):
	
	print("a: "+str(a)+" b: "+str(b)+" c: " +str(c))




if __name__ == '__main__':
	main()


