ARGS_CONFIG = {
    "ansible": {
        "output_dir": ("playbook",),
        "template_file": ("ansible.cfg.j2",)
    },
    "hpc_conf": {
        "output_dir": ("PLAYBOOK_DIR", "TORQUE_TEMPLATE_DIR", "AUTOFS_FILES_DIR", "AUTOFS_FILES_DIR", "NFS_FILES_DIR", "TORQUE_TEMPLATE_DIR", "TORQUE_TEMPLATE_DIR"),
        "template_file": ("hosts.j2", "etc_hosts.j2", "auto.master.j2", "auto.pool.j2", "exports.j2", "config.j2", "server_name.j2")
    }
}