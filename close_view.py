import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# --- Function to build the graph ---
def build_stock_graph(csv_path, corr_threshold=0.5):
    df = pd.read_csv(csv_path)
    features = ['DailyReturn', 'PrevReturn']
    correlation_matrix = df.set_index('Ticker')[features].transpose().corr()

    G = nx.Graph()

    # Node weights = Close * Volume * (1 + DailyReturn)
    for _, row in df.iterrows():
        valuation = row['Close'] * row['Volume'] * (1 + row['DailyReturn'])
        G.add_node(row['Ticker'], 
                   close=row['Close'], 
                   volume=row['Volume'], 
                   daily_return=row['DailyReturn'], 
                   valuation=valuation)

    # Add edges based on correlation
    for i in correlation_matrix.columns:
        for j in correlation_matrix.columns:
            if i != j and correlation_matrix.loc[i, j] > corr_threshold:
                G.add_edge(i, j, weight=correlation_matrix.loc[i, j])

    return G

# --- Function to visualize graph and report connections for a given ticker ---
def show_connected_info(G, target_ticker):
    if target_ticker not in G:
        print(f"{target_ticker} not in graph.")
        return

    neighbors = list(G.neighbors(target_ticker))
    print(f"\nTarget Ticker: {target_ticker}")
    print(f"Valuation: {G.nodes[target_ticker]['valuation']:.2f}\n")
    print("Connected Nodes:")

    for neighbor in neighbors:
        edge_weight = G[target_ticker][neighbor]['weight']
        valuation = G.nodes[neighbor]['valuation']
        print(f"  {neighbor} - Correlation: {edge_weight:.2f}, Valuation: {valuation:.2f}")

    # Graph Visualization
    sub_nodes = neighbors + [target_ticker]
    subgraph = G.subgraph(sub_nodes)

    pos = nx.spring_layout(subgraph, seed=42)
    plt.figure(figsize=(10, 8))
    node_colors = ['gold' if node == target_ticker else 'lightblue' for node in subgraph.nodes()]

    nx.draw(subgraph, pos, with_labels=True, node_size=800, node_color=node_colors, edge_color='gray', width=2)
    
    plt.title(f"Graph of {target_ticker} and Connected Stocks")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# --- Example Usage ---
if __name__ == "__main__":
    graph = build_stock_graph("stock_one_day_snapshot.csv", corr_threshold=0)
    show_connected_info(graph, "^NSEI")
