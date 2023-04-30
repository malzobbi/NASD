import csv
import subprocess
import itertools
import os
from random import randint
import pandas as pd
import random
import numpy as np
import time
from decimal import Decimal
from scipy.stats import skew 
from collections import Counter
from scipy.stats import pearsonr
t0= time.time()

ind1=[];ind2=[];ind3=[];ind4=[];ind5=[];ind6=[];ind7=[];the_ind=[]
indS1=[];indS2=[];indS3=[];indS4=[];indS5=[];indS6=[];indS7=[]
depS1=[];depS2=[];depS3=[];depS4=[];depS5=[];depS6=[];depS7=[]
dep=[];error_rate=0;id=0
dependent_variable=0;number_of_independent=0;error_percentage=0;average=0.0;minimum=0;maximum=0;skewness=0.0;stdev=0.0;num=0;averageS=0.0
def ind_number():
    number_of_independent=int(input("How many indpendent variables do you have in your data? [maximum 6] "))
    #set the number of independent variables 6
    if number_of_independent>6:
        number_of_independent=6
        print("the number of variable has been setup to 6")
    dep_number(number_of_independent)
    return number_of_independent
def dep_number(number_of_independent):
    #The dep. variabile should be followed by the independent variable
    dep_variable="The dependent variable will be number ",number_of_independent+1,", if this is not correct, please choose the number of the dependent variable, otherwise press enter"
    dep_variable=input(dep_variable)
    if dep_variable=="":
        dependent_variable=number_of_independent+1
    else:
        dependent_variable=int(dep_variable)
    openCSV(number_of_independent,dependent_variable)
    
#read from the csv file
def openCSV(number_of_independent,dependent_variable):
    with open("E:/Australian Institute/Capstone Master/our theory/original_data2.csv", encoding="utf8") as f:
            
            csv_reader = csv.reader(f)
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:
                    print(line)  # header
                
                else:
                    dep.append(int(line[dependent_variable-1]))
                    ind1.append(int(line[0]))
                    if number_of_independent==2:
                        ind2.append(int(line[1]))
                    if number_of_independent==3:
                        ind2.append(int(line[1]))
                        ind3.append(int(line[2]))
                    if number_of_independent==4:
                        ind2.append(int(line[1]))
                        ind3.append(int(line[2]))
                        ind4.append(int(line[3]))
                    if number_of_independent==5:
                        ind2.append(int(line[1]))
                        ind3.append(float(line[2]))
                        ind4.append(int(line[3]))
                        ind5.append(int(line[4]))
                    if number_of_independent==6:
                        ind2.append(int(line[1]))
                        ind3.append(int(line[2]))
                        ind4.append(int(line[3]))
                        ind5.append(int(line[4]))
                        ind6.append(int(line[5]))
                    
            

def one_dim(the_ind,id):
    
    #find statistics
    minimum=min(the_ind)
    maximum=max(the_ind)
    average=sum(the_ind)/len(the_ind)
    stdev=np.std(the_ind)
    
    skewness=skew(the_ind)
    
    gen_range(the_ind,minimum,maximum,average,stdev,skewness,id)

def gen_range(the_ind,minimum,maximum,average,stdev,skewness,id):
    i=0
   
    while i<len(the_ind):
        randoms=random.randint(minimum,maximum)
        indS1.append(randoms)
        i+=1
    
    calculate_statistics(the_ind,minimum,maximum,average,stdev,skewness,id)
    
    
def calculate_statistics(the_ind,minimum,maximum,average,stdev,skewness,id):
    #get the error rate
    ranges=maximum-minimum
    error_rate1=settings(1,ranges)
    error_rate2=settings(2,ranges)
    
    #calculate statistics for synthetic data
    averageS=sum(indS1)/len(indS1)
    
    
    stdevS=np.std(indS1)
    skewnessS=skew(indS1)
    
    
    if average-error_rate1 <=averageS <=average+error_rate1 and stdev-error_rate1 <=stdevS <=stdev+error_rate1 and skewness-(error_rate2) <=skewnessS <=skewness+(error_rate2):
        
        
         #find the interval
        the_interval=intervals(minimum,maximum,average,stdev,skewness)
        #find two dimension 
        two_dim(the_ind,minimum,maximum,average,stdev,skewness,the_interval,error_rate,id)
    else:
        
        indS1.clear()

        gen_range(the_ind,minimum,maximum,average,stdev,skewness,id) 
    
   

def settings(error,ranges):
    if error==1 and ranges<20:
        one_dim_error=0.07
        error_percentage=one_dim_error
    elif error==1 and ranges>=20 and ranges<50:
        one_dim_error=2
        error_percentage=one_dim_error
    elif error==1 and ranges>=50 and ranges<100:
        one_dim_error=3
        error_percentage=one_dim_error
    elif error==1 and ranges>=100 and ranges<150:
        one_dim_error=6
        error_percentage=one_dim_error
    elif error==1 and ranges>=150:
        one_dim_error=10
        error_percentage=one_dim_error
    elif error==2:
        two_dim_error=0.08
        error_percentage=two_dim_error
    return error_percentage

def intervals(minimum,maximum,average,stdev,skewness):
    num_values = len(Counter(indS1).keys())
    intvl=(maximum-minimum)
    the_interval=0
    if intvl<=1:
        the_interval=0.2
    elif intvl<=2 and intvl >1:
        the_interval=2
    elif intvl>=3 and intvl<=100:
        the_interval=3
    else:
        the_interval=5
    return the_interval

def two_dim(the_ind,minimum,maximum,average,stdev,skewness,the_interval,error_rate,id):
    #ascending order for the synthetic list
    #organize on acending
    indS1.sort()
    
    #ascending order for the real list
    #organize on acending
    
    for asc2 in range(0,len(the_ind)):
        for ord2 in range(asc2+1,len(the_ind)):
            if(the_ind[asc2]>the_ind[ord2]):
                temp=the_ind[asc2]
                temp2=dep[asc2]
                the_ind[asc2]=the_ind[ord2]
                dep[asc2]=dep[ord2]
                the_ind[ord2]=temp
                dep[ord2]=temp2

    
    count=0;countS=0;filterV=0;filterList=[];filterListS=[];u=0;depTempS1=[];x=0;r=0;indx=0;filterListOnes=[]
    
    
    if the_ind[0]<the_interval:
        rng=the_interval
    else:
        rng=the_interval+minimum-1
    
    
    #create intervals for real data
    #FilterList: stores the number rows and total of 1's in each interval [real data]
    for k in the_ind:
        if k <=rng:
            indx+=1                #calculate number of rows
            count+=int(dep[u])      #calculate number of ones

            u+=1
        else:
            indx+=1
            filterListOnes.append(count)
            filterList.append(indx)
            count=0
            indx=0
            #update the rng                      
            rng=rng+the_interval
    #add the final value
    filterListOnes.append(count) 
    filterList.append(indx) 
    
    if indS1[0]<the_interval:
        rng=the_interval
    else:
        rng=the_interval+minimum-1
    #create intervals for synthetic data
    k=0;u=0
    
    #FilterListS: stores the number rows in each interval [synthetic data]
    for k in indS1:
        if k <=rng:
            u+=1
        else:
            u+=1
            filterListS.append(u)
            u=0
            #update the rng                      
            rng=rng+the_interval
    #add the final value
    filterListS.append(u)  
      
    # generate synthetic dependent variables according to the real dependent data
    #create the synthetic list
    
    
    g=0;x=0;n=0
    
    
    
    while x <len(filterListS) and id==1:
        
        r=int(filterListS[x]*(filterListOnes[x]/filterList[x])) #calculate the percentage of ones 
        if r==0:
            r= 1 
           
        g=0
        
        
        if r-(r*0.1) <=filterV <=r+(r*0.1): #the condition to stop the range
            
            
            for i in depTempS1:
                depS1.append(i)
                
            x+=1
            
            filterV=0
            depTempS1.clear() 
        
        else:
            depTempS1.clear() 
            #generate
            g=0
            while g<filterListS[x]:
                    randoms=random.randint(0,1)
                    
                    if randoms!=0 and randoms!=1:
                        randoms=1
                    depTempS1.append(randoms) #this is the first dependent synthetic variable
                    
                    g+=1
            filterV= sum(depTempS1) 
             
        
    depTempS1.clear() 
    
              

    #the correlation coeffient 
    #1. synthetic data 
    correlationS,p_valueS = pearsonr(indS1, depS1)

     #2. real data 
    correlation,p_value = pearsonr(the_ind, dep)
    
      
    #if synthetic data is does not match the real data correlation coeeficinet then shuffle the independent list indS1
    #if correlation of original data is minus
    if correlation<0:
        while not round(correlationS,2)==round(correlation,2):
            #shuffle the list
            random.shuffle(indS1)
            correlationS,p_valueS = pearsonr(indS1, depS1)
            #correlationS=abs(correlationS)
            #correlation=abs(correlation)
            '''
            print("(=====================================================)")
            print("MINUS ",correlationS)
            print("the original minus data correlations is: ",correlation)
            print("(=====================================================)")
            '''
    else:
         #if correlation of original data is plus
        while not correlation-0.001 <=correlationS <=correlation+0.001:
            #shuffle the list
            random.shuffle(indS1)
            correlationS,p_valueS = pearsonr(indS1, depS1)
            #correlationS=abs(correlationS)
            #correlation=abs(correlation)
            '''
            print("PLUS ",correlationS)
            print("the original data correlations is: ",correlation)
            '''
    z=0 
          
    #if correlation-0.001 <=correlationS <=correlation+0.001:
        
        
        
    #store in a notepad File
    if id==1:
        '''
        print("******************************************************DATA ONE *********************************************")
        print("The Correlation Coefficientrrr for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData1.csv"
        file = open(theFile,"w") 
        file.write("A\n")
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1
            
    if id==2:
        '''
        print("******************************************************DATA TWO *********************************************")
        print("The Correlation Coefficient for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData2.csv"
        file = open(theFile,"w")
        file.write("B\n") 
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1
    if id==3:
        '''
        print("******************************************************DATA THREE *********************************************")
        print("The Correlation Coefficient for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData3.csv" 
        file = open(theFile,"w") 
        file.write("C\n")
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1 
    if id==4:
        '''
        print("******************************************************DATA FOUR *********************************************")
        print("The Correlation Coefficient for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData4.csv" 
        file = open(theFile,"w")
        file.write("D\n") 
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1 
    if id==5:
        '''
        print("******************************************************DATA FIVE *********************************************")
        print("The Correlation Coefficient for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData5.csv" 
        file = open(theFile,"w") 
        file.write("E\n")
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1 
    if id==6:
        '''
        print("******************************************************DATA SIX *********************************************")
        print("The Correlation Coefficient for synthetic data is: ",correlationS," and for real data is: ",correlation)
        print("(==========================================================================================================)")
        '''
        theFile="E:/Australian Institute/Capstone Master/our theory/data/generatedData6.csv"
        file = open(theFile,"w") 
        file.write("F")
        for a in indS1:
            message =str(a)+","+str(depS1[z])+"\n"
            file.write(message)
            
            z+=1
    
    
    
    
    
    file.close()
    indS1.clear()
        
#collect all csv files
def collectAll():
    numbers1=[];numbers2=[];numbers3=[];numbers4=[];numbers5=[];numbers6=[];hd=[];allFiles=[];j=0;s=0
    path = "E:/Australian Institute/Capstone Master/our theory/data"
    for x in os.listdir(path):
        if x.endswith(".csv"):
            allFiles.append(x)
        

    for k in allFiles:
        with open(path+"/"+k, encoding="unicode_escape") as f:
            j+=1
            csv_reader = csv.reader(f)
            for line_no, line in enumerate(csv_reader, 1):
                if line_no == 1:
                    hd.append(line[0])
                    
                else:
                    
                    #read from lines
                    if len(allFiles)==1:
                        if j==1:
                            numbers1.append(line[0])
                    elif len(allFiles)==2:
                        if j==1:
                            numbers1.append(line[0])
                        elif j==2:
                            numbers2.append(line[0])
                    elif len(allFiles)==3:
                        if j==1:
                            numbers1.append(line[0])
                        elif j==2:
                            numbers2.append(line[0])
                        elif j==3:
                            numbers3.append(line[0])
                    elif len(allFiles)==4:
                        if j==1:
                            numbers1.append(line[0])
                        elif j==2:
                            numbers2.append(line[0])
                        elif j==3:
                            numbers3.append(line[0])
                        elif j==4:
                            numbers4.append(line[0])  
                    elif len(allFiles)==5:
                        if j==1:
                            numbers1.append(line[0])
                        elif j==2:
                            numbers2.append(line[0])
                        elif j==3:
                            numbers3.append(line[0])
                        elif j==4:
                            numbers4.append(line[0])
                        elif j==5:
                            numbers5.append(line[0])
                    elif len(allFiles)==6:
                        if j==1:
                            numbers1.append(line[0])
                        elif j==2:
                            numbers2.append(line[0])
                        elif j==3:
                            numbers3.append(line[0])
                        elif j==4:
                            numbers4.append(line[0])
                        elif j==5:
                            numbers5.append(line[0])
                        elif j==6:
                            numbers6.append(line[0])
    #save into file
    
    if len(allFiles)==1:
                file = open(path+"/RESULT/allData.csv","w") 
                file.write(hd[0]+","+"Class (N)"+"\n")

                for a in numbers1:
                    file.write(a+","+","+str(depS1[s])+"\n")
                    s+=1
    if len(allFiles)==2:
                file = open(path+"/RESULT/allData.csv","w") 
                file.write(hd[0]+","+hd[1]+","+"Class (N)"+"\n")

                for a in numbers1:
                    file.write(a+","+numbers2[s]+","+str(depS1[s])+"\n")
                    s+=1
    if len(allFiles)==3:
                file = open(path+"/RESULT/allData.csv","w") 
                file.write(hd[0]+","+hd[1]+","+hd[2]+","+"Class (N)"+"\n")

                for a in numbers1:
                    file.write(a+","+numbers2[s]+","+numbers3[s]+","+str(depS1[s])+"\n")
                    s+=1
    if len(allFiles)==4:
                file = open(path+"/RESULT/allData.csv","w") 
                file.write(hd[0]+","+hd[1]+","+hd[2]+","+hd[3]+","+"Class (N)"+"\n")

                for a in numbers1:
                    file.write(a+","+numbers2[s]+","+numbers3[s]+","+numbers4[s]+","+str(depS1[s])+"\n")
                    s+=1
    if len(allFiles)==5:
                file = open(path+"/RESULT/allData.csv","w") 
                file.write(hd[0]+","+hd[1]+","+hd[2]+","+hd[3]+","+hd[4]+","+"Class (N)"+"\n")
                #print(len(numbers1))
                for a in numbers1:
                    file.write(a+","+numbers2[s]+","+numbers3[s]+","+numbers4[s]+","+numbers5[s]+","+str(depS1[s])+"\n")
                    s+=1
 
    t1 = time.time() - t0
    print("Time elapsed: ", t1)    
#initiate variable
num=ind_number()  
#generate the indpendent variable 
#loop for number of ind


if num==1:
    id=1
    one_dim(ind1,id)
    
if num==2:
    id=1
    one_dim(ind1,id)
    id=2
    one_dim(ind2,id)
if num==3:
    id=1
    one_dim(ind1,id)
    id=2
    one_dim(ind2,id)
    id=3
    one_dim(ind3,id)
if num==4:
    id=1
    one_dim(ind1,id)
    id=2
    one_dim(ind2,id)
    id=3
    one_dim(ind3,id)
    id=4
    one_dim(ind4,id)
if num==5:
    id=1
    one_dim(ind1,id)
    id=2
    one_dim(ind2,id)
    id=3
    one_dim(ind3,id)
    id=4
    one_dim(ind4,id)
    id=5
    one_dim(ind5,id)
    
if num==6:
    id=1
    one_dim(ind1,id)
    id=2
    one_dim(ind2,id)
    id=3
    one_dim(ind3,id)
    id=4
    one_dim(ind4,id)
    id=5
    one_dim(ind5,id)
    id=6
    one_dim(ind6,id)

collectAll()                          