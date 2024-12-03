import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=str, help="Input file containing the graph")
    args = parser.parse_args()

    # Open the file
    with open(args.filename, "r") as file:
        args.datafile = file
        graph = load_graph(args)
        print("Loaded graph:")
        for node, targets in graph.items():
            print(f"{node} -> {', '.join(targets)}")
