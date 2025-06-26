#!/bin/bash

# example: sh deploy.sh $iSourceTargetBranch $pipeline_id $tag
set -e
set -o pipefail

source /etc/profile


TARGET_BRANCH=$1
PIPELINE_ID=$2
TAG=$3
server_name=lobechatservice


if echo TARGET_BRANCH=$TARGET_BRANCH|grep 'feature';then
	BUILD_TYPE=feature;
	ENV_TYPE=test;
fi
if echo TARGET_BRANCH=$TARGET_BRANCH|grep 'master';then
	BUILD_TYPE=master;
	ENV_TYPE=release;
fi

if [ "$BUILD_TYPE" = "feature" ];then
	echo deploy ENV is test
	curl -d "component=$server_name&version=$PIPELINE_ID&publish_type=develop&overwrite=true" http://helm-cd.ps-rancher.inhuawei.com/v1/task/release
elif [ "$BUILD_TYPE" = "master" ];then
	echo deploy ENV is release

    server_version=${PIPELINE_ID}

	curl -d "component=$server_name&version=$server_version&publish_type=hlt&overwrite=true" http://helm-cd.ps-rancher.inhuawei.com/v1/task/release
else
	echo "there is no appropriate deploy ENV when BUILD_TYPE=$BUILD_TYPE ";
	exit 1;
fi
echo 'complete'
if [ "$?" != "0" ];then
    echo deploy failed!
    exit 1
fi