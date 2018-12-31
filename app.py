import os
import dash
import gspread
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']

SHEET_PRIVATE_KEY = os.environ['SHEET_PRIVATE_KEY']
SHEET_PRIVATE_KEY = SHEET_PRIVATE_KEY.replace('\\n', '\n')

credential = {
                "type": "service_account",
                "project_id": os.environ['SHEET_PROJECT_ID'],
                "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
                "private_key": SHEET_PRIVATE_KEY,
                "client_email": os.environ['SHEET_CLIENT_EMAIL'],
                "client_id": os.environ['SHEET_CLIENT_ID'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url":  os.environ['SHEET_CLIENT_X509_CERT_URL']
             }

credentials = ServiceAccountCredentials.from_json_keyfile_dict(credential,scope)

#DataFrame spreadsheet
file = gspread.authorize(credentials)
sheet = file.open("Copy of Semester 2 Report Card (data) 2018/2019")
wks = sheet.worksheet("master")
df = pd.DataFrame(wks.get_all_records())

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())
select_year = select_opt[select_level[0]]

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
	[
		html.H2('YUAI International Islamic School - Progress Report Card'),
		html.Div([
		dcc.Dropdown(
			id='level-dropdown',
			options=[{'label':i,'value':i} for i in select_level],
			placeholder="Select level",
			),
		],
		),
		html.Div([
		dcc.Dropdown(
			id='year-dropdown',
			placeholder="Select year"
			),
			],	
		),
		html.Div([
		dcc.Dropdown(
			id='name-dropdown',
			placeholder="Select name"
			),
			],	
		),
		html.Hr(),
		html.Div(id='display-value')
	]
)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

@app.callback(
	dash.dependencies.Output('year-dropdown','options'), 
	[dash.dependencies.Input('level-dropdown','value')])
def update_dropdown_level(level):
	return [{'label':i,'value':i} for i in select_opt[level]]

@app.callback(
	dash.dependencies.Output('name-dropdown','options'), 
	[dash.dependencies.Input('level-dropdown','value'),
	dash.dependencies.Input('year-dropdown','value')])
def update_dropdown_name(level,year):
	select_df = df[(df.Level.isin([level])) & (df.Year.isin([year]))]
	return [{'label':i,'value':i} for i in list(select_df['Name'])]

@app.callback(
	dash.dependencies.Output('display-value','children'), 
	[dash.dependencies.Input('level-dropdown','value'),
	dash.dependencies.Input('year-dropdown','value'),
	dash.dependencies.Input('name-dropdown','value')])
def display_value(s_level,s_year, s_name):
	return 'You have selected {} {} {}'.format(s_level,s_year, s_name)

if __name__ == '__main__':
	app.run_server(debug=True)
