import pandas as pd
from multiprocessing import Process,Queue
import numpy as np
import queue 
import time


CSV_LOCATION = "../../vixData/cleanVixData.csv"
MULTIPLIER = 100
TIME_INTERVAL = 5
INCRAMENT = int(0.1 * MULTIPLIER) 
B_PRIME = int(0.4 * MULTIPLIER )
NUM_PROC = 24


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
	q=Queue(maxsize=1000)
	queue_list=[]
	proc_count=1

	print(max_vix)
	print(min_vix)

	for a in np.arange(min_vix , max_vix - (INCRAMENT*2) , INCRAMENT):
		for b in np.arange(a + (INCRAMENT*1), max_vix - (INCRAMENT*1), INCRAMENT):
			for c in np.arange(b + (INCRAMENT*1), max_vix , INCRAMENT):
				if proc_count%1000 == 0:
					queue_list.append(q)
					q=Queue(maxsize=1000)
				proc = Process(target=run_test, args=(a,b,c,df,q)) #df.copy() may not be nesisary
				procs.append(proc)
				proc.start()
				proc.join(timeout=0)
				if a==891 and b==941 and c == 5001:
					print("break")
				#time.sleep(1)
				while(len(procs)>=NUM_PROC):					
					time.sleep(1)
					i=0
					while(i<len(procs)):
						if(not procs[i].is_alive()):
							del procs[i]
							i -=1
						i +=1
				proc_count+=1



	max_result=[-1,-1,-1,-1]
	for q_temp in queue_list:
		while(not q_temp.empty()):
			result = q.get()
			if(result[3]>result[4] and result[3]>max_result[3]):
				max_result=result


	print("*******************Final: a: "+str(max_result[0])+" b: "+str(max_result[1])+ " c: "+str(max_result[2])+"\n"+"prof: "+str(max_result[3])+ " unprof: "+str(max_result[4])+"\n")







def run_test(a,b,c,df,q):
	prev=-1
	num_prof = 0
	num_unprof=0
	hit_a = False
	hit_b = False

	#testing
	print("started proc"+ " a: "+str(a)+ " b: "+str(b)+ " c: "+str(c))
	result=[-1,-1,-1,-1]
	q.put(result)
	return
	#

	result = []
	for index, row in df.iterrows():

		#need testing, this is also only for values going up

		#going up
		if(prev<=row['Last']):
			if( (a>prev and a<=row['Last']) or (a<prev and a<=row['Last']) ):
				hit_a=True
				hit_b=False
			if((b>prev and b<=row['Last']) or (b<prev and b>=row['Last']) ):
				if(hit_a):
					hit_b=True
			if(((b-B_PRIME)>prev and(b-B_PRIME)<=row['Last']) or ((b-B_PRIME)<prev and(b-B_PRIME)>=row['Last'])):
				if(hit_b):
					hit_a=False
					hit_b=False
					num_unprof+=1
			if((c>prev and c<=row['Last'])or(c<prev and c>=row['Last'])):
				if(hit_a and hit_b):
					num_prof+=1
				hit_a=False
				hit_b=False

		#going down
		# if(prev>row['Last']):
		# 	if(c<prev and c>=row['Last']):
		# 		if (window[-1] != 4):
		# 			window.append(4)
		# 	if(b<prev and b>=row['Last']):
		# 		if (window[-1] != 3):
		# 			window.append(3)
		# 	if((b-B_PRIME)<prev and(b-B_PRIME)>=row['Last']):
		# 		if (window[-1] != 2):
		# 			window.append(2)
		# 	if(a<prev and a<=row['Last']):
		# 		if(window[-1]!=1):
		# 			window.append(1)

		prev=row['Last']
	result.append(a)
	result.append(b)
	result.append(c)
	result.append(num_prof)
	result.append(num_unprof)
	print("a: "+str(a)+" b: "+str(b)+ " c: "+str(c)+"\n"+"prof: "+str(num_prof*((c-b)/MULTIPLIER))+ " unprof: "+str(num_unprof*B_PRIME/MULTIPLIER)+"\n")
	q.put(result)










if __name__ == '__main__':
	main()


