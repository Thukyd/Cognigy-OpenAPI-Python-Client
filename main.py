"""
    The main script is an example which shows how to integrate the helper functions into your own code.

    If you want to run the example, add a "secrets.json" file to the root directory of this project.
    The file should contain the following information:
    {
        "username": "ADD_YOUR_OWN_USERNAME_HERE",
        "password": "ADD_YOUR_OWN_PASSWORD_HERE"
    }
"""


# Import helper function for Cognitive OpenAPI requests
import endpoints_managment_ui as via_mgmt_ui
import endpoints_api_key as via_api_key

# Import other modules
from tqdm import tqdm # progress bar

import logging

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
    # filename='example.log',  # Specify the log file
    # filemode='a'  # Use 'a' to append to the log file, 'w' to overwrite it
)

################################################################################################
# Functions

"""
    Add your own function which make use of the helper functions
"""


################################################################################################
# Execution

def main(base_url, username, password):
    # e.g use the management ui to query all admin users
    logging.info("Getting all Admin users")
    admin_user_id_list = via_mgmt_ui.get_admin_user_ids(base_url, username, password)

    """
        Add your own code here
    """

################################################################################################
# Run the script with configs

if __name__ == "__main__":
    # Configs
    API_URL = "ADD_YOUR_OWN_COGNIGY_API_URL_HERE"


    #### For Management UI Authentication
    # If you want to use the management UI to get the credentials, you can use the following code
    logging.info(f"Using {API_URL} as base URL")
    USERNAME, PASSWORD = via_mgmt_ui.load_management_ui_credentials("secrets.json")

    #### For API Key Authentication ####
    """
        Add your own code here. Change the main function so it passes your API key to the helper functions
    """

    # Main functionality
    main(API_URL, USERNAME, PASSWORD)