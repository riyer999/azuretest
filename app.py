# Import required libraries
from dash import Dash, dcc, html
import plotly.graph_objs as go

# Initialize the app
app = Dash(__name__)

# Sample data for the line graph
x_values = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
y_values = [10, 15, 8, 25, 18]

# Define the layout of the app
app.layout = html.Div([
    html.H1("Basic Line Graph"),
    dcc.Graph(
        id="line-graph",
        figure={
            'data': [
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode='lines+markers',
                    name='Sample Data'
                )
            ],
            'layout': go.Layout(
                title="Monthly Data",
                xaxis={'title': 'Month'},
                yaxis={'title': 'Value'},
                template="plotly_dark"
            )
        }
    )
])

# Run the app
server = app.server

if __name__ == '__main__':
    app.run_server()
