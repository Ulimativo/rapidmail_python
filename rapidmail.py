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
from datetime import datetime

# CONFIGURATION
config=dotenv_values(".env") # config = {"RAPIDMAIL_USERNAME" : "username", "RAPIDMAIL_PASSWORD" : "password"}


class APIBasic():
     def __init__(self) -> None:
          self.base_url="https://apiv3.emailsys.net"

     def __str__(self) -> str:
          # sends request and prints connection status to the console
          response=self.get_request(f"{self.base_url}/v1/apiusers")
          return f" Connection status: {response.status_code} - {response.reason}"


     def get_request(self, endpoint):
               # returns response of requests as object
               return requests.get(endpoint, auth=HTTPBasicAuth(config['RAPIDMAIL_USERNAME'], config['RAPIDMAIL_PASSWORD']))

     def get_request_params(self, endpoint, query_params):
               # returns response of requests as object
               return requests.get(endpoint, params=query_params, auth=HTTPBasicAuth(config['RAPIDMAIL_USERNAME'], config['RAPIDMAIL_PASSWORD']))


     def list_api_users(self):
          # fetch and list all api users by ID, Name and Last Updated Timestamp
          endpoint_spec='/v1/apiusers' # specific endpoint addition to base URL
          endpoint=self.base_url+endpoint_spec
          api_user_list=self.get_request(endpoint).json()
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

class Blacklist(APIBasic):
     """
     Class handling blacklist entries
     """
     def __init__(self) -> None:
         super().__init__()
         endpoint_spec="/v1/blacklist"
         endpoint=self.base_url+endpoint_spec
         self.blacklist=self.get_request(endpoint).json()

     def __str__(self) -> str:
         return super().__str__()


class Forms(APIBasic):
     """
     Class handling form lists
     """
     def __init__(self) -> None:
         super().__init__()
         endpoint_spec="/v2/forms"
         endpoint=self.base_url+endpoint_spec
         self.forms_list=self.get_request(endpoint).json()


class Recipientlists(APIBasic):
     """
     Class handling recipientlists
     """
     def __init__(self) -> None:
         super().__init__()
         endpoint_spec="/v1/recipientlists"
         endpoint=self.base_url+endpoint_spec
         recipient_lists=self.get_request(endpoint).json()
         for recipient_list in recipient_lists['_embedded']['recipientlists']:
               if recipient_list['description'] == "":
                    recipient_list['description']="No Description"
               total=Recipientlist(recipient_list['id']).total
               print(f"{recipient_list['id']} - {recipient_list['name']} ({recipient_list['description']}) - total Subs: {total}")

class Recipientlist(APIBasic):
     def __init__(self, list_id) -> None:
          super().__init__()
          endpoint_spec=f"/v1/recipientlists/{list_id}"
          self.endpoint=self.base_url+endpoint_spec
          self.recipientlist=self.get_request(self.endpoint).json()
          self.creation_date=self.recipientlist['created'][0:10]
          self.total=self.get_list_total()  
          self.details=self.get_list_details().json()      

     def get_list_total(self):
          response=self.get_list_details()
          return response.json()['total']
     
     def get_list_details(self):
          today=datetime.today().strftime('%Y-%m-%d')
          endpoint_spec=f"{self.endpoint}/stats/activity"
          query_params={'from':self.creation_date, 'to':today, 'status':'active'}
          return self.get_request_params(endpoint_spec, query_params)          


########################################################################

#print(APIBasic()) 
#print(APIUser(10345))
#print(Recipientlists())
#print(json.dumps(Recipientlist(5613).details, indent=2))








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