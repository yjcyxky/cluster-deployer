#!/bin/bash
#
# Script to install a test linux distro to cobbler using ansible
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

echo ">>>>> Running Ansible install distro playbook..."
cd ../playbook
ansible-playbook add_distro.yml

echo ">>>>> Finished!"
echo ">>>>> Now create a virtualbox PXE boot VM to boot from the same virtual network as the cobbler VM"
