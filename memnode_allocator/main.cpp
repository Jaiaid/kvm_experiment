#include <iostream>
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <memory>

#include "system_analyser.h"

#define NUMA_NODE_COUNT 1

#define MAX_CONFIGURATION_FILE_CHAR_COUNT 8191
#define TEMPLATE_PART1_FILEPATH "template_preamble.part"
#define TEMPLATE_NUMATUNE_FILEPATH "numatune.part"
#define TEMPLATE_TAIL_FILEPATH "template_tail.part"

#define NUMATUNE_START_TAG "  <numatune>\n"
#define NUMATUNE_FINISH_TAG "  </numatune>\n"
#define MEMORY_NODE_TAG_FMTSTR "    <memory nodeset='%s'/>\n"
#define MEMORY_INTERLEAVE_PART "    <memory mode='interleave' nodeset='%s'/>\n"

int numa_dist_matrix[NUMA_NODE_COUNT][NUMA_NODE_COUNT] = {{1}};//{{10,21},{21,10}};

void random_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf);
void interleave_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf);
void local_pref_interleaved_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf);


void read_whole_file(const char* fpath, char* buf, int position);
void create_file(const char* fpath, const char* buf);

int main()
{
    auto system = std::make_unique<SystemAnalyser>();

    int allocated_vm_count = 0;
    int cpu, memory_mib;
    char configuration_build[MAX_CONFIGURATION_FILE_CHAR_COUNT + 1];
    char configuration_footer[MAX_CONFIGURATION_FILE_CHAR_COUNT + 1];
    char vm_define_cmd[MAX_CONFIGURATION_FILE_CHAR_COUNT + 1];
    char vm_start_cmd[MAX_CONFIGURATION_FILE_CHAR_COUNT + 1];

    // read the templates, two file to read from
    // read the preamble
    read_whole_file(TEMPLATE_PART1_FILEPATH, configuration_build, MAX_CONFIGURATION_FILE_CHAR_COUNT);
    int preamble_length = strlen(configuration_build);
    // read the footer
    read_whole_file(TEMPLATE_TAIL_FILEPATH, configuration_footer, MAX_CONFIGURATION_FILE_CHAR_COUNT);

    while(scanf("%d%d", &cpu, &memory_mib)!=EOF)
    {
        std::string vm_name = "vm" + std::to_string(allocated_vm_count);
        std::string template_name = vm_name + "_template.xml";

        // get memory node configuration from scheduler algorithm
        // function will copy it at provided char*
        // random_alloc_conf_generation(&numa_dist_matrix[0][0], NUMA_NODE_COUNT, &configuration_build[preamble_length]);
        interleave_alloc_conf_generation(&numa_dist_matrix[0][0], NUMA_NODE_COUNT, &configuration_build[preamble_length]);
        // copy the remaining part to build the final configuration build at proper offset
        int offset = strlen(configuration_build);
        strcpy(&configuration_build[offset], configuration_footer);

        // create the template file with memory configuration
        create_file(template_name.c_str(), configuration_build);

        printf("allocating vm %d with %d cpu and %d MiB memory\n", allocated_vm_count, cpu, memory_mib);
        printf("defining vm\n");
        snprintf(vm_define_cmd, MAX_CONFIGURATION_FILE_CHAR_COUNT,
        "../scripts/define_vm.sh -n %s -t %s -m %d -c %d -i ../image/focal-server-cloudimg-amd64.img\n", vm_name.c_str(), template_name.c_str(), memory_mib, cpu);
        printf("%s\n%s\n", vm_define_cmd, vm_start_cmd);

        system->RunCommand(vm_define_cmd);
        allocated_vm_count++;
    }

    for(int i=0;i<allocated_vm_count;i++)
    {
        std::string vm_name = "vm" + std::to_string(i);
        snprintf(vm_start_cmd, MAX_CONFIGURATION_FILE_CHAR_COUNT, "virsh start %s\n", vm_name.c_str());
        system->RunCommand(vm_start_cmd);
    }

    return 0;
}

void read_whole_file(const char* fpath, char* buf, int max_read_count)
{
    std::ifstream template_f(fpath);
    template_f.read(buf, max_read_count);
    template_f.close();
}

void create_file(const char* fpath, const char* buf)
{
    std::ofstream template_f(fpath);
    template_f.write(buf, strlen(buf));
    template_f.close();
}

void random_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf)
{
    int memnode_id = rand()%node_count;
    snprintf(conf_buf, MAX_CONFIGURATION_FILE_CHAR_COUNT, NUMATUNE_START_TAG MEMORY_NODE_TAG_FMTSTR NUMATUNE_FINISH_TAG, std::to_string(memnode_id).c_str());
}

void interleave_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf)
{
    // interleaved memory allocation across all available NUMA node
    snprintf(conf_buf, MAX_CONFIGURATION_FILE_CHAR_COUNT, NUMATUNE_START_TAG "<memory mode='interleave' nodeset='0-%d'/>"  NUMATUNE_FINISH_TAG, node_count-1);
}


void local_pref_interleaved_alloc_conf_generation(int* numa_dist_matrix, int node_count, char* conf_buf)
{

}
