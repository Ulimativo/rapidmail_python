########################################
# Python Module for the RapidMail API. #
# v. 0.2 - Alpha                       #
########################################

# TODO: include all pages - currently only reading page 1. Done for mailings an recipients


# IMPORTS
# API handling - obligatory libraries
import requests
from requests.auth import HTTPBasicAuth

# Optional Libraries - uncomment if not needed
from datetime import datetime


"""
CONFIGURATION VIA .ENV
You should use a .env file for your API credentials, especially in production.
If you want to use hardcoded login-information, comment out the import and config 
and uncomment the block below.
"""
# import dotenv library
from dotenv import dotenv_values
config = dotenv_values(".env")

# Config without .env file - development only
#config={"RAPIDMAIL_USERNAME" : "username",
#        "RAPIDMAIL_PASSWORD" : "password"}


class APIBasic():
    """
    Basic API class handling API calls.

    Methods
    --------
    get_request(endpoint=String, query_params=Dict)
    returns API request, using given endpoint. Query parameters are optional, given as dictionary.

    list_api_users()
    prints list of API users, including last time of update
    """

    def __init__(self) -> None:
        self.base_url = "https://apiv3.emailsys.net"
        self.endpoint = {
            "apiusers": f"{self.base_url}/v1/apiusers",
            "mailings": f"{self.base_url}/v1/mailings",
            "recipientslists": f"{self.base_url}/v1/recipientlists",
            "recipients": f"{self.base_url}/v1/recipients",
            "blacklist": f"{self.base_url}/v1/blacklist",
            "forms": f"{self.base_url}/v2/forms",
        }

    def get_request(self, endpoint, query_params=None):
        # returns response of requests as object, either with query parameters or without.
        if query_params == None:
            return requests.get(endpoint, auth=HTTPBasicAuth(config['RAPIDMAIL_USERNAME'], config['RAPIDMAIL_PASSWORD']))
        else:
            return requests.get(endpoint, params=query_params, auth=HTTPBasicAuth(config['RAPIDMAIL_USERNAME'], config['RAPIDMAIL_PASSWORD']))

    def list_api_users(self):
        # fetch and list all api users by ID, Name and Last Updated Timestamp
        api_user_list = self.get_request(self.endpoint['apiusers']).json()
        for api_user in api_user_list['_embedded']['apiusers']:
            print(
                f"{api_user['id']} - {api_user['description']} - last updated: {api_user['updated']}")

    def __str__(self) -> str:
        """
        sends request and prints connection status to the console, e.g. for connection tests
        usage example: print(APIBasic())
        """
        response = self.get_request(self.endpoint['apiusers'])
        return f" Connection status: {response.status_code} - {response.reason}"


class APIUser(APIBasic):
    """
    Class representing API User information
    returns User ID, Description and time of Last Update
    """

    def __init__(self, user_id) -> int:
        super().__init__()
        self.api_user = self.get_request(
            f"{self.endpoint['apiusers']}/{user_id}").json()

    def __str__(self) -> str:
        return f"{self.api_user['id']} - {self.api_user['description']} - last updated: {self.api_user['updated']}"


class Blacklist(APIBasic):
    """
    TODO Class handling blacklist entries
    """

    def __init__(self) -> None:
        super().__init__()
        self.blacklist = self.get_request(self.endpoint['blacklist']).json()

    def __str__(self) -> str:
        return super().__str__()


class Forms(APIBasic):
    """
    TODO Class handling form lists
    """

    def __init__(self) -> None:
        super().__init__()
        self.forms_list = self.get_request(self.endpoint['forms']).json()


class Recipientlists(APIBasic):
    """
    Class handling recipientlists.
    Prints list of all recipient lists, including:
    ID, Name, Description, Total Subscribers
    """

    def __init__(self) -> None:
        super().__init__()
        recipient_lists = self.get_request(
            self.endpoint['recipientslists']).json()
        for recipient_list in recipient_lists['_embedded']['recipientlists']:
            if recipient_list['description'] == "":
                recipient_list['description'] = "No Description"
            total = Recipientlist(recipient_list['id']).total
            print(
                f"{recipient_list['id']} - {recipient_list['name']} ({recipient_list['description']}) - total Subs: {total}")


class Recipientlist(APIBasic):
    """
    Class providing details of a given recipient list id.
    """

    def __init__(self, list_id) -> None:
        super().__init__()
        self.list_id = list_id
        self.recipientlist = self.get_request(
            f"{self.endpoint['recipientslists']}/{list_id}").json()
        self.creation_date = self.recipientlist['created'][0:10]
        self.total = self.get_list_total()
        self.details = self.get_list_details().json()

    def get_list_total(self):
        response = self.get_list_details()
        return response.json()['total']

    def get_list_details(self):
        today = datetime.today().strftime('%Y-%m-%d')
        query_params = {'from': self.creation_date,
                        'to': today, 'status': 'active'}
        return self.get_request(f"{self.endpoint['recipientslists']}/{self.list_id}/stats/activity", query_params)


class Mailings(APIBasic):
    """
    Class representing Mailing object from API.

    """

    def __init__(self) -> None:
        super().__init__()
        # self.mailings=self.get_request(self.endpoint['mailings']).json()
        self.all_mailings = self.get_all_results()

    def __str_(self) -> str:
        return super().__str__()

    def get_all_results(self):
        self.mailings = self.get_request(self.endpoint['mailings']).json()
        mailing_list = self.mailings['_embedded']['mailings']
        next_key = self.mailings['_links']['next']['href']
        # while loop to run until no more pages exist:
        while next_key:
            print("Next Found!")
            print(next_key)
            self.mailings = self.get_request(next_key).json()
            mailing_list.extend(self.mailings['_embedded']['mailings'])
            try:
                next_key = self.mailings['_links']['next']['href']
                continue
            except:
                break
        return mailing_list


class Mailing(APIBasic):
    """
    Class for detailes mailing statistics
    """

    def __init__(self, mailing_id) -> None:
        super().__init__()
        self.mail_stats = self.get_mailing_stats(mailing_id)

    def get_mailing_stats(self, mailing_id):
        endpoint_url = f"{self.endpoint['mailings']}/{mailing_id}/stats"
        return self.get_request(endpoint_url).json()


class Recipient(APIBasic):

    def __init__(self, list_id) -> None:
        super().__init__()
        self.details = self.get_recipients(list_id)

    def get_recipients(self, list_id):
        query_params = {'recipientlist_id': list_id}
        self.recipients = self.get_request(
            self.endpoint['recipients'], query_params).json()
        recipients_list = self.recipients['_embedded']['recipients']
        next_key = self.recipients['_links']['next']['href']
        while next_key:
            self.recipients = self.get_request(next_key).json()
            recipients_list.extend(self.recipients['_embedded']['recipients'])
            try:
                next_key = self.recipients['_links']['next']['href']
                continue
            except:
                break
        return recipients_list



def main():
    print("--------------------------------------------------------------------")
    print("This is the Rapidmail API Python Module.")
    print("Source can be found at https://github.com/Ulimativo/rapidmail_python")
    print("--------------------------------------------------------------------")

if __name__ == "__main__":
    main()
