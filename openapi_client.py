"""    
    Cognigy OpenAPI Authentication and Pagination Module

    This module simplifies interactions with OpenAPI endpoints by handling:
    1. Authentication: Supports both Basic Auth (Management UI) and API Key (Cognigy AI)
    2. Pagination: Automatically manages paginated responses
    3. HTTP Methods: Includes functions for GET, POST, PATCH, and DELETE requests
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
    with open(path_to_secrets_json) as f:
        json_content = json.load(f)
    return json_content["username"], json_content["password"]

def handle_pagination(response, base_url, endpoint, auth=None, headers=None, params=None):
    """
    Helper function to handle pagination for API requests.

    Args:
        response (requests.Response): The initial API response.
        base_url (str): The base URL of the API.
        endpoint (str): The API endpoint.
        auth (HTTPBasicAuth, optional): Authentication for the request.
        headers (dict, optional): Headers for the request.
        params (dict, optional): Parameters for the request.

    Returns:
        dict: The complete JSON response with all paginated items.
    """
    if response.status_code != 200:
        raise Exception(f"Error retrieving data from {base_url}/{endpoint}. Error: {response.text}")

    json_content = response.json()
    if "items" not in json_content:
        return json_content

    json_items = json_content["items"]
    while json_content.get("nextCursor"):
        params = params or {}
        params["next"] = json_content["nextCursor"]
        url = f'{base_url}/{endpoint}'
        
        response = requests.get(
            url,
            params=params,
            auth=auth,
            headers=headers,
            verify=True
        )
        
        if response.status_code != 200:
            raise Exception(f"Error retrieving data from {url}. Error: {response.text}")
        
        r_content = response.json()
        json_items.extend(r_content['items'])
        json_content['items'] = json_items
        json_content['nextCursor'] = r_content.get("nextCursor")

    return json_content

def get_request_basic_auth(base_url, endpoint, username, password, params={}):
    """
    Method: GET
    Component: Management UI
    See: https://api.your-url/openapi

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

    url = f'{base_url}/{endpoint}'
    auth = HTTPBasicAuth(username, password)

    response = requests.get(
        url,
        params=params,
        auth=auth,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    return handle_pagination(response, base_url, endpoint, auth, headers, params)

def patch_request_basic_auth(base_url, endpoint, username, password, json_payload, params={}):
    """
    Method: PATCH
    Component: Management UI
    See: https://api.your-url/openapi
    

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

    url = f'{base_url}/{endpoint}'
    auth = HTTPBasicAuth(username, password)

    response = requests.patch(
        url,
        json=json_payload,
        params=params,
        auth=auth,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    return handle_pagination(response, base_url, endpoint, auth, headers, params)

def get_requests_api_key(base_url, endpoint, api_key, params={}):
    """
    Method: GET
    Component: Cognigy AI
    See: https://api.your-url/openapi
    

    Args:
    - base_url: url where OpenAPI is
    - endpoint: endpoint to query
    - api_key: the API key for authentication
    - params: optional parameters for the request   
    """
    headers = {
        'Accept': 'application/json',
        'X-API-Key': api_key
    }

    url = f'{base_url}/v2.0/{endpoint}'
    response = requests.get(url, params=params, headers=headers, verify=True)
    get_size_of_response(response)

    return handle_pagination(response, f'{base_url}/v2.0', endpoint, headers=headers, params=params)

def post_requests_api_key(base_url, endpoint, api_key, params={}):
    """
    Method: POST
    Component: Cognigy AI
    See: https://api.your-url/openapi

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
        verify=True
    )

    get_size_of_response(response)

    if response.status_code == 204:
        logging.info(f"Successful post request: {response.status_code}")    
        return True
    else:
        raise Exception(f"Error retrieving data from {url}. Error: {response.text}")

def delete_requests_api_key(base_url, endpoint, api_key, params={}):
    """
    Method: DELETE
    Component: Cognigy AI
    See: https://api.your-url/openapi

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

    params = {
        'ignoreOwnership': 'true',
        **params
    }

    url = f'{base_url}/v2.0/{endpoint}'

    try:
        response = requests.delete(
            url,
            params=params,
            headers=headers,
            verify=True
        )
        
        get_size_of_response(response)

        if response.status_code in [200, 204]:
            logging.info(f"Successful delete request: {response.status_code}")
            return True
        
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during API request to {url}: {e}")
        raise Exception(f"Error retrieving data from {url}. Error: {e}")

def post_request_basic_auth(base_url, endpoint, username, password, json_payload, params={}):
    """
    Method: POST
    Component: Management UI
    See: https://api.your-url/openapi

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

    url = f'{base_url}/{endpoint}'
    auth = HTTPBasicAuth(username, password)

    response = requests.post(
        url,
        json=json_payload,
        params=params,
        auth=auth,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    if response.status_code in [200, 201, 204]:
        logging.info(f"Successful post request: {response.status_code}")
        return response.json() if response.content else True
    else:
        raise Exception(f"Error posting data to {url}. Error: {response.text}")

def put_request_basic_auth(base_url, endpoint, username, password, json_payload, params={}):
    """
    Method: PUT
    Component: Management UI
    See: https://api.your-url/openapi

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

    url = f'{base_url}/{endpoint}'
    auth = HTTPBasicAuth(username, password)

    response = requests.put(
        url,
        json=json_payload,
        params=params,
        auth=auth,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    return handle_pagination(response, base_url, endpoint, auth, headers, params)

def put_requests_api_key(base_url, endpoint, api_key, json_payload, params={}):
    """
    Method: PUT
    Component: Cognigy AI
    See: https://api.your-url/openapi

    Args:
    - base_url: url where OpenAPI is
    - endpoint: endpoint to query
    - api_key: the API key for authentication
    - json_payload: dictionary containing the JSON data to be sent in the request body
    - params: optional parameters for the request   
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }

    params = {
        'ignoreOwnership': 'true',
        **params
    }

    url = f'{base_url}/v2.0/{endpoint}'

    response = requests.put(
        url,
        json=json_payload,
        params=params,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    return handle_pagination(response, f'{base_url}/v2.0', endpoint, headers=headers, params=params)

def patch_requests_api_key(base_url, endpoint, api_key, json_payload, params={}):
    """
    Method: PATCH
    Component: Cognigy AI
    See: https://api.your-url/openapi

    Args:
    - base_url: url where OpenAPI is
    - endpoint: endpoint to query
    - api_key: the API key for authentication
    - json_payload: dictionary containing the JSON data to be sent in the request body
    - params: optional parameters for the request   
    """
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-API-Key': api_key
    }

    params = {
        'ignoreOwnership': 'true',
        **params
    }

    url = f'{base_url}/v2.0/{endpoint}'

    response = requests.patch(
        url,
        json=json_payload,
        params=params,
        headers=headers,
        verify=True
    )

    get_size_of_response(response)
    return handle_pagination(response, f'{base_url}/v2.0', endpoint, headers=headers, params=params)

def delete_request_basic_auth(base_url, endpoint, username, password, params={}):
    """
    Method: DELETE
    Component: Management UI
    See: https://api.your-url/openapi

    Args:
    - base_url: url where OpenAPI is
    - endpoint: endpoint to query
    - username: username from the Management UI user
    - password: password from the Management UI user
    - params: dictionary of query parameters (optional)
    """
    headers = {
        'Accept': 'application/json',
    }

    url = f'{base_url}/{endpoint}'
    auth = HTTPBasicAuth(username, password)

    try:
        response = requests.delete(
            url,
            params=params,
            auth=auth,
            headers=headers,
            verify=True
        )
        
        get_size_of_response(response)

        if response.status_code in [200, 204]:
            logging.info(f"Successful delete request: {response.status_code}")
            return True
        
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during DELETE request to {url}: {e}")
        raise Exception(f"Error deleting data from {url}. Error: {e}")