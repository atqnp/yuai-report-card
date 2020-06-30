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
            'BS':'Business Studies',
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
    sheet = file.open("Copy of Semester 3 Report Card (data) 2018/2019")
    wks = sheet.worksheet(access)
    return wks


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


def notes_table(dataframe):
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
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Progress','Grade']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['CC{}'.format(num)])] +
            [html.Td(dataframe['CC{}A'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}P'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}E'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}AT'.format(num)],style=center)] +
            [html.Td(dataframe['CC{}PR'.format(num)],style=center)] +                    
            [html.Td(dataframe['CC{}G'.format(num)],style=center)]
            ) for num in range(1,6)], className="fulltable"
            )


def extra_table(dataframe):
    """return table for extra-curricular activities (grades) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No','Component','Attendance','Participation','Effort','Attitude','Progress','Grade']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['extraCC{}'.format(num)])] +
            [html.Td(dataframe['extraCC{}A'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}P'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}E'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}AT'.format(num)],style=center)] +
            [html.Td(dataframe['extraCC{}PR'.format(num)],style=center)] +                   
            [html.Td(dataframe['extraCC{}G'.format(num)],style=center)]
            ) for num in range(1,4)], className="fulltable"
        )


def co_notes(dataframe):
    """return table for co-curricular activities (notes/comments) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No.','Component','Competency and Accomplishment']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['CC{}'.format(num)])] +
            [html.Td([html.P(value) for index, value in dataframe['CC{}comment'.format(num)].str.split('\n',expand=True).items()])]
            ) for num in range(1,6)], className="fulltable"
        )


def extra_notes(dataframe):
    """return table for extra-curricular activities (notes/comments) of a student"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['No.','Component','Competency and Accomplishment']])] +

        #Body
        [html.Tr(
            [html.Td(num)] +
            [html.Td(dataframe['extraCC{}'.format(num)])] +
            [html.Td([html.P(value) for index, value in dataframe['extraCC{}comment'.format(num)].str.split('\n',expand=True).items()])]
            ) for num in range(1,4)], className="fulltable"
        )


def attitude(dataframe):
    """return table for attitude grades of a student"""
    attlist = ['Akhlaq','Discipline','Diligent','Interaction','Respect']
    return html.Table(
        #Body
        [html.Tr(
            [html.Td(no,style=center)] + [html.Td(att,style=center)] + [html.Td(dataframe[att],style=center)]
            ) for no,att in zip(list(range(1,len(attlist)+1)),attlist)],className="narrowtable"
        )


def attendance(dataframe,period):
    """return table for attendance"""
    return html.Table(
        #Header
        [html.Tr([html.Th(col) for col in ['MONTH',period,'GRADE']])] +
        #Body
        [html.Tr([html.Td('School days')] + [html.Td(dataframe['School days'],style=center)] + [html.Td(dataframe['Grade'],style=center,rowSpan='3')])] +
        [html.Tr([html.Td('Absence')] + [html.Td(dataframe['Absence'],style=center)])] +
        [html.Tr([html.Td('Coming late')] + [html.Td(dataframe['Coming late'],style=center)])] +
        [html.Tr([html.Td('Leaving early')] + [html.Td(dataframe['Leaving early'],style=center)])],
        className="widetable"
        )


def comments(dataframe):
    """return table for teacher's comment on student"""
    return html.Table(
        #Header
        [html.Tr([html.Th("Teacher's Comment")])] +
        #Body
        [html.Tr([html.Td(dataframe['full_comments'])])], className="fulltable"
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
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['PM_grade'],style=center)] + [html.Td(dataframe['PM_marks'],style=center)]
            )] +
        [html.Tr(
            [html.Td('15')] +
            [html.Td(subject['BS'])] + 
            [html.Td(dataframe['BS_grade'],style=center)] + [html.Td(dataframe['BS_marks'],style=center)] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)]
            )] +
        [html.Tr(
            [html.Td('16')] +
            [html.Td(subject['ART'])] + 
            [html.Td('-',style=center)] + [html.Td('-',style=center)] + 
            [html.Td(dataframe['ART_grade'],style=center)] + [html.Td(dataframe['ART_marks'],style=center)]
            )]
        )

def grade_range():
    return html.Table(
        [html.Tr([html.Th('Range',style=center)] + [html.Th('Grade',style=center)]
            )] +
        [html.Tr([html.Td('80 - 100',style=center)] + [html.Td('A',style=center)]
            )] +
        [html.Tr([html.Td('70 - 79',style=center)] + [html.Td('B',style=center)]
            )] +
        [html.Tr([html.Td('60 - 69',style=center)] + [html.Td('C',style=center)]
            )] +
        [html.Tr([html.Td('50 - 59',style=center)] + [html.Td('D',style=center)]
            )] +
        [html.Tr([html.Td('0 - 49',style=center)] + [html.Td('F',style=center)]
            )],className="narrowtable"
        )
