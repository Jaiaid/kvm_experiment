import re
import argparse
import os
import matplotlib.pyplot as plot

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
    
    # to show all the vms change in one plot
    combined_copy_fig, combined_copy_fig_ax = plot.subplots()
    combined_scale_fig, combined_scale_fig_ax = plot.subplots()
    combined_add_fig, combined_add_fig_ax = plot.subplots()
    combined_triad_fig, combined_triad_fig_ax = plot.subplots()
    
    
    for filename in os.listdir(args.input_dir):
        if not filename.endswith('.expresult'):
            continue

        path = os.path.join(args.input_dir, filename)
        
        # first value is best, second is average, then min and max
        copy_host_vals = [[], [], [], []]
        scale_host_vals = [[], [], [], []]
        add_host_vals = [[], [], [], []]
        triad_host_vals = [[], [], [], []]
        # sample count in a file
        val_occurance = 0
        with open(path) as result_fin:
            for logline in result_fin.readlines():
                logline = logline.split('\n')[0]
                
                result = re.search(REGEX_COPY_RESULT_OUTPUT, logline)
                if result is not None:
                    # four ops values stays line by line, so one is enough to calculate occurance
                    val_occurance += 1
                    copy_host_vals[0].append(float(result.groups()[0]))
                    copy_host_vals[1].append(float(result.groups()[1]))
                    copy_host_vals[2].append(float(result.groups()[2]))
                    copy_host_vals[3].append(float(result.groups()[3]))
                
                result = re.search(REGEX_SCALE_RESULT_OUTPUT, logline)
                if result is not None:
                    scale_host_vals[0].append(float(result.groups()[0]))
                    scale_host_vals[1].append(float(result.groups()[1]))
                    scale_host_vals[2].append(float(result.groups()[2]))
                    scale_host_vals[3].append(float(result.groups()[3]))
                
                
                result = re.search(REGEX_TRIAD_RESULT_OUTPUT, logline)
                if result is not None:
                    triad_host_vals[0].append(float(result.groups()[0]))
                    triad_host_vals[1].append(float(result.groups()[1]))
                    triad_host_vals[2].append(float(result.groups()[2]))
                    triad_host_vals[3].append(float(result.groups()[3]))
                
                
                result = re.search(REGEX_ADD_RESULT_OUTPUT, logline)
                if result is not None:
                    add_host_vals[0].append(float(result.groups()[0]))
                    add_host_vals[1].append(float(result.groups()[1]))
                    add_host_vals[2].append(float(result.groups()[2]))
                    add_host_vals[3].append(float(result.groups()[3]))

        
        # generate a line plot of throughput for copy operation
        x = list(range(len(copy_host_vals[0])))
        
        # to show per vms change in plot
        fig, fig_ax = plot.subplots()
        fig_ax.plot(x, copy_host_vals[0], label="copy")
        fig_ax.plot(x, scale_host_vals[0], label="scale")
        fig_ax.plot(x, add_host_vals[0], label="add")
        fig_ax.plot(x, triad_host_vals[0], label="triad")
        fig_ax.legend()
        fig.savefig(os.path.join(args.input_dir, "vm_{0}.png".format(filename)))
        
        combined_copy_fig_ax.plot(x, copy_host_vals[0])
        combined_scale_fig_ax.plot(x, scale_host_vals[0])
        combined_add_fig_ax.plot(x, add_host_vals[0])
        combined_triad_fig_ax.plot(x, triad_host_vals[0])
    
    combined_copy_fig.savefig(os.path.join(args.input_dir, "all_vm_change_throughput_copy_operation.png"))
    combined_scale_fig.savefig(os.path.join(args.input_dir, "all_vm_change_throughput_scale_operation.png"))
    combined_triad_fig.savefig(os.path.join(args.input_dir, "all_vm_change_throughput_triad_operation.png"))
    combined_add_fig.savefig(os.path.join(args.input_dir, "all_vm_change_throughput_add_operation.png"))