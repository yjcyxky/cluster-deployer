Torque ansible role
=========================

Installs and configure Torque/PBS LRMS in a cluster of nodes.
The Torque server node must be the Ansible node.

How to use it:
You need to add the host information of managers and workers into the hosts file,
And then you need to run the command 'ansible-playbook install_torque.yml'