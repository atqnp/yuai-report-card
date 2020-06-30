import dash
import dash_core_components as dcc
import dash_html_components as html

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