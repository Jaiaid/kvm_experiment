# KVM Experiment

Some experiment done to observe effect of controlling NUMA node of VM memory. Target observation was to check if changing NUMA allocation can achieve better throughput for VM applications. The experiments were inconclusive and discontinued. This repo may be helpful if someone is looking for followings,
* multiple VM define/creation based on stored image targeted to run using virsh+libvirt
* qemu based virtual machine start

## Prerequisite
I kind of forgot but basically you need libvirt library for virtualization, virsh for controlling vm, libnuma for numa allocation and and qemu for emulation. Probably installing libvirt will suffice
```
sudo apt-get install libvirt libvirt-clients qemu-kvm
```

## Scripts
Scripts are used by C code in memnode_allocator directory. There are two scripts
 1. create_disk.sh : To create the disk with specific size (parameter given to script execution, default 2G) for virtual machine
 2. define_vm.sh : To define virtual machine configuration xml file based on which using virsh we can start a qemu vm.

Both scripts has help menu. To see,
```
bash create_disk.sh -h
```
```
bash define_vm.sh -h
```

## Code
memnode_allocator directory contains some C code. main.cpp contains main function. This program will take cpu node count and memory in MiB in each line. It will continue until EoF. After each line, it will create disk and xml defn. file from the template provided in same directory (the templates are provided in conf directory of this repo). After creating defn. it will start the VM through virsh cmd. Sample input can be found in input1.txt to create and define two VM.

To build,
```
g++ main.cpp -o main.out
```
Example run,
```
./main.out < input1.txt
```

main.cpp contains different function. This function are responsible for allocating memory for VM across NUMA nodes. It is done by controlling <Memory><\Memory> tag in the defn. file for VM. This is controlled by changing in code. Function call for generating defn. string is in line 59 of main.cpp . There are three policy implementation can be found in main.cpp
 1. random_alloc_conf_generation : randomly one NUMA node is selected for memory for the VM
 2. interleave_alloc_conf_generation : according to provided node count memory will be allocated interleaving manner from 0 upto the given node
 3. single_node_round_robin_alloc_conf_generation : Among 0 to upto given nodeid one node is assigned to the VM and for next another. This change is done in round robin fashion.

## STREAM mod
Above NUMA policies effects are checked for single program by modifying STREAM and modifying its memory allocation for the memory array on which it operates and generate time data. libnuma is used to control allocation at NUMA level.

To build,
```
gcc page_allocation_across_node_simulation_rand_access.c -fopenmp -lnuma -o <exec name>
gcc page_allocation_across_node_simulation_seq_access.c -fopenmp -lnuma -o <exec name>
```
To generate output result
```
<exec name> > result.txt
```
This STREAM program's throughput, latency, and while running the memory compaction state can be analyzed by given python scripts (the input files are generated as result of running the VMs, VMs send the image to main host through scp),
```
python3 mem_compaction_change_plot.py <mem compaction log>
# to analyze per VMs
python3 throughput_change_plot_perhost.py -dir <folder containing VMs output file>
# to generate average performance data
python3 throughput_result_compile.py -dir <folder containing VMs output file>
```

## Modified VM
I have lost the modified ubuntu image to create VM image which will run STREAM. I will come back after I find it.
    
