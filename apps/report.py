import dash
import dash_core_components as dcc
import dash_html_components as html

select_opt = {'Primary' : list(range(1,7)), 'Secondary' : list(range(7,10))}
select_level = list(select_opt.keys())

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

layout = html.Div(
		[
			html.Div([
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
			html.Div(id='display-attitude')
			]
	)
