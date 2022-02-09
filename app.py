from flask import Flask, render_template, jsonify, Response
from google.oauth2 import service_account
import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from configparser import ConfigParser


def get_config(key):
    #Read config.ini file
    config_object = ConfigParser()
    config_object.read("config.ini")

    apiconfig = config_object["APICONFIG"]
    return apiconfig[key]


def get_credentials():
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    GOOGLE_PRIVATE_KEY = get_config("GooglePrivateKey")
    GOOGLE_PRIVATE_KEY = GOOGLE_PRIVATE_KEY.replace('\\n', '\n')

    account_info = {
      "private_key": GOOGLE_PRIVATE_KEY,
      "client_email": get_config("GoogleEmail"),
      "token_uri": "https://accounts.google.com/o/oauth2/token",
    }

    credentials = service_account.Credentials.from_service_account_info(account_info, scopes=scopes)
    return credentials


def get_service():
    credentials = get_credentials()
    service = gspread.authorize(credentials)

    return service


def retrieve_data():
    gc = get_service()
    spreadsheet_id = get_config("SpreadsheetID")
    sheet_name = get_config("SheetName")
    range_name = get_config("RangeName")

    wb = gc.open_by_key(spreadsheet_id)
    ws = wb.worksheet(sheet_name)
    #ws = wb.values_get(range_name)
    df = get_as_dataframe(ws)

    return df


app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():
    data = retrieve_data()
    return render_template('index.html', data)


@app.route('/api/json', methods=['GET'])
def skills_and_proficiency():
    data = retrieve_data()

    # Columns
    # A - category
    # B - value
    # C - skill
    # D - proficiency

    # Where the magic happens...
    # Group by A, B (for parent/child structure)
    gb = (data.groupby(['category', 'value'])
            .apply(lambda x: x[['skill','proficiency']].to_dict('records'))
            .reset_index()
            .rename(columns={0:'skill-prof'})
            .to_json(orient='records'))

    # Can't really use jsonify here, as the df is already in JSON form
    #return jsonify(gb.to_json(orient = 'records'))
    return Response(gb, mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
