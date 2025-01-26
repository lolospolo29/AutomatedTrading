import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

# Initialize Dash app
app = dash.Dash(__name__)

# Define the nodes and logical flow edges of the dataflow
nodes = ["API Request", "Controller", "Service", "Manager", "Strategy Analyzer", "Facade", "Database", "Error"]
edges = [
    ("API Request", "Controller"),
    ("Controller", "Service"),
    ("Service", "Manager"),
    ("Manager", "Strategy Analyzer"),
    ("Strategy Analyzer", "Facade"),
    ("Facade", "Database"),
    ("Controller", "Error"),  # Error path from Controller
    ("Service", "Error"),  # Error path from Service
    ("Manager", "Error"),  # Error path from Manager
]

# Prepare node indices and initialize flows
node_labels = nodes
node_indices = {node: i for i, node in enumerate(node_labels)}

# Initialize flows as zero for all edges
flows = {edge: 0 for edge in edges}

# Active requests that track their positions in the flow
active_requests = []

# App layout
app.layout = html.Div([
    html.H1("Interactive Dataflow Simulation", style={"textAlign": "center"}),

    # Graph container
    dcc.Graph(
        id="dataflow-graph",
        config={"displayModeBar": False},  # Hide toolbar
    ),

    # Input fields for adding flows
    html.Div([
        html.Label("Add Flow:", style={"fontWeight": "bold"}),

        html.Div([
            dcc.Dropdown(
                id="from-dropdown",
                options=[{"label": node, "value": node} for node in nodes],
                placeholder="From Node",
                style={"width": "45%", "display": "inline-block", "marginRight": "5px"}
            ),
            dcc.Dropdown(
                id="to-dropdown",
                options=[{"label": node, "value": node} for node in nodes],
                placeholder="To Node",
                style={"width": "45%", "display": "inline-block"}
            )
        ]),

        html.Button("Add Flow", id="add-flow-button", n_clicks=0, style={"marginTop": "10px"}),
    ], style={"textAlign": "center", "margin": "20px"}),

    # Interval for refreshing the graph and simulation
    dcc.Interval(
        id="refresh-interval",
        interval=1000,  # Update every second
        n_intervals=0,
    )
])


# Helper function to create the Sankey diagram
def create_sankey():
    # Convert flows to sources, targets, and values for the Sankey diagram
    link_sources = [node_indices[edge[0]] for edge in flows]
    link_targets = [node_indices[edge[1]] for edge in flows]
    link_values = list(flows.values())  # Flow values are dynamic

    # Generate the Sankey diagram
    figure = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels
        ),
        link=dict(
            source=link_sources,
            target=link_targets,
            value=link_values
        )
    ))

    figure.update_layout(title_text="Interactive Dataflow Simulation", font_size=10)
    return figure


# Simulate dataflow for all active requests
def simulate_flow():
    global flows, active_requests

    # Decay old flows slowly
    for edge in flows:
        flows[edge] = max(flows[edge] - 1, 0)

    # Progress active requests through the flow
    for request in active_requests:
        current_position = request["position"]
        if current_position < len(edges):
            # Get the current edge for the request
            edge = edges[current_position]

            # Increment flow on the current edge
            flows[edge] += 1

            # Move the request to the next step
            request["position"] += 1

    # Remove completed requests
    active_requests[:] = [req for req in active_requests if req["position"] < len(edges)]


# Combined callback to handle both manual flow addition and simulation refresh
@app.callback(
    Output("dataflow-graph", "figure"),
    [Input("add-flow-button", "n_clicks"), Input("refresh-interval", "n_intervals")],
    [State("from-dropdown", "value"), State("to-dropdown", "value")]
)
def update_graph(n_clicks, n_intervals, from_node, to_node):
    global active_requests

    # Identify the trigger
    ctx = dash.callback_context
    if not ctx.triggered:
        return create_sankey()

    triggered_input = ctx.triggered[0]["prop_id"]

    if "add-flow-button" in triggered_input:
        # Handle manual flow addition
        if from_node and to_node:
            edge = (from_node, to_node)
            if edge in edges:  # Ensure the edge is valid
                flows[edge] += 1  # Increment initial flow
                start_index = edges.index(edge)  # Find the starting position
                active_requests.append({"position": start_index})  # Add a new active request

    elif "refresh-interval" in triggered_input:
        # Handle periodic simulation refresh
        simulate_flow()

    # Update the graph with the latest flows
    return create_sankey()


if __name__ == "__main__":
    app.run_server(debug=True)
