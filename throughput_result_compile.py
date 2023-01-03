import re
import argparse
import os
import numpy as np

REGEX_COPY_RESULT_OUTPUT = \
    r"Copy:\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)"
REGEX_SCALE_RESULT_OUTPUT = \
    r"Scale:\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)"
REGEX_TRIAD_RESULT_OUTPUT = \
    r"Triad:\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)"
REGEX_ADD_RESULT_OUTPUT = \
    r"Add:\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)\s*(\d+\.?\d*)"


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", "--input_dir", help="folder path containing the input files", required=True)
    
    # get cmd line arguments
    args = parser.parse_args()
    
    avg_copy_throughput_MB_per_host = []
    avg_scale_throughput_MB_per_host = []
    avg_triad_throughput_MB_per_host = []
    avg_add_throughput_MB_per_host = []
    
    for filename in os.listdir(args.input_dir):
        if not filename.endswith('.expresult'):
            continue

        path = os.path.join(args.input_dir, filename)
        
        # first value is best, second is average, then min and max
        copy_host_vals = [0, 0, 0, 0]
        scale_host_vals = [0, 0, 0, 0]
        add_host_vals = [0, 0, 0, 0]
        triad_host_vals = [0, 0, 0, 0]
        # sample count in a file
        val_occurance = 0
        with open(path) as result_fin:
            for logline in result_fin.readlines():
                logline = logline.split('\n')[0]
                
                result = re.search(REGEX_COPY_RESULT_OUTPUT, logline)
                if result is not None:
                    # four ops values stays line by line, so one is enough to calculate occurance
                    val_occurance += 1
                    copy_host_vals[0] += float(result.groups()[0])
                    copy_host_vals[1] += float(result.groups()[1])
                    copy_host_vals[2] += float(result.groups()[2])
                    copy_host_vals[3] += float(result.groups()[3])
                
                result = re.search(REGEX_SCALE_RESULT_OUTPUT, logline)
                if result is not None:
                    scale_host_vals[0] += float(result.groups()[0])
                    scale_host_vals[1] += float(result.groups()[1])
                    scale_host_vals[2] += float(result.groups()[2])
                    scale_host_vals[3] += float(result.groups()[3])
                
                
                result = re.search(REGEX_TRIAD_RESULT_OUTPUT, logline)
                if result is not None:
                    triad_host_vals[0] += float(result.groups()[0])
                    triad_host_vals[1] += float(result.groups()[1])
                    triad_host_vals[2] += float(result.groups()[2])
                    triad_host_vals[3] += float(result.groups()[3])
                
                
                result = re.search(REGEX_ADD_RESULT_OUTPUT, logline)
                if result is not None:
                    add_host_vals[0] += float(result.groups()[0])
                    add_host_vals[1] += float(result.groups()[1])
                    add_host_vals[2] += float(result.groups()[2])
                    add_host_vals[3] += float(result.groups()[3])
        
        print(path)
        # average all the samples for each operation
        for i in range(4):
            copy_host_vals[i] /= val_occurance
            scale_host_vals[i] /= val_occurance
            triad_host_vals[i] /= val_occurance
            add_host_vals[i] /= val_occurance
        print
        
        avg_copy_throughput_MB_per_host.append(copy_host_vals)
        avg_scale_throughput_MB_per_host.append(scale_host_vals)
        avg_triad_throughput_MB_per_host.append(triad_host_vals)
        avg_add_throughput_MB_per_host.append(add_host_vals)
        
    copy_throughput_array = np.array(avg_copy_throughput_MB_per_host)
    scale_throughput_array = np.array(avg_scale_throughput_MB_per_host)
    triad_throughput_array = np.array(avg_triad_throughput_MB_per_host)
    add_throughput_array = np.array(avg_add_throughput_MB_per_host)
    
    print("Copy Operation throughput averaged over all vms (Best MB/s, Avg time, Min time, Max time):")
    print(np.mean(copy_throughput_array, axis=0))
    
    print("Scale Operation throughput averaged over all vms (Best MB/s, Avg time, Min time, Max time):")
    print(np.mean(scale_throughput_array, axis=0))
    
    print("Triad Operation throughput averaged over all vms (Best MB/s, Avg time, Min time, Max time):")
    print(np.mean(triad_throughput_array, axis=0))
    
    print("Add Operation throughput averaged over all vms (Best MB/s, Avg time, Min time, Max time):")
    print(np.mean(add_throughput_array, axis=0))
