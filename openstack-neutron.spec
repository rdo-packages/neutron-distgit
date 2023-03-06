%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global service neutron

%define cleanup_orphan_rootwrap_daemons() \
for pid in $(ps -f --ppid 1 | awk '/.*neutron-rootwrap-daemon/ { print $2 }'); do \
   kill $(ps --ppid $pid -o pid=) \
done \
%nil

%global common_desc \
Neutron is a virtual network service for Openstack. Just like \
OpenStack Nova provides an API to dynamically request and configure \
virtual servers, Neutron provides an API to dynamically request and \
configure virtual networks. These networks connect "interfaces" from \
other OpenStack services (e.g., virtual NICs from Nova VMs). The \
Neutron API supports extensions to provide advanced network \
capabilities (e.g., QoS, ACLs, network monitoring, etc.)

Name:           openstack-%{service}
Version:        XXX
Release:        XXX
Epoch:          1
Summary:        OpenStack Networking Service

License:        ASL 2.0
URL:            http://launchpad.net/%{service}/

Source0:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:        %{service}.logrotate
Source2:        %{service}-sudoers
Source10:       neutron-server.service
Source11:       neutron-linuxbridge-agent.service
Source12:       neutron-openvswitch-agent.service
Source15:       neutron-dhcp-agent.service
Source16:       neutron-l3-agent.service
Source17:       neutron-metadata-agent.service
Source18:       neutron-ovs-cleanup.service
Source19:       neutron-macvtap-agent.service
Source20:       neutron-metering-agent.service
Source21:       neutron-sriov-nic-agent.service
Source22:       neutron-netns-cleanup.service
Source29:       neutron-rpc-server.service

Source30:       %{service}-dist.conf
Source31:       conf.README
Source32:       neutron-linuxbridge-cleanup.service
Source33:       neutron-enable-bridge-firewall.sh
Source34:       neutron-l2-agent-sysctl.conf
# We use the legacy service to load modules because it allows to gracefully
# ignore a missing kernel module (f.e. br_netfilter on earlier kernels). It's
# essentially because .modules files are shell scripts.
Source35:       neutron-l2-agent.modules
Source36:       neutron-destroy-patch-ports.service
Source37:       neutron-ovn-metadata-agent.service
Source38:       neutron-ovn-agent.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core
BuildRequires:  openstack-macros
BuildRequires:  python3-ddt
BuildRequires:  python3-devel
BuildRequires:  python3-babel
BuildRequires:  python3-keystoneauth1 >= 3.14.0
BuildRequires:  python3-keystonemiddleware
BuildRequires:  python3-neutron-lib
BuildRequires:  python3-novaclient
BuildRequires:  python3-os-resource-classes
BuildRequires:  python3-os-xenapi
BuildRequires:  python3-oslo-cache
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-db
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-oslo-privsep
BuildRequires:  python3-oslo-reports
BuildRequires:  python3-oslo-rootwrap
BuildRequires:  python3-oslo-service
BuildRequires:  python3-oslo-upgradecheck
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-osprofiler >= 1.3.0
BuildRequires:  python3-ovsdbapp
BuildRequires:  python3-pbr >= 4.0.0
BuildRequires:  python3-psutil >= 3.2.2
BuildRequires:  python3-pyroute2 >= 0.7.3
BuildRequires:  python3-pecan >= 1.3.2
BuildRequires:  python3-tenacity >= 4.4.0
BuildRequires:  python3-oslotest
BuildRequires:  python3-hacking
BuildRequires:  python3-stestr
BuildRequires:  python3-testresources
BuildRequires:  python3-testscenarios
BuildRequires:  python3-designateclient
BuildRequires:  python3-neutronclient
BuildRequires:  python3-neutron-lib-tests
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-os-ken
BuildRequires:  python3-os-vif
BuildRequires:  python3-tooz
BuildRequires:  python3-webtest
BuildRequires:  systemd


Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}

# dnsmasq is not a hard requirement, but is currently the only option
# when neutron-dhcp-agent is deployed.
Requires:       dnsmasq >= 2.76
Requires:       dnsmasq-utils >= 2.76

# radvd is not a hard requirement, but is currently the only option
# for IPv6 deployments.
Requires:       radvd

# dibbler is not a hard requirement, but is currently the default option
# for IPv6 prefix delegation.
Requires:       dibbler-client

# conntrack is not a hard requirement, but is currently used by L3 agent
# to immediately drop connections after a floating IP is disassociated
Requires:       conntrack-tools

# keepalived is not a hard requirement, but is currently used by DVR L3
# agent
Requires:       keepalived

# haproxy implements metadata proxy process
Requires:       haproxy >= 1.5.0

# Those are not hard requirements, ipset is used by ipset-cleanup in the subpackage,
# iptables is used by the l3-agent which currently is not in a separate package,
# iputils provides tools like arping which are used by l3-agent and iproute-tc
# (or iproute in case of CentOS 7 and RHEL 7), provides tc binary which is
# used by e.g. l3-agent and openvswitch-agent when QoS extension is enabled
# in agent's config.
Requires:       ipset
Requires:       iptables
Requires:       iputils
Requires:       iproute-tc


%{?systemd_ordering}


Obsoletes:      openstack-%{service}-dev-server

%description
%{common_desc}


%package -n python3-%{service}
Summary:        Neutron Python libraries
%{?python_provide:%python_provide python3-%{service}}
Requires:       python3-alembic >= 1.6.5
Requires:       python3-debtcollector >= 1.19.0
Requires:       python3-designateclient >= 2.7.0
Requires:       python3-eventlet >= 0.26.1
Requires:       python3-greenlet >= 0.4.10
Requires:       python3-futurist >= 1.2.0
Requires:       python3-jinja2 >= 2.10
Requires:       python3-keystoneauth1 >= 3.14.0
Requires:       python3-keystonemiddleware >= 5.1.0
Requires:       python3-netaddr >= 0.7.18
Requires:       python3-neutronclient >= 7.8.0
Requires:       python3-neutron-lib >= 3.4.0
Requires:       python3-novaclient >= 9.1.0
Requires:       python3-os-vif >= 3.1.0
Requires:       python3-oslo-cache >= 1.26.0
Requires:       python3-oslo-concurrency >= 3.26.0
Requires:       python3-oslo-config >= 2:9.0.0
Requires:       python3-oslo-context >= 2.22.0
Requires:       python3-oslo-db >= 4.44.0
Requires:       python3-oslo-i18n >= 3.20.0
Requires:       python3-oslo-log >= 4.5.0
Requires:       python3-oslo-messaging >= 7.0.0
Requires:       python3-oslo-middleware >= 3.31.0
Requires:       python3-oslo-policy >= 3.12.0
Requires:       python3-oslo-privsep >= 2.3.0
Requires:       python3-oslo-reports >= 1.18.0
Requires:       python3-oslo-rootwrap >= 5.15.0
Requires:       python3-oslo-serialization >= 2.25.0
Requires:       python3-oslo-service >= 2.8.0
Requires:       python3-oslo-upgradecheck >= 1.3.0
Requires:       python3-oslo-utils >= 4.8.0
Requires:       python3-oslo-versionedobjects >= 1.35.1
Requires:       python3-osprofiler >= 2.3.0
Requires:       python3-ovsdbapp >= 1.16.0
Requires:       python3-pecan >= 1.4.0
Requires:       python3-pbr >= 4.0.0
Requires:       python3-psutil >= 5.3.0
Requires:       python3-pyroute2 >= 0.7.3
Requires:       python3-requests >= 2.18.0
Requires:       python3-tenacity >= 6.0.0
Requires:       python3-routes >= 2.3.1
Requires:       python3-os-ken >= 2.2.0
Requires:       python3-os-resource-classes >= 1.1.0
Requires:       python3-sqlalchemy >= 1.4.23
Requires:       python3-stevedore >= 2.0.1
Requires:       python3-tooz >= 1.58.0
Requires:       python3-webob >= 1.8.2
Requires:       python3-openstacksdk >= 0.31.2
Requires:       python3-pyOpenSSL >= 17.1.0
Requires:       python3-packaging >= 20.4

Requires:       python3-httplib2 >= 0.9.1
Requires:       python3-netifaces >= 0.10.4
Requires:       python3-paste >= 2.0.2
Requires:       python3-paste-deploy >= 1.5.0
Requires:       python3-decorator >= 4.1.0

Obsoletes:      python3-networking-ovn
Provides:       python3-networking-ovn = %{epoch}:%{version}-%{release}


%description -n python3-%{service}
%{common_desc}

This package contains the Neutron Python library.


%package -n python3-%{service}-tests
Summary:        Neutron tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}
Requires:       python3-ddt >= 1.0.1
Requires:       python3-fixtures >= 3.0.0
Requires:       python3-mock >= 2.0
Requires:       python3-subunit >= 0.0.18
Requires:       python3-testrepository >= 0.0.18
Requires:       python3-testtools >= 1.4.0
Requires:       python3-testresources >= 0.2.4
Requires:       python3-testscenarios >= 0.4
Requires:       python3-oslotest >= 1.10.0
Requires:       python3-os-testr >= 0.7.0
Requires:       python3-PyMySQL >= 0.6.2
Requires:       python3-tempest >= 12.1.0

Requires:       python3-webtest >= 2.0


# pstree is used during functional testing to ensure our internal
# libraries managing processes work correctly.
Requires:       psmisc
# nfs-utils is needed because it creates user with uid 65534 which
# is required by neutron functional tests.
Requires:       nfs-utils


%description -n python3-%{service}-tests
%{common_desc}

This package contains Neutron test files.


%package common
Summary:        Neutron common files
Requires(pre): shadow-utils
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}
Requires:       sudo


%description common
%{common_desc}

This package contains Neutron common files.


%package linuxbridge
Summary:        Neutron Linuxbridge agent
Requires:       ebtables
Requires:       ipset
Requires:       iproute
Requires:       iptables
# kmod is needed to get access to /usr/sbin/modprobe needed by
# neutron-enable-bridge-firewall.sh triggered by the service unit file
Requires:       kmod
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description linuxbridge
%{common_desc}

This package contains the Neutron agent that implements virtual
networks using VLAN or VXLAN using Linuxbridge technology.


%package macvtap-agent
Summary:        Neutron macvtap agent
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description macvtap-agent
%{common_desc}

This package contains the Neutron agent that implements
macvtap attachments for libvirt qemu/kvm instances.


%package ml2
Summary:        Neutron ML2 plugin
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}
# needed for brocade and cisco drivers
#(TODO) ncclient is not in reuirement projects so it should be requirement in neutron
# plugin packages, not in main neutron. Remove this lines completely if everythin keeps
# working.
#Requires:       python3-ncclient


%description ml2
%{common_desc}

This package contains a Neutron plugin that allows the use of drivers
to support separately extensible sets of network types and the mechanisms
for accessing those types.


%package openvswitch
Summary:        Neutron openvswitch plugin
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}
# We require openvswitch when using vsctl to access ovsdb;
# but if we use native access, then we just need python bindings.
# since we don't know what users actually use, we depend on both.
Requires:       ipset
Requires:       iptables
Requires:       openvswitch
Requires:       python3-openvswitch >= 2.10.0
# kmod is needed to get access to /usr/sbin/modprobe needed by
# neutron-enable-bridge-firewall.sh triggered by the service unit file
Requires:       kmod


%description openvswitch
%{common_desc}

This package contains the Neutron plugin that implements virtual
networks using Open vSwitch.


%package metering-agent
Summary:        Neutron bandwidth metering agent
Requires:       iptables
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description metering-agent
%{common_desc}

This package contains the Neutron agent responsible for generating bandwidth
utilization notifications.


%package rpc-server
Summary:        Neutron (RPC only) Server
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description rpc-server
%{common_desc}

This package contains an alternative Neutron server that handles AMQP RPC
workload only.


%package sriov-nic-agent
Summary:        Neutron SR-IOV NIC agent
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description sriov-nic-agent
%{common_desc}

This package contains the Neutron agent to support advanced features of
SR-IOV network cards.


%package ovn-metadata-agent
Summary:        OVN metadata agent
BuildRequires:  systemd
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}
Requires:       openvswitch >= 2.10.0
Obsoletes:      python3-networking-ovn-metadata-agent
Provides:       python3-networking-ovn-metadata-agent = %{epoch}:%{version}-%{release}
%{?systemd_requires}

%description ovn-metadata-agent
OVN provides virtual networking for Open vSwitch and is a component of the
Open vSwitch project.

This package contains the agent that implements the metadata proxy so that VM's
can retrieve metadata from OpenStack Nova.


%package ovn-agent
Summary:        Neutron OVN agent
BuildRequires:  systemd
Requires:       openstack-%{service}-common = %{epoch}:%{version}-%{release}
Requires:       openvswitch >= 2.10.0
%{?systemd_requires}

%description ovn-agent
OVN provides virtual networking for Open vSwitch and is a component of the
Open vSwitch project.

This package contains the agent that implements any functionality not provided
by the ovn-controller service.


%package ovn-migration-tool
Summary:        networking-ovn ML2/OVS to OVN migration tool
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}
Obsoletes:      python3-networking-ovn-migration-tool
Provides:       python3-networking-ovn-migration-tool = %{epoch}:%{version}-%{release}

%description ovn-migration-tool

This package provides the necessary tools to update an existing ML2/OVS
OpenStack to OVN based backend.

%package ml2ovn-trace
Summary:        ML2 OVN trace tool
Requires:       python3-%{service} = %{epoch}:%{version}-%{release}
Provides:       python3-neutron-ml2ovn-trace = %{epoch}:%{version}-%{release}

%description ml2ovn-trace

This package provides tool that allows one to pass in OpenStack objects
to fill in the eth/ip src/dst data when running ovn-trace.

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{service}-%{upstream_version} -S git
sed -i 's/\/usr\/bin\/python/\/usr\/bin\/python3/' %{SOURCE36}

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourseleves
%py_req_cleanup

# Kill egg-info in order to generate new SOURCES.txt
rm -rf neutron.egg-info

%build
export SKIP_PIP_INSTALL=1
%{py3_build}
# Generate i18n files
# (amoralej) we can remove '-D neutron' once https://review.openstack.org/#/c/485070/ is merged
%{__python3} setup.py compile_catalog -d build/lib/%{service}/locale -D neutron

# Generate configuration files
PYTHONPATH=.
for file in `ls etc/oslo-config-generator/*`; do
    oslo-config-generator --config-file=$file
done

find etc -name *.sample | while read filename
do
    filedir=$(dirname $filename)
    file=$(basename $filename .sample)
    mv ${filename} ${filedir}/${file}
done

# Loop through values in neutron-dist.conf and make sure that the values
# are substituted into the neutron.conf as comments. Some of these values
# will have been uncommented as a way of upstream setting defaults outside
# of the code.
while read name eq value; do
  test "$name" && test "$value" || continue
  sed -ri "0,/^(#)? *$name *=/{s!^(#)? *$name *=.*!# $name = $value!}" etc/%{service}.conf
done < %{SOURCE30}

%install
%{py3_install}

# Remove unused files
rm -rf %{buildroot}%{python3_sitelib}/bin
rm -rf %{buildroot}%{python3_sitelib}/doc
rm -rf %{buildroot}%{python3_sitelib}/tools

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/%{service}/rootwrap
mv %{buildroot}/usr/etc/%{service}/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/%{service}/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}

# The generated config files are not moved automatically by setup.py
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/plugins/ml2

mv etc/%{service}.conf %{buildroot}%{_sysconfdir}/%{service}/%{service}.conf
mv etc/neutron/ovn.ini %{buildroot}%{_sysconfdir}/%{service}/ovn.ini
for agent in dhcp l3 metadata metering neutron_ovn_metadata
do
  mv etc/${agent}_agent.ini %{buildroot}%{_sysconfdir}/%{service}/${agent}_agent.ini
done
for file in linuxbridge_agent ml2_conf openvswitch_agent sriov_agent ovn_agent
do
  mv etc/%{service}/plugins/ml2/${file}.ini %{buildroot}%{_sysconfdir}/%{service}/plugins/ml2/${file}.ini
done

# (TODO) Backwards compatibility for networking-ovn-metadata-agent.ini

install -d -m 755 %{buildroot}%{_sysconfdir}/neutron/plugins/networking-ovn
ln -s /etc/neutron/neutron_ovn_metadata_agent.ini %{buildroot}%{_sysconfdir}/%{service}/plugins/networking-ovn/networking-ovn-metadata-agent.ini

# (TODO) Backwards compatibility for ovn.ini
ln -s /etc/neutron/ovn.ini %{buildroot}%{_sysconfdir}/%{service}/plugins/networking-ovn/networking-ovn.ini

# (TODO) Backwards compatibility for networking-ovn-metadata-agent executable
ln -s %{_bindir}/neutron-ovn-metadata-agent  %{buildroot}%{_bindir}/networking-ovn-metadata-agent

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{service}

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/%{service}

# Install systemd units
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/neutron-server.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/neutron-linuxbridge-agent.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/neutron-openvswitch-agent.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/neutron-dhcp-agent.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/neutron-l3-agent.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/neutron-metadata-agent.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/neutron-ovs-cleanup.service
install -p -D -m 644 %{SOURCE19} %{buildroot}%{_unitdir}/neutron-macvtap-agent.service
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/neutron-metering-agent.service
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/neutron-sriov-nic-agent.service
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_unitdir}/neutron-netns-cleanup.service
install -p -D -m 644 %{SOURCE29} %{buildroot}%{_unitdir}/neutron-rpc-server.service
install -p -D -m 644 %{SOURCE32} %{buildroot}%{_unitdir}/neutron-linuxbridge-cleanup.service
install -p -D -m 644 %{SOURCE36} %{buildroot}%{_unitdir}/neutron-destroy-patch-ports.service
install -p -D -m 644 %{SOURCE37} %{buildroot}%{_unitdir}/neutron-ovn-metadata-agent.service
install -p -D -m 644 %{SOURCE38} %{buildroot}%{_unitdir}/neutron-ovn-agent.service

# (TODO) - Backwards compatibility for systemd unit networking-ovn-metadata-agent

ln -s %{_unitdir}/neutron-ovn-metadata-agent.service %{buildroot}%{_unitdir}/networking-ovn-metadata-agent.service

# Install helper scripts
install -p -D -m 755 %{SOURCE33} %{buildroot}%{_bindir}/neutron-enable-bridge-firewall.sh

# Install sysctl and modprobe config files to enable bridge firewalling
# NOTE(ihrachys) we effectively duplicate same settings for each affected l2
# agent. This can be revisited later.
install -p -D -m 644 %{SOURCE34} %{buildroot}%{_sysctldir}/99-neutron-openvswitch-agent.conf
install -p -D -m 644 %{SOURCE34} %{buildroot}%{_sysctldir}/99-neutron-linuxbridge-agent.conf
install -p -D -m 755 %{SOURCE35} %{buildroot}%{_sysconfdir}/sysconfig/modules/neutron-openvswitch-agent.modules
install -p -D -m 755 %{SOURCE35} %{buildroot}%{_sysconfdir}/sysconfig/modules/neutron-linuxbridge-agent.modules

# Install README file that describes how to configure services with custom configuration files
install -p -D -m 755 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{service}/conf.d/README

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}/kill_scripts

# Install dist conf
install -p -D -m 640 %{SOURCE30} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf

# Create and populate configuration directory for L3 agent that is not accessible for user modification
mkdir -p %{buildroot}%{_datadir}/%{service}/l3_agent
ln -s %{_sysconfdir}/%{service}/l3_agent.ini %{buildroot}%{_datadir}/%{service}/l3_agent/l3_agent.conf

# Create dist configuration directory for neutron-server (may be filled by advanced services)
mkdir -p %{buildroot}%{_datadir}/%{service}/server

# Create configuration directories for all services that can be populated by users with custom *.conf files
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/common
for service in server rpc-server ovs-cleanup netns-cleanup linuxbridge-cleanup macvtap-agent; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service
done
for service in linuxbridge openvswitch dhcp l3 metadata metering sriov-nic ovn-metadata ovn; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service-agent
done

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*/LC_*/%{service}*po
rm -f %{buildroot}%{python3_sitelib}/%{service}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{service}/locale %{buildroot}%{_datadir}/locale

# Find language files
%find_lang %{service} --all-name

%check
export PYTHON=%{__python3}
stestr-3 run

%pre common
getent group %{service} >/dev/null || groupadd -r %{service}
getent passwd %{service} >/dev/null || \
    useradd -r -g %{service} -d %{_sharedstatedir}/%{service} -s /sbin/nologin \
    -c "OpenStack Neutron Daemons" %{service}
exit 0


%post
%systemd_post neutron-dhcp-agent.service
%systemd_post neutron-l3-agent.service
%systemd_post neutron-metadata-agent.service
%systemd_post neutron-server.service
%systemd_post neutron-netns-cleanup.service
%systemd_post neutron-ovs-cleanup.service
%systemd_post neutron-linuxbridge-cleanup.service


%preun
%systemd_preun neutron-dhcp-agent.service
%systemd_preun neutron-l3-agent.service
%systemd_preun neutron-metadata-agent.service
%systemd_preun neutron-server.service
%systemd_preun neutron-netns-cleanup.service
%systemd_preun neutron-ovs-cleanup.service
%systemd_preun neutron-linuxbridge-cleanup.service


%postun
%systemd_postun_with_restart neutron-dhcp-agent.service
%systemd_postun_with_restart neutron-l3-agent.service
%systemd_postun_with_restart neutron-metadata-agent.service
%systemd_postun_with_restart neutron-server.service
%cleanup_orphan_rootwrap_daemons


%post macvtap-agent
%systemd_post neutron-macvtap-agent.service


%preun macvtap-agent
%systemd_preun neutron-macvtap-agent.service


%postun macvtap-agent
%systemd_postun_with_restart neutron-macvtap-agent.service
%cleanup_orphan_rootwrap_daemons


%post linuxbridge
%systemd_post neutron-linuxbridge-agent.service


%preun linuxbridge
%systemd_preun neutron-linuxbridge-agent.service


%postun linuxbridge
%systemd_postun_with_restart neutron-linuxbridge-agent.service
%cleanup_orphan_rootwrap_daemons

%post openvswitch
%systemd_post neutron-openvswitch-agent.service
%systemd_post neutron-destroy-patch-ports.service

if [ $1 -ge 2 ]; then
    # We're upgrading

    # Detect if the neutron-openvswitch-agent is running
    ovs_agent_running=0
    systemctl status neutron-openvswitch-agent > /dev/null 2>&1 && ovs_agent_running=1 || :

    # If agent is running, stop it
    [ $ovs_agent_running -eq 1 ] && systemctl stop neutron-openvswitch-agent > /dev/null 2>&1 || :

    # Search all orphaned neutron-rootwrap-daemon processes and since all are triggered by sudo,
    # get the actual rootwrap-daemon process.
    %cleanup_orphan_rootwrap_daemons

    # If agent was running, start it back with new code
    [ $ovs_agent_running -eq 1 ] && systemctl start neutron-openvswitch-agent > /dev/null 2>&1 || :
fi


%preun openvswitch
%systemd_preun neutron-openvswitch-agent.service
%systemd_preun neutron-destroy-patch-ports.service


%post metering-agent
%systemd_post neutron-metering-agent.service


%preun metering-agent
%systemd_preun neutron-metering-agent.service


%postun metering-agent
%systemd_postun_with_restart neutron-metering-agent.service
%cleanup_orphan_rootwrap_daemons


%post sriov-nic-agent
%systemd_post neutron-sriov-nic-agent.service


%preun sriov-nic-agent
%systemd_preun neutron-sriov-nic-agent.service


%postun sriov-nic-agent
%systemd_postun_with_restart neutron-sriov-nic-agent.service
%cleanup_orphan_rootwrap_daemons


%post ovn-metadata-agent
%systemd_post neutron-ovn-metadata-agent.service


%preun ovn-metadata-agent
%systemd_preun neutron-ovn-metadata-agent.service


%postun ovn-metadata-agent
%systemd_postun_with_restart neutron-ovn-metadata-agent.service


%post ovn-agent
%systemd_post neutron-ovn-agent.service


%preun ovn-agent
%systemd_preun neutron-ovn-agent.service


%postun ovn-agent
%systemd_postun_with_restart neutron-ovn-agent.service


%files
%license LICENSE
%{_bindir}/neutron-api
%{_bindir}/neutron-db-manage
%{_bindir}/neutron-debug
%{_bindir}/neutron-dhcp-agent
%{_bindir}/neutron-ipset-cleanup
%{_bindir}/neutron-keepalived-state-change
%{_bindir}/neutron-l3-agent
%{_bindir}/neutron-linuxbridge-cleanup
%{_bindir}/neutron-metadata-agent
%{_bindir}/neutron-netns-cleanup
%{_bindir}/neutron-ovs-cleanup
%{_bindir}/neutron-pd-notify
%{_bindir}/neutron-remove-duplicated-port-bindings
%{_bindir}/neutron-sanity-check
%{_bindir}/neutron-status
%{_bindir}/neutron-server
%{_bindir}/neutron-usage-audit
%{_bindir}/neutron-ovn-metadata-agent
%{_bindir}/neutron-ovn-agent
%{_bindir}/neutron-sanitize-port-binding-profile-allocation
%{_bindir}/neutron-sanitize-port-mac-addresses
%{_bindir}/networking-ovn-metadata-agent
%{_bindir}/neutron-ovn-db-sync-util
%{_unitdir}/neutron-dhcp-agent.service
%{_unitdir}/neutron-l3-agent.service
%{_unitdir}/neutron-metadata-agent.service
%{_unitdir}/neutron-server.service
%{_unitdir}/neutron-netns-cleanup.service
%{_unitdir}/neutron-ovs-cleanup.service
%{_unitdir}/neutron-linuxbridge-cleanup.service
%dir %{_datadir}/%{service}/l3_agent
%dir %{_datadir}/%{service}/server
%{_datadir}/%{service}/l3_agent/*.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/api-paste.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/dhcp_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/l3_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/metadata_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-dhcp-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-l3-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-metadata-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-server
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-netns-cleanup
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-ovs-cleanup
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-linuxbridge-cleanup
%dir %{_sysconfdir}/%{service}/kill_scripts


%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests

%files -n python3-%{service}
%license LICENSE
%{python3_sitelib}/%{service}
%{python3_sitelib}/%{service}-*.egg-info
%exclude %{python3_sitelib}/%{service}/tests


%files common -f %{service}.lang
%license LICENSE
%doc README.rst
# though this script is not exactly needed on all nodes but for ovs and
# linuxbridge agents only, it's probably good enough to put it here
%{_bindir}/neutron-enable-bridge-firewall.sh
%{_bindir}/neutron-rootwrap
%{_bindir}/neutron-rootwrap-daemon
%dir %{_sysconfdir}/%{service}
%{_sysconfdir}/%{service}/conf.d/README
%dir %{_sysconfdir}/%{service}/conf.d
%dir %{_sysconfdir}/%{service}/conf.d/common
%dir %{_sysconfdir}/%{service}/plugins
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/ovn.ini
%{_sysconfdir}/%{service}/plugins/networking-ovn/networking-ovn.ini
%config(noreplace) %{_sysconfdir}/%{service}/rootwrap.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sudoers.d/%{service}
%dir %attr(0755, %{service}, %{service}) %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, %{service}) %{_localstatedir}/log/%{service}
%dir %{_datarootdir}/%{service}
%dir %{_datarootdir}/%{service}/rootwrap
%{_datarootdir}/%{service}/rootwrap/rootwrap.filters


%files linuxbridge
%license LICENSE
%{_bindir}/neutron-linuxbridge-agent
%{_unitdir}/neutron-linuxbridge-agent.service
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-linuxbridge-agent
%{_sysctldir}/99-neutron-linuxbridge-agent.conf
%{_sysconfdir}/sysconfig/modules/neutron-linuxbridge-agent.modules


%files macvtap-agent
%license LICENSE
%{_bindir}/neutron-macvtap-agent
%{_unitdir}/neutron-macvtap-agent.service
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-macvtap-agent


%files ml2
%license LICENSE
%doc %{service}/plugins/ml2/README
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/*.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini


%files openvswitch
%license LICENSE
%{_bindir}/neutron-openvswitch-agent
%{_unitdir}/neutron-openvswitch-agent.service
%{_unitdir}/neutron-destroy-patch-ports.service
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-openvswitch-agent
%{_sysctldir}/99-neutron-openvswitch-agent.conf
%{_sysconfdir}/sysconfig/modules/neutron-openvswitch-agent.modules


%files metering-agent
%license LICENSE
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/metering_agent.ini
%{_unitdir}/neutron-metering-agent.service
%{_bindir}/neutron-metering-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-metering-agent


%files rpc-server
%license LICENSE
%{_bindir}/neutron-rpc-server
%{_unitdir}/neutron-rpc-server.service
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-rpc-server


%files sriov-nic-agent
%license LICENSE
%{_unitdir}/neutron-sriov-nic-agent.service
%{_bindir}/neutron-sriov-nic-agent
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/sriov_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-sriov-nic-agent


%files ovn-metadata-agent
%license LICENSE
%{_bindir}/neutron-ovn-metadata-agent
%{_bindir}/networking-ovn-metadata-agent
%{_unitdir}/neutron-ovn-metadata-agent.service
%{_unitdir}/networking-ovn-metadata-agent.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/neutron_ovn_metadata_agent.ini
%dir %{_sysconfdir}/neutron/plugins/networking-ovn
%{_sysconfdir}/neutron/plugins/networking-ovn/networking-ovn-metadata-agent.ini
/etc/neutron/plugins/networking-ovn/networking-ovn.ini
%dir %{_sysconfdir}/neutron/conf.d/neutron-ovn-metadata-agent


%files ovn-agent
%license LICENSE
%{_bindir}/neutron-ovn-agent
%{_unitdir}/neutron-ovn-agent.service
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/ovn_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-ovn-agent


%files ovn-migration-tool
%license LICENSE
%{_bindir}/neutron-ovn-migration-mtu
%{_bindir}/ovn_migration.sh
%{_datadir}/ansible/neutron-ovn-migration/


%files ml2ovn-trace
%license LICENSE
%{_bindir}/ml2ovn-trace

%changelog

