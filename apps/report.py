import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())
select_year = select_opt[select_level[0]]

layout = html.Div(
		[
			html.Div([
			html.Div(id='refresh-data'),
			dcc.Dropdown(
				id='level-dropdown',
				options=[{'label':i,'value':i} for i in select_level],
				placeholder="Select level",
				),
			dcc.Dropdown(
				id='year-dropdown',
				placeholder="Select year"
				),
			dcc.Dropdown(
				id='name-dropdown',
				placeholder="Select name"
				),
			]),
			html.Hr(),
			html.Div(id='display-value'),
			html.Hr(),
			html.H5('Academics Achievement'),
			html.Div(id='display-grade'),
			html.Hr(),
			html.H5("Academics Achievement - Teacher's Note"),
			html.Div(id='display-comments'),
			html.Hr(),
			html.H5('Co-curricular Activities'),
			html.Div(id='display-cc-grade'),
			html.H5("Extra-curricular Activities"),
			html.Div(id='display-ex-grade'),
			html.Hr(),
			html.H5("Co-curricular Activities - Teacher's Note"),
			html.Div(id='display-cc-comments'),
			html.H5("Extra-curricular Activities - Teacher's Note"),
			html.Div(id='display-ex-comments'),
			html.Hr(),
			html.H5("Behaviour/Affectiveness"),
			html.Div(id='display-attitude')		]
	)
