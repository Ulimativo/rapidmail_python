import requests
from requests.auth import HTTPBasicAuth
import json


def get_list_stats():
     endpoint="https://apiv3.emailsys.net/recipientlists/5677/stats/activity"
     query_params={'from':'2021-11-17', 'to':'2021-11-17'}
     response=requests.get(endpoint, params=query_params, auth=HTTPBasicAuth('30c207496d66c3d0192e62e135ba40080957150e', '6b8f14c0b919fdacb05d587de792a5466dbe1576'))
     print(f"Connecing... {response.status_code} - {response.reason}")
     jdict=response.json()
     print(json.dumps(jdict, indent=2))

def get_subscriber_stat(subscriber_list, status):
     endpoint="https://apiv3.emailsys.net/recipients"
     query_params={'recipientlist_id':subscriber_list, 'status':status}
     response=requests.get(endpoint, params=query_params, auth=HTTPBasicAuth('30c207496d66c3d0192e62e135ba40080957150e', '6b8f14c0b919fdacb05d587de792a5466dbe1576'))
     print(f"Connecting... {response.status_code} - {response.reason}")
     jdict=response.json()
     return jdict
     
     
 
recipients=get_subscriber_stat(subscriber_list=5677, status='active')
#print(json.dumps(recipients['_embedded']['recipients'], indent=2))
#print(f"{len(recipients['_embedded']['recipients'])} records found.")
#print(json.dumps(recipients, indent=2))

if recipients['_links']['next'] is not None:
     print("Next page found - downloading ", recipients['_links']['next'])
     response=requests.get(recipients['_links']['next'])
     data=response.json
     print(json.dumps(data, indent=2))
