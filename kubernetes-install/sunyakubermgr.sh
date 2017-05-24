#!/usr/bin/env bash

github='https://github.com/zhuyongliang095/gcr.io.git'
dockerhub='yongliang095/gcr-images'
gcr='gcr.io/google_containers'
tmp_gcr='/tmp/gcr-images'

git --version
if [[ $? -ne 0 ]]
then
    yum install -y git
fi


if [ -d $tmp_gcr ]
then
    rm $tmp_gcr
fi
git clone $github $tmp_gcr

cd $tmp_gcr

for file in ` find . -name Dockerfile | xargs `
do
    image=`cat $file | awk -F'/' '{print $3}'| awk -F':' '{print $1}' | sed 's/-amd64//g'`
    tag=`cat $file | awk -F'/' '{print $3}'| awk -F':' '{print $2}' `
    docker pull ${dockerhub}:$image
    docker tag ${dockerhub}:${image}  ${gcr}/${image}-amd64:${tag}
    docker rmi ${dockerhub}:$image
done

rm -rf $tmp_gcr
