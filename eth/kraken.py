import rest
import time
import logging,datetime
import pandas as pd

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('kraken')
logger.setLevel(logging.DEBUG)


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

def localTimeFromEpoch(epoch):
    return datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S.%f')

def getOHLC(pair,interval=1440,since=0):
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
            totEntr = totEntr+ent
            #pivot data into  multi l=column format
            d=r["result"][pair]
            if len(columns)!=len(d[0]):
                logger.error("len(columns)!=len(d) "+str(len(columns))+" "+str(len(d)))
                return None
                
            for i in range(0,len(d)):
                d[i][0]=localTimeFromEpoch(d[i][0])
                df.loc[i]=d[i]

            time.sleep(1)
        except Exception as e:
            logger.error('Exception while calling: '+url+" exception: "+str(e))
            return None
            
    logger.debug("Total entries: "+str(totEntr))
    df= df.drop_duplicates("time").set_index("time").sort_index()
    #remove the last row the data may not be complete
    df.drop(df.index[len(df)-1], inplace=True)
    return df
            
            
df=getOHLC("XETHZUSD",1440,1441148619) 
print(df)           
    
