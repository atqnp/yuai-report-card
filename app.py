import time
import os
import dash
import dash_auth
import gspread
import fiscalyear as fy
import pandas as pd
import appfunction
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from oauth2client.service_account import ServiceAccountCredentials
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from apps import report

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

SHEET_PRIVATE_KEY = os.environ['SHEET_PRIVATE_KEY']
SHEET_PRIVATE_KEY = SHEET_PRIVATE_KEY.replace('\\n', '\n')

username = os.environ['BASIC_USER']
password = os.environ['BASIC_PASS']

VALID_USERNAME_PASSWORD_PAIRS = [[username,password]]

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
    global df, wks
    file = gspread.authorize(credentials)
    sheet = file.open("YUAI Report Card (data)")
    wks = sheet.worksheet("master")
    df = pd.DataFrame(wks.get_all_records())

def get_new_update(period=UPDATE_INTERVAL):
    while True:
        get_data()
        time.sleep(period)

#set fiscal year (1st apr)
fy.START_YEAR = 'same'
fy.START_MONTH = 4
fy.START_DATE = 1
year_now = fy.FiscalDate.today().fiscal_year

#List of students
select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,13))}
select_level = list(select_opt.keys())
select_sem = ['{}/{}/{}'.format(num,year_now,year_now+1) for num in range(1,4)]

#List of subject
subject = {'TJ':'Tajweed',
            'TF':'Tahfidz',
            'IS':'Islamic Studies',
            'AR':'Arabic',
            'EN':'English',
            'JP':'Japanese',
            'MT':'Mathematics',
            'SC':'Science',
            'PE':'Physical Education',
            'LS':'Living Skill',
            'IT':'Information and Communication in Technology',
            'SS':'Social Study',
            'GE':'Geography',
            'PM':'Public Moral',
            'BS':'Business Studies',
            'ART':'Art'}

#List of co and extra curricular
select_act = {'Co-Curricular' : list(range(1,6)), 'Extra-Curricular' : list(range(1,4))}
select_item = list(select_act.keys())

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Harmattan">
        {%metas%}
        <title>YUAI - Report Card</title>
        {%favicon%}
        {%css%}
    </head>
    <body class="A4">
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
        html.H4('YUAI International Islamic School - Progress Report Card', className="no-print", style={'text-align':'center'}),
        #header(),
        html.Div([html.Div([
                    dcc.Dropdown(
                        id='level-dropdown',
                        options=[{'label':i,'value':i} for i in select_level],
                        placeholder="Select level"
                        ),
                    dcc.Dropdown(
                        id='year-dropdown',
                        placeholder="Select year"
                        ),
                    dcc.Dropdown(
                        id='name-dropdown',
                        placeholder="Select name"
                        ),
                    dcc.Dropdown(
                        id='semester-dropdown',
                        options=[{'label':i,'value':i} for i in select_sem],
                        placeholder="Select semester"
                        ),
                    html.Hr(),
                    html.Div(id='display-value')
                    ], className="no-print sheet padding-10mm"),
                    html.Br(),       
        dcc.Tabs(id='tabs-id', value='tab-report',children=[
            dcc.Tab(label='Full Report', value='tab-report'),
            ])], className="no-print"),
        html.Div(id='tab-contents')
        ])

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(get_new_update)

app.layout = serve_layout

@app.callback(Output('tab-contents','children'),
            [Input('tabs-id','value')])
def render_content(tab):
    if tab == 'tab-report':
        return report.layout

#selection year
@app.callback(
    Output('year-dropdown','options'), 
    [Input('level-dropdown','value')])
def update_dropdown_level(level):
    return [{'label':i,'value':i} for i in select_opt[level]]

#selection name
@app.callback(
    Output('name-dropdown','options'), 
    [Input('level-dropdown','value'), 
    Input('year-dropdown','value')])
def update_dropdown_name(level,year):
    select_df = df[(df.Level.isin([level])) & (df.Year.isin([year]))]
    return [{'label':i,'value':i} for i in list(select_df['Name'])]

#selected person
@app.callback(
    Output('display-value','children'), 
    [Input('level-dropdown','value'),
    Input('year-dropdown','value'),
    Input('name-dropdown','value')])
def display_value(level,year,name):
    return html.P('You have selected:'), html.P('{} Year {} - {}'.format(level,year,name))

#full report page - student's data
@app.callback(
    Output('display-student-info','children'), 
    [Input('level-dropdown','value'),
    Input('year-dropdown','value'),
    Input('name-dropdown','value'),
    Input('semester-dropdown','value')])
def display_info(level,year,name,sem):
    return appfunction.student_info(name,level,year,sem)

#full report page - grades and marks table
@app.callback(
    Output('display-grade','children'),
    [Input('name-dropdown','value')])
def display_grade(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.grades_table(dfi)

#full report page - full academics table
@app.callback(
    Output('display-report','children'),
    [Input('name-dropdown','value')])
def display_fullgrade(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.academic_report(dfi)

#full report page - attendance table
@app.callback(
    Output('display-attendance','children'),
    [Input('name-dropdown','value'),
    Input('semester-dropdown','value')])
def display_attendance(name, sem):
    dfi = df[df.Name.isin([name])]
    if sem == '1/{}/{}'.format(year_now,year_now+1):
        period = 'APRIL - JULY {}'.format(year_now)
    elif sem == '2/{}/{}'.format(year_now,year_now+1):
        period = 'SEPTEMBER - DECEMBER {}'.format(year_now)
    elif sem == '3/{}/{}'.format(year_now,year_now+1):
        period = 'JANUARY - MARCH {}'.format(year_now+1)
    return appfunction.attendance(dfi,period)

#full report page - academic teacher's note table
@app.callback(
    Output('display-notes','children'),
    [Input('name-dropdown','value')])
def display_notes(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.notes_table(dfi)

#full report page - co-curricular grade table
@app.callback(
    Output('display-cc-grade','children'),
    [Input('name-dropdown','value')])
def display_grade_cc(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.co_table(dfi)

#full report page - extra-curricular grade table
@app.callback(
    Output('display-ex-grade','children'),
    [Input('name-dropdown','value')])
def display_grade_ex(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.extra_table(dfi)

#full report page - co-curricular teacher's note table
@app.callback(
    Output('display-cc-notes','children'),
    [Input('name-dropdown','value')])
def display_notes_cc(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.co_notes(dfi)

#full report page - extra-curricular teacher's note table
@app.callback(
    Output('display-ex-notes','children'),
    [Input('name-dropdown','value')])
def display_notes_ex(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.extra_notes(dfi)

#full report page - behaviour attitude table
@app.callback(
    Output('display-attitude','children'),
    [Input('name-dropdown','value')])
def display_attitude(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.attitude(dfi)

#full report page - teacher's comments
@app.callback(
    Output('display-comments','children'),
    [Input('name-dropdown','value')])
def display_comments(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.comments(dfi)

#full report page - grade table
@app.callback(
    Output('display-range','children'),
    [Input('name-dropdown','value')])
def display_table(name):
    return appfunction.grade_range()

#full report page - teacher
@app.callback(
    Output('display-teacher','children'),
    [Input('name-dropdown','value')])
def display_attitude(name):
    return html.Div([html.P('Homeroom Teacher:'),
        html.Br(), html.Br(),
        html.P('_________________')
        ])

#full report page - parent
@app.callback(
    Output('display-parents','children'),
    [Input('name-dropdown','value')])
def display_attitude(name):
    return html.Div([html.P('Parents:'),
        html.Br(), html.Br(),
        html.P('_________________'),
        html.Br(),
        html.P('Headmistress : Yetti Dalimi'),
        html.Br(), html.Br(),
        html.P('_________________')
        ])
    
if __name__ == '__main__':
    app.run_server(debug=True)
