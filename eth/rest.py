import os, sys

import ctypes
import base64
import random, time, re
import urllib2,json
import subprocess
import socket
import ssl
import os.path,shutil

# disable self-sign cert validation
#gsslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

def getAuthHeader():
    return {} 
#    up=testcfg.user+':'+testcfg.password
#    userAndPass = base64.b64encode(str.encode(up)).decode("ascii")
#    headers = { 'Authorization' : 'Basic %s' %  userAndPass }
    return headers
    
def restCall(url, params):
    if(params != None):
        params = json.dumps(params).encode('utf-8')

    headers = getAuthHeader()
    headers['Content-Type'] = 'application/json'
#    headers['Accept'] = 'application/json'
    request = urllib2.Request(url,params,headers=headers)
    req = urllib2.urlopen(request)  
    response = req.read()
    #response = urllib2.request.urlopen(req,context=gsslcontext).read() 
    str_response = response.decode('utf-8')
    o = json.loads(str_response) 
    return o
        
def restPOST(url, body):
    return restCall(url, body)
    
def restGET(url):
    headers = getAuthHeader()
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/json'
    request = urllib2.Request(url, headers=headers)
    req = urllib2.urlopen(request)
    response=req.read()
    #response = urllib2.request.urlopen(req,context=gsslcontext).read()   
    str_response = response.decode('utf-8')
    o = json.loads(str_response) 
    return o