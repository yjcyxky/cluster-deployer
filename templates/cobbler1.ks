# kickstart template for Fedora 8 and later.
# (includes %end blocks)
# do not use with earlier distros

#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth --enableshadow --passalgo=sha512
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
clearpart --all --initlabel
# Use text mode install
text
# Firewall configuration
firewall --disable
# Run the Setup Agent on first boot
firstboot --disable
# System keyboard
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US

# Reboot after installation
reboot

#Root password
rootpw --iscrypted $6$28hHR4Rs.X.PQM0Z$EOAgBBHSmL9RLMqzP4R6nSWzBsb/CLudMFWDkJmunfr3vi1irY2mqOREfbNwnunrib64UI5rb1UR7oCOMLBAZ.
# SELinux configuration
services --disabled="selinux"
# Do not configure the X Window System
skipx
# System timezone
timezone Asia/Shanghai --isUtc --nontp

# Add a user: supersan
user --groups=wheel --homedir=/supersan --name=supersan --password=$6$lDvp99/0ct3mwvca$3LIMhZwY4R0.yW8wxYIEdxKqR9Sk7dkq0pSOT/eYGVLwknkZ/aAbTxjFsXNPQ9O82j2AHEMz36EZbSYSRWxuV. --iscrypted --gecos="supersan"
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr

# System bootloader configuration
bootloader --location=mbr --boot-drive=sda
# Partition clearing information
clearpart --none --initlabel
# Disk partitioning information
part pv.833 --fstype="lvmpv" --ondisk=sda --size=19088
part /boot --fstype="xfs" --ondisk=sda --size=953
volgroup supersan --pesize=4096 pv.833
logvol /  --fstype="xfs" --size=9536 --name=root --vgname=supersan
logvol /tmp  --fstype="xfs" --size=9536 --name=tmp --vgname=supersan

%packages
# '#'号标注的package为CentOS7中未找到的，需要继续核实
@base
@core
# @TeX support
@Additional Development
# @Desktop Platform
# @Desktop Platform Development
# @Development tools
# @FCoE Storage Client
@Hardware monitoring utilities
@Infiniband Support 
@Java Platform 
@Large Systems Performance
@Network file system client 
@Networking Tools 
@Performance Tools 
@Perl Support 
@Ruby Support 
@Scientific support 
# @iSCSI Storage Client 
# @Storage Availability Tools
# @Chinese Support 
@Directory Server 
@Directory Client
@NFS file server 
@Network Storage Server 
@System administration tools 
@Messaging Client Support
@SNMP Support
@System Management 
@Scalable Filesystems
@X Window System
# @Server Platform
# @Server Platform Development
%end