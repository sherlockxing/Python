# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:58:53 2019

@author: dell
"""

from sklearn.decomposition import PCA
import pandas as pd
import os

codepath = os.getcwd()
#path
#os.chdir(path)

def density():
    for i in range(1,15):
        nom = 'nom'+str(i)
        li = pd.read_csv(nom+'wide25gec0.csv')
        pca=PCA(n_components=1)
        newData=pca.fit_transform(li)
        pca0 = pd.DataFrame(data=newData,columns=['pca1'])
        
        li = pd.read_csv(nom+'wide25gec10.csv')
        pca=PCA(n_components=1)
        newData=pca.fit_transform(li)
        pca1 = pd.DataFrame(data=newData,columns=['pca1'])
        
        xx = 'pca1'
        yy = 'pca2'
        ax = pca0.plot.density(color='Blue', label='gec0')
        bx = pca1.plot.density(color='RED', label='gec1', ax=ax,title=nom).get_figure()
        bx.savefig(codepath+'/'+'density'+path.split('/')[0]+nom+'.png') 
        
def scatter():
    for i in range(1,15):
        nom = 'nom'+str(i)
        li = pd.read_csv(nom+'wide25gec0.csv')
        pca=PCA(n_components=2)
        newData=pca.fit_transform(li)
        pca0 = pd.DataFrame(data=newData,columns=['pca1','pca2'])
        
        li = pd.read_csv(nom+'wide25gec10.csv')
        pca=PCA(n_components=2)
        newData=pca.fit_transform(li)
        pca1 = pd.DataFrame(data=newData,columns=['pca1','pca2'])
        
        xx = 'pca1'
        yy = 'pca2'
        ax = pca0.plot.scatter(x=xx,y=yy,color='Blue', label='gec0')
        bx = pca1.plot.scatter(x=xx,y=yy,color='RED', label='gec1', ax=ax,title=nom).get_figure()
        bx.savefig(codepath+'/'+'scatter'+path.split('/')[0]+nom+'.png') 
        
#density()
scatter()