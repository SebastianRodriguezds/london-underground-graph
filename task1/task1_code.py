import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Approx geographical coordinates (latitude, longitude)
coords_geo = {
    "Hyde Park Corner": (51.5027, -0.1526),
    "Green Park":        (51.5069, -0.1426),
    "Piccadilly Circus": (51.5101, -0.1337),
    "Leicester Square":  (51.5116, -0.1284),
    "Covent Garden":     (51.5129, -0.1247),
    "Holborn":           (51.5171, -0.1188)
}

# Function to calculate distance
def haversine_km(coord1, coord2):
    R = 6371.0  # radius of the Earth in km
    lat1, lon1 = np.radians(coord1)
    lat2, lon2 = np.radians(coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

# Calculate real distances between stations
edges = [
    ("Hyde Park Corner", "Green Park"),
    ("Green Park", "Piccadilly Circus"),
    ("Piccadilly Circus", "Leicester Square"),
    ("Leicester Square", "Covent Garden"),
    ("Covent Garden", "Holborn")
]

# Create DataFrame with distances
df_edges = pd.DataFrame(edges, columns=["from", "to"])
df_edges["distance_km"] = df_edges.apply(
    lambda row: haversine_km(coords_geo[row["from"]], coords_geo[row["to"]]),
    axis=1
)

# Create Graph
G = nx.Graph()
for station in coords_geo:
    G.add_node(station)

for _, row in df_edges.iterrows():
    G.add_edge(row["from"], row["to"], weight=row["distance_km"])

# positions
pos = {
    "Hyde Park Corner": (0, -1),
    "Green Park": (1, 0.5),
    "Piccadilly Circus": (3, 0.5),
    "Leicester Square": (5, 0.5),
    "Covent Garden": (6.5, 1.2),
    "Holborn": (8, 2.2)
}

# Draw nodes and edges
plt.figure(figsize=(10, 4))
nx.draw_networkx_nodes(G, pos, node_size=600, node_color='blue')
nx.draw_networkx_edges(G, pos, width=2, edge_color='blue')

# Station labels (moved down)
label_pos = {k: (v[0], v[1] - 0.25) for k, v in pos.items()}
nx.draw_networkx_labels(G, label_pos, font_size=8, font_color='black')

# Labels with distances
edge_labels = {
    (u, v): f"{d['weight']:.2f} km"
    for u, v, d in G.edges(data=True)
}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Title "Key" outside the box
plt.text(7, -0.3, "Key", fontsize=9, fontweight='bold')

# Legend box
plt.gca().add_patch(plt.Rectangle((6.9, -1.4), 2, 0.8,
                                  fill=True, facecolor='white', edgecolor='black'))

# Content inside legend box
plt.plot([7.0, 7.4], [-1.0, -1.0], color='blue')
plt.text(7.5, -1.05, "Piccadilly", fontsize=8, color='blue')

plt.axis('off')
plt.title("Section of the Piccadilly line (actual distances)", fontsize=12)
plt.tight_layout()

plt.savefig("task1_image.png", dpi = 300)
plt.show()
