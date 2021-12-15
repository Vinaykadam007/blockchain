import requests
from argparse import ArgumentParser
import urllib
import json

# filedatabinary = ""
# with open(r"D:\WORK\Blockchain\Blockchain MockupV3.pdf","rb") as f:
#     # filedatabinary = urllib.parser.quote_plus(f.read())
#     filedatabinary = urllib.parse.quote_plus(f.read())
#     # data = f.read()
#     # print("DATA",data)
#     # f.close()
# print(filedatabinary)
# parser = ArgumentParser()
# parser.add_argument('-ip','--ipaddress')
# parser.add_argument('-filename','--filenamepath')
# parser.add_argument('-filedata','--filedatabinary')
# args = parser.parse_args()
# ipaddress = args.ipaddress
# filenamepath = args.filenamepath
# filedatabinary = args.filedatabinary

# # payload = "{\n \"nodes\":[\"http://192.168.34.145\"] \n}\n"
# payload = "{\n \"certificateName\":\""+str(filenamepath)+"\",\n \"certificateData\":\""+str(filedatabinary)+"\"\n}\n"
# # payload = json.dumps({"certificateName" : "mycert.pdf","certificateData":filedatabinary})
# print("PAYLOAD", payload)
# headers ={
#     'Content-Type': 'application/json'
# }

# r = requests.request("POST","http://"+str(ipaddress)+":3000/transactions/new", data= payload)
# print(r.text,r.reason)



parser = ArgumentParser()
parser.add_argument('-ip','--ipaddress')
parser.add_argument('-filename','--filenamepath')
# parser.add_argument('-filedata','--filedatabinary')
args = parser.parse_args()
ipaddress = args.ipaddress
filenamepath = args.filenamepath
# filedatabinary = args.filedatabinary


filedatabinary = ""
with open(str(filenamepath),"rb") as f:
    # filedatabinary = urllib.parser.quote_plus(f.read())
    filenames=""
    temp_file = f.read()
    filedatabinary = urllib.parse.quote(temp_file)
    # print(filedatabinary)
    print(str(filenamepath).split('/')[-1])
    filenames = str(filenamepath).split('/')[-1]
    print(filenames)

# print(temp_file)

payload = json.dumps({"certificateName" :str(filenames),"certificateData":str(filedatabinary)})
# print(payload)


# payload = "{}"
# payload = "{\n \"certificateName\":\"Mockup.pdf\",\n \"certificateData\":\""+str(filedatabinary)+"\"\n}\n"

headers ={
    'Content-Type': 'application/json'
}

# r = requests.request("POST","http://192.168.114.23:5000/transactions/new", data= urllib.parse.quote_plus(payload))

# urlstr = "http://{0}:3000/transactions/new".format(str(ipaddress))
# print(urlstr)

# r = requests.request("POST",urlstr, data= payload)
r = requests.request("POST","http://"+str(ipaddress)+":3000/transactions/new", data= payload)
print(r.text,r.reason)