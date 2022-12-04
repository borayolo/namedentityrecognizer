from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

import en_core_web_sm
from spacy.displacy.render import DEFAULT_LABEL_COLORS

# initialize web app
app = Dash(__name__)
app.title = 'Named Entity Recognizer'
app._favicon = "/assets/images/favicon.ico"
server = app.server

# CSS
button = {
    'background-color': 'initial',
    'background-image': 'linear-gradient(#42A1EC, #0070C9)',
    'border-radius': '6px',
    'box-shadow': 'rgba(0, 0, 0, 0.1) 0 2px 4px',
    'color': '#FFFFFF',
    'cursor': 'pointer',
    'display': 'inline-block',
    'font-family': 'Inter,-apple-system,system-ui,Roboto,"Helvetica Neue",Arial,sans-serif',
    'font-size': '1.0em',
    'font-weight': 'bold',
    'height': '40px',
    'line-height': '40px',
    'outline': '0',
    'overflow': 'hidden',
    'padding': '0 20px',
    'pointer-events': 'auto',
    'position': 'relative',
    'text-align': 'center',
    'touch-action': 'manipulation',
    'vertical-align': 'top',
    'white-space': 'nowrap',
    'width': '100%',
    'z-index': '9',
    'border': '0',
}

textarea = {
    'width': '100%',
    'height': '400px',
    'padding': '12px 12px',
    'margin': '8px 0',
    'box-sizing': 'border-box',
    'outline': 'none',
    'resize': 'none'
}

output = {
    'font-family': 'Inter,-apple-system,system-ui,Roboto,"Helvetica Neue",Arial,sans-serif',
    'font-size': '1.0em',
    'line-height': '2.4',
    'padding': '1em 0.2em'
}


def ent_name(name):
    return html.Span(name, style={
        "font-size": "0.8em",
        "font-weight": "bold",
        "line-height": "1",
        "border-radius": "0.35em",
        "text-transform": "uppercase",
        "vertical-align": "middle",
        "margin-left": "0.5rem"
    })


def ent_box(children, color):
    return html.Mark(children, style={
        "background": color,
        "padding": "0.45em 0.6em",
        "margin": "0 0.25em",
        "line-height": "1",
        "border-radius": "0.35em",
    })


def entity(children, name):
    if type(children) is str:
        children = [children]

    children.append(ent_name(name))
    color = DEFAULT_LABEL_COLORS[name]
    return ent_box(children, color)


def render(doc):
    children = []
    last_idx = 0
    for ent in doc.ents:
        children.append(doc.text[last_idx:ent.start_char])
        children.append(
            entity(doc.text[ent.start_char:ent.end_char], ent.label_))
        last_idx = ent.end_char
    children.append(doc.text[last_idx:])
    return children


app.layout = html.Div([
    html.H1('Named Entity Recognizer', style={'font-family': 'Inter,-apple-system,system-ui,Roboto, "Helvetica Neue", Arial,sans-serif',
                                              'font-weight': 'bold',
                                              'font-size': '2.0em'}),
    dcc.Textarea(id='textarea', placeholder='Enter your text here', style=textarea), html.Br(),
    html.Button('Analyze', id='textarea-button', n_clicks=0, style=button),
    html.Div(id='textarea-output', style=output)
])


@app.callback(
    Output('textarea-output', 'children'),
    Input('textarea-button', 'n_clicks'),
    State('textarea', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        nlp = en_core_web_sm.load()
        doc = nlp(value)
        return render(doc)


if __name__ == '__main__':
    app.run_server()