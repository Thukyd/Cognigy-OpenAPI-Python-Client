###########################################################################################
### B) API requests via API Key Authentication (https://api.eu.prod.cai.allianz.net/new) ###

"""
    Module to make APIrequests (https://api.eu.prod.cai.allianz.net/openapi)

    Uses "cognigy_open_api.py" to handle authentication and pagination for OpenAPI requests. 

    Contains following endpoints: 
    - get_audit_events: retrieves a list of all audit events.
    - post_deprecate_password: deprecates the password of a user.

"""

import warnings 
warnings.filterwarnings('ignore')

from tqdm import tqdm # progress bar


import openapi_client # Import helper function for Cognitive OpenAPI requests


def get_audit_events(base_url, api_key, params=None):
    """
    get-/management/v2.0/audit/events

    Retrieves a list of all audit events.

    Args:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        params (dict, optional): A dictionary containing parameters to add to the query. 
                                 Defaults to None.

    Returns:
        list: A list of dictionaries containing details of all audit events.
              Each dictionary represents an audit event's details.

    """
    # Define the endpoint for retrieving the list of audit events
    audit_events_endpoint = "auditevents"

    if params is None:
        params = {}

    # Make a query to get the list of audit events
    audit_events = openapi_client.get_requests_api_key(
        base_url=base_url,
        endpoint=audit_events_endpoint,
        api_key=api_key,
        params=params
    )


    # Return the list of details for all audit events
    return audit_events



def post_deprecate_password(base_url, api_key, user_id):
    """
    post-/management/v2.0/users/-userId-/deprecatePassword

    Deprecates the password of a user.

    Args:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        user_id (str): The ID of the user whose password should be deprecated.

    Returns:
        dict: A dictionary containing details of the user whose password was deprecated.
              The dictionary represents the user's details.

    """
    # Define the endpoint for deprecating the password of a user
    deprecate_password_endpoint = f"users/deprecatepassword"

    # Make a query to deprecate the password of a user
    password_deprecated_bool = openapi_client.post_requests_api_key(
        base_url=base_url,
        endpoint=deprecate_password_endpoint,
        api_key=api_key,
        params={"userId": user_id}
    )

    # Return if password was deprecated
    return password_deprecated_bool