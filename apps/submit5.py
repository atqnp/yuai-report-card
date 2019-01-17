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
			html.Div(id='display-attitude')
		]
	)