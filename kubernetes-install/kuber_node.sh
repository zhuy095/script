#!/usr/bin/env bash


function echoUsage()
{
    echo "Usage: $1 Token MasterIP"
    echo "you can run \"kubeadm token list\" in master to see tokens"
    exit 200   
}


if [ -z $1 ] || [ -z $2 ]
then
    echoUsage $0
fi


source ./kuber_env.sh

stop_firewallSelinux
KubernetesInstall $kubernetesReop
get_GcrImage $github $dockerhub $gcr

kubeadm join --token $1 $2:6443