"""
    Module to requests via API Key Authentication 

    Uses "cognigy_open_api.py" to handle authentication and pagination for OpenAPI requests. 

    This doesn't cover all possible request of Cognigy but it's fairly easy to add new ones. 
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

def get_user_by_id(base_url, api_key, user_id):
    response = openapi_client.get_requests_api_key(
            base_url,
            f"users/{user_id}",
            api_key, {}
        )
    return response

def delete_project_by_id(base_url, api_key, project_id):
    """
    Deletes a project by its project ID.

    Args:
        base_url (str): The base URL of the API.
        api_key (str): The API key for authentication.
        project_id (str): The ID of the project to be deleted.

    Returns:
        bool: True if the project was successfully deleted, False otherwise.
    
    Raises:
        Exception: If the deletion fails or the API returns an error.
    """

    # Define the endpoint for deleting a project by ID
    delete_project_endpoint = f"projects/{project_id}"

    # Make a DELETE request to delete the project
    project_deleted_bool = openapi_client.delete_requests_api_key(
        base_url=base_url,
        endpoint=delete_project_endpoint,
        api_key=api_key
    )

    # Return if the project was successfully deleted
    return project_deleted_bool