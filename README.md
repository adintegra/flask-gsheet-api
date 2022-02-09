# Flask gSheet API

A simple project demonstrating how to build a JSON API endpoint using gSheet and Flask. I Recommend removing all blank rows and columns from the gSheet for clean output when calling the API.

Main inspiration taken from: https://github.com/jessamynsmith/flask-google-sheets


## Setup

git clone this repo, e.g.:

    git clone git@ssh.code.roche.com:pdex-oi-group/applications/flask-gsheet-api.git

Create a virtualenv using Python 3 and install dependencies. I recommend getting python3 using a package manager (homebrew on OSX), then installing [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation) to that python. NOTE! You must change 'path/to/python3'
to be the actual path to python3 on your system.

    mkvirtualenv flask-google-sheets --python=/path/to/python3
    pip install -r requirements.txt


## Set up Google Sheets

1. Open https://console.developers.google.com/iam-admin/serviceaccounts

1. If you already have a Google API project, select it. Otherwise, create one.

1. Click "CREATE SERVICE ACCOUNT"

1. Enter a Service account name. Set Role to Owner. Ensure that "Furnish a new private key" is checked, and that Key type "JSON" is selected. Click "CREATE".

1. Open the automatically downloaded JSON credentials file. You will use the values to set the following variables in your config.ini file in the [APICONFIG] section:

    ```
    GooglePrivateKey = <private_key_from_credentials_json>
    GoogleEmail = <client_email_from_credentials_json>
    ```

1. Set environment variables for the Google Sheet you want to retrieve data from:

    ```
    SpreadsheetID = <spreadsheet_id_from_google_sheets>
    RangeName = <sheetname>!<range>  # e.g. 'Dogs!A1:C'
    SheetName = <sheetname>
    ```

1. Ensure that your API Project has the Google Sheets API enabled. You can go to https://console.developers.google.com/apis/dashboard to select the project, then click "ENABLE APIS AND SERVICES" and look for sheets.

1. Log into Google Sheets and share your sheet with the service account user, as specified in client_email in the JSON credentials file.

## Run server

Ensure you rename config.ini.example to config.ini. Run using flask:

```
env.bat
flask run
```
