

import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import multiprocessing as mp
import pandas.io.data as web
import matplotlib.pyplot as plt
from multiprocessing import Lock
lock = Lock()



def compTrade(dt):
    d=0.001
    dt['reg']=np.where(dt['dmacd']>d,1,0)
    dt['reg']=np.where(dt['dmacd']<-d,-1,dt['reg'])
    dt['strategy']=dt['reg'].shift(1)*dt['market']
    return dt
    
def getSymbols(h5):
    l=[]
    for c in h5.keys():
        l.append(h5[c]['Adj Close'].columns.values)
        
    return [item for items in l for item in items]  

def getClose(h5,sym):
    df = pd.DataFrame()
    for c in h5.keys():
        for i in h5[c]['Adj Close'].columns:
            if sym == i:
                df['Adj Close']=h5[c]['Adj Close'][i]
        
    return df

def fromYahoo(name,sdate='2015-01-01',edate='2015-12-31'):
    
    dt = web.DataReader(name, data_source='yahoo',
                 start=sdate,end=edate)    
    return dt

def macd(dt):
    
    dt['Date'] = pd.to_datetime( dt.index)
    tempds = dt.sort('Date',ascending = True )
    firstDate = tempds['Date'][0]
    dt['CloseN'] = dt['Adj Close']/dt['Adj Close'][firstDate]
    
    cs = tempds['Adj Close']
    firstClose=tempds['Adj Close'][firstDate]
    macd=pd.ewma(cs,span=12)-pd.ewma(cs,span=26)
    signal=pd.ewma(macd,span=9)
    
    dt['macd'] = macd
    dt['signal'] = signal
    dt['dmacd'] = macd-signal
    dt['market']=np.log(cs/cs.shift(1))
    return compTrade(dt)


def plotMacd(dt):
    

    figsize=(20, 10)
    fig, axs1 = plt.subplots(1,1,figsize=figsize)
    fig, axs2 = plt.subplots(1,1,figsize=figsize)
    fig, axs3 = plt.subplots(1,1,figsize=figsize)
    fig, axs4 = plt.subplots(1,1,figsize=figsize)
            
    dt['CloseN'].plot(ax=axs1, grid=True)
    dt['macd'].plot(ax=axs2, grid=True)
    dt['signal'].plot(ax=axs2, grid=True)
    dt['dmacd'].plot(ax=axs3, grid=True)
    dt['reg'].plot(ax=axs3, grid=True)
    dt[['market','strategy']].cumsum().apply(np.exp).plot(ax=axs4, grid=True)
    
def doCumsum(dt):
    ntrades=0
    prev=0
    for e in dt['reg']:
        if prev !=e:
            ntrades=ntrades+1
        prev = e
        
    dcumsum = dt[['market','strategy']].cumsum()    
    dcumsum['delta']=(dcumsum['strategy']-dcumsum['market'])*100
    mean=dcumsum['delta'].mean()
    rmse = np.sqrt(((dcumsum['delta']-mean)**2).mean())
    win=np.compress(dcumsum['delta']>0.001,dcumsum['delta']).size*1.0/len(dcumsum['delta'])*100
    lpos=len(dcumsum)-1
    last=dcumsum['delta'][lpos]
    strat=np.exp(dcumsum['strategy'][lpos])
    bhold=np.exp(dcumsum['market'][lpos])

    res={}
    res['meanpct']=mean
    res['rmsepct']=rmse
    res['win']=win
    res['strategy']=strat
    res['buyhold']=bhold
    res['ntrades']=ntrades
    res['totwinpct']=last
    return dcumsum,res
    
def doCumsumonSymbols(p):
    filename,sym,start,end=p    
    h5 = pd.HDFStore(filename, 'r')           
    fd=pd.DataFrame()
    try:
        lock.acquire()
        dt0=getClose(h5,sym)[start:end]
        lock.release()

        dt = macd(dt0) 
        dcs,res=doCumsum(dt)
        res['sym']=sym
        tfd=pd.DataFrame(res,index=[sym])
        fd=fd.append(tfd)
    except: # catch *all* exceptions
        print "exception with", sym
        print sys.exc_info()  
    return fd
    
def parallelCumsum(filename,syms,start,end,procs=1):

    alists=[]
    for i in syms:
        alists.append((filename,i,start,end))
    #print alists,procs
    pool = mp.Pool(processes=procs)
    res=pool.map(doCumsumonSymbols,alists)

    df=pd.DataFrame()
    for r in res:
        df=df.append(r)
    df=df.sort('totwinpct',ascending=False) 
    return df    