# 安装指南
## 依赖安装
1. 安装Python3
2. 安装Python3依赖库：pyyaml、jinja2
3. 安装ansible

## 其它配置
1. 网络配置：至少需要两张网卡
无线网卡/第一张有线网卡连接外网，并且需要设置其为**默认路由**
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

# Quickstart Guide
1. 拷贝hpc_config.yml.sample为hpc_config.yml文件
2. 修改hpc_config.yml文件，依据实际情况填入相应的参数
3. 运行`deploy_hpc -i deploy_torque -c hpc_config.yml`将会依据hpc_config.yml文件中指定的集群管理节点和计算节点配置安装torque等集群软件

# 软件详解
1. init_deploy负责将templates目录下的jinja2文件渲染成相关配置文件并拷贝到指定目录
    ansible.cfg.j2 ----> setup_cobbler/playbook/ansible.cfg
    hosts.j2 ----> setup_cobbler/playbook/hosts

2. deploy_hpc负责调用各个ansible模块完成HPC配置工作，共包含5个子命令：deploy_infiniband、deploy_torque、deploy_nfs，每个子命令均可多次调用了

# TODO List
1. 增加NIS配置模块
2. 增加 Infiniband 配置模块
3. 增加账户模块+免密登录

# 软件信息
> 作者: JingchengYang
>
> 邮箱: yjcyxky@163.com