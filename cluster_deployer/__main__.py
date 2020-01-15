#!/usr/bin/env python
#
# Copyright (C) 2016-2020 Jingcheng Yang <yjcyxky@163.com>
#

import os
import yaml
import jinja2
import re
import sys
import argparse
import copy
import click

TEMPLATE_DIR = "."


def parse_hpc_config(file_name):
    """
    Parse the hpc config file: hpc_config.yml
    """
    with open(file_name, "r") as f:
        hpc_config = yaml.load(f, Loader=yaml.FullLoader)

    return hpc_config

def render(config_vars, template_file, template_dir="."):
    jinja2.filters.FILTERS["zip"] = zip
    template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
    template_env = jinja2.Environment(loader=template_loader)
    if not os.path.isfile(os.path.join(template_dir, template_file)):
        print("No such file: %s" % template_file)
        sys.exit(1)
    template = template_env.get_template(template_file)
    rendered_text = template.render(config_vars)
    return rendered_text

def check_hpc_conf(hpc_conf):
    manager = hpc_conf.get("manager")
    storage = hpc_conf.get("storage")
    workers = hpc_conf.get("workers")

    manager_ip = manager.get("ip")
    manager_ib_ip = manager.get("infiniband_ip")
    storage_ip = storage.get("ip")
    storage_ib_ip = storage.get("infiniband_ip")

    ip_addr = [ worker.get("ip") for worker in workers ]
    ib_ip_addr = [worker.get("infiniband_ip") for worker in workers ]

    ip_addr.extend([manager_ip, storage_ip])
    ib_ip_addr.extend([manager_ib_ip, storage_ib_ip])

    if manager_ip == storage_ip or manager_ib_ip == storage_ib_ip:
        # manager的IP地址与storage相同时，则manager与storage在同一台机器上，此时不允许再有机器IP地址与之相同
        if len(ip_addr) - 1 > len(set(ip_addr)) or len(ib_ip_addr) - 1 > len(set(ib_ip_addr)):
            print("manager或storage与workers中IP地址有重复，请重新设置")
            sys.exit(1)
    else:
        # manager的IP地址与storage不同时，那么所有地址都应该不同
        if len(ip_addr) > len(set(ip_addr)) or len(ib_ip_addr) - 1 > len(set(ib_ip_addr)):
            print("manager或storage与workers中IP地址有重复，请重新设置")
            sys.exit(1)

def gen_config_file(config_vars, template_file, output_dir):
    def conf_generator(config_vars, template_file, output_dir):
        if not os.path.isdir(output_dir):
            print("No such directory: %s" % output_dir)
            sys.exit(1)

        # 依据hpc_conf-->storage-->pools生成autofs配置文件
        if re.search("auto\.[a-zA-Z\.\-_]+\.j2", template_file) and template_file != "auto.master.j2":
            pools = config_vars["hpc_conf"]["storage"]["pools"]
            for pool in pools:
                pool_config_vars = copy.deepcopy(config_vars)
                pool_config_vars["hpc_conf"]["storage"]["pool_name"] = pool
                with open(os.path.join(output_dir, "auto.%s" % pool.replace("/", "_")), "w") as f:
                    f.write(render(pool_config_vars, template_file, TEMPLATE_DIR))
            return True

        if re.search("[a-zA-Z0-9\.\-_#]+\.j2", template_file):
            output_file = template_file[:-3]
            output_file = re.sub(r"#.*#", "", output_file)
            with open(os.path.join(output_dir, output_file), "w") as f:
                f.write(render(config_vars, template_file, TEMPLATE_DIR))
            return True
        else:
            print("%s: 模板文件名不符合要求，只能包含大小写字母、数字、下划线、#号、点号，且末尾必须以.j2结尾" % template_file)
            sys.exit(2)

    if isinstance(template_file, tuple) and isinstance(output_dir, tuple):
        for file_name, dir_name in zip(template_file, output_dir):
            conf_generator(config_vars, file_name, dir_name)
    else:
        conf_generator(config_vars, template_file, output_dir)
    return True


def set_config(hpc_config_file=None):
    BASE_DIR = os.path.dirname(__file__)

    if hpc_config_file:
        HPC_CONFIG_FILE = hpc_config_file
    else:
        HPC_CONFIG_FILE = os.path.join(BASE_DIR, "hpc_config.yml.sample")

    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

    HPC_CONFIG = parse_hpc_config(HPC_CONFIG_FILE)
    PLAYBOOK_DIR = os.path.join(BASE_DIR, "playbook")
    ROLE_DIR = os.path.join(BASE_DIR, "playbook", "roles")

    NFS_FILES_DIR = os.path.join(ROLE_DIR, "deploy_nfs", "files")
    FSTAB_FILES_DIR = os.path.join(ROLE_DIR, "deploy_fstab", "files")
    NIS_DEFAULT_DIR = os.path.join(ROLE_DIR, "deploy_nis", "defaults")

    INFINIBAND_FILES_DIR = os.path.join(ROLE_DIR, "deploy_infiniband", "files")
    INFINIBAND_DEFAULT_DIR = os.path.join(ROLE_DIR, "deploy_infiniband", "defaults")

    PACKAGES_FILES_DIR = os.path.join(ROLE_DIR, "deploy_packages", "files")
    PACKAGES_TEMPLATE_DIR = os.path.join(ROLE_DIR, "deploy_packages", "templates")
    PACKAGES_DEFAULT_DIR = os.path.join(ROLE_DIR, "deploy_packages", "defaults")

    AUTOFS_FILES_DIR = os.path.join(NFS_FILES_DIR, "autofs")
    TORQUE_TEMPLATE_DIR = os.path.join(ROLE_DIR, "deploy_torque", "templates")

    ARGS_CONFIG = {
        "ansible": {
            "output_dir": (os.path.join(BASE_DIR, "playbook"),),
            "template_file": ("ansible.cfg.j2",),
            # fromkeys从seq创建字典，因此需要第一个参数需要构建成tuple或list形式
            "config_vars": HPC_CONFIG.fromkeys(("ansible",), HPC_CONFIG.get("ansible"))
        },
        "hpc_conf": {
            "output_dir": (PLAYBOOK_DIR, TORQUE_TEMPLATE_DIR, AUTOFS_FILES_DIR, AUTOFS_FILES_DIR,
                           NFS_FILES_DIR, TORQUE_TEMPLATE_DIR, TORQUE_TEMPLATE_DIR, FSTAB_FILES_DIR,
                           FSTAB_FILES_DIR, NIS_DEFAULT_DIR, INFINIBAND_DEFAULT_DIR, INFINIBAND_FILES_DIR,
                           PACKAGES_DEFAULT_DIR, PACKAGES_TEMPLATE_DIR, PACKAGES_FILES_DIR),
            "template_file": ("hosts.j2", "etc_hosts.j2", "auto.master.j2", "auto.pool.j2",
                              "exports.j2", "config.j2", "server_name.j2", "fstab.j2",
                              "volumes.j2", "#nis#main.yml.j2", "#infiniband#main.yml.j2", "#infiniband#infiniband.repo.j2",
                              "#packages#main.yml.j2", "#packages#packages.repo.j2", "#packages#bashrc.j2"),
            "config_vars": HPC_CONFIG.fromkeys(("hpc_conf",), HPC_CONFIG.get("hpc_conf"))
        }
    }

    return TEMPLATE_DIR, HPC_CONFIG, ARGS_CONFIG


def get_file_path(dir, file_name):
    return os.path.join(dir, file_name)


def remove_suffix(path, suffix=".j2"):
    return re.sub(r"#.*#", "", path.replace(suffix, ""))


def replace_special_str(path, prefix=r"auto\..*$", repl="auto.*"):
    return re.sub(prefix, repl, path)


@click.group()
def version_cli():
    pass


@version_cli.command(help="Show version.")
def version():
    from cluster_deployer.version import get_version
    print("Cluster Deployer: %s" % get_version())


@click.group()
def clean_cli():
    pass


@clean_cli.command(help="Clean old config files.")
@click.option("--dry-run", '-d', help="Dry run.", is_flag=True)
def clean(dry_run):
    import json
    import subprocess

    _, _, ARGS_CONFIG = set_config()
    clean_files = [replace_special_str(remove_suffix(get_file_path(dir, file)))
                    for item in ARGS_CONFIG.values()
                        for dir, file in zip(item.get("output_dir"), item.get("template_file"))]
    uniq_clean_files = set(clean_files)

    if dry_run:
        print(json.dumps(list(uniq_clean_files), indent=2, sort_keys=True))
    else:
        try:
            remove_cmd_lst = ["rm -rf %s" % item for item in uniq_clean_files]
            for cmd in remove_cmd_lst:
                subprocess.run(cmd, shell=True, universal_newlines=True, check=True)
        except Exception as err:
            print(err)

        print("Clean old files successfully. Run cluster-deployer clean --dry-run to know which files are cleaned.")


@click.group()
def init_cli():
    pass


@init_cli.command(help="Initialize the config for HPC cluster.")
@click.option("-c", help="Configuration file path.", type=str, default=None)
def init(c):
    global TEMPLATE_DIR
    TEMPLATE_DIR, HPC_CONFIG, ARGS_CONFIG = set_config(c)

    # generate ansible configure file
    # 校验HPC配置信息
    check_hpc_conf(HPC_CONFIG.get("hpc_conf"))

    if gen_config_file(**ARGS_CONFIG.get("ansible")):
        print("生成ansible.cfg配置文件：成功")

    # generate cobbler host configure file
    if gen_config_file(**ARGS_CONFIG.get("hpc_conf")):
        print("生成hosts/etc_hosts/autofs配置文件：成功")


@click.group()
def run_cli():
    pass


@run_cli.command(help="Deploy HPC Cluster.")
@click.argument("command", type=click.Choice(["torque", "nfs"]))
@click.option("--skip", "-s", help="Skip the check_prerequisite", is_flag=True)
@click.option("--debug", "-d", help="Show debug information.", is_flag=True)
def deploy(command, skip, debug):
    import subprocess

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    deploy_hpc_bin = os.path.join(BASE_DIR, "bin", "deploy_hpc")
    try:
        if skip:
            skip = "-k"
        else:
            skip = ""

        cmd = "%s -i deploy_%s %s" % (deploy_hpc_bin, command, skip)
        subprocess.run(cmd, shell=True, universal_newlines=True, check=True)
    except Exception as err:
        if debug:
            print(str(err))
        else:
            pass


cli = click.CommandCollection(sources=[version_cli, run_cli, clean_cli, init_cli])

if __name__ == "__main__":
    cli()
