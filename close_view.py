import os
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from itertools import combinations

def compute_valid_correlations(folder_path):
    correlations = []
    file_names = []

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)
            df = df.select_dtypes(include=[np.number])
            df = df.dropna(axis=1)

            if df.shape[1] < 2:
                print(f"⚠️ Skipped {file} (not enough valid numeric columns).")
                continue

            corr_matrix = df.corr(method='spearman')
            upper_triangle = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
            corr_values = upper_triangle.stack().values
            correlations.append(corr_values)
            file_names.append(file)

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")
    
    return file_names, correlations

def compute_pairwise_spearman(file_names, correlations, threshold=0.5):
    pairwise_results = []

    for (i, j) in combinations(range(len(correlations)), 2):
        corr_i = correlations[i]
        corr_j = correlations[j]

        min_len = min(len(corr_i), len(corr_j))
        if min_len == 0:
            continue

        rho, _ = spearmanr(corr_i[:min_len], corr_j[:min_len])

        if rho >= threshold:
            pairwise_results.append((file_names[i], file_names[j], rho))

    return pairwise_results

def build_and_draw_graph(pairwise_edges):
    G = nx.Graph()

    for file1, file2, weight in pairwise_edges:
        G.add_edge(file1, file2, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

    # Draw nodes and labels
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Draw edges with weights
    nx.draw_networkx_edges(G, pos, width=2, edge_color=edge_weights, edge_cmap=plt.cm.plasma)
    edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title("📊 Spearman Correlation Graph (Threshold ≥ 0.5)")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# --- Folder path and pipeline ---
folder_path = "data/1week"
file_names, all_correlations = compute_valid_correlations(folder_path)
pairwise_edges = compute_pairwise_spearman(file_names, all_correlations, threshold=0.8)
build_and_draw_graph(pairwise_edges)
