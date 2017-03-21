#!/bin/env python
import os, yaml, jinja2, re, sys, argparse

BASE_DIR = os.path.dirname(__file__)
HPC_CONFIG_FILE = os.path.join(BASE_DIR, "hpc_config.yml")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def parse_hpc_config(file_name):
    '''
    Parse the hpc config file: hpc_config.yml
    '''
    with open(file_name, 'r') as f:
        hpc_config = yaml.load(f)

    return hpc_config

def render(config_vars, template_file):
    template_loader = jinja2.FileSystemLoader(searchpath=TEMPLATE_DIR)
    template_env = jinja2.Environment(loader=template_loader)
    if not os.path.isfile(os.path.join(TEMPLATE_DIR, template_file)):
        print("No such file: %s" % template_file)
        sys.exit(1)
    template = template_env.get_template(template_file)
    rendered_text = template.render(config_vars)
    return rendered_text

def gen_config_file(config_vars, template_file, output_dir):
    def conf_generator(config_vars, template_file, output_dir):
        if not os.path.isdir(output_dir):
            print("No such directory: %s" % output_dir)
            sys.exit(1)

        if re.search("[a-zA-Z0-9\.\-_]+\.j2", template_file):
            output_file = template_file[:-3]
            with open(os.path.join(output_dir, output_file), 'w') as f:
                f.write(render(config_vars, template_file))
            return True
        else:
            print("模板文件名不符合要求，只能包含大小写字母、数字、下划线、点号，且末尾必须以.j2结尾")
            sys.exit(2)

    if isinstance(template_file, tuple) and isinstance(output_dir, tuple):
        for file_name, dir_name in zip(template_file, output_dir):
            conf_generator(config_vars, file_name, dir_name)
    else:
        conf_generator(config_vars, template_file, output_dir)
    return True

HPC_CONFIG = parse_hpc_config(HPC_CONFIG_FILE)
ARGS_CONFIG = {
    'ansible': {
        'output_dir': os.path.join(BASE_DIR, "playbook"),
        'template_file': 'ansible.cfg.j2',
        # fromkeys从seq创建字典，因此需要第一个参数需要构建成tuple或list形式
        'config_vars': HPC_CONFIG.fromkeys(('ansible',), HPC_CONFIG.get('ansible'))
    },
    'hpc_conf': {
        'output_dir': (os.path.join(BASE_DIR, "playbook"), os.path.join(BASE_DIR, "playbook", "roles", "install_torque", "templates")),
        'template_file': ('hosts.j2', "etc_hosts.j2"),
        'config_vars': HPC_CONFIG.fromkeys(('hpc_conf',), HPC_CONFIG.get('hpc_conf'))
    },
    'cobbler_conf': {
        'output_dir': os.path.join(BASE_DIR, "playbook", "host_vars"),
        'template_file': 'cobbler1.yml.j2',
        'config_vars': HPC_CONFIG.fromkeys(('cobbler_conf',), HPC_CONFIG.get('cobbler_conf'))
    },
    'client_conf': {
        'output_dir': os.path.join(BASE_DIR, "setup_cobbler", "clients"),
        'template_file': 'client.yml.j2',
        'config_vars': HPC_CONFIG.fromkeys(('client_conf',), HPC_CONFIG.get('client_conf'))
    },
    'ks_conf': {
        'output_dir': os.path.join(BASE_DIR, "playbook", "roles", "add_distro", "files"),
        'template_file': 'ks_template.ks.j2',
        'config_vars': HPC_CONFIG.fromkeys(('ks_conf',), HPC_CONFIG.get('ks_conf'))
    }
}

def main():
    # parser = argparse.ArgumentParser(prog=__file__)
    # parser.add_argument('-v', help="显示软件版本信息")
    # subparsers = parser.add_subparsers(help="子命令")
    # subparser_init = subparsers.add_parser('init', help="初始化hpc_deploy软件")
    # subparser_clean = subparsers.add_parser('clean', help="清除所有配置文件")
    # subparser_setup_cobbler = subparsers.add_parser('setup_cobbler', help="安装配置cobbler服务器")
    # subparser_get_iso = subparsers.add_parser('get_iso', help="下载ISO镜像")
    # subparser_config_hpc = subparsers.add_parser('config_hpc', help="配置HPC集群")
    # subparser_add_client = subparsers.add_parser('setup_client', help="添加客户机")
    # args = parser.parse_args()
    # print(args.func(args))

    # generate ansible configure file
    if gen_config_file(**ARGS_CONFIG.get('ansible')):
        print("生成ansible.cfg配置文件：成功")

    # generate cobbler host configure file
    if gen_config_file(**ARGS_CONFIG.get('hpc_conf')):
        print("生成hosts配置文件：成功")

    if gen_config_file(**ARGS_CONFIG.get('cobbler_conf')):
        print("生成cobbler1.yml配置文件：成功")

if __name__ == '__main__':
    main()