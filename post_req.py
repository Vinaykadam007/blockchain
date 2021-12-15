import requests
from argparse import ArgumentParser

from requests.models import Response

parser = ArgumentParser()
parser.add_argument('-ip','--ipaddress')
parser.add_argument('-yourip','--youripaddress')
parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
args = parser.parse_args()
port = args.port
ipaddress = args.ipaddress
youripaddress = args.youripaddress


url = "http://{0}:{1}/nodes/register".format(ipaddress,port)

payload="{\n \"nodes\":[\""+str(youripaddress)+"\"]\n}\n"
print("PAYLOAD", payload)
# payload="{\n \"nodes\":[\"{0}\"]\n}\n".format(youripaddress)
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
