import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(
        [
            html.Section([
                html.Div(id='display-student-info'),
                html.Hr(),
                html.H6('Academics Achievement'),
                html.Div(id='display-report'),
                ], className="sheet padding-10mm"),
            html.Section([
                html.H6("Academics Achievement - Teacher's Note"),
                html.Div(id='display-comments'),
                ], className="sheet padding-10mm"),
            html.Section([
                html.H6('Co-curricular Activities'),
                html.Div(id='display-cc-grade'),
                html.H6("Extra-curricular Activities"),
                html.Div(id='display-ex-grade'),
                html.H6("Co-curricular Activities - Teacher's Note"),
                html.Div(id='display-cc-comments'),
                html.H6("Extra-curricular Activities - Teacher's Note"),
                html.Div(id='display-ex-comments'),
                ], className="sheet padding-10mm"),
            html.Section([
                html.H6("Behaviour/Affectiveness"),
                html.Div(id='display-attitude'),
                html.Hr(),
                html.Div(id='display-attendance'),
                html.Hr(),
                html.Div(id='display-range'),
                html.P('Date :'),
                html.Div(id='display-parents'),
                html.Div(id='display-teacher')
                ],className="sheet padding-10mm")
        ]
    )
