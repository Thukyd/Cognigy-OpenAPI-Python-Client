
# Cognigy OpenAPI Client for Python

## Overview

The Client is designed to be the base for interactions with the Cognigy OpenAPI. It provides a simple interface to the OpenAPI endpoints, and handles authentication and pagination.
There are some example endpoints included. You can extend this by check the OpenAPI documentation `https://api-trial.cognigy.ai/openapi#` and adding the endpoints you need.

## Features

- **API Key Authentication:** Handles specialized API requests using an API key.
- **HTTP Basic Authentication:** Manages API requests through HTTP Basic Authentication.
- **Different Endpoints:** Provides access to various endpoints, including user management and audit event tracking.

## Modules

1. `openapi_client.py`: Responsible for authentication and pagination related to OpenAPI requests.
2. `endpoints_api_key.py`: Manages API requests via API Key Authentication.
3. `endpoints_managment_ui.py`: Handles API requests via HTTP Basic Authentication.

## Dependencies

- Python 3.x
- logging
- - tqdm (optional but useful for progress bars)

## Installation

Clone the repository and install the necessary dependencies:

```bash
git clone [repository-url]
cd [repository-directory]
pip install -r requirements.txt
```

## Usage

You can import the libaries to you own clients. You don't import the `openapi_client.py` directly but the sub-modules. This is how the structure looks like:

```bash

openapi_client.py
│
├── endpoints_managment_ui.py
│   └── main.py (if it uses Management UI functionalities)
│
└── endpoints_api_key.py
    └── main.py (if it uses API Key functionalities)

In the main.py script there is an example. You can run it by adding an endpoint url and a secret.json file.
```

```Python
   The main script is an example which shows how to integrate the helper functions into your own code.

    If you want to run the example, add a "secrets.json" file to the root directory of this project.
    The file should contain the following information:
    {
        "username": "ADD_YOUR_OWN_USERNAME_HERE",
        "password": "ADD_YOUR_OWN_PASSWORD_HERE"
    }
```

## Contributing

Contributions to this project are welcome. Please follow the standard fork-and-pull request workflow.
