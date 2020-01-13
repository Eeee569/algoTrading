import pandas as pd
from multiprocessing import Process
import numpy as np
import queue 
import time


CSV_LOCATION = "../../vixData/cleanVixData.csv"
MULTIPLIER = 100
TIME_INTERVAL = 5
INCRAMENT = int(0.1 * MULTIPLIER) 
B_PRIME = int(0.4 * MULTIPLIER )
NUM_PROC = 16


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
	#q=queue.Queue(maxsize=16)

	for a in np.arange(min_vix , max_vix - (INCRAMENT*2) , INCRAMENT):
		for b in np.arange(a + (INCRAMENT*1), max_vix - (INCRAMENT*1), INCRAMENT):
			for c in np.arange(b + (INCRAMENT*1), max_vix , INCRAMENT):

				proc = Process(target=run_test, args=(a,b,c,df.copy())) #df.copy() may not be nesisary
				procs.append(proc)
				proc.start()
				proc.join(timeout=0)

				while(len(procs)>=NUM_PROC):					
					time.sleep(1)
					i=0
					while(i<len(procs)):
						if(not procs[i].is_alive()):
							del procs[i]
							i -=1
						i +=1






#maybe dont use string
def build_string(a,b,c,df):

	prev=-1
	string_list=[]
	for index, row in df.iterrows():

		#need testing, this is also only for values going up

		if(a>prev and a<=row['Last']):
			string_list.append('a')
		elif((b-B_PRIME)>prev and(b-B_PRIME)<=row['Last']):
			string_list.append('b`')
		elif(b>prev and b<=row['Last']):
			string_list.append('b')
		elif(c>prev and c<=row['Last']):
			string_list.append('c')
		
		prev=row['Last']

	return string_list


def run_test(a,b,c,df):
	
	string_list=build_string(a,b,c,df)

	for i in string_list:
		print(i)








if __name__ == '__main__':
	main()


