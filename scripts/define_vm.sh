#!/bin/bash

ROOT_DIR='/home/jm5071/Desktop/kvm_experiment/'

DISK_SIZE=2G
MEMORY=2048
CPU=1
UUID=$(cat /proc/sys/kernel/random/uuid)
VM_NAME=`openssl rand -base64 12`
TEMP_CONF_PATH=;
TEMP_IMAGE_PATH=;
CDROM=;

# template configuration xml
TEMP_CONFIGURATION_XML=../confs/template.xml

# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Provided size of disk and name of the template image, create a new vm"
   echo
   echo "Syntax: create_vm.sh [-s <disk size>] [-h] [-i <template image file path>] [-m <memory amount in MiB>] [-c <core count>] [-t <template configuration file>]"
   echo "options:"
   echo "s     give the "
   echo "h     Print Help."
   echo
}

# parse cmd line arg
while getopts "hs:i:n:m:c:t:" option; do
   case $option in
      h) # display Help
         Help;
         exit;;
      s)
         DISK_SIZE=${OPTARG};;
      i)
         TEMP_IMAGE_PATH=${OPTARG};;
      n)
         VM_NAME=${OPTARG};;
      m)
         MEMORY=${OPTARG};;
      c)
         CPU=${OPTARG};;
      t)
         TEMP_CONF_PATH=${OPTARG};;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# create separate img file for new vm from the template
# create only if template is newer
echo ${TEMP_IMAGE_PATH}
echo ${ROOT_DIR}/vm_installed_images/${VM_NAME}.img
cp ${TEMP_IMAGE_PATH} -u ${ROOT_DIR}/vm_installed_images/${VM_NAME}.img
VM_IMAGE_PATH=${ROOT_DIR}/vm_installed_images/${VM_NAME}.img
# default 2
# install to define the vm and start it
# if success go to  console
# virt-install --virt-type=kvm --name=${IMAGE_NAME} --vcpus=2 --memory=1024 --disk path=${VM_IMAGE_PATH},format=raw --check path_in_use=off --graphics none --network default  && virsh console ${IMAGE_NAME}
# create the template
sed -e "s;%NAME%;${VM_NAME};g" -e "s;%UUID%;${UUID};g" -e "s;%MEMORY%;${MEMORY};g" \
-e "s;%CPU%;${CPU};g" -e "s;%IMAGE_PATH%;${VM_IMAGE_PATH};g" ${TEMP_CONF_PATH} > \
${ROOT_DIR}/conf/${VM_NAME}.xml
# create the domain
virsh define ${ROOT_DIR}/conf/${VM_NAME}.xml
