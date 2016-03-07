#mean reverting strategy based on macd

import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import sys,dateutil.parser
import krakenutl


import macd1
import pandas.io.data as web
import matplotlib.pyplot as plt
import multiprocessing as mp

FROM = '2015-01-01 00:00:00.000000'
INTERVAL=krakenutl.DAY

def compute(pair,fr,interval=INTERVAL,foo=macd1.compTradeDmacd):
    filename=krakenutl.getH5source()
    h5 = pd.HDFStore(filename, 'r')
    tag=krakenutl.getTagFromPair(pair,interval)
    df=h5[tag]
    dtSlice = df[df.index > dateutil.parser.parse(fr)]
    dt = macd1.compMacd(dtSlice,foo)

    #comparison between market and strategy
    dcumsum = dt[['market','strategy']].cumsum() 
    lpos=len(dcumsum)-1
    strat=np.exp(dcumsum['strategy'][lpos])
    bhold=np.exp(dcumsum['market'][lpos])
    return (bhold,strat,lpos+1)
  
def computeAll(interval=INTERVAL):
    df=pd.DataFrame(columns=['pair','from','interval','bhold','strat','strat1','nintervals'])
    intStr = krakenutl.intervalToStr(interval)
    for p in krakenutl.PAIRS:
        (bhold,strat,nint)=compute(p,FROM,interval,macd1.compTradeDmacd)
        (bhold1,strat1,nint1)=compute(p,FROM,interval,macd1.compTradeDmacdNoShort)
        df.loc[len(df)] = [p, FROM, intStr, bhold,strat,strat1,nint]
    print(df)


if __name__ == '__main__':    
    computeAll(krakenutl.DAY)
    computeAll(krakenutl.WEEK)     
    computeAll(krakenutl.H3)
    computeAll(krakenutl.H1)     
    computeAll(krakenutl.M30)
    computeAll(krakenutl.M15)
    computeAll(krakenutl.M5)             
 