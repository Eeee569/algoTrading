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



				#print("a: "+str(a)+" b: "+str(b)+" c: " +str(c))

#	for p in procs:
#		p.join()


def run_test(a,b,c,df):
	
	print("a: "+str(a)+" b: "+str(b)+" c: " +str(c))




class Stop_Queue:
	def __init__(self):
		self.q=queue.Queue(maxsize=16) 
		self.size = 0
	def put(self,proc):
		if(not q.full()):
			q.put(proc)
			self.size +=1
			return True
		else:
			return False
	def pop(self):
		if(self.size<=0):
			return False; 


if __name__ == '__main__':
	main()


