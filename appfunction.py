import dash
import dash_core_components as dcc
import dash_html_components as html

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())
select_year = select_opt[select_level[0]]

#List of subject
subject = ['TJ','TF','IS','AR','EN','JP','MT','SC','PE','LS','IT','SS','GE','ART']
sub_grade = ['{}_grade'.format(sub) for sub in subject]
sub_marks = ['{}_marks'.format(sub) for sub in subject]
sub_com = ['{}_comments'.format(sub) for sub in subject]

def grades_table(dataframe):
        return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in ['Component','Grade', 'Marks']])] +

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

def co_table(dataframe):
        return html.Table(
                #Header
                [html.Tr([html.Th(col) for col in ['Component','Attendance','Participation','Effort','Attitude','Grade']])] +

                #Body
                [html.Tr(
                        [html.Td(dataframe['CC{}'.format(num)])] +
                        [html.Td(dataframe['CC{}A'.format(num)])] +
                        [html.Td(dataframe['CC{}P'.format(num)])] +
                        [html.Td(dataframe['CC{}E'.format(num)])] +
                        [html.Td(dataframe['CC{}AT'.format(num)])] +
                        [html.Td(dataframe['CC{}G'.format(num)])]
                        ) for num in range(1,6)]
                )

def extra_table(dataframe):
        return html.Table(
                #Header
                [html.Tr([html.Th(col) for col in ['Component','Attendance','Participation','Effort','Attitude','Grade']])] +

                #Body
                [html.Tr(
                        [html.Td(dataframe['extraCC{}'.format(num)])] +
                        [html.Td(dataframe['extraCC{}A'.format(num)])] +
                        [html.Td(dataframe['extraCC{}P'.format(num)])] +
                        [html.Td(dataframe['extraCC{}E'.format(num)])] +
                        [html.Td(dataframe['extraCC{}AT'.format(num)])] +
                        [html.Td(dataframe['extraCC{}G'.format(num)])]
                        ) for num in range(1,4)]
                )

def co_comments(dataframe):
        return html.Table(
                #Header
                [html.Tr([html.Th(col) for col in ['Component','Competency and Accomplishment']])] +

                #Body
                [html.Tr(
                        [html.Td(dataframe['CC{}'.format(num)])] +
                        [html.Td(dataframe['CC{}comment'.format(num)])]
                        ) for num in range(1,6)]
                )

def extra_comments(dataframe):
        return html.Table(
                #Header
                [html.Tr([html.Th(col) for col in ['Component','Competency and Accomplishment']])] +

                #Body
                [html.Tr(
                        [html.Td(dataframe['extraCC{}'.format(num)])] +
                        [html.Td(dataframe['extraCC{}comment'.format(num)])]
                        ) for num in range(1,4)]
                )

def attitude(dataframe):
        return html.Table(
                #Header
                [html.Tr([html.Th(col) for col in ['Component','Grade']])] +

                #Body
                [html.Tr(
                        [html.Td(att)] +
                        [html.Td(dataframe[att])]
                        ) for att in ['Akhlaq','Discipline','Diligent','Interaction','Respect']]
                )