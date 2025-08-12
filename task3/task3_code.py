import numpy as np
import pandas as pd
import networkx as nx

# Load the graph saved in Task 2
G = nx.read_graphml("../task2/london_transport.graphml")

# Extract distances from edges (weight might be stored as string, convert to float)
distances = [float(data['weight']) for _, _, data in G.edges(data=True)]

# Convert distances list to a NumPy array for calculations
dist_arr = np.array(distances)

# Calculate total length, average distance, and standard deviation of distances
total_length = np.sum(dist_arr)
average_distance = np.mean(dist_arr)
std_deviation = np.std(dist_arr)

# Print the statistics
print(f"Total length of the transport network: {total_length:.2f} km")
print(f"Average distance between stations: {average_distance:.2f} km")
print(f"Standard deviation of distances: {std_deviation:.2f} km")

# Save the results to a CSV file
df_stats = pd.DataFrame({
    "Metric": ["Total Length (km)", "Average Distance (km)", "Standard Deviation (km)"],
    "Value": [total_length, average_distance, std_deviation]
})

df_stats.to_csv("task3_data.csv", index=False)
print("Task 3 data saved to task3_data.csv")