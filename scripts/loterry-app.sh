#!/bin/bash
# By Narunas Kapocius
# 2020 01 11
# Loterry app K8s start/stop script

#Change working directory where K8s deployments definitions are kept
workdir=../kubernetes/deployments
pushd $workdir

case $1 in
  start)
    echo "Starting.."
    kubectl apply -f .
    ;;
  stop)
    echo "Stopping.."
    kubectl delete -f .
    ;;
  *)
    echo "Provide start/stop parameter"
    ;;
esac