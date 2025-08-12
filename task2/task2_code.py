import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Function to calculate haversine distance
def haversine_km(coord1, coord2):
    R = 6371.0
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Approximate coordinates of stations
coords_geo = {
    # Piccadilly Line
    "Hyde Park Corner": (51.5027, -0.1526),
    "Green Park": (51.5069, -0.1426),
    "Piccadilly Circus": (51.5101, -0.1337),
    "Leicester Square": (51.5116, -0.1284),
    "Covent Garden": (51.5129, -0.1247),
    "Holborn": (51.5171, -0.1188),

    # Central Line
    "Oxford Circus": (51.5154, -0.1410),
    "Tottenham Court Road": (51.5162, -0.1310),
    "Chancery Lane": (51.5185, -0.1110),
    "St. Paul's": (51.5143, -0.0972),
    "Bank": (51.5133, -0.0890),
    "Green Park": (51.5069, -0.1426),

    # Victoria Line
    "Victoria": (51.4952, -0.1440),
    "Green Park": (51.5069, -0.1426),
    "Pimlico": (51.4893, -0.1334),
    "Vauxhall": (51.4857, -0.1232),
    "Stockwell": (51.4722, -0.1226),
    "Brixton": (51.4627, -0.1140),

    # Jubilee Line
    "Westminster": (51.5010, -0.1246),
    "Green Park": (51.5069, -0.1426),
    "Bond Street": (51.5142, -0.1494),
    "Baker Street": (51.5225, -0.1570),  
    "Waterloo": (51.5033, -0.1133),
    "Southwark": (51.5043, -0.1046),
}

# Dictionary with lines, their stations, and colors
lines = {
    "Piccadilly": {
        "stations": [
            "Hyde Park Corner", "Green Park", "Piccadilly Circus",
            "Leicester Square", "Covent Garden", "Holborn"
        ],
        "color": "blue"
    },
    "Central": {
        "stations": [
        "Green Park", 
        "Oxford Circus",
        "Tottenham Court Road",
        "Chancery Lane",
        "St. Paul's",
        "Bank"
    ],
    "color": "red"
    },
    "Victoria": {
        "stations": [
            "Victoria", "Green Park", "Pimlico",
            "Vauxhall", "Stockwell", "Brixton"
        ],
        "color": "lightblue"
    },
    "Jubilee": {
        "stations": [
            "Westminster", "Green Park", "Bond Street",
            "Baker Street", "Waterloo", "Southwark"
        ],
        "color": "gray"
    }
}

# Create graph and add edges
G = nx.Graph()

# Add nodes
for station, coord in coords_geo.items():
    G.add_node(station, pos=coord)

# Add edges for each line with distance as weight
edges_with_colors = []
for line_name, line_data in lines.items():
    stations = line_data["stations"]
    color = line_data["color"]
    for i in range(len(stations) - 1):
        s1, s2 = stations[i], stations[i+1]
        dist = haversine_km(coords_geo[s1], coords_geo[s2])
        G.add_edge(s1, s2, weight=dist, color=color)
        edges_with_colors.append(((s1, s2), color))

# Layout (spring layout for schematic look)
pos = nx.spring_layout(G, seed=42)

# Draw network
plt.figure(figsize=(10, 6))

# Draw edges by line color
for line_name, line_data in lines.items():
    edges = [(line_data["stations"][i], line_data["stations"][i+1])
             for i in range(len(line_data["stations"]) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=edges,
                           width=2, edge_color=line_data["color"])
    
# Assign node colors based on first line they appear in
node_colors = {}
for line_name, line_data in lines.items():
    color = line_data["color"]
    for station in line_data["stations"]:
        if station not in node_colors:
            node_colors[station] = color

colors_list = [node_colors[node] for node in G.nodes()]

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=200, node_color=colors_list)

# Draw station labels slightly below nodes
label_pos = {k: (v[0], v[1] - 0.05) for k, v in pos.items()}
nx.draw_networkx_labels(G, label_pos, font_size=8, font_color='black')

# Draw distance labels
edge_labels = {(u, v): f"{d['weight']:.2f} km"
               for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

# Draw legend (Key)
legend_x = 0.70
legend_y = 0.02
legend_width = 0.12
legend_height = 0.25

# Transparent box with black border
plt.gca().add_patch(
    plt.Rectangle(
        (legend_x, legend_y), legend_width, legend_height,
        fill=False, edgecolor='black', linewidth=1.2,
        transform=plt.gca().transAxes, zorder=5
    )
)

# Legend title "Key" (placed above the box)
plt.text(
    legend_x + 0.02, legend_y + legend_height + 0.02,
    "Key", fontsize=9, fontweight='bold',
    color='black', transform=plt.gca().transAxes, zorder=6
)

# Legend content
y_offset = legend_y + legend_height - 0.06
for line_name, line_data in lines.items():
    # Color line
    plt.plot(
        [legend_x + 0.02, legend_x + 0.05],
        [y_offset, y_offset],
        color=line_data["color"], linewidth=2,
        transform=plt.gca().transAxes, zorder=6
    )
    # Line name text
    plt.text(
        legend_x + 0.06, y_offset - 0.01,
        line_name, fontsize=8,
        color='black', transform=plt.gca().transAxes, zorder=6
    )
    y_offset -= 0.05

plt.axis('off')
plt.title("Task 2: London Transport Network Section with Four Lines, Interchanges, and Distance Annotations", fontsize=12)
plt.tight_layout()

plt.savefig("task2_image.png", dpi=300)
plt.show()

# Convert 'pos' attribute (tuple) to string to avoid GraphML error
for node in G.nodes(data=True):
    coord = node[1]['pos']
    node[1]['pos'] = f"{coord[0]},{coord[1]}"

nx.write_graphml(G, "london_transport.graphml")
