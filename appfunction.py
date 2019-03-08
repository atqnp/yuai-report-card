import os
import gspread
import dash
import dash_core_components as dcc
import dash_html_components as html
from oauth2client.service_account import ServiceAccountCredentials

#center style for table
center = {'text-align':'center'}

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
            'ART':'Art'}

sub_grade = ['{}_grade'.format(sub) for sub in subject.keys()]
sub_marks = ['{}_marks'.format(sub) for sub in subject.keys()]
sub_com = ['{}_comments'.format(sub) for sub in subject.keys()]

def access_wsheet(item):
    """accessing worksheet based on item(input)"""
    access = 'all {}'.format(item)
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
    file = gspread.authorize(credentials)
    sheet = file.open("Copy of Semester 2 Report Card (data) 2018/2019")
    wks = sheet.worksheet(access)
    return wks

def new_name():
    return html.Table(
        [html.Tr([html.Th(html.P('Input new information to be added'),colSpan='3')])] +
        [html.Tr([html.Th(col) for col in ['Name','Level','Year']])] +
        [html.Tr(
            [html.Td(html.Div(dcc.Input(id='input-name',type='text')))] + 
            [html.Td(html.Div(dcc.Input(id='input-level',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-year',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-new')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(id='container-new'),colSpan='3')]
            )]
        )

def update_name(level,year,name):
    return html.Table(
        [html.Tr([html.Th(html.P('Current information'),colSpan='3')])] +
        [html.Tr([html.Th(col) for col in ['Name','Level','Year']])] +
        [html.Tr(
            [html.Td(name)] + [html.Td(level)] + [html.Td(year, style=center)]
            )] +
        [html.Tr([html.Td('',colSpan=3)])] +
        [html.Tr([html.Th(html.P('Changes/Input for submission'),colSpan='3')])] +
        [html.Tr(
            [html.Td(name)] + 
            [html.Td(html.Div(dcc.Input(id='update-level',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='update-year',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-update')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(id='container-update'),colSpan='3')]
            )]
        )

def student_info(name,level,year,sem):
    return html.Table(
        [html.Tr([html.Td('Name',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(name,className="no-border")]
            )] +
        [html.Tr([html.Td('Level',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(level,className="no-border")]
            )] +
        [html.Tr([html.Td('Year',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(year,className="no-border")]
            )] +
        [html.Tr([html.Td('Semester',className="no-border")] + 
            [html.Td(':',style=center,className="no-border")] + 
            [html.Td(sem,className="no-border")]
            )], 
        className="no-border"
        )

def grades_table(dataframe):
    """return table for marks and grades of a student"""
    return html.Table(
    # Header
    [html.Tr([html.Th(col) for col in ['Component','Grade','Marks']])] +

    # Body
    [html.Tr(
        [html.Td(sub)] +
        [html.Td(dataframe[grade],style=center)] +
        [html.Td(dataframe[marks],style=center)]
        ) for sub,grade,marks in zip(subject.values(),sub_grade,sub_marks)
    ]
    )

def comments_table(dataframe):
    """return table for notes/comments of a student"""
    return html.Table(
    # Header
    [html.Tr([html.Th(col) for col in ['No','Component','Competency and Accomplishment']])] +

    # Body
    [html.Tr(
        [html.Td(no)] +
        [html.Td(sub)] +
        [html.Td([html.P(value) for index, value in dataframe[comments].str.split('\n',expand=True).items()])]
        ) for no,sub,comments in zip(list(range(1,len(sub_com)+1)),subject.values(),sub_com)
    ],className="fulltable"
    )

def co_table(dataframe):
    """return table for co-curricular activities (grades) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Grade']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['CC{}'.format(num)])] +
            [html.Td(dataframe['CC{}A'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}P'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}E'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}AT'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}G'.format(num)],style=center)]
            ) for num in range(1,6)]
            )

def extra_table(dataframe):
    """return table for extra-curricular activities (grades) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Grade']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['extraCC{}'.format(num)])] +
            [html.Td(dataframe['extraCC{}A'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}P'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}E'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}AT'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}G'.format(num)],style=center)]
            ) for num in range(1,4)]
        )

def co_comments(dataframe):
    """return table for co-curricular activities (notes/comments) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No.','Component','Competency and Accomplishment']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['CC{}'.format(num)])] +
            [html.Td(dataframe['CC{}comment'.format(num)])]
            ) for num in range(1,6)]
        )

def extra_comments(dataframe):
    """return table for extra-curricular activities (notes/comments) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No.','Component','Competency and Accomplishment']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['extraCC{}'.format(num)])] +
            [html.Td(dataframe['extraCC{}comment'.format(num)])]
            ) for num in range(1,4)]
        )

def attitude(dataframe):
    """return table for attitude grades of a student"""
    attlist = ['Akhlaq','Discipline','Diligent','Interaction','Respect']
    return html.Table(
        #Body
        [html.Tr(
            [html.Td(no,style=center)] + [html.Td(att,style=center)] + [html.Td(dataframe[att],style=center)]
            ) for no,att in zip(list(range(1,len(attlist)+1)),attlist)],className="widetable"
        )

def attendance(dataframe,period):
    '''return table for attendance'''
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['MONTH',period]])] +
        #Body
        [html.Tr([html.Td('School days')] + [html.Td(dataframe['School days'],style=center)])] +
        [html.Tr([html.Td('Absence')] + [html.Td(dataframe['Absence'],style=center)])] +
        [html.Tr([html.Td('Coming late')] + [html.Td(dataframe['Coming late'],style=center)])] +
        [html.Tr([html.Td('Leaving early')] + [html.Td(dataframe['Leaving early'],style=center)])],
        className="widetable"
        )

def submit_sub_marks(dataframe,subcode,grade,marks):
    """return table for marks submission of a student based on selected subject"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component to Submit','Grade (Before submission)','Marks (Before submission)']])] +

        #Body
        [html.Tr(
                [html.Td(subject.get(subcode))] + 
                [html.Td(dataframe[grade],style=center)] +
                [html.Td(dataframe[marks],style=center)] +
                [html.Td(html.Div(dcc.Input(id='input-marks',type='number')))] + 
                [html.Td(html.Div(html.Button('Submit',id='submit-marks')))] +
                [html.Td(html.Div(id='container-marks'))]
                )
        ]
        )

def submit_sub_comments(dataframe,subcode,comment):
    """return table for notes/comments submission of a student based on selected subject"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component to Submit','Notes (Before submission)']])] +

        #Body
        [html.Tr(
                [html.Td(subject.get(subcode))] + 
                [html.Td([html.P(value) for index, value in dataframe[comment].str.split('\n',expand=True).items()])]
            )
        ] +
        [html.Tr(
                [html.Td(html.P("Notes/Comments to Submit"))] +
                [html.Td(html.Div(dcc.Textarea(id='input-comments',placeholder='Enter your notes/comments here..',style={'width': '100%'})))] 
            )
        ] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-comments')))] +
            [html.Td(html.Div(id='container-comments'))]
            )]
        )

def submit_act_grades(dataframe,num,items):
    """return table for notes/comments submission 
        of a student based on 
        selected item(co-curricular/extra-curricular)
        and placeholder number"""
    return html.Table(
        [html.Tr(html.Th(html.P('Data before submission'),colSpan='7'))] +
        #Header - info
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Grade']])] +
        #Body - info
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe[items])] +
            [html.Td(dataframe[items + 'A'],style=center)] +
            [html.Td(dataframe[items + 'P'],style=center)] +
            [html.Td(dataframe[items + 'E'],style=center)] +
            [html.Td(dataframe[items + 'AT'],style=center)] +
            [html.Td(dataframe[items + 'G'],style=center)] 
            )] +
        [html.Tr([html.Td('',colSpan='7')])] +
        [html.Tr(html.Th(html.P('Changes/Input for submission'),colSpan='7'))] +
        #Header - submit
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Grade']])] +
        #Body - submit
        [html.Tr(
            [html.Td(num)] +
            [html.Td(html.Div(dcc.Input(id='input-act-component',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-act-attendance',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-act-participation',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-act-effort',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-act-attitude',type='text')))] +
            [html.Td(html.Div(dcc.Input(id='input-act-grade',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-actgrades')),colSpan='2')] +
            [html.Td(html.Div(id='container-act-grades'))]
        )]
        )

def submit_act_comments(dataframe,num,items):
    """return table for notes/comments submission 
        of a student based on 
        selected item(co-curricular/extra-curricular)
        and placeholder number"""
    return html.Table(
        [html.Tr(html.Th(html.P('Data before submission'),colSpan='3'))] +
        #Header - info
        [html.Tr([html.Th(col) for col in ['No','Component','Competency and Accomplishment']])] +
        #Body - info
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe[items])] +
            [html.Td(dataframe[items + 'comment'])]
            )] +
        [html.Tr([html.Td('',colSpan='3')])] +
        [html.Tr(html.Th(html.P('Changes/Input for submission'),colSpan='3'))] +
        #Header - submit
        [html.Tr([html.Th(col) for col in ['No','Component','Competency and Accomplishment']])] +
        #Body - submit
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe[items])] +
            [html.Td(html.Div(dcc.Textarea(id='input-act-comments',placeholder='Enter your notes/comments here..',style={'width': '100%'})))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-actcomments')),colSpan='2')] +
            [html.Td(html.Div(id='container-act-comments'))]
        )]
        )

def submit_attitude(dataframe):
    """return table for attitude grades submission of a student"""
    return html.Table(
        [html.Tr(html.Th(html.P('Changes/Input for submission'),colSpan='3'))] +
        #Header
        [html.Tr([html.Th(col) for col in ['Component','Grade (Before submission)','']])] +

        #Body
        [html.Tr(
            [html.Td(html.P('Akhlaq'))] + [html.Td(dataframe['Akhlaq'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-1',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Discipline'))] + [html.Td(dataframe['Discipline'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-2',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Diligent'))] + [html.Td(dataframe['Diligent'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-3',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Interaction'))] + [html.Td(dataframe['Interaction'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-4',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Respect'))] + [html.Td(dataframe['Respect'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-att-5',type='text')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-att')),colSpan='2')] +
            [html.Td(html.Div(id='container-att'))]
        )]
        )

def submit_attendance(dataframe):
    '''return table for attendance submission'''
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['Component','Data before submission','Input data']])] +
        #Body
        [html.Tr(
            [html.Td(html.P('School days'))] + [html.Td(dataframe['School days'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-1',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Absence'))] + [html.Td(dataframe['Absence'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-2',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Coming late'))] + [html.Td(dataframe['Coming late'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-3',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.P('Leaving early'))] + [html.Td(dataframe['Leaving early'],style=center)] + 
            [html.Td(html.Div(dcc.Input(id='input-attend-4',type='number',placeholder='Input value here..')))]
            )] +
        [html.Tr(
            [html.Td(html.Div(html.Button('Submit',id='submit-attendance-button')),colSpan='2')] +
            [html.Td(html.Div(id='container-attendance'))]
        )]
        )

def academic_report(dataframe):
    return html.Table(
        #Header
        [html.Tr([html.Th('No', rowSpan='2'),html.Th('Component', rowSpan='2'),html.Th('Cognitive',colSpan='2'),html.Th('Practical',colSpan='2')])] +
        [html.Tr([html.Th('Grade'),html.Th('Marks'),html.Th('Grade'),html.Th('Marks')])] +
        [html.Tr([html.Td('Academics',colSpan='6')])] +
        #Body
        [html.Tr(
            [html.Td('1')] +
            [html.Td(subject['TJ'])] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['TJ_grade'],style=center)] + [html.Td(dataframe['TJ_marks'],style=center)]
            )] +
        [html.Tr(
            [html.Td('2')] +
            [html.Td(subject['TF'])] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['TF_grade'],style=center)] + [html.Td(dataframe['TF_marks'],style=center)]
            )] +
        [html.Tr(
            [html.Td('3')] +
            [html.Td(subject['IS'])] + 
            [html.Td(dataframe['IS_grade'],style=center)] + [html.Td(dataframe['IS_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] 
            )] +
        [html.Tr(
            [html.Td('4')] +
            [html.Td(subject['AR'])] + 
            [html.Td(dataframe['AR_grade'],style=center)] + [html.Td(dataframe['AR_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('5')] +
            [html.Td(subject['EN'])] + 
            [html.Td(dataframe['EN_grade'],style=center)] + [html.Td(dataframe['EN_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('6')] +
            [html.Td(subject['JP'])] + 
            [html.Td(dataframe['JP_grade'],style=center)] + [html.Td(dataframe['JP_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('7')] +
            [html.Td(subject['MT'])] + 
            [html.Td(dataframe['MT_grade'],style=center)] + [html.Td(dataframe['MT_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('8')] +
            [html.Td(subject['SC'])] + 
            [html.Td(dataframe['SC_grade'],style=center)] + [html.Td(dataframe['SC_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('9')] +
            [html.Td(subject['PE'])] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['PE_grade'],style=center)] + [html.Td(dataframe['PE_marks'],style=center)]
            )] +
        [html.Tr(
            [html.Td('10')] +
            [html.Td(subject['LS'])] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['LS_grade'],style=center)] + [html.Td(dataframe['LS_marks'],style=center)]
            )] +
        [html.Tr(
            [html.Td('11')] +
            [html.Td(subject['IT'])] + 
            [html.Td(dataframe['IT_grade'],style=center)] + [html.Td(dataframe['IT_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('12')] +
            [html.Td(subject['SS'])] + 
            [html.Td(dataframe['SS_grade'],style=center)] + [html.Td(dataframe['SS_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('13')] +
            [html.Td(subject['GE'])] + 
            [html.Td(dataframe['GE_grade'],style=center)] + [html.Td(dataframe['GE_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('14')] +
            [html.Td(subject['PM'])] + 
            [html.Td(dataframe['PM_grade'],style=center)] + [html.Td(dataframe['PM_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('15')] +
            [html.Td(subject['ART'])] + 
            [html.Td(dataframe['ART_grade'],style=center)] + [html.Td(dataframe['ART_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )]
        )
