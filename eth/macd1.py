import numpy as np
import pandas as pd

REGDELTA=0.001

def compTrade(dt):
    dt['regime']=np.where(dt['dmacd']>REGDELTA,1,0)
    dt['regime']=np.where(dt['dmacd']<-REGDELTA,-1,dt['regime'])
    dt['strategy']=dt['regime'].shift(1)*dt['market']
    return dt
    
def compMacd(dt):
    
    tempds = dt.sort_index(ascending = True)
    firstDate = tempds.index[0]
    firstClose = float(tempds.iloc[0]['close'])
        
    cs = tempds['close'].astype(float)
    macd=pd.ewma(cs,span=12)-pd.ewma(cs,span=26)
    signal=pd.ewma(macd,span=9)
    
    dt['macd'] = macd
    dt['signal'] = signal
    dt['dmacd'] = macd-signal
    dt['market']=np.log(cs/cs.shift(1))
    return compTrade(dt)    