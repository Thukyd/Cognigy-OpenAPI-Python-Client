###########################################################################################
### API requests via HTTP Basic Authentication (https://api.your-url/openapi)    ###
"""
    Module to make Mangement UI requests to the Cognitive OpenAPI (https://api.your-url/openapi).

    Uses "cognigy_open_api.py" to handle authentication and pagination for OpenAPI requests. 

    Contains following endpoints:
    - get_user_list: retrieves a list of all users.
    - get_user_details: retrieves details of a specific user.
    - get_admin_user_ids: retrieves a list of user details for users with the 'admin' role of all organisations.
    - get_organisations: retrieves a list of all organisations.
    - create_temporary_api_key: creates a new ApiKey with admin permissions for a specific organisation.

"""

import warnings 
warnings.filterwarnings('ignore')

import requests
from requests.auth import HTTPBasicAuth

from tqdm import tqdm # progress bar
import json

import openapi_client # Import helper function for Cognitive OpenAPI requests
import logging


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


def get_user_list(url, username, password):
    """
    get-/management/v2.0/users
    
    Retrieves a list of all users.

    Args:
        url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        list: A list of dictionaries containing details of all users.
              Each dictionary represents a user's details.

    Example:
        users = get_users("https://api.example.com", "my_username", "my_password")
        for user in users:
            print("User Details:", user)
    """
    # Define the endpoint for retrieving the list of users
    user_list_endpoint = "new/management/v2.0/users"

    # Make a query to get the list of users
    user_list = openapi_client.get_request_basic_auth(
        base_url=url,
        endpoint=user_list_endpoint,
        username=username,
        password=password
    )

    # Return the list of details for all users
    return user_list

def get_user_details(url, username, password, user_id):
    """
    get-/management/v2.0/users/-userId-

    Get full data of a User from the system.

    Args:
        url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.
        user_id (str): The ID of the user for which to retrieve the details.

    Returns:
        dict: A dictionary containing details of the user if the request is successful, else None.

    Raises:
        Exception: Raises an exception if the HTTP request fails.

    Example:
        user_details = get_user_details("https://api.example.com", "my_username", "my_password", "user123")
        if user_details:
            print("User Details:", user_details)
        else:
            print("Failed to retrieve user details.")
    """
    # Define the endpoint for retrieving details of a specific user
    user_details_endpoint = f"new/management/v2.0/users/{user_id}"

    # Make a query to get details of the specific user
    user_details = openapi_client.get_request_basic_auth(
        base_url=url,
        endpoint=user_details_endpoint,
        username=username,
        password=password
    )

    # Return the details of the user
    return user_details

def get_admin_user_ids(url, username, password):
    """
    Retrieves a list of user details for users with the 'admin' role of all organisations.

    Args:
        url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        list: A list of dictionaries containing details of users with the 'admin' role.
              Each dictionary represents a user's details.

    Example:
        admin_users = get_admin_user_ids("https://api.example.com", "my_username", "my_password")
        for user in admin_users:
            print("Admin User Details:", user)
    """

    # Make a query to get the list of users
    user_list = get_user_list(url, username, password)

    # Initialize an empty list to store details of admin users
    admin_user_ids = []

    # Iterate through each user in the user list
    for user in tqdm(user_list['items']):
        # Define the endpoint for retrieving details of a specific user
        user_details = get_user_details(url, username, password, user["_id"])

        # Check if the user has the 'admin' role
        if "admin" in user_details["roles"]:
            # Add the details of the admin user to the list
            admin_user_ids.append(user_details)

    # Return the list of details for users with the 'admin' role
    return admin_user_ids

def get_organisations(url, username, password):
    """
    get-/management/v2.0/organisations

    Get organisations. By defualt it only queries the first 25 organisations but the get_request_basic_auth function goes through all results.

    Args:
        url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        list: A list of dictionaries containing details of all organizations.
              Each dictionary represents an organization's details.

    Example:
        organisations = get_organisations("https://api.example.com", "my_username", "my_password")
        for org in organisations:
            print("Organization Details:", org)
    """
    # Define the endpoint for retrieving the list of organizations
    organisation_list_endpoint = "new/management/v2.0/organisations"

    # Make a query to get the list of organizations
    organisation_list = openapi_client.get_request_basic_auth(
        base_url=url,
        endpoint=organisation_list_endpoint,
        username=username,
        password=password
    )

    # Return the list of details for all organizations
    return organisation_list

def create_temporary_api_key(base_url, username, password, organisation_id):
    """
    /management/v2.0/organisations/-organisationId-/apikeys
    
    Creates a new ApiKey with admin permissions for a specific organisation. 
    The ApiKey is valid for 15 minutes. This feature needs to be enabled server-side by setting the FEATURE_USE_SUPERAPIKEY_API to "true".

    Args:
        base_url (str): The base URL of the API.
        username (str): The username for authentication.
        password (str): The password for authentication.
        organisation_id (str): The ID of the organization for which to retrieve the API key.

    Returns:
        dict: A dictionary containing the API key information if the request is successful, else None.

    Raises:
        Exception: Raises an exception if the HTTP request fails.

    Example:
        api_key = get_api_key("https://api.example.com", "my_username", "my_password", "org123")
        if api_key:
            print("API Key:", api_key)
        else:
            print("Failed to retrieve API key.")
    """
    # Construct the URL for the API key request
    url = f"{base_url}/new/management/v2.0/organisations/{organisation_id}/apikeys"

    # Define headers for the HTTP request
    headers = {
        "Accept": "application/json",
    }

    # Make a POST request to the API to retrieve the API key
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, password))

    # Check if the request was successful (status code 2xx)
    if response.ok:
        logging.debug(f"Retrieved API Key for Organization ID: {organisation_id}")
        logging.debug(f"API Key Response: {response.json()}")
        # Return the API key information in JSON format
        return response.json()
    else:
        # Raise an exception if the HTTP request fails
        response.raise_for_status()


