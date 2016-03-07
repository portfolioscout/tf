import rest
import time,os,codecs
import logging,datetime
import pandas as pd
import krakenutl
from pandas import HDFStore,DataFrame

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('kraken')
logger.setLevel(logging.DEBUG)

# jan 1 2015
#STARTDATE=1420070400
#1/1/12
STARTDATE=1325377003
INTERVAL=krakenutl.DAY



#print rest.restGET('https://api.kraken.com/0/public/Time')
#print rest.restPOST('https://api.kraken.com/0/public/Assets',{"asset":"XETH"})

#input:
#pair = asset pair to get OHLC data for
#interval = time frame interval in minutes (optional):
#	1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600
#since = return committed OHLC data since given id (optional.  exclusive)

#output:
#pair_name" = pair name
#    array of array entries("time", "open", "high", "low", "close", "vwap", "volume", "count")
#last = id to be used as since when polling for new, committed OHLC data

def toUtf8(s):
    return s.encode('utf-8') if isinstance(s, basestring)   else s

def localTimeFromEpoch(epoch):
    return datetime.datetime.fromtimestamp(epoch)

def getOhlc(pair,interval=1440,since=0):
    last = since
    last1 = -1
    totEntr = 0

    columns = ["time", "open", "high", "low", "close", "vwap", "volume", "count"]
    df=pd.DataFrame(columns=columns)
    while last1!=last:
        body={
        "pair":pair,
        "interval":interval,
        "since":last
        }
        url = 'https://api.kraken.com/0/public/OHLC'
        try:
            logger.debug(body)
            r = rest.restPOST(url,body)
            if not "result" in r.keys():
                break
                
            #print r
            last1=last
            last = r["result"]["last"] if "last" in r["result"].keys() else 0
            ent=len(r["result"][pair])
            logger.debug('ent: '+str(ent))
            totEntr = totEntr+ent
            #pivot data into  multi l=column format
            d=r["result"][pair]
            if len(columns)!=len(d[0]):
                logger.error("len(columns)!=len(d) "+str(len(columns))+" "+str(len(d)))
                return None
                
            for i in range(0,len(d)):
                d[i][0]=localTimeFromEpoch(d[i][0])
                df.loc[i]=[toUtf8(x) for x in d[i]]

            time.sleep(1)
        except Exception as e:
            logger.error('Exception while calling: '+url+" exception: "+str(e))
            return None
            
    logger.debug("Total entries: "+str(totEntr))
    df= df.drop_duplicates("time").set_index("time").sort_index()
    #remove the last row the data may not be complete
    df.drop(df.index[len(df)-1], inplace=True)
    return df

def storeHdf5(data, tag, path):
    hdf = HDFStore(path,'a')
    if tag in hdf.keys():
        hdf.append(tag,data)
    else:
        hdf.put(tag,data)
    hdf.close()          

def getKrakenData(interval=1440,since=0):
    directory = krakenutl.SRCDIR
    if not os.path.exists(directory):
        os.makedirs(directory)
    for p in krakenutl.PAIRS:
        logger.debug('download data for: '+p+' interval: '+str(interval)+' since:'+str(localTimeFromEpoch(since)))
        pdata = getOhlc(p, interval,since)
        storeHdf5(pdata,krakenutl.getTagFromPair(p,interval),krakenutl.getH5source())


if __name__ == '__main__':   
    getKrakenData(krakenutl.DAY,STARTDATE) 
    getKrakenData(krakenutl.WEEK,STARTDATE)            
    getKrakenData(krakenutl.H3,STARTDATE) 
    getKrakenData(krakenutl.H1,STARTDATE)
    getKrakenData(krakenutl.M30,STARTDATE) 
    getKrakenData(krakenutl.M15,STARTDATE)
    getKrakenData(krakenutl.M5,STARTDATE) 
    #df=getOhlc("XXBTZUSD",5,1441148619) 
    #print(df) 
    hdf = HDFStore(krakenutl.getH5source())
    for k in hdf.keys():
        print(k,len(hdf[k]))
    hdf.close()              
    
