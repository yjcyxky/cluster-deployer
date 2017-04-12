#!/bin/bash
# Author: JingchengYang<yjcyxky@163.com>
# 功能：在集群所有节点间建立免密登录

show_help(){
cat << EOF
usage: $(echo $0) [-a] [-f <HOST_FILE>]
       -a 重新生成ssh密钥
       -f 指定主机文件
EOF
}

while getopts ":ahf:" arg
do
    case "$arg" in
        "a")
            yes="yes"
            ;;
        "f")
            hosts="$OPTARG"
            # echo "$OPTARG"
            ;;
        "?")
            echo "Unkown option: $OPTARG"
            exit 1
            ;;
        ":")
            echo "No argument value for option $OPTARG"
            ;;
        h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown error while processing options"
            show_help
            exit 1
            ;;
    esac
done

cd $HOME

if [ ! -f "$hosts" ];then
    echo "未找到主机文件$hosts"
    show_help
    exit 1
fi

if [ "$yes" == 'yes' ];then
    echo "重新生成密钥"
    if [ -d ".ssh" ];then
        echo "覆盖当前.ssh目录"
        rm -rf .ssh
    fi
    mkdir .ssh > /dev/null
    chmod 700 .ssh > /dev/null
    cd .ssh
    ssh-keygen -f id_rsa -t rsa -N ''
    cp id_rsa.pub authorized_keys
    chmod 600 authorized_keys
fi

num_of_col=`cat $hosts | grep '^[0-9].*' | awk '{print NF;exit}'`
ip_or_not=`cat $hosts | grep '^[0-9].*' | awk '{print $1;}' | grep -E '[0-9]+(?:.[0-9]+){0,3}'`
host_or_not=`cat $hosts | grep '^[0-9].*' | awk '{print $2;}' | grep -E '^[a-zA-Z0-9\_-]+$'`
if [ "$num_of_col" == '2' ] && [ ! -z "$ip_or_not" ] && [ ! -z "$host_or_not" ];then
    while read ip host
    do
        if [ ! -z `echo $ip | grep ^[0-9].*` ];then
            echo $ip, $host
            ssh-keyscan -H $ip >> ~/.ssh/known_hosts
            ssh-keyscan -H $host >> ~/.ssh/known_hosts
        fi
    done < $hosts
else
    echo "$num_of_col  $ip_or_not  $host_or_not"
    echo "$hosts不是合格的hosts文件"
    echo "格式要求："
    printf "\t第一列为IP地址\n"
    printf "\t第二列为主机名(只能包含大小写、短横线、下划线)\n"
    exit 2
fi