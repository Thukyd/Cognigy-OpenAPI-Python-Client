import main as main_module
import logging  
from datetime import datetime, timedelta

"""
    Module in usage
"""
# Module to handle  authentication and pagination for OpenAPI requests. (https://api.your-url/openapi)
import openapi_client
# Module to make request which require an API-Key
import endpoints_api_key as via_api_key 
# Module to make request which require Management UI credentials 
import endpoints_managment_ui as via_mgmt_ui


# Configure the logging module
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
    #filename='example.log',  # Specify the log file
    #filemode='a'  # Use 'a' to append to the log file, 'w' to overwrite it
)

################################################################################################
# Global Variables
BASE_URL = "ADD_YOUR_OWN_COGNIGY_API_URL_HERE"
USERNAME, PASSWORD = openapi_client.load_management_ui_credentials("secrets.json")

################################################################################################
# Unit Test | Get the list of organizations
"""
list = via_mgmt_ui.get_organisations(BASE_URL, USERNAME, PASSWORD)
logging.info(f"list: {list}")
"""

################################################################################################
# Unit Test | ...
"""
    Add more unit tests here

"""