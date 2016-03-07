
import time,datetime
PAIRS=["XETHZUSD","XXBTZUSD","XLTCZUSD"]
H5FILE="kraken.h5"
SRCDIR = 'source'

DAY=1440
WEEK=10080
WEEK2=21600
H3=240
H1=60
M30=30
M15=15
M5=5

intToStr = {
    DAY:'day',
    WEEK:'week',
    WEEK2:'2 weeks',
    H3:'3 hours',
    H1:'hour',
    M30:'30 mins',
    M15:'15 mins',
    M5:'5 mins'
}

def getH5source():
    return SRCDIR+'/'+H5FILE
    
def getTagFromPair(pair,interval):
    return pair+'_'+str(interval)

def intervalToStr(interval):
    if interval not in intToStr.keys():
        raise 'invalid interval'
    else:
        return  intToStr[interval] 
        
def toUtf8(s):
    return s.encode('utf-8') if isinstance(s, basestring)   else s

def localTimeFromEpoch(epoch):
    return datetime.datetime.fromtimestamp(epoch)  
    
def epochFromLocalTime(lt):
    return int(time.mktime(time.strptime(lt, "%Y-%m-%d %H:%M:%S")))         


