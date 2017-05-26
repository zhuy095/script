#!/usr/bin/env bash

github='https://github.com/zhuyongliang095/gcr.io.git'
dockerhub='yongliang095/gcr-images'
kubernetesReop='http://sunyasec.com/yum/centos7/kubernetes'
gcr='gcr.io/google_containers'


function KubernetesInstall()
{
    rpm -qa | grep kubelet 
    if [ $? -eq 0 ]
    then
        return
    fi

    if [ -n $1 ] 
    then
        reop=$1
    else
        echo" no kubernetes repo links"
        exit 200
    fi

    cat << OEF > /etc/yum.repos.d/kubernetes.repo 
[kubernetes]
name=kubernetes
baseurl=$reop
enabled=1
gpgcheck=0
OEF
    yum clean all
    yum makecache
    yum install -y docker kubelet kubeadm kubectl kubernetes-cni
    systemctl enable docker && systemctl start docker
    systemctl enable kubelet && systemctl start kubelet
}

function pull_gcrImage()
{
    dockerhub=$1
    gcr=$2
    stat=true
    for file in ` find . -name Dockerfile | xargs `
    do
        image=`cat ${file} | awk -F'/' '{print $3}'| awk -F':' '{print $1}' | sed 's/-amd64//g'`
        tag=`cat ${file} | awk -F'/' '{print $3}'| awk -F':' '{print $2}' `
        docker images | grep ${image} 
        if [[ $? -ne 0 ]]
        then
            echo "log : local no have ${image} "
            docker pull ${dockerhub}:${image}
            if [ $? -ne 0 ] ; then stat=false; fi
            if [ ${image} != "flannel" ]
            then
                docker tag ${dockerhub}:${image}  ${gcr}/${image}-amd64:${tag} 
            else
                docker tag ${dockerhub}:${image}  "quay.io/coreos"/${image}:${tag}
            fi
            docker rmi ${dockerhub}:${image}
        fi
    done
    if [ $stat == false ] 
    then
        pull_gcrImage $dockerhub $gcr
    fi
}

function get_GcrImage()
{
    github=$1
    dockerhub=$2
    gcr=$3
    tmp_gcr='/tmp/gcr-images'
    git --version
    if [[ $? -ne 0 ]]; then yum install -y git ;fi
    if [ -d $tmp_gcr ]; then rm -rf $tmp_gcr ;fi
    git clone $github $tmp_gcr
    cd $tmp_gcr
    pull_gcrImage $dockerhub $gcr
    rm -rf ${tmp_gcr}
}



function stop_firewallSelinux()
{
    systemctl stop firewalld
    systemctl disable firewalld
    setenforce 0
    sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config 
}
