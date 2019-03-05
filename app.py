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
from apps import report, submit1, submit2, submit3, submit4, submit5, submit6

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
    sheet = file.open("Copy of Semester 2 Report Card (data) 2018/2019")
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
select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
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
            'ART':'Art'}

sub_grade = ['{}_grade'.format(sub) for sub in subject.keys()]
sub_marks = ['{}_marks'.format(sub) for sub in subject.keys()]
sub_com = ['{}_comments'.format(sub) for sub in subject.keys()]

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
            dcc.Tab(label='Submit Marks and Grade (Academics)', value='tab-submit1'),
            dcc.Tab(label='Submit Notes (Academics)', value='tab-submit2'),
            dcc.Tab(label='Submit Co-curricular and Extra-curricular (Grade)', value='tab-submit3'),
            dcc.Tab(label='Submit Co-curricular and Extra-curricular (Comments)', value='tab-submit4'),
            dcc.Tab(label='Submit Behaviour or Affectiveness', value='tab-submit5'),
            dcc.Tab(label='Submit or Update Students Info', value='tab-submit5'),
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
    elif tab == 'tab-submit6':
        return submit6.layout

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
    return html.Div([html.P('Name : {}'.format(name)),
        html.Br(), html.P('Level : {}'.format(level)),
        html.Br(), html.P('Year : {}'.format(year)),
        html.Br(), html.P('Semester : {}'.format(sem)),
        ])

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

#full report page - academic teacher's note table
@app.callback(
    Output('display-comments','children'),
    [Input('name-dropdown','value')])
def display_comments(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.comments_table(dfi)

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
    Output('display-cc-comments','children'),
    [Input('name-dropdown','value')])
def display_comments_cc(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.co_comments(dfi)

#full report page - extra-curricular teacher's note table
@app.callback(
    Output('display-ex-comments','children'),
    [Input('name-dropdown','value')])
def display_comments_ex(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.extra_comments(dfi)

#full report page - behaviour attitude table
@app.callback(
    Output('display-attitude','children'),
    [Input('name-dropdown','value')])
def display_attitude(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.attitude(dfi)

#submit1 - selected subject for submitting (marks table output)
@app.callback(
    Output('submit-subject-marks','children'),
    [Input('subject-dropdown','value'),
    Input('name-dropdown','value')])
def marks_submit_table(subcode, name):
    dfi = df[df.Name.isin([name])]
    grade = '{}_grade'.format(subcode)
    marks = '{}_marks'.format(subcode)
    return appfunction.submit_sub_marks(dfi,subcode,grade,marks)

#submit1 - update cell (marks)
@app.callback(
    Output('container-marks','children'),
    [Input('submit-marks','n_clicks'), 
	 Input('submit-marks','n_submit'),
    Input('name-dropdown','value'),
    Input('subject-dropdown','value')],
    [State('input-marks','value')])
def submit_marks(clicks, submit, name, subcode, value):
    works = appfunction.access_wsheet('marks')
    sub_row = works.find(name).row
    sub_col = works.find((subject.get(subcode)).upper()).col
    works.update_cell(sub_row,sub_col,value)

#submit2 - selected subject for submitting (comments table output)
@app.callback(
    Output('submit-subject-comments','children'),
    [Input('subject-dropdown','value'),
    Input('name-dropdown','value')])
def comments_submit_table(subcode,name):
    dfi = df[df.Name.isin([name])]
    comments = '{}_comments'.format(subcode)
    return appfunction.submit_sub_comments(dfi,subcode,comments)

#submit2 - update cell (notes/comments)
@app.callback(
    Output('container-comments','children'),
    [Input('submit-comments','n_clicks'), 
	Input('submit-comments','n_submit'),
    Input('name-dropdown','value'),
    Input('subject-dropdown','value')],
    [State('input-comments','value')])
def submit_comments(clicks, submit, name, subcode, value):
    works = appfunction.access_wsheet('comments')
    sub_row = works.find(name).row
    sub_col = works.find((subject.get(subcode)).upper()).col
    works.update_cell(sub_row,sub_col,value)

#submit3 and 4 - selection of items for submitting (activity level)
@app.callback(
    Output('placeholder-dropdown','options'), 
    [Input('activity-dropdown','value')])
def update_dropdown_activity(activity):
    return [{'label':i,'value':i} for i in select_act[activity]]

#submit3 - selected item for submitting (grades table output)
@app.callback(
    Output('submit-actgrades','children'),
    [Input('activity-dropdown','value'),
    Input('placeholder-dropdown','value'),
    Input('name-dropdown','value')])
def act_grades_submit_table(act, pholder, name):  
    dfi = df[df.Name.isin([name])] 
    if act == 'Co-Curricular':
        return appfunction.submit_act_grades(dfi,pholder,items='CC{}'.format(pholder))
    elif act == 'Extra-Curricular':
        return appfunction.submit_act_grades(dfi,pholder,items='extraCC{}'.format(pholder))

#submit3 - update cell (activity grades)
@app.callback(
    Output('container-act-grades','children'),
    [Input('submit-actgrades','n_clicks'), 
	Input('submit-actgrades','n_submit'),
    Input('name-dropdown','value'), 
    Input('activity-dropdown','value'),
    Input('placeholder-dropdown','value')],
    [State('input-act-component','value'), State('input-act-attendance','value'), State('input-act-participation','value'),
    State('input-act-effort','value'), State('input-act-attitude','value'), State('input-act-grade','value'),])
def submit_coextra_grades(clicks, submit, name, act, pholder, v_comp, v_attend, v_part, v_eff, v_att, v_grade):
    if act == 'Co-Curricular':
        works = appfunction.access_wsheet('cocurricular')
    elif act == 'Extra-Curricular':
        works = appfunction.access_wsheet('extra')
    sub_row = works.find(name).row
    works.update_cell(sub_row, works.find('{} {} (Activity)'.format(act,pholder)).col, v_comp)
    works.update_cell(sub_row, works.find('{} {} (Attendance)'.format(act,pholder)).col, v_attend)
    works.update_cell(sub_row, works.find('{} {} (Participation)'.format(act,pholder)).col, v_part)
    works.update_cell(sub_row, works.find('{} {} (Effort)'.format(act,pholder)).col, v_eff)
    works.update_cell(sub_row, works.find('{} {} (Attitude)'.format(act,pholder)).col, v_att)
    works.update_cell(sub_row, works.find('{} {} (Grade)'.format(act,pholder)).col, v_grade)

#submit4 - selected item for submitting (comments table output)
@app.callback(
    Output('submit-activity-comments','children'),
    [Input('activity-dropdown','value'),
    Input('placeholder-dropdown','value'),
    Input('name-dropdown','value')])
def act_comments_submit_table(act, pholder, name):  
    dfi = df[df.Name.isin([name])] 
    if act == 'Co-Curricular':
        return appfunction.submit_act_comments(dfi,pholder,items='CC{}'.format(pholder))
    elif act == 'Extra-Curricular':
        return appfunction.submit_act_comments(dfi,pholder,items='extraCC{}'.format(pholder))

#submit4 - update cell (activity notes/comments)
@app.callback(
    Output('container-act-comments','children'),
    [Input('submit-act-com','n_clicks'), 
	Input('submit-act-com','n_submit'),
    Input('name-dropdown','value'),
    Input('activity-dropdown','value'),
    Input('placeholder-dropdown','value')],
    [State('input-act-comments','value')])
def submit_coextra_comments(clicks, submit, name, act, pholder, value):
    if act == 'Co-Curricular':
        works = appfunction.access_wsheet('cocurricular com')
    elif act == 'Extra-Curricular':
        works = appfunction.access_wsheet('extra com')
    sub_row = works.find(name).row
    sub_col = works.find('{} {} (Comments)'.format(act,pholder)).col
    works.update_cell(sub_row,sub_col,value)

#submit5 - selected name for submitting (comments table output)
@app.callback(
    Output('submit-attitude','children'),
    [Input('name-dropdown','value')])
def att_table(name):
    dfi = df[df.Name.isin([name])]
    return appfunction.submit_attitude(dfi)

#submit5 - update cell (attitude/behaviour)
@app.callback(
    Output('container-att','children'),
    [Input('submit-att','n_clicks'), 
	Input('submit-att','n_submit'),
    Input('name-dropdown','value')],
    [State('input-att-1','value'), State('input-att-2','value'), State('input-att-3','value'),
    State('input-att-4','value'), State('input-att-5','value')])
def submit_attitude(clicks, submit, name, val1, val2, val3, val4, val5):
    works = appfunction.access_wsheet('att behaviour')
    sub_row = works.find(name).row
    works.update_cell(sub_row, works.find('Akhlaq').col, val1)
    works.update_cell(sub_row, works.find('Discipline').col, val2)
    works.update_cell(sub_row, works.find('Diligent').col, val3)
    works.update_cell(sub_row, works.find('Interaction').col, val4)
    works.update_cell(sub_row, works.find('Respect').col, val5)

#submit6 - selection
@app.callback(
    Output('display-submit','children'), 
    [Input('update-dropdown','value'),
    Input('level-dropdown','value'),
    Input('year-dropdown','value'),
    Input('name-dropdown','value')])
def display_selection(value, level, year, name):
    dfi = df[df.Name.isin([name])]
    if value == 'UP':
        return appfunction.update_name(level,year,name)
    elif value == 'SUB':
        return appfunction.new_name()

#submit6 - new student submission
@app.callback(
    Output('container-new','children'),
    [Input('submit-new','n_clicks'), 
	Input('submit-new','n_submit')],
    [State('input-name','value'),
    State('input-level','value'),
    State('input-year','value')])
def submit_name(clicks, submit, name, level, year):
    def next_available_row(worksheet):
        str_list = list(filter(None, worksheet.col_values(1)))
        return len(str_list)+1

    next_row = next_available_row(wks)
    #column, row, input item
    if not name in list(df['Name']):
        wks.update_cell(next_row,1,name)
        wks.update_cell(next_row,2,level)
        wks.update_cell(next_row,3,year)
        return html.P('You have added:'), html.P('{} Year {} - {}'.format(level,year,name))
    else:
        return html.P('The name is already available.')

#submit6 - update student info
@app.callback(
    Output('container-update','children'),
    [Input('submit-update','n_clicks'), 
	Input('submit-update','n_submit'),
    Input('name-dropdown','value')],
    [State('update-level','value'),
    State('update-year','value')])
def submit_update(clicks, submit, name, level, year):
    sub_row = wks.find(name).row
    wks.update_cell(sub_row, 2, level)
    wks.update_cell(sub_row, 3, year)

if __name__ == '__main__':
    app.run_server(debug=True)
