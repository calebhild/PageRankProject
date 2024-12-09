import sys
import argparse
import time
import numpy as np
from scipy.sparse import csr_matrix
from progress import Progress

def load_graph(args):
    nodes = {}  # Map from node to index
    edges = []  # Store edges as (source, target)

    for line in args.datafile:
        src, tgt = line.split()
        if src not in nodes:
            nodes[src] = len(nodes)
        if tgt not in nodes:
            nodes[tgt] = len(nodes)
        edges.append((nodes[src], nodes[tgt]))

    num_nodes = len(nodes)
    row = np.array([src for src, tgt in edges], dtype=np.int32)
    col = np.array([tgt for src, tgt in edges], dtype=np.int32)
    data = np.ones(len(edges), dtype=np.float32)

    # Build a sparse adjacency matrix
    adjacency_matrix = csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes))
    return adjacency_matrix, list(nodes.keys())

def print_stats(graph):
    num_nodes = graph.shape[0]
    num_edges = graph.nnz
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

def stochastic_page_rank(graph, args):
    num_nodes = graph.shape[0]
    hit_count = np.zeros(num_nodes, dtype=np.int32)

    # Perform random walks
    for _ in range(args.repeats):
        current_node = np.random.randint(0, num_nodes)
        hit_count[current_node] += 1
        for _ in range(args.steps):
            if graph[current_node].nnz == 0:  # Dead end
                current_node = np.random.randint(0, num_nodes)
            else:
                current_node = np.random.choice(graph[current_node].indices)
            hit_count[current_node] += 1

    # Normalise hit counts to get probabilities
    return hit_count / hit_count.sum()

def distribution_page_rank(graph, args):
    num_nodes = graph.shape[0]
    node_prob = np.full(num_nodes, 1 / num_nodes, dtype=np.float32)
    prog = Progress(args.steps, "Running distribution PageRank")

    # Normalise adjacency matrix rows
    row_sums = np.array(graph.sum(axis=1)).flatten()
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    transition_matrix = csr_matrix(graph.multiply(1 / row_sums[:, None]))

    for _ in range(args.steps):
        node_prob = transition_matrix.T @ node_prob
        prog += 1

    prog.finish()
    return node_prob

parser = argparse.ArgumentParser(description="Estimates PageRanks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Text file of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="Selected PageRank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="Number of random walks")
parser.add_argument('-s', '--steps', type=int, default=100, help="Number of steps per walk")
parser.add_argument('-n', '--number', type=int, default=20, help="Number of top results to display")

if __name__ == '__main__':
    args = parser.parse_args()
    graph, node_names = load_graph(args)
    print_stats(graph)

    start = time.time()
    if args.method == 'stochastic':
        ranking = stochastic_page_rank(graph, args)
    else:
        ranking = distribution_page_rank(graph, args)
    stop = time.time()

    top = np.argsort(ranking)[::-1]
    sys.stderr.write(f"Top {args.number} pages:\n")
    for i in range(args.number):
        sys.stderr.write(f"{100 * ranking[top[i]]:.2f}\t{node_names[top[i]]}\n")
    sys.stderr.write(f"Calculation took {stop - start:.2f} seconds.\n")
