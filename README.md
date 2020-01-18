# 快速指南
## 系统依赖
网络配置：至少需要两张网卡，无线网卡/第一张有线网卡连接外网，并且需要设置其为**默认路由**

```
DEFROUTE=yes
```

另外一张网卡为有线网卡，网卡配置如下：

```
TYPE=Ethernet
BOOTPROTO=static
DEFROUTE=no
IPADDR=192.192.192.21
NETMASK=255.255.255.0
GATEWAY=192.192.192.1
# 注意NAME、UUID以及DEVICE需要依据设备实际情况进行设置
NAME=enp1s0f0
UUID=082ff747-d8d6-4d31-bcd6-09bbbca1bff3
DEVICE=enp1s0f0
ONBOOT=yes
```

## 下载 cluster-deployer

```
# 假定：下载 Cluster Deployer 至用户 Home 目录
git clone https://github.com/go-choppy/cluster-deployer
```

## 安装依赖库

```
# 安装前置依赖
yum install sshpass

# 依据机器实际情况，选择安装方式
## 1. 使用 conda

### 创建 cluster-deployer 环境
conda create -n cluster-deployer python=3.7

### 激活环境（ 务必激活环境后再安装依赖库 ）
conda activate cluster-deployer

### 安装依赖，requirements 文件位于 cluster-deployer 目录下
pip3 install -r ~/cluster-deployer/requirements

## 2. 使用 virtualenv
### 确认是否按照 Python3、pip3 和 virtualenv
which python3
which pip3
which virtualenv

### 若未安装，则通过以下命令安装
yum install python3
yum install python3-pip
pip3 install virtualenv

### 切换到 cluster-deployer 目录（ 假定 cluster-deployer 位于 HOME 目录 ）
cd ~/cluster-deployer
virtualenv .env -p python3

## 激活环境（ 务必激活环境后再安装依赖库 ）
source .env/bin/activate

## 安装依赖
pip3 install -r requirements
```

## 配置环境变量

```
echo "export PATH=~/cluster-deployer/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
```

## 修改配置文件

```
# 拷贝hpc_config.yml.sample为hpc_config.yml文件
cp cluster-deployer/cluster_deployer/hpc_config.yml.sample ~/hpc_config.yml

# 修改 hpc_config.yml 文件，依据实际情况填入相应的参数
```

## 初始化配置

```
# 运行`cluster-deployer init -c hpc_config.yml`将会依据hpc_config.yml文件中指定的集群管理节点和计算节点配置生成集群配置文件

cluster-deployer init -c ~/hpc_config.yml
```

## 部署模块
运行部署命令；注意运行的先后顺序，详情参考[HPC Configuration](./cluster_deployer/hpc_config.yml.sample)

```
cluster-deployer deploy [torque|nfs|infiniband|packages|nis|fstab]

# 查看命令帮助
cluster-deployer deploy --help
```

# 软件详解
## `cluster-deployer init` 命令
负责将templates目录下的jinja2文件渲染成相关配置文件并拷贝到指定目录

    ansible.cfg.j2 ----> setup_cobbler/playbook/ansible.cfg
    hosts.j2 ----> setup_cobbler/playbook/hosts

## `cluster-deployer deploy` 命令
负责调用各个部署模块完成HPC配置工作

## 当前支持的模块
1. 部署集群调度软件
2. 部署 NFS
3. 部署 Infiniband 驱动
4. 部署 Module + 集群管理附加软件包 cluster-utils
5. 部署集群认证软件 NIS
6. 配置与挂载存储卷并发布至计算节点

# TODO List
暂无

# 软件信息
> 作者: JingchengYang
>
> 邮箱: yjcyxky@163.com