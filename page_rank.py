import sys
import argparse
import time
import numpy as np
from scipy.sparse import csr_matrix
from progress import Progress
import multiprocessing                                                      # Import for parallel processing

'''Comments are placed to the right of each line.'''

def load_graph(args):
    """
    Load the graph from the input file and build a sparse adjacency matrix.
    """
    nodes = {}                                                              # Map from node names to unique indices
    edges = []                                                              # List of edges

# Read edges from the input file
    for line in args.datafile:
        line = line.strip()                                                 # Remove whitespace
        # Skip empty lines or lines that do not contain exactly two elements
        if not line or len(line.split()) != 2:
            continue
        
        src, tgt = line.split()                                             # Unpack the source and target nodes
        if src not in nodes:
            nodes[src] = len(nodes)                                         # Assign a unique index to each source node
        if tgt not in nodes:
            nodes[tgt] = len(nodes)                                         # Assign a unique index to each target node
        edges.append((nodes[src], nodes[tgt]))                              # Add edge as indices

    num_nodes = len(nodes)                                                  # Total number of unique nodes
    row = np.array([src for src, tgt in edges], dtype=np.int32)             # Source indices
    col = np.array([tgt for src, tgt in edges], dtype=np.int32)             # Target indices
    data = np.ones(len(edges), dtype=np.float32)                            # Edge weights (all 1s for unweighted graph)

    # Build the sparse adjacency matrix
    adjacency_matrix = csr_matrix((data, (row, col)), shape=(num_nodes, num_nodes))
    return adjacency_matrix, list(nodes.keys())                             # Return matrix and list of nodes

def print_stats(graph):
    """
    Print basic stats about the graph.
    """
    num_nodes = graph.shape[0]                                              # Number of nodes (rows in matrix)
    num_edges = graph.nnz                                                   # Number of edges (non-zero entries in matrix)
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

def stochastic_page_rank(graph, args):
    """
    Compute PageRank using the stochastic random walk method.
    """
    num_nodes = graph.shape[0]                                              # Total number of nodes
    hit_count = np.zeros(num_nodes, dtype=np.int32)                         # Array to count hits for each node

    # Perform random walks
    for _ in range(args.repeats):
        current_node = np.random.randint(0, num_nodes)                      # Start at a random node
        hit_count[current_node] += 1                                        # Increment hit count for starting node
        for _ in range(args.steps):
            if graph[current_node].nnz == 0:                                # Dead end: node has no outgoing links
                current_node = np.random.randint(0, num_nodes)              # Restart at a random node
            else:
                # Choose a random outgoing link
                current_node = np.random.choice(graph[current_node].indices)
            hit_count[current_node] += 1                                    # Increment hit count for the visited node

    # Normalise hit counts to calculate probabilities
    return hit_count / hit_count.sum()

def distribution_page_rank(graph, args):
    """
    Compute PageRank using the distribution-based iterative method.
    """
    num_nodes = graph.shape[0]                                              # Total number of nodes
    node_prob = np.full(num_nodes, 1 / num_nodes, dtype=np.float32)         # Initial uniform probabilities (all nodes have equal probablility of being in the ranked page)
    prog = Progress(args.steps, "Running distribution PageRank")            # Progress bar

# Normalise adjacency matrix rows to create a transition matrix
    row_sums = np.array(graph.sum(axis=1)).flatten()                        # Sum of outgoing links for each node
    row_sums[row_sums == 0] = 1                                             # Avoid division by zero for nodes with no outgoing links
    transition_matrix = csr_matrix(graph.multiply(1 / row_sums[:, None]))   # Normalise rows

    for _ in range(args.steps):
        node_prob = transition_matrix.T @ node_prob                         # Update probabilities via matrix multiplication
        prog += 1                                                           # Update progress bar

    prog.finish()                                                           # Finish the progress bar
    return node_prob

# Parallelised stochastic PageRank
def parallel_stochastic_page_rank(graph, args):
    """
    Compute PageRank using the parallelised stochastic random walk method.
    """
    num_nodes = graph.shape[0]                                              # Total number of nodes
    hit_count = np.zeros(num_nodes, dtype=np.int32)                         # Array to count hits for each node

    # Function for a single random walk
    def walk(start_node):
        local_hit_count = np.zeros(num_nodes, dtype=np.int32)
        current_node = start_node
        local_hit_count[current_node] += 1
        for _ in range(args.steps):
            if graph[current_node].nnz == 0:                                # Dead end: node has no outgoing links
                current_node = np.random.randint(0, num_nodes)              # Restart at a random node
            else:
                current_node = np.random.choice(graph[current_node].indices)
            local_hit_count[current_node] += 1
        return local_hit_count

    # Use multiprocessing for the random walks
    with multiprocessing.Pool() as pool:
        results = pool.map(walk, np.random.randint(0, num_nodes, args.repeats)) # Parallel random walks
        for result in results:
            hit_count += result

    # Normalise hit counts to calculate probabilities
    return hit_count / hit_count.sum()

# Command line argument parsing
parser = argparse.ArgumentParser(description="Estimates PageRanks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Text file of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="Selected PageRank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="Number of random walks")
parser.add_argument('-s', '--steps', type=int, default=100, help="Number of steps per walk")
parser.add_argument('-n', '--number', type=int, default=20, help="Number of top results to display")

if __name__ == '__main__':
    # Parse command line arguments
    args = parser.parse_args()

    # Load the graph and print stats
    graph, node_names = load_graph(args)
    print_stats(graph)

    # Choose the algorithm and run it
    start = time.time()
    if args.method == 'stochastic':
        ranking = parallel_stochastic_page_rank(graph, args)                  # Use parallel version for stochastic
    else:
        ranking = distribution_page_rank(graph, args)
    stop = time.time()

    # Display the top ranked nodes
    top = np.argsort(ranking)[::-1]                                           # Sort nodes by PageRank in descending order
    sys.stderr.write(f"Top {args.number} pages:\n")
    for i in range(args.number):
        sys.stderr.write(f"{100 * ranking[top[i]]:.2f}\t{node_names[top[i]]}\n") # Print the top sites
    sys.stderr.write(f"Calculation took {stop - start:.2f} seconds.\n")       # Print how long the calculation took
