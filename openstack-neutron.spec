%global release_name juno

Name:		openstack-neutron
Version:    XXX
Release:    XXX{?dist}
Provides:	openstack-quantum = %{version}-%{release}
Obsoletes:	openstack-quantum < 2013.2-0.4.b3
Summary:	OpenStack Networking Service

Group:		Applications/System
License:	ASL 2.0
URL:		http://launchpad.net/neutron/

Source0:	http://launchpad.net/neutron/%{release_name}/%{version}/+download/neutron-%{version}.tar.gz
Source1:	neutron.logrotate
Source2:	neutron-sudoers
Source10:	neutron-server.service
Source11:	neutron-linuxbridge-agent.service
Source12:	neutron-openvswitch-agent.service
Source14:	neutron-nec-agent.service
Source15:	neutron-dhcp-agent.service
Source16:	neutron-l3-agent.service
Source17:	neutron-metadata-agent.service
Source18:	neutron-ovs-cleanup.service
Source19:	neutron-mlnx-agent.service
Source20:	neutron-metering-agent.service
Source21:	neutron-sriov-nic-agent.service
Source22:	neutron-netns-cleanup.service
Source23:	neutron-netns-cleanup.init
Source24:	neutron-ovs-cleanup.init
Source25:	NetnsCleanup.ocf_ra
Source26:	OVSCleanup.ocf_ra
Source27:	NeutronScale.ocf_ra

Source30:	neutron-dist.conf

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-d2to1
BuildRequires:	python-pbr
BuildRequires:	python-setuptools
BuildRequires:	systemd-units

Requires:	python-neutron = %{version}-%{release}
Requires:	openstack-utils

# dnsmasq is not a hard requirement, but is currently the only option
# when neutron-dhcp-agent is deployed.
Requires:	dnsmasq
Requires:	dnsmasq-utils

# radvd is not a hard requirement, but is currently the only option
# for IPv6 deployments.
Requires:	radvd

# conntrack is not a hard requirement, but is currently used by L3 agent
# to immediately drop connections after a floating IP is disassociated
Requires:	conntrack-tools

# keepalived is not a hard requirement, but is currently used by DVR L3
# agent
Requires:	keepalived

# those are not hard requirements, but are used to implement firewall
# drivers.
Requires:	ipset
Requires:	iptables

Requires(pre): shadow-utils
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Neutron is a virtual network service for Openstack. Just like
OpenStack Nova provides an API to dynamically request and configure
virtual servers, Neutron provides an API to dynamically request and
configure virtual networks. These networks connect "interfaces" from
other OpenStack services (e.g., virtual NICs from Nova VMs). The
Neutron API supports extensions to provide advanced network
capabilities (e.g., QoS, ACLs, network monitoring, etc.)


%package -n python-neutron
Summary:	Neutron Python libraries
Group:		Applications/System

Provides:	python-quantum = %{version}-%{release}
Obsoletes:	python-quantum < 2013.2-0.4.b3

Requires:	MySQL-python
Requires:	python-alembic >= 0.6.4
Requires:	python-anyjson >= 0.3.3
Requires:	python-babel >= 1.3
Requires:	python-eventlet >= 0.15.1
Requires:	python-greenlet >= 0.3.2
Requires:	python-httplib2 >= 0.7.5
Requires:	python-iso8601 >= 0.1.9
Requires:	python-jinja2
Requires:	python-jsonrpclib
Requires:	python-keystoneclient >= 0.10.0
Requires:	python-keystonemiddleware >= 1.0.0
Requires:	python-netaddr >= 0.7.12
Requires:	python-neutronclient >= 2.3.6
Requires:	python-novaclient >= 2.18.0
Requires:	python-oslo-config >= 2:1.4.0
Requires:	python-oslo-db >= 1.0.0
Requires:	python-oslo-messaging >= 1.4.0.0
Requires:	python-oslo-rootwrap >= 1.3.0.0
Requires:	python-oslo-serialization >= 1.0.0
Requires:	python-oslo-utils >= 1.1.0
Requires:	python-oslo-context
Requires:	python-paste
Requires:	python-paste-deploy >= 1.5.0
Requires:	python-pbr
Requires:	python-qpid
Requires:	python-requests >= 1.2.1
Requires:	python-routes >= 1.12.3
Requires:	python-sqlalchemy >= 0.9.7
Requires:	python-stevedore >= 1.0.0
Requires:	python-six >= 1.7.0
Requires:	python-webob >= 1.2.3
Requires:	sudo
Requires:	python-retrying
Requires:	python-oslo-concurrency
Requires:	python-oslo-i18n
Requires:	python-oslo-middleware



%description -n python-neutron
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron Python library.


%package -n python-neutron-tests
Summary:	Neutron tests
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}


%description -n python-neutron-tests
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains Neutron test files.


%package bigswitch
Summary:	Neutron Big Switch plugin
Group:		Applications/System

Provides:	openstack-quantum-bigswitch = %{version}-%{release}
Obsoletes:	openstack-quantum-bigswitch < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description bigswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using the FloodLight Openflow Controller or the Big Switch
Networks Controller.


%package brocade
Summary:	Neutron Brocade plugin
Group:		Applications/System

Provides:	openstack-quantum-brocade = %{version}-%{release}
Obsoletes:	openstack-quantum-brocade < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}
Requires:	python-ncclient


%description brocade
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Brocade VCS switches running NOS.


%package cisco
Summary:	Neutron Cisco plugin
Group:		Applications/System

Provides:	openstack-quantum-cisco = %{version}-%{release}
Obsoletes:	openstack-quantum-cisco < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}
Requires:	python-ncclient


%description cisco
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Cisco UCS and Nexus.


%package embrane
Summary:	Neutron Embrane plugin
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}


%description embrane
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
L3-L7 network services using Embrane's heleos platform.


%package hyperv
Summary:	Neutron Hyper-V agent
Group:		Applications/System

Provides:	openstack-quantum-hyperv = %{version}-%{release}
Obsoletes:	openstack-quantum-hyperv < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description hyperv
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron agent that implements virtual
networks using Microsoft Hyper-V.


%package ibm
Summary:	Neutron IBM plugin
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}


%description ibm
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks from IBM.


%package linuxbridge
Summary:	Neutron linuxbridge plugin
Group:		Applications/System

Provides:	openstack-quantum-linuxbridge = %{version}-%{release}
Obsoletes:	openstack-quantum-linuxbridge < 2013.2-0.4.b3

Requires:	bridge-utils
Requires:	openstack-neutron = %{version}-%{release}


%description linuxbridge
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks as VLANs using Linux bridging.


%package mellanox
Summary:	Neutron Mellanox plugin
Group:		Applications/System

Provides:	openstack-quantum-mellanox = %{version}-%{release}
Obsoletes:	openstack-quantum-mellanox < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description mellanox
This plugin implements Neutron v2 APIs with support for Mellanox embedded
switch functionality as part of the VPI (Ethernet/InfiniBand) HCA.


%package metaplugin
Summary:	Neutron meta plugin
Group:		Applications/System

Provides:	openstack-quantum-metaplugin = %{version}-%{release}
Obsoletes:	openstack-quantum-metaplugin < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description metaplugin
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using multiple other Neutron plugins.


%package midonet
Summary:	Neutron MidoNet plugin
Group:		Applications/System

Provides:	openstack-quantum-midonet = %{version}-%{release}
Obsoletes:	openstack-quantum-midonet < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description midonet
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using MidoNet from Midokura.


%package ml2
Summary:	Neutron ML2 plugin
Group:		Applications/System

Provides:	openstack-quantum-ml2 = %{version}-%{release}
Obsoletes:	openstack-quantum-ml2 < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}
# needed for brocade and cisco drivers
Requires:	python-ncclient


%description ml2
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains a Neutron plugin that allows the use of drivers
to support separately extensible sets of network types and the mechanisms
for accessing those types.


%package nec
Summary:	Neutron NEC plugin
Group:		Applications/System

Provides:	openstack-quantum-nec = %{version}-%{release}
Obsoletes:	openstack-quantum-nec < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description nec
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using the NEC OpenFlow controller.


%package nuage
Summary:	Neutron Nuage plugin
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}


%description nuage
This plugin implements Neutron v2 APIs with support for Nuage Networks
Virtual Service Platform (VSP).


%package ofagent
Summary:	Neutron ofagent plugin from ryu project
Group:		Applications/system

Requires:	openstack-neutron = %{version}-%{release}


%description ofagent
This plugin implements Neutron v2 APIs with support for the ryu ofagent
plugin.


%package oneconvergence-nvsd
Summary:	Neutron One Convergence NVSD plugin
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}


%description oneconvergence-nvsd
Neutron provides an API to dynamnically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using One Convergence NVSD


%package opencontrail
Summary:	Neutron OpenContrail plugin
Group:		Applications/system

Requires:	openstack-neutron = %{version}-%{release}


%description opencontrail
This plugin implements Neutron v2 APIs with support for the OpenContrail
plugin.


%package openvswitch
Summary:	Neutron openvswitch plugin
Group:		Applications/System

Provides:	openstack-quantum-openvswitch = %{version}-%{release}
Obsoletes:	openstack-quantum-openvswitch < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}
Requires:	openvswitch


%description openvswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Open vSwitch.


%package plumgrid
Summary:	Neutron PLUMgrid plugin
Group:		Applications/System

Provides:	openstack-quantum-plumgrid = %{version}-%{release}
Obsoletes:	openstack-quantum-plumgrid < 2013.2-0.4.b3

Requires:	openstack-neutron = %{version}-%{release}


%description plumgrid
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using the PLUMgrid platform.


%package vmware
Summary:	Neutron Nicira plugin
Group:		Applications/System

Provides:	openstack-neutron-nicira = %{version}-%{release}
Obsoletes:	openstack-neutron-nicira < 2014.1-0.5.b2

Requires:	openstack-neutron = %{version}-%{release}


%description vmware
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using VMware NSX.


%package metering-agent
Summary:	Neutron bandwidth metering agent
Group:		Applications/System

Requires:	openstack-neutron = %{version}-%{release}

%description metering-agent
Neutron provides an API to measure bandwidth utilization

This package contains the Neutron agent responsible for generating bandwidth
utilization notifications.


%package sriov-nic-agent
Summary:	Neutron SR-IOV NIC agent
Group:		Applications/system

Requires:	openstack-neutron = %{version}-%{release}


%description sriov-nic-agent
Neutron allows to run virtual instances using SR-IOV NIC hardware

This package contains the Neutron agent to support advanced features of
SR-IOV network cards.


%prep
%setup -q -n neutron-%{upstream_version}

find neutron -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourseleves
rm -f requirements.txt


%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build

# Loop through values in neutron-dist.conf and make sure that the values
# are substituted into the neutron.conf as comments. Some of these values
# will have been uncommented as a way of upstream setting defaults outside
# of the code. For notification_driver, there are commented examples
# above uncommented settings, so this specifically skips those comments
# and instead comments out the actual settings and substitutes the
# correct default values.
while read name eq value; do
  test "$name" && test "$value" || continue
  if [ "$name" = "notification_driver" ]; then
    sed -ri "0,/^$name *=/{s!^$name *=.*!# $name = $value!}" etc/neutron.conf
  else
    sed -ri "0,/^(#)? *$name *=/{s!^(#)? *$name *=.*!# $name = $value!}" etc/neutron.conf
  fi
done < %{SOURCE30}

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python2_sitelib}/bin
rm -rf %{buildroot}%{python2_sitelib}/doc
rm -rf %{buildroot}%{python2_sitelib}/tools
rm %{buildroot}/usr/etc/init.d/neutron-server

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/neutron/rootwrap
mv %{buildroot}/usr/etc/neutron/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/neutron/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/neutron
mv %{buildroot}/usr/etc/neutron/* %{buildroot}%{_sysconfdir}/neutron
mv %{buildroot}%{_sysconfdir}/neutron/api-paste.ini %{buildroot}%{_datadir}/neutron/api-paste.ini
chmod 640  %{buildroot}%{_sysconfdir}/neutron/plugins/*/*.ini

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-neutron

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/neutron

# Install systemd units
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/neutron-server.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/neutron-linuxbridge-agent.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/neutron-openvswitch-agent.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/neutron-nec-agent.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/neutron-dhcp-agent.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/neutron-l3-agent.service
install -p -D -m 644 %{SOURCE17} %{buildroot}%{_unitdir}/neutron-metadata-agent.service
install -p -D -m 644 %{SOURCE18} %{buildroot}%{_unitdir}/neutron-ovs-cleanup.service
install -p -D -m 644 %{SOURCE19} %{buildroot}%{_unitdir}/neutron-mlnx-agent.service
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/neutron-metering-agent.service
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/neutron-sriov-nic-agent.service
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_unitdir}/neutron-netns-cleanup.service

# Install scripts for pacemaker support
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_prefix}/lib/ocf/lib/neutron/neutron-netns-cleanup
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_prefix}/lib/ocf/lib/neutron/neutron-ovs-cleanup
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/NetnsCleanup
install -p -D -m 755 %{SOURCE26} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/OVSCleanup
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/NeutronScale

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/neutron
install -d -m 755 %{buildroot}%{_sharedstatedir}/neutron
install -d -m 755 %{buildroot}%{_localstatedir}/log/neutron
install -d -m 755 %{buildroot}%{_localstatedir}/run/neutron

# Install dist conf
install -p -D -m 640 %{SOURCE30} %{buildroot}%{_datadir}/neutron/neutron-dist.conf

# Create and populate configuration directory for L3 agent
mkdir -p %{buildroot}%{_sysconfdir}/neutron/l3_agent
ln -s ../l3_agent.ini %{buildroot}%{_sysconfdir}/neutron/l3_agent/l3_agent.conf

%pre
getent group neutron >/dev/null || groupadd -r neutron
getent passwd neutron >/dev/null || \
    useradd -r -g neutron -d %{_sharedstatedir}/neutron -s /sbin/nologin \
    -c "OpenStack Neutron Daemons" neutron
exit 0


%post
%systemd_post neutron-dhcp-agent.service
%systemd_post neutron-l3-agent.service
%systemd_post neutron-metadata-agent.service
%systemd_post neutron-server.service


%preun
%systemd_preun neutron-dhcp-agent.service
%systemd_preun neutron-l3-agent.service
%systemd_preun neutron-metadata-agent.service
%systemd_preun neutron-server.service


%postun
%systemd_postun_with_restart neutron-dhcp-agent.service
%systemd_postun_with_restart neutron-l3-agent.service
%systemd_postun_with_restart neutron-metadata-agent.service
%systemd_postun_with_restart neutron-server.service


%preun linuxbridge
%systemd_preun neutron-linuxbridge-agent.service


%postun linuxbridge
%systemd_postun_with_restart neutron-linuxbridge-agent.service


%preun mellanox
%systemd_preun neutron-mlnx-agent.service


%postun mellanox
%systemd_postun_with_restart neutron-mlnx-agent.service


%preun nec
%systemd_preun neutron-nec-agent.service


%postun nec
%systemd_postun_with_restart neutron-nec-agent.service


%preun openvswitch
%systemd_preun neutron-openvswitch-agent.service


%postun openvswitch
%systemd_postun_with_restart neutron-openvswitch-agent.service


%preun metering-agent
%systemd_preun neutron-metering-agent.service


%postun metering-agent
%systemd_postun_with_restart neutron-metering-agent.service


%preun sriov-nic-agent
%systemd_preun neutron-sriov-nic-agent.service


%postun sriov-nic-agent
%systemd_postun_with_restart neutron-sriov-nic-agent.service


%files
%license LICENSE
%doc README.rst

%{_bindir}/neutron-db-manage
%{_bindir}/neutron-debug
%{_bindir}/neutron-dhcp-agent
%{_bindir}/neutron-l3-agent
%{_bindir}/neutron-metadata-agent
%{_bindir}/neutron-netns-cleanup
%{_bindir}/neutron-ns-metadata-proxy
%{_bindir}/neutron-ovs-cleanup
%{_bindir}/neutron-rootwrap
%{_bindir}/neutron-rootwrap-daemon
%{_bindir}/neutron-rootwrap-xen-dom0
%{_bindir}/neutron-sanity-check
%{_bindir}/neutron-server
%{_bindir}/neutron-usage-audit

%{_prefix}/lib/ocf/lib/neutron/neutron-netns-cleanup
%{_prefix}/lib/ocf/lib/neutron/neutron-ovs-cleanup
%{_prefix}/lib/ocf/resource.d/neutron/NetnsCleanup
%{_prefix}/lib/ocf/resource.d/neutron/OVSCleanup
%{_prefix}/lib/ocf/resource.d/neutron/NeutronScale

%{_unitdir}/neutron-dhcp-agent.service
%{_unitdir}/neutron-l3-agent.service
%{_unitdir}/neutron-metadata-agent.service
%{_unitdir}/neutron-server.service
%{_unitdir}/neutron-netns-cleanup.service
%{_unitdir}/neutron-ovs-cleanup.service
%dir %{_sysconfdir}/neutron
%attr(-, root, neutron) %{_datadir}/neutron/neutron-dist.conf
%attr(-, root, neutron) %{_datadir}/neutron/api-paste.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/dhcp_agent.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/l3_agent.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/metadata_agent.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/policy.json
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/neutron.conf
%config(noreplace) %{_sysconfdir}/neutron/rootwrap.conf
%dir %{_sysconfdir}/neutron/plugins
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config %{_sysconfdir}/sudoers.d/neutron
%{_sysconfdir}/neutron/l3_agent/*.conf
%dir %attr(0755, neutron, neutron) %{_sharedstatedir}/neutron
%dir %attr(0750, neutron, neutron) %{_localstatedir}/log/neutron
%dir %{_datarootdir}/neutron
%dir %{_datarootdir}/neutron/rootwrap
%{_datarootdir}/neutron/rootwrap/debug.filters
%{_datarootdir}/neutron/rootwrap/dhcp.filters
%{_datarootdir}/neutron/rootwrap/ipset-firewall.filters
%{_datarootdir}/neutron/rootwrap/iptables-firewall.filters
%{_datarootdir}/neutron/rootwrap/l3.filters


%files -n python-neutron-tests
%{python2_sitelib}/neutron/tests


%files -n python-neutron
%doc LICENSE
%doc README.rst
%{python2_sitelib}/neutron
%{python2_sitelib}/neutron-*.egg-info
%exclude %{python2_sitelib}/neutron/tests


%files bigswitch
%doc LICENSE
%{_bindir}/neutron-restproxy-agent
%dir %{_sysconfdir}/neutron/plugins/bigswitch
%{_sysconfdir}/neutron/plugins/bigswitch/ssl
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/bigswitch/*.ini


%files brocade
%doc LICENSE
%doc neutron/plugins/brocade/README.md
%dir %{_sysconfdir}/neutron/plugins/brocade
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/brocade/*.ini
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/brocade/vyatta/*.ini


%files cisco
%doc LICENSE
%doc neutron/plugins/cisco/README
%dir %{_sysconfdir}/neutron/plugins/cisco
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/cisco/*.ini


%files embrane
%doc LICENSE
%doc neutron/plugins/embrane/README
%dir %{_sysconfdir}/neutron/plugins/embrane
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/embrane/*.ini


%files hyperv
%doc LICENSE
%{_bindir}/neutron-hyperv-agent


%files ibm
%doc LICENSE
%{_bindir}/neutron-ibm-agent
%doc neutron/plugins/ibm/README
%dir %{_sysconfdir}/neutron/plugins/ibm
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ibm/*.ini


%files linuxbridge
%doc LICENSE
%doc neutron/plugins/linuxbridge/README
%{_bindir}/neutron-linuxbridge-agent
%{_unitdir}/neutron-linuxbridge-agent.service
%{_datarootdir}/neutron/rootwrap/linuxbridge-plugin.filters
%dir %{_sysconfdir}/neutron/plugins/linuxbridge
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/linuxbridge/*.ini


%files mellanox
%doc LICENSE
%doc neutron/plugins/ml2/drivers/mlnx/README
%{_bindir}/neutron-mlnx-agent
%{_unitdir}/neutron-mlnx-agent.service
%dir %{_sysconfdir}/neutron/plugins/mlnx
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/mlnx/*.ini


%files metaplugin
%doc LICENSE
%doc neutron/plugins/metaplugin/README
%dir %{_sysconfdir}/neutron/plugins/metaplugin
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/metaplugin/*.ini


%files midonet
%doc LICENSE
#%doc neutron/plugins/midonet/README
%dir %{_sysconfdir}/neutron/plugins/midonet
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/midonet/*.ini


%files ml2
%doc LICENSE
%doc neutron/plugins/ml2/README
%dir %{_sysconfdir}/neutron/plugins/ml2
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/ml2/*.ini


%files nec
%doc LICENSE
%doc neutron/plugins/nec/README
%{_bindir}/neutron-nec-agent
%{_unitdir}/neutron-nec-agent.service
%{_datarootdir}/neutron/rootwrap/nec-plugin.filters
%dir %{_sysconfdir}/neutron/plugins/nec
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/nec/*.ini


%files nuage
%doc LICENSE
%{python2_sitelib}/neutron/plugins/nuage
%dir %{_sysconfdir}/neutron/plugins/nuage
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/nuage/*.ini


%files ofagent
%doc LICENSE


%files oneconvergence-nvsd
%doc LICENSE
%doc neutron/plugins/oneconvergence/README
%dir %{_sysconfdir}/neutron/plugins/oneconvergence
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/oneconvergence/*.ini
%{_bindir}/neutron-nvsd-agent


%files opencontrail
%doc LICENSE
#%doc neutron/plugins/opencontrail/README
%dir %{_sysconfdir}/neutron/plugins/opencontrail
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/opencontrail/*.ini


%files openvswitch
%doc LICENSE
%doc neutron/plugins/openvswitch/README
%{_bindir}/neutron-openvswitch-agent
%{_unitdir}/neutron-openvswitch-agent.service
%{_datarootdir}/neutron/rootwrap/openvswitch-plugin.filters
%dir %{_sysconfdir}/neutron/plugins/openvswitch
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/openvswitch/*.ini


%files plumgrid
%doc LICENSE
%doc neutron/plugins/plumgrid/README
%dir %{_sysconfdir}/neutron/plugins/plumgrid
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/plumgrid/*.ini


%files vmware
%doc LICENSE
%dir %{_sysconfdir}/neutron/plugins/vmware
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/plugins/vmware/*.ini


%files metering-agent
%doc LICENSE
%config(noreplace) %attr(0640, root, neutron) %{_sysconfdir}/neutron/metering_agent.ini
%{_unitdir}/neutron-metering-agent.service
%{_bindir}/neutron-metering-agent


%files sriov-nic-agent
%doc LICENSE
%{_unitdir}/neutron-sriov-nic-agent.service
%{_bindir}/neutron-sriov-nic-agent


%changelog
