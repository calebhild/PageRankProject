# PageRankProject
## CSC1034 Case Study 3
```bash
>>> python3 page_rank.py school_web2024-1.txt -m distribution -s 1000 -n 20
Returns:
Number of nodes: 515
Number of edges: 10,462
Top 20 pages:
x

Calculation took: z seconds.
```

## Code Optimisation (Written Report)

Once the code was working as expected, I shifted my focus to improving performance and reducing the calculation time. Initially, the program took over 50 seconds to compute the top 20 pages, which was unacceptable. I needed to find ways to handle large datasets more efficiently.

### 1. Progress Bar Optimisation:
The first optimisation I made was adjusting the progress bar in the progress.py file by adding a 'frequency' parameter to control how often it updates. Originally, the progress bar updated after every single step, even when the calculations were quick, which unnecessarily slowed the program down. By setting the progress bar to update only every 500 steps, I reduced the overhead. This change did speed things up slightly—cutting about 5 seconds off the total time, bringing it down to 55.60 seconds for 100,000 steps.

### 2. Dictionary to defaultdict(list):
Next, I switched from a regular dictionary to a defaultdict(list) for storing the graph. This change was beneficial because the defaultdict automatically creates an empty list for each new key, eliminating the need to check if a node already exists before adding a target. This simplification sped up the graph-building process, especially when dealing with a large number of nodes and edges.

### 3. Transition to Sparse Adjacency Matrix:
Even after these improvements, the performance was not optimal, so I replaced the defaultdict with a sparse adjacency matrix. Using the csr_matrix (Compressed Sparse Row) format significantly improved memory efficiency and speed. This format allows for faster matrix operations, such as multiplication, which are essential for PageRank calculations. Additionally, I normalised the rows of the adjacency matrix to create a transition matrix, further streamlining the PageRank calculations. This reduced the computation time to about 2 seconds.

### 4. Parallel Processing:
To speed up the computation further, I introduced parallel processing into the stochastic algorithm. Since the stochastic algorithm involves running many independent random walks, I distributed the work across multiple CPU cores. Each core handled a subset of the walks, providing near-linear speedup based on the number of available cores. For example, on a 4-core processor, the time could be reduced by approximately four times. This required modifying the stochastic_page_rank() function to use multiprocessing, while the distribution_page_rank() method remained unchanged, as it doesn’t benefit from parallelisation in the same way.

### Conclusion

These optimisations had a significant impact on performance, reducing the total calculation time from 60 seconds to approximately 1.5 seconds. This was achieved through a combination of improvements, including the enhancement of memory efficiency and faster processing using a sparse adjacency matrix. Parallel processing enabled random walks to be distributed across multiple CPU cores, which led to near-linear speedup. Additionally, reducing unnecessary overhead with the progress bar optimisation further contributed to the reduced calculation time.

Each optimisation played a crucial role in enhancing the program's ability to handle large datasets quickly and efficiently.