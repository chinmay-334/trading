import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load your stock data
df = pd.read_csv("stock_one_day_snapshot.csv")

# Example: Map sectors manually (you can expand this dictionary)
sector_map = {
    "RELIANCE.NS": "Energy", "TCS.NS": "IT", "INFY.NS": "IT", "HDFCBANK.NS": "Banking",
    "ICICIBANK.NS": "Banking", "LT.NS": "Construction", "SBIN.NS": "Banking",
    # Add all other tickers with appropriate sectors...
}

# Dummy inclusion in index
nifty50 = set(df["Ticker"])  # assuming all are in NIFTY50 for now
sensex = set([
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "SBIN.NS", "ASIANPAINT.NS", "BAJAJ-AUTO.NS", "SUNPHARMA.NS"
    # Add actual SENSEX members
])

# Prepare correlation matrix
features = ['DailyReturn', 'PrevReturn']
correlation_matrix = df.set_index('Ticker')[features].transpose().corr()

# Initialize graph
G = nx.Graph()

# Add NIFTY and SENSEX index nodes
G.add_node("NIFTY50", type="index")
G.add_node("SENSEX", type="index")

# Add stock nodes with attributes
for _, row in df.iterrows():
    ticker = row['Ticker']
    sector = sector_map.get(ticker, "Unknown")
    in_nifty = ticker in nifty50
    in_sensex = ticker in sensex
    G.add_node(ticker, sector=sector, in_nifty=in_nifty, in_sensex=in_sensex)
    if in_nifty:
        G.add_edge(ticker, "NIFTY50", weight=0.9)
    if in_sensex:
        G.add_edge(ticker, "SENSEX", weight=0.7)

# Define composite score-based edges
alpha = 0.6
beta = 0.3
gamma = 0.1

for i in correlation_matrix.columns:
    for j in correlation_matrix.columns:
        if i != j and not G.has_edge(i, j):
            corr = correlation_matrix.loc[i, j]
            same_sector = 1 if sector_map.get(i) == sector_map.get(j) else 0
            same_index = 1 if (i in nifty50 and j in nifty50) else 0.5 if ((i in nifty50) or (j in nifty50)) else 0
            weight = alpha * corr + beta * same_sector + gamma * same_index
            if weight > 0.5:  # Threshold to reduce clutter
                G.add_edge(i, j, weight=round(weight, 2))

# Draw the graph
plt.figure(figsize=(18, 16))
pos = nx.spring_layout(G, seed=42, k=0.35)

# Node color logic
node_colors = []
for node in G.nodes(data=True):
    if node[0] == "NIFTY50":
        node_colors.append("gold")
    elif node[0] == "SENSEX":
        node_colors.append("orange")
    elif node[1].get("sector") == "IT":
        node_colors.append("lightblue")
    elif node[1].get("sector") == "Banking":
        node_colors.append("lightgreen")
    else:
        node_colors.append("gray")

# Draw components
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
nx.draw_networkx_labels(G, pos, font_size=9)
nx.draw_networkx_edges(G, pos, width=[d['weight']*2 for (_, _, d) in G.edges(data=True)], alpha=0.5)

plt.title("Financial Stock Relationship Graph with Real-World Influence", fontsize=16)
plt.axis('off')
plt.show()