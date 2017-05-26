#!/usr/bin/env bash


source ./kuber_env.sh

function kubernetes_init()
{
    kubeadm init --pod-network-cidr 10.244.0.0/16 --kubernetes-version v1.6.3
    cat ~/.bashrc | grep KUBECONFIG 
    if [ $? -ne 0 ]
    then
        echo 'export KUBECONFIG=/etc/kubernetes/admin.conf' >> ~/.bashrc
    fi
    source ~/.bashrc
}


function kubernetes_flannel()
{
    kubectl create -f https://github.com/coreos/flannel/raw/master/Documentation/kube-flannel-rbac.yml
    kubectl create -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
}


stop_firewallSelinux
KubernetesInstall $kubernetesReop
get_GcrImage $github $dockerhub $gcr

kubernetes_init
kubernetes_flannel

echo "you can run \"kubeadm token list\" in master to see tokens"
