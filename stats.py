#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 22:14:55 2017

@author: rodrigo
"""

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import operator as op

# Importing the dataset
dataset = pd.read_csv('full.csv', delimiter='|')
#X = dataset.iloc[:, :-1].values
#y = dataset.iloc[:, 3].values

dataset = []
with open('full.csv', 'r') as file:
    for line in file:
        a = line.split('|')
        if len(a) == 7:
            dataset.append(a)
            
dataset = dataset[1:]

classes_count = {}
for data in dataset:
    classes = data[1].split(',')
    cl_set = set()
    for cl in classes:
        c = cl.upper()
        c = c.replace(' ', '')    
        try:
            cl_set.add(c[0])
        except:
            pass
    for i in list(cl_set):
        if i in classes_count:
            classes_count[i] += 1
        else:
            classes_count[i] = 1

sorted_keys, sorted_vals = zip(*sorted(classes_count.items(), key=op.itemgetter(0)))
plt.figure(figsize=(12,6))
sns.barplot(sorted_keys, sorted_vals, alpha=0.8)
plt.ylabel('Número de patentes', fontsize=12)
plt.xlabel('Classe', fontsize=12)
plt.xticks(rotation='vertical')
plt.show()

n_classes_count = {}
for data in dataset:
    classes = data[1].split(',')
    if len(classes) in n_classes_count:
        n_classes_count[len(classes)] += 1
    else:
        n_classes_count[len(classes)] = 1

sorted_keys, sorted_vals = zip(*sorted(n_classes_count.items(), key=op.itemgetter(0)))
plt.figure(figsize=(12,6))
sns.barplot(sorted_keys, sorted_vals, alpha=0.8)
plt.ylabel('Número de patentes', fontsize=12)
plt.xlabel('Número de classes', fontsize=12)
plt.xticks(rotation='vertical')
plt.show()