#!/bin/bash

# exmaple: sh package.sh $pipeline_id $iSourceTargetBranch $tag

source /etc/profile

PIPELINE_ID=$1
TARGET_BRANCH=$2
HARBOR_PASSWORD=$3
TAG=$4

#=====================================================

image_repo_name='corecdimage.inhuawei.com'
image_name_prefix='corecdimage.inhuawei.com/lobechat/lobechatbackend'
server_name=`grep -P '^LABEL name="[a-z0-9]([-a-z0-9]*[a-z0-9])?"\s*$' Dockerfile | tail -1 | awk -F '"' '{print $2}'`
replica=`grep -P '^LABEL replica\=\d+\s*$' Dockerfile | tail -1 | awk -F '=' '{print $2}'`
port=`grep -P '^LABEL port\=\d+\s*$' Dockerfile | tail -1 | awk -F '=' '{print $2}'`
nodePort=`grep -P '^LABEL nodeport\=\d+\s*$' Dockerfile | tail -1 | awk -F '=' '{print $2}'`
base_image_name=`grep -P '^FROM .*$' Dockerfile | tail -1 | awk -F ' ' '{print $2}'`
namespace=`grep -P '^LABEL namespace\="[a-z0-9]([-a-z0-9]*[a-z0-9])?"\s*$' Dockerfile | tail -1 | awk -F '"' '{print $2}'`

if [ "$namespace" = "" ];then
    namespace=default
fi

if [ "$replica" = "" ];then
    replica=1
fi


#===========================此处为推送镜像至harbor============================================================

docker pull ${base_image_name}
docker build -t=${image_name_prefix}:${PIPELINE_ID} .
docker login --username svc-registry --password ${HARBOR_PASSWORD} ${image_repo_name}
docker push ${image_name_prefix}:${PIPELINE_ID}
docker rmi -f ${image_name_prefix}:${PIPELINE_ID}
#=============================================================================================================

if [ "$?" != "0" ];then
	echo generate docker image failed!
    exit 1
fi

