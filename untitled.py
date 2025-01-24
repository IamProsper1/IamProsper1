from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the Gapminder dataset
df = px.data.gapminder()

# Initialize the Dash app
app = Dash(__name__)

#tried this
# App layout with dark theme and cool colors
app.layout = html.Div(
    style={
        "backgroundColor": "#121212",  # Dark background color
        "color": "#E0E0E0",  # Light text color
        "padding": "20px",  # Padding around the page
        "font-family": "Arial, sans-serif",  # Modern font family
    },
    children=[
        # Header with cool color scheme
        html.H4(
            "Animated GDP and Population over Decades",
            style={"color": "#00D1C1", "text-align": "center", "font-size": "30px"},
        ),
        html.Label(
            "Select an animation:",
            style={"font-size": "18px", "color": "#E0E0E0", "margin-bottom": "10px"},
        ),
        # RadioItems with cool design and hover effect
        dcc.RadioItems(
            id="selection",
            options=[
                {"label": "GDP - Scatter", "value": "GDP - Scatter"},
                {"label": "Population - Bar", "value": "Population - Bar"},
            ],
            value="GDP - Scatter",
            style={
                "display": "flex",
                "justify-content": "center",
                "color": "#E0E0E0",
                "font-size": "16px",
                "margin-bottom": "30px",
                "backgroundColor": "#333333",  # Dark background for the items
                "border-radius": "5px",
                "padding": "10px",
            },
            inputStyle={"margin-right": "10px"},
        ),
        # Loading spinner wrapped around the graph
        dcc.Loading(dcc.Graph(id="graph", style={'backgroundColor': 'transparent'}), type="circle"),
    ]
)

# Callback to update the graph based on the selected animation
@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="selection", component_property="value"),
)
def display_animated_graph(selection):
    animations = {
        "GDP - Scatter": px.scatter(
            df,
            x="gdpPercap",
            y="lifeExp",
            animation_frame="year",
            animation_group="country",
            size="pop",
            color="continent",
            hover_name="country",
            log_x=True,
            size_max=55,
            range_x=[100, 100000],
            range_y=[25, 90],
        ),
        "Population - Bar": px.bar(
            df,
            x="continent",
            y="pop",
            color="continent",
            animation_frame="year",
            animation_group="country",
            range_y=[0, 4000000000],
        ),
    }

    # Set transparent background for the graph layout
    fig = animations[selection]
    fig.update_layout(
        plot_bgcolor='rgba(34, 45, 234, 0)',  # Set plot background to transparent
        paper_bgcolor='rgba(34, 234, 231, 0)',  # Set paper background to transparent
        font=dict(color="#E0E0E0"),  # Light color for text
        margin=dict(l=40, r=40, t=40, b=40)  # Optional: add some margin for better spacing
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


