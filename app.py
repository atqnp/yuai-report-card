import time
import os
import dash
import dash_table
import gspread
import pandas as pd
import appfunction
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apps import report, submit1, submit2, submit3, submit4, submit5

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

UPDATE_INTERVAL = 30

#DataFrame spreadsheet
def get_data():
	#updates the data
	global df
	file = gspread.authorize(credentials)
	sheet = file.open("Copy of Semester 2 Report Card (data) 2018/2019")
	wks = sheet.worksheet("master")
	df = pd.DataFrame(wks.get_all_records())


def get_new_update(period=UPDATE_INTERVAL):
	while True:
		get_data()
		time.sleep(period)

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())
select_year = select_opt[select_level[0]]

#List of subject
subject = ['TJ','TF','IS','AR','EN','JP','MT','SC','PE','LS','IT','SS','GE','ART']
sub_grade = ['{}_grade'.format(sub) for sub in subject]
sub_marks = ['{}_marks'.format(sub) for sub in subject]
sub_com = ['{}_comments'.format(sub) for sub in subject]

app = dash.Dash(__name__)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>YUAI - Report Card</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
        </footer>
    </body>
</html>
'''

app.config.suppress_callback_exceptions = True
server = app.server
get_data()

def serve_layout():
	return html.Div([
		html.H3('YUAI International Islamic School - Progress Report Card'),
		dcc.Tabs(id='tabs-id', value='tab-report',children=[
			dcc.Tab(label='Full Report', value='tab-report'),
			dcc.Tab(label='Submit Marks and Grade (Academics)', value='tab-submit1'),
			dcc.Tab(label='Submit Notes (Academics)', value='tab-submit2'),
			dcc.Tab(label='Submit Co-curricular and Extra-curricular (Grade)', value='tab-submit3'),
			dcc.Tab(label='Submit Co-curricular and Extra-curricular (Comments)', value='tab-submit4'),
			dcc.Tab(label='Submit Behaviour/Affectiveness', value='tab-submit5'),
			]),
		html.Div(id='tab-contents')
		])

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_update)

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = serve_layout

@app.callback(Output('tab-contents','children'),
			[Input('tabs-id','value')])
def render_content(tab):
	if tab == 'tab-report':
		return report.layout
	elif tab == 'tab-submit1':
		return submit1.layout
	elif tab == 'tab-submit2':
		return submit2.layout
	elif tab == 'tab-submit3':
		return submit3.layout
	elif tab == 'tab-submit4':
		return submit4.layout
	elif tab == 'tab-submit5':
		return submit5.layout

@app.callback(
	Output('year-dropdown','options'), 
	[Input('level-dropdown','value')])
def update_dropdown_level(level):
	return [{'label':i,'value':i} for i in select_opt[level]]

@app.callback(
	Output('name-dropdown','options'), 
	[Input('level-dropdown','value'), 
	Input('year-dropdown','value')])
def update_dropdown_name(level,year):
	select_df = df[(df.Level.isin([level])) & (df.Year.isin([year]))]
	return [{'label':i,'value':i} for i in list(select_df['Name'])]

@app.callback(
	Output('display-value','children'), 
	[Input('level-dropdown','value'),
	Input('year-dropdown','value'),
	Input('name-dropdown','value')])
def display_value(s_level,s_year, s_name):
	return html.P('You have selected:'), html.P('{} Year {} - {}'.format(s_level,s_year, s_name))

@app.callback(
	Output('display-grade','children'),
	[Input('name-dropdown','value')])
def display_grade(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.grades_table(dfi)

@app.callback(
	Output('display-comments','children'),
	[Input('name-dropdown','value')])
def display_comments(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.comments_table(dfi)

@app.callback(
	Output('display-cc-grade','children'),
	[Input('name-dropdown','value')])
def display_grade_cc(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.co_table(dfi)

@app.callback(
	Output('display-ex-grade','children'),
	[Input('name-dropdown','value')])
def display_grade_ex(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.extra_table(dfi)

@app.callback(
	Output('display-cc-comments','children'),
	[Input('name-dropdown','value')])
def display_comments_cc(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.co_comments(dfi)

@app.callback(
	Output('display-ex-comments','children'),
	[Input('name-dropdown','value')])
def display_comments_ex(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.extra_comments(dfi)

@app.callback(
	Output('display-attitude','children'),
	[Input('name-dropdown','value')])
def display_attitude(name):
	dfi = df[df.Name.isin([name])]
	return appfunction.attitude(dfi)

if __name__ == '__main__':
	app.run_server(debug=True)
