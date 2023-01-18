import sys
import os
import numpy as np
import matplotlib.pyplot as plot

if __name__=="__main__":
    path = os.path.join(sys.argv[1])

    MB_chunk_count_plot, MB_chunk_count_ax = plot.subplots()
    # first value is best, second is average, then min and max
    node_MB_chunk_count_dict = {}
    # sample count in a file
    sample_count = 0
    with open(path) as result_fin:
        for logline in result_fin.readlines():
            logline_tokens = logline.split()

            if logline_tokens[3] == "Normal":
                node_id = int(logline_tokens[1][:-1])
                if node_id not in node_MB_chunk_count_dict:
                    node_MB_chunk_count_dict[node_id] = {}
                for i in range(9, 15, 1):
                    if i not in node_MB_chunk_count_dict[node_id]:
                        node_MB_chunk_count_dict[node_id][i] = []
                    val = int(logline_tokens[i])
                    node_MB_chunk_count_dict[node_id][i].append(val)

    for node_id in node_MB_chunk_count_dict.keys():
        for MB_chunk_val in node_MB_chunk_count_dict[node_id]:
            node_val_list = node_MB_chunk_count_dict[node_id][MB_chunk_val]
            times = [i*10 for i in range(len(node_val_list))]
            MB_chunk_count_ax.plot(times, node_val_list, label="Node {0}:{1}MB".format(node_id, 2**(MB_chunk_val-9)))

    MB_chunk_count_ax.legend()
    MB_chunk_count_plot.savefig("MB_chunk_count_vs_time.png")