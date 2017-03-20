#!/bin/bash
#
# Script to start a vagrant VM and configure cobbler using ansible
#
# Copyright (C) 2016  Mark Einon <mark.einon@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# Version 2.1 only as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

echo ">>>>> Running Ansible cobbler install playbook..."
cd ../playbook
ansible-playbook deploy_cobbler.yml

echo ">>>>> Finished!"
echo ">>>>> Now halt the VM, then use the VirtualBox GUI to:"
echo "          - Add a Centos7 iso as a virtual DVD device to the Vagrant VM"
echo "          - Change the boot order so that the Hard Disk boots before the DVD drive"
echo "... then run ./install_distro.sh"
