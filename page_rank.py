import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    graph = {}
    for line in args.datafile:
        node, target = line.split()
        if node not in graph:
            graph[node] = []
        graph[node].append(target)
    return graph

def print_stats(graph):
    num_nodes = len(graph)
    num_edges = sum(len(targets) for targets in graph.values())
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

def stochastic_page_rank(graph, args):
    hit_count = {node: 0 for node in graph}
    num_nodes = len(graph)
    
    # Perform the random walks
    for _ in range(args.repeats):
        current_node = random.choice(list(graph.keys()))  # Start at a random node
        hit_count[current_node] += 1
        
        for _ in range(args.steps):
            if current_node not in graph or len(graph[current_node]) == 0:
                current_node = random.choice(list(graph.keys()))  # No outgoing links, choose a new random node
            else:
                current_node = random.choice(graph[current_node])  # Move to a random target
            hit_count[current_node] += 1

    # Return the hit counts as the PageRank approximation
    return hit_count


def distribution_page_rank(graph, args):
    num_nodes = len(graph)
    node_prob = {node: 1 / num_nodes for node in graph}
    
    # Initialize the progress bar for the distribution algorithm
    prog = Progress(args.steps, "Running distribution page rank")
    
    for step in range(args.steps):
        next_prob = {node: 0 for node in graph}
        
        for node, targets in graph.items():
            if len(targets) == 0:
                continue  # Skip nodes with no out-links
            
            probability = node_prob[node] / len(targets)
            for target in targets:
                next_prob[target] += probability
        
        node_prob = next_prob
        
        prog += 1  # Update progress bar after each step
    
    prog.finish()  # Finish the progress bar
     
    return node_prob




parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
 ##CURENT CALCULATION TIME AROUND 60s