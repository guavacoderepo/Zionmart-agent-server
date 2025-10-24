from graphviz import Digraph

# Create a directed graph
dot = Digraph(comment='Agentic Customer Care Graph', format='png')

# Set graph size and ratio
dot.attr(size='12,10')        # width,height in inches
dot.attr(rankdir='TB')         # top-to-bottom layout

# Define nodes with colors based on their role
nodes = [ "_start_", "rewriter", "supervisor", "order", "enquiry", "complaint", "off_topic", "create_order", "edit_order", "cancel_order", "retrieve_items", "_end_" ]

# Add nodes
for node in nodes: 
    dot.node(node, node.capitalize())

# Define edges with conditional routes highlighted
edges = [
    ("_start_", "rewriter", "black"),
    ("rewriter", "supervisor", "black"),
    ("supervisor", "enquiry", "green"),  # conditional route
    ("supervisor", "complaint", "red"),  # conditional route
    ("supervisor", "off_topic", "gray"),
    ("supervisor", "order", "orange"),
    ("order", "create_order", "blue"),   # conditional route
    ("order", "edit_order", "blue"),
    ("order", "cancel_order", "blue"),
    ("order", "retrieve_items", "blue"),
    ("create_order", "supervisor", "black"),
    ("edit_order", "supervisor", "black"),
    ("enquiry", "supervisor", "black"),
    ("complaint", "supervisor", "black"),
    ("cancel_order", "supervisor", "black"),
    ("retrieve_items", "supervisor", "black"),
    ("supervisor", "_end_", "black"),
    ("off_topic", "_end_", "black"),
]

# Add edges with colors
for src, dst, color in edges:
    dot.edge(src, dst, color=color)

# Render to file and view
dot.render('agent_graph_conditional', view=True)
