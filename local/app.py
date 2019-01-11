import time
import os
import dash
import dash_table
import gspread
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from apps import report, submit1, submit2, submit3, submit4

scope = ['https://spreadsheets.google.com/feeds',
		 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('gspreadsheet-yuai-638e20a7f7b0.json',scope)

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
def grades_table(dataframe):
	return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['Component','Grade','Marks']])] +

        # Body
        [html.Tr(
        	[html.Td(grade.strip('_grade'))] +
        	[html.Td(dataframe[grade])] +
        	[html.Td(dataframe[marks])]
        	) for grade,marks in zip(sub_grade,sub_marks)
        ]
        )

def comments_table(dataframe):
	return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['Component','Competency and Accomplishment']])] +

        # Body
        [html.Tr(
        	[html.Td(sub.strip('_comments'))] +
        	[html.Td([html.P(value) for index, value in dataframe[sub].str.split('\n',expand=True).items()])]
        	) for sub in sub_com
        ]
        )
def serve_layout():
	return html.Div([
		html.H3('YUAI International Islamic School - Progress Report Card'),
		dcc.Tabs(id='tabs-id', value='tab-report',children=[
			dcc.Tab(label='Full Report', value='tab-report'),
			dcc.Tab(label='Submit Marks and Grade (Academics)', value='tab-submit1'),
			dcc.Tab(label='Submit Notes (Academics)', value='tab-submit2'),
			dcc.Tab(label='Submit Co-curricular', value='tab-submit3'),
			dcc.Tab(label='Submit Extra-curricular', value='tab-submit4'),
			]),
		html.Div(id='tab-contents')
		])

server = app.server
app.config.suppress_callback_exceptions = True
get_data()

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
def display_report(name):
	dfi = df[df.Name.isin([name])]
	return grades_table(dfi)

@app.callback(
	Output('display-comments','children'),
	[Input('name-dropdown','value')])
def display_report(name):
	dfi = df[df.Name.isin([name])]
	return comments_table(dfi)

# @app.callback(
# 	Output('display-subjects','children'),
# 	[InputInput('year-dropdown','value')])
# def display_subject(level,year):
# 	select_df = df[(df.Level.isin([level])) & (df.Year.isin([year]))]

if __name__ == '__main__':
	app.run_server(debug=True)
