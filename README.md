# 备注
1. init.py负责将templates目录下的jinja2文件渲染成相关配置文件并拷贝到指定目录
    ansible.cfg.j2 ----> setup_cobbler/playbook/ansible.cfg
    CentOS-7.ks.j2 ----> setup_cobbler/playbook/roles/add_distro/files   <!--具体命名依据hpc_config.yml中client_conf区块确定-->
    client.yml.j2 ----> setup_cobbler/clients/{{待定}}   <!--需要依据程序设计而定，即add_distro role需要重写-->
    cobbler1.yml.j2 ----> setup_cobbler/playbook/host_vars/cobbler1.yml
    hosts.j2 ----> setup_cobbler/playbook/hosts

2. deploy_hpc.py负责调用各个ansible模块完成HPC配置工作，共包含5个子命令：init、prepare_env、setup_cobbler、get_iso、config_hpc，每个子命令均可多次调用了