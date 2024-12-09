# PageRankProject
CSC1034 Case Study 3

Running the File in the Terminal: 
>>> python3 page_rank.py school_web2024-1.txt -m distribution -s 1000 -n 20

Returns:
Number of nodes: 515
Number of edges: 10462
Top 20 pages:
x

# Code Optimisation
Once I had the code running how I expected I was ready to start optimising the code to reduce the calculation time. Upon finnishing the code, the time it took to gather the Top 20 pages was 53.95 seconds. This was far to slow and I needed a way of optimising it.


Firstly I began by changing the progress.py file by adding a 'frequency' parameter, this will control how often the progress bar updates as at the moment it updates everytime, even when a calculation is very quick. By making these changes the code will now only update the progress bar every 500 steps. This did infact speed up my program however not by a noticable amount, reducing it by about 5 seconds, resulting in a calculation time of 55.60 seconds with 100000 steps. 
