# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 22:33:23 2018

@author: saranshmohanty
"""
import pandas as pd
import re
import glob
import os 
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
import numpy as np
from nltk.stem.snowball import  SnowballStemmer
import nltk
import csv
from nltk.tokenize import RegexpTokenizer
from string import digits

'''
Array lookup
A_temp- first row of the raw data
A - URL Split + Lemmetizer
B - numbers removed
C - punctuations removed
user_count- second row of the raw data
'''


nltk.download('stopwords')
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('wordnet')
stemmer = PorterStemmer()
lemmatiser = WordNetLemmatizer()



#############################change directory##################################
os.chdir('C:/Users/saranshmohanty/Desktop')
count=0
A=[]
A_temp=[]
user_count=[]

########################## change filename####################################
with open('Online mba reddit comment.csv','r') as csvfile:
    sv_reader = csv.reader(csvfile, delimiter=',')
    for row in sv_reader:
        A_temp.append(row[0])
        
#############removes delimiters and then form a sentence#######################
for i in A_temp:
    b=re.split('; |, |\*|\n |/|-|@|:',i)
    c=' '.join(word for word in b)
    A.append(c)

B=[]
stop = list(stopwords.words('english'))

my_dict={}

for i in A:
    j=word_tokenize(i)
    #print(len(j))
    #print(j[0])
    k=" "
    for l in j:
        remove_digits = str.maketrans('', '', digits)
        res = l.translate(remove_digits)
        m=lemmatiser.lemmatize(res)
        if m not in stop:
            #print(m)
            k+=" "
            k+=m
    B.append(k)
    
C=[]

#######################################we tokenise#######################################
for i in B:
    tokenizer = RegexpTokenizer(r'\w+')
    #removes the punctuations
    alpha=tokenizer.tokenize(i)
    if alpha in ['http','com','www','org','in','co','https','true','undefined','c','d'] and len(alpha)>1:
        print("http found")
    else:
        C.append(alpha)
        

from collections import defaultdict  # available in Python 2.5 and newer
urls_d = defaultdict(int)


####################################scoring########################################
###############################we can modify the exclusion array accordingly#################
for i in C:
    j=0
    k=0
    for j in range(0,len(i)):
        for k in range(j,len(i)):
            a=min([i[j],i[k]])
            #print(j)
            b=max([i[j],i[k]])
            #print(k)
            if(a,b) in my_dict and a!=b and a not in ['http','com','www','org','in','co','https','true','@'] and b not in ['http','com','www','org','in','co','https','true'] and len(a)>1 and len(b)>1 and len(a)<10 and len(b)<10:
                my_dict[(a,b)]+=1
            else:
                my_dict[(a,b)]=1
                

          
for keys in my_dict.keys():
    
    x,y=keys
    '''
    ind=[]
    ind_count=0
    for i in range(0,len(A)):
        if x in A[i] and y in A[i]:
          ind.append(i)
    for i in ind:
        ind_count+=int(user_count[i])
    my_dict[(x,y)]+=ind_count
    '''
    if x==y or x in ['http','com','www','org','in','co','https','true'] or y in ['http','com','www','org','in','co','https','true'] or len(x)<=1 or len(x)>=15 or len(y)<=1 or len(y)>=15 :
        my_dict[(x,y)]-=1000

################################33 here the stock words are removed#####################################    
temp2=[]
for i in my_dict.keys():
    x,y=i
    if(my_dict[(x,y)]>0):
        temp2.append((x,y,my_dict[(x,y)]))
temp1=[]
temp1=pd.DataFrame(list(temp2))
temp1.columns=['word1','word2','score']
temp=[]
temp=temp1.sort_values(by=['score'],ascending=False)

#################check the name of output file################################
temp.to_csv('NBAonline__comments_test.csv',index=False)
        

        
