#!/bin/bash

DISK_SIZE=2G
IMAGE_NAME=`openssl rand -base64 12`
IMAGE_PATH=;
CDROM=;

# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Provided size of disk and name of cdrom(iso), create a disk image for kvm"
   echo
   echo "Syntax: create_disk.sh [-s <disk size>] [-h] [-d <output disk path>] [-i <iso file path>]"
   echo "options:"
   echo "s     give the "
   echo "h     Print Help."
   echo
}

# parse cmd line arg
while getopts "hs:d:n:i:" option; do
   case $option in
      h) # display Help
         Help;
         exit;;
      s) 
         DISK_SIZE=${OPTARG};;
      i)
         CDROM=${OPTARG};;
      d)
         IMAGE_PATH=${OPTARG};;
      n)
         IMAGE_NAME=${OPTARG};;
     \?) # Invalid option
         echo "Error: Invalid option"
         exit;;
   esac
done

# create qemu-img of given size
# default 2GB
qemu-img create -f qcow2 ${IMAGE_PATH} ${DISK_SIZE}
# install iso to created disk
# if success go to  console
virt-install --connect qemu:///system --virt-type=kvm --name=${IMAGE_NAME} --cdrom=${CDROM} --vcpus=2 --memory=1024 --disk path=${IMAGE_PATH},format=qcow2 --check path_in_use=off --graphics none --network default --serial pty && virsh console ${IMAGE_NAME}
