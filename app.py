import os
import dash
import gspread
import dash_core_components as dcc
import dash_html_components as html
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']

credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": os.environ['SHEET_PRIVATE_KEY'],
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential,scope)

file = gspread.authorize(credentials)
sheet = file.open("Copy of Semester 2 Report Card (data) 2018/2019")
wks = sheet.worksheet("master")
col_1 = wks.col_values(1)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
	html.H2('YUAI International Islamic School - Progress Report Card'),
	dcc.Markdown('''
		Click this [LINK](https://docs.google.com/spreadsheets/d/1OUvxRYf2UnIqz_DHCu-SL3Q7b0ghADSEzC3wz5gVxj8/edit#gid=1819952105) to go the source Google Spreadsheet file.
		'''),
	dcc.Dropdown(
		id='dropdown',
		options=[{'label':i,'value':i} for i in col_1],
	),
	html.Div(id='display-value')
])

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

@app.callback(dash.dependencies.Output('display-value','children'), [dash.dependencies.Input('dropdown','value')])
def display_value(value):
	return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
	app.run_server(debug=True)
