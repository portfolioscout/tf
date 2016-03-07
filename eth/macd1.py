import numpy as np
import pandas as pd

REGDELTA=0.001
#transaction cost is 0.5%
XCOSTPCT=0.5

# classical mean reverting, buy and short
def compTradeDmacd(dt):
    dt['regime']=np.where(dt['dmacd']>REGDELTA,1,0)
    dt['regime']=np.where(dt['dmacd']<-REGDELTA,-1,dt['regime'])
    dt['strategy']=dt['regime'].shift(1)*dt['market']
    dt['strategy_fee']=dt['regime'].shift(1)*dt['market']*(1.0-XCOSTPCT/100.)
    return dt
    
# classical mean reverting, buy but don't short
def compTradeDmacdNoShort(dt):
    dt['regime']=np.where(dt['dmacd']>REGDELTA,1,0)
    dt['regime']=np.where(dt['dmacd']<-REGDELTA,0,dt['regime'])
    dt['strategy']=dt['regime'].shift(1)*dt['market']
    dt['strategy_fee']=dt['regime'].shift(1)*dt['market']*(1.0-XCOSTPCT/100.)
    return dt
        
def compMacd(dt,foo):
    
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
    return foo(dt)
    
      
      