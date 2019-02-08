import dash
import dash_core_components as dcc
import dash_html_components as html

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())

layout = html.Div(
		[
			html.Div([
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
			html.H5("Report of Behaviour or Affectiveness for submission"),
			html.Div(id='submit-attitude'),
		]
	)

