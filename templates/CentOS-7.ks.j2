#version=RHEL7
# X Window System configuration information
xconfig  --startxonboot

# License agreement
eula --agreed
# System authorization information
auth --enableshadow --passalgo=sha512
# Use CDROM installation media
cdrom
# Run the Setup Agent on first boot
firstboot --enable
# Keyboard layouts
keyboard --vckeymap=uk --xlayouts='gb'
# System language
lang en_GB.UTF-8

ignoredisk --only-use=sda
# Network information
network  --bootproto=dhcp --device=enp13s0 --ipv6=auto --activate
# Root password
rootpw einon
# System timezone
timezone Europe/London --isUtc
# System bootloader configuration
bootloader --location=mbr --boot-drive=sda
# Partition clearing information - DESTROYS ALL DATA! Ensure there are backups
clearpart --all
# Disk partitioning information
part /boot --fstype="xfs" --size=500 --grow
part pv.13 --fstype="lvmpv" --ondisk=sda --size=7000 --grow
volgroup centos --pesize=4096 pv.13
logvol /home  --fstype="xfs" --size=1000 --name=home --vgname=centos
logvol swap  --fstype="swap" --size=100 --name=swap --vgname=centos
logvol /  --fstype="xfs" --size=5000 --name=root --vgname=centos

%packages
@base
@compat-libraries
@core
@desktop-debugging
@development
@dial-up
@fonts
@gnome-desktop
@guest-agents
@guest-desktop-agents
@input-methods
@internet-browser
@java-platform
@mariadb
@multimedia
@network-file-system-client
@postgresql
@print-client
@remote-desktop-clients
@x11

%end

