########################################
# Python Module for the RapidMail API. #
# v. 0.1 - Alpha                       #
########################################

# IMPORTS

# General imports
from dotenv import dotenv_values

# API handling
import requests
from requests.auth import HTTPBasicAuth

# Additional Libraries
import json

# CONFIGURATION
config=dotenv_values(".env") # config = {"RAPIDMAIL_USERNAME" : "username", "RAPIDMAIL_PASSWORD" : "password"}


class APIBasic():
     def __init__(self) -> None:
          self.base_url="https://apiv3.emailsys.net"

     def get_request(self, endpoint):
               # returns response of requests as object
               return requests.get(endpoint, auth=HTTPBasicAuth(config['RAPIDMAIL_USERNAME'], config['RAPIDMAIL_PASSWORD']))

     def conn_stat(self, response):
          # prints connection status to the console
          print(f" Connection status: {response.status_code} - {response.reason}")

     def get_api_users(self):
          # basic method returning list of API users to object variable api_uses
          endpoint_spec='/v1/apiusers' # specific endpoint addition to base URL
          endpoint=self.base_url+endpoint_spec
          return self.get_request(endpoint).json()

     def list_api_users(self):
          # fetch and list all api users by ID, Name and Last Updated Timestamp
          api_user_list=self.get_api_users()
          for api_user in api_user_list['_embedded']['apiusers']:
               print(f"{api_user['id']} - {api_user['description']} - last updated: {api_user['updated']}")
          
class APIUser(APIBasic):
     """
     Class representing API User information
     """
     def __init__(self, user_id) -> int:
          super().__init__()
          endpoint_spec=f"/v1/apiusers/{user_id}"
          endpoint=self.base_url+endpoint_spec
          self.api_user=self.get_request(endpoint).json()

     def __str__(self) -> str:
          return f"{self.api_user['id']} - {self.api_user['description']} - last updated: {self.api_user['updated']}"
          

print(APIUser(10345))




"""
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
"""