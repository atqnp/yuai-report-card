import dash
import dash_core_components as dcc
import dash_html_components as html

select_act = {'Co-Curricular' : list(range(1,6)), 'Extra-Curricular' : list(range(1,4))}
select_item = list(select_act.keys())

layout = html.Div(
		[
			html.Hr(),
			html.H5("Report of Co-curricular Activities - Teacher's Note"),
			html.Div(id='display-cc-comments'),
			html.Hr(),
			html.H5("Report of Extra-curricular Activities - Teacher's Note"),
			html.Div(id='display-ex-comments'),
			html.Br(),
			html.P('Select the Activities to submit the notes:'),
			html.Div([
			dcc.Dropdown(
				id='activity-dropdown',
				options=[{'label':i,'value':i} for i in select_item],
				placeholder="Select activity",
				),
			dcc.Dropdown(
				id='placeholder-dropdown',
				placeholder="Select the placeholder number"
				),
			]),
			html.Div(id='submit-activity-comments')
		], className="sheet padding-10mm"
	)
