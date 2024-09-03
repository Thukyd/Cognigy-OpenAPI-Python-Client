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


def patch_request_basic_auth(base_url, endpoint, username, password, json_payload, params={}):
    """
    Helper Functionality for management ui queries Cogniyion OpenAPI (https://api.your-url/openapi)
    Make PATCH queries to OpenAPI endpoints based on a base_url, username, password, and JSON payload.
    It handles a dict of parameters to add to the query.

    Args:
    - base_url: url where OpenAPI is
    - endpoint: endpoint to query
    - username: username from the Management UI user
    - password: password from the Management UI user
    - json_payload: dictionary containing the JSON data to be sent in the request body
    - params: dictionary of query parameters (optional)
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # params = {
    # **{
    # #'ignoreOwnership': 'false',
    # 'api_key': api_key,
    # },
    # **params
    # }

    url = f'{base_url}/{endpoint}'
    response = requests.patch(
        url,
        json=json_payload,
        params=params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
        verify=True  # Enable SSL verification
    )

    # DEBUG: Log the size of the response
    get_size_of_response(response)

    if response.status_code == 200:
        json_content = response.json()
        if "items" not in json_content:
            return json_content
        else:
            # Handle paginated responses if applicable
            json_items = json_content["items"]
            end = json_content.get("nextCursor") is None

            while not end:
                url = f'{base_url}/{endpoint}'
                params = {
                    # "api_key": api_key,
                    "next": json_content["nextCursor"]
                }
                response = requests.patch(
                    url,
                    json=json_payload,
                    params=params,
                    auth=HTTPBasicAuth(username, password),
                    headers=headers,
                    verify=False
                )

                if response.status_code == 200:
                    r_content = response.json()
                    json_items.extend(r_content['items'])
                    json_content['items'] = json_items
                    json_content['nextCursor'] = r_content.get("nextCursor")
                    end = r_content.get("nextCursor") is None
                else:
                    raise Exception(f"Error retrieving data from {url}. Error: {response.text}")

            return json_content
    else:
        raise Exception(f"Error retrieving data from {url}. Error: {response.text}")

def get_requests_api_key(base_url, endpoint, api_key, params={}):
    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }

    url = f'{base_url}/v2.0/{endpoint}'
    response = requests.get(url, params=params, headers=headers, verify=True)
    get_size_of_response(response)

    if response.status_code == 200:
        json_content = response.json()
        logging.debug(f"Full response: {json_content}")
        if "items" in json_content:
            json_items = json_content["items"]
            while json_content.get("nextCursor"):
                params = {"api_key": api_key, "next": json_content["nextCursor"]}
                response = requests.get(url, params=params, headers=headers, verify=True)
                if response.status_code == 200:
                    r_content = response.json()
                    json_items.extend(r_content['items'])
                    json_content['items'] = json_items
                    json_content['nextCursor'] = r_content["nextCursor"]
                else:
                    raise Exception(f"Error retrieving data from {url}. Error: {response.text}")
            return json_content
        else:
            return json_content
    else:
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
            'ignoreOwnership': 'true',
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
        return False

def delete_requests_api_key(base_url, endpoint, api_key, params={}):
    """
    Make DELETE requests to an API endpoint using a base URL, endpoint, API key, and parameters.

    Args:
        base_url (str): The base URL where the API is hosted.
        endpoint (str): The specific API endpoint to query.
        api_key (str): The API key used for authentication.
        params (dict): A dictionary of additional parameters to include in the request.

    Returns:
        dict: JSON response from the request, if applicable.
    
    Raises:
        Exception: If the request fails or the API returns an error.
    """

    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }

    # Combine provided parameters with default ones
    params = {
        'ignoreOwnership': 'true',
        **params
    }

    url = f'{base_url}/{endpoint}'

    try:
        response = requests.delete(
            url,
            params=params,  # DELETE requests often send parameters in the URL
            headers=headers,
            verify=True  # SSL verification is enabled
        )
        
        # Log the size of the response for debugging
        get_size_of_response(response)

        # Check for successful status code
        if response.status_code in [200, 204]:
            logging.info(f"Successful delete request: {response.status_code}")
            return True
        
        # Attempt to return JSON response
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API request to {url}: {e}")
        raise Exception(f"Error retrieving data from {url}. Error: {e}")
    

