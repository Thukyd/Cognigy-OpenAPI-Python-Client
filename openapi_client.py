"""
    Module to handle authentication and pagination for OpenAPI requests.

    Manegement UI based requests
    - load_management_ui_credentials: loads and retrieves username and password from a JSON file containing secret information.
    - get_request_basic_auth: helper function to make GET queries to OpenAPI endpoints based on a base_url, and username and password - aka Management UI credentials.
    API Key based requests
    - get_requests_api_key: helper function to make queries to OpenAPI endpoints based on a base_url, and api_key and different parameters - aka API Key credentials.

"""
import warnings 
warnings.filterwarnings('ignore')

import requests
from requests.auth import HTTPBasicAuth
import json

import logging

def get_size_of_response(response):
    """
    Helper function to get the size of a response in bytes, kb and mb.
    """
    size_in_bytes = len(response.content)
    size_in_mb = size_in_bytes / 1024 / 1024 # conversion in mb
    logging.info(f"Response size: {size_in_mb} MB")


def load_management_ui_credentials(path_to_secrets_json):
    """
    Loads and retrieves username and password from a JSON file containing secret information.

    Args:
        secrets_json (str): The path to the JSON file containing secret information.

    Returns:
        tuple: A tuple containing the username and password retrieved from the JSON file.

    Example:
        username, password = load_management_ui_credentials("path/to/secrets.json")
        print("Username:", username)
        print("Password:", password)
    """
    # Open the JSON file containing secret information
    with open(path_to_secrets_json) as f:
        # Load the JSON content
        json_content = json.load(f)

    # Retrieve and return the username and password from the JSON content
    return json_content["username"], json_content["password"]

def get_request_basic_auth(base_url, endpoint, username, password, params={}):
    """
        Helper Functionality for management ui queries Cogniyion OpenAPI (https://api.your-url/openapi)

        Make GET queries to OpenAPI endpoints based on a base_url, and username and password.
        It handles a dict of parameters to add to the query. This function follows pagination until there
        are no more items to fetch from the endpoint.

        Args:
         - base_url: url where OpenAPI is
         - endpoint: enpoint to query
         - username: username from the Management UI user
         - password: password from the Management UI user
         - params: dictionary
    """

    headers = {
        'Accept': 'application/json',
    }

    # params = {
    #    **{
    #        #'ignoreOwnership': 'false',
    #        'api_key': api_key,
    #    },
    #    **params
    # }

    url = f'{base_url}/{endpoint}'

    response = requests.get(
        url,
        params=params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
        verify=True # Enable SSL verification
    )

    # DEBUG: Log the size of the response
    get_size_of_response(response)

    if response.status_code == 200:
        if "items" not in response.json():
            return response.json()
        else:
            # Print the API response data
            json_content = response.json()
            json_items = json_content["items"]
            end = json_content["nextCursor"] is None
            while not end:
                url = f'{base_url}/{endpoint}'
                params = {
                    # "api_key": api_key,
                    "next": json_content["nextCursor"]
                }
                response = requests.get(
                    url,
                    params=params,
                    auth=HTTPBasicAuth(username, password),
                    headers=headers,
                    verify=False
                )
                if response.status_code == 200:
                    r_content = response.json()
                    json_items.extend(r_content['items'])
                    json_content['items'] = json_items
                    json_content['nextCursor'] = r_content["nextCursor"]
                    end = r_content["nextCursor"] is None
                else:
                    raise Exception(f"Error retrieving data from {url}. Error: {response.text}")
            return json_content
    else:
        raise Exception(f"Error retrieving data from {url}. Error: {response.text}")


def get_requests_api_key(base_url, endpoint, api_key, params={}):
    """
        Make queries to OpenAPI endpoints based on a base_url, and api_key and different parameters.

        Args:
         - base_url: url where OpenAPI is
         - endpoint: enpoint to query
         - api_key: api key to for authentication
         - params: dictionary
    """

    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }

    params = {
        **{
            # 'ignoreOwnership': 'false',
            'api_key': api_key,
        },
        **params
    }

    url = f'{base_url}/v2.0/{endpoint}'

    response = requests.get(
        url,
        params=params,
        headers=headers,
        verify=True # Enable SSL verification
    )


    # DEBUG: Log the size of the response
    get_size_of_response(response)

    if response.status_code == 200:
        # Print the API response data
        json_content = response.json()
        json_items = json_content["items"]
        end = json_content["nextCursor"] is None
        while not end:
            url = f'{base_url}/new/v2.0/{endpoint}'
            params = {
                "api_key": api_key,
                "next": json_content["nextCursor"]
            }
            response = requests.get(
                url,
                params=params,
                headers=headers,
                verify=True # Enable SSL verification
            )
            r_content = response.json()
            json_items.extend(r_content['items'])
            json_content['items'] = json_items
            json_content['nextCursor'] = r_content["nextCursor"]
            end = r_content["nextCursor"] is None

        return json_content
    else:
        # Print the API error message
        raise Exception(f"Error retrieving data from {url}. Error: {response.text}")

def post_requests_api_key(base_url, endpoint, api_key, params={}):
    """
        Make queries to OpenAPI endpoints based on a base_url, and api_key and different parameters.

        Args:
         - base_url: url where OpenAPI is
         - endpoint: enpoint to query
         - api_key: api key to for authentication
         - params: dictionary

        Returns:
            json: json response from the request
    """

    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }

    params = {
        **{
            # 'ignoreOwnership': 'false',
            'api_key': api_key,
        },
        **params
    }

    url = f'{base_url}/v2.0/{endpoint}'

    response = requests.post(
        url,
        params=params,
        headers=headers,
        verify=True # Enable SSL verification
    )

    # DEBUG: Log the size of the response
    get_size_of_response(response)

    if response.status_code == 204:
        logging.info(f"Succesful post request: {response.status_code}")    
        return True
    else:
        # Print the API error message
        raise Exception(f"Error retrieving data from {url}. Error: {response.text}")
        return F
