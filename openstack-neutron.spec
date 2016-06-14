%global service neutron

Name:		openstack-%{service}
Version:    XXX
Release:    XXX{?dist}
Epoch:		1
Summary:	OpenStack Networking Service

License:	ASL 2.0
URL:		http://launchpad.net/%{service}/

Source0:	http://tarballs.openstack.org/%{service}/%{service}-master.tar.gz
Source1:	%{service}.logrotate
Source2:	%{service}-sudoers
Source10:	neutron-server.service
Source11:	neutron-linuxbridge-agent.service
Source12:	neutron-openvswitch-agent.service
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
Source28:	neutron-dev-server.service
Source29:	neutron-rpc-server.service

Source30:	%{service}-dist.conf
Source31:	conf.README

BuildArch:	noarch

BuildRequires:	git
BuildRequires:	python2-devel
BuildRequires:	python-d2to1
BuildRequires:	python-pbr
BuildRequires:	python-pecan
BuildRequires:	python-setuptools
BuildRequires:	systemd-units

Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}

# dnsmasq is not a hard requirement, but is currently the only option
# when neutron-dhcp-agent is deployed.
Requires:	dnsmasq
Requires:	dnsmasq-utils

# radvd is not a hard requirement, but is currently the only option
# for IPv6 deployments.
Requires:	radvd

# dibbler is not a hard requirement, but is currently the default option
# for IPv6 prefix delegation.
Requires:	dibbler-client

# conntrack is not a hard requirement, but is currently used by L3 agent
# to immediately drop connections after a floating IP is disassociated
Requires:	conntrack-tools

# keepalived is not a hard requirement, but is currently used by DVR L3
# agent
Requires:	keepalived

# Those are not hard requirements, ipset is used by ipset-cleanup in the subpackage,
# and iptables is used by the l3-agent which currently is not in a separate package.
Requires:	ipset
Requires:	iptables

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


%package -n python-%{service}
Summary:	Neutron Python libraries
Requires:	MySQL-python
Requires:	python-alembic >= 0.8.0
Requires:	python-debtcollector >= 0.3.0
Requires:	python-eventlet >= 0.17.4
Requires:	python-greenlet >= 0.3.2
Requires:	python-httplib2 >= 0.7.5
Requires:	python-jinja2 >= 2.6
Requires:	python-keystoneclient >= 1.6.0
Requires:	python-keystonemiddleware >= 2.0.0
Requires:	python-netaddr >= 0.7.12
Requires:	python-neutronclient >= 2.6.0
Requires:	python-novaclient >= 2.26.0
Requires:	python-oslo-concurrency >= 2.3.0
Requires:	python-oslo-config >= 2:2.1.0
Requires:	python-oslo-context >= 0.2.0
Requires:	python-oslo-db >= 2.0
Requires:	python-oslo-i18n >= 1.5.0
Requires:	python-oslo-log >= 1.8.0
Requires:	python-oslo-messaging >= 1.16.0
Requires:	python-oslo-middleware >= 2.4.0
Requires:	python-oslo-policy >= 0.5.0
Requires:	python-oslo-rootwrap >= 2.0.0
Requires:	python-oslo-serialization >= 1.4.0
Requires:	python-oslo-service >= 0.6.0
Requires:	python-oslo-utils >= 2.0.0
Requires:	python-oslo-versionedobjects >= 0.6.0
Requires:	python-oslo-context >= 0.2.0
Requires:	python-paste
Requires:	python-paste-deploy >= 1.5.0
Requires:	python-pecan >= 1.0.0
Requires:	python-pbr
Requires:	python-requests >= 2.5.2
Requires:	python-retrying >= 1.2.3
Requires:	python-routes >= 1.12.3
Requires:	python-ryu >= 3.23.2
Requires:	python-six >= 1.9.0
Requires:	python-sqlalchemy >= 0.9.7
Requires:	python-stevedore >= 1.5.0
Requires:	python-webob >= 1.2.3



%description -n python-%{service}
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron Python library.


%package -n python-%{service}-tests
Summary:	Neutron tests
Requires:	openstack-%{service} = %{epoch}:%{version}-%{release}
Requires:       python-tempest-lib >= 0.8.0
Requires:	python-tempest-lib >= 0.8.0


%description -n python-%{service}-tests
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains Neutron test files.


%package common
Summary:	Neutron common files
Requires(pre):	shadow-utils
Requires:	python-%{service} = %{epoch}:%{version}-%{release}
Requires:	sudo


%description common
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains Neutron common files.


%package bigswitch
Summary:	Neutron Big Switch plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description bigswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using the FloodLight Openflow Controller or the Big Switch
Networks Controller.


%package brocade
Summary:	Neutron Brocade plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}
Requires:	python-ncclient


%description brocade
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Brocade VCS switches running NOS.


%package cisco
Summary:	Neutron Cisco plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}
Requires:	python-ncclient


%description cisco
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Cisco UCS and Nexus.


%package dev-server
Summary:	Neutron Server (WSGI pecan)
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description dev-server
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains an alternative Neutron server implementation that uses
pecan library as its WSGI backend.


%package embrane
Summary:	Neutron Embrane plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description embrane
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
L3-L7 network services using Embrane's heleos platform.


%package linuxbridge
Summary:	Neutron linuxbridge plugin
Requires:	bridge-utils
Requires:	ebtables
Requires:	ipset
Requires:	iptables
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description linuxbridge
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks as VLANs using Linux bridging.


%package mellanox
Summary:	Neutron Mellanox plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description mellanox
This plugin implements Neutron v2 APIs with support for Mellanox embedded
switch functionality as part of the VPI (Ethernet/InfiniBand) HCA.


%package ml2
Summary:	Neutron ML2 plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}
# needed for brocade and cisco drivers
Requires:	python-ncclient


%description ml2
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains a Neutron plugin that allows the use of drivers
to support separately extensible sets of network types and the mechanisms
for accessing those types.


%package nuage
Summary:	Neutron Nuage plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description nuage
This plugin implements Neutron v2 APIs with support for Nuage Networks
Virtual Service Platform (VSP).


%package ofagent
Summary:	Neutron ofagent plugin from ryu project
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description ofagent
This plugin implements Neutron v2 APIs with support for the ryu ofagent
plugin.


%package oneconvergence-nvsd
Summary:	Neutron One Convergence NVSD plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description oneconvergence-nvsd
Neutron provides an API to dynamnically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using One Convergence NVSD


%package opencontrail
Summary:	Neutron OpenContrail plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description opencontrail
This plugin implements Neutron v2 APIs with support for the OpenContrail
plugin.


%package openvswitch
Summary:	Neutron openvswitch plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}
# We require openvswitch when using vsctl to access ovsdb;
# but if we use native access, then we just need python bindings.
# since we don't know what users actually use, we depend on both.
Requires:	ipset
Requires:	iptables
Requires:	openvswitch
Requires:	python-openvswitch


%description openvswitch
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using Open vSwitch.


%package ovsvapp
Summary:	Neutron OVSvApp vSphere plugin
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description ovsvapp
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains the Neutron plugin that implements virtual
networks using OVSvApp vSphere L2 agent.


%package metering-agent
Summary:	Neutron bandwidth metering agent
Requires:	iptables
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description metering-agent
Neutron provides an API to measure bandwidth utilization

This package contains the Neutron agent responsible for generating bandwidth
utilization notifications.


%package rpc-server
Summary:	Neutron (RPC only) Server
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description rpc-server
Neutron provides an API to dynamically request and configure virtual
networks.

This package contains an alternative Neutron server that handles AMQP RPC
workload only.


%package sriov-nic-agent
Summary:	Neutron SR-IOV NIC agent
Requires:	openstack-%{service}-common = %{epoch}:%{version}-%{release}


%description sriov-nic-agent
Neutron allows to run virtual instances using SR-IOV NIC hardware

This package contains the Neutron agent to support advanced features of
SR-IOV network cards.


%prep
%autosetup -n %{service}-%{upstream_version} -S git

find %{service} -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Let's handle dependencies ourseleves
rm -f requirements.txt

# Kill egg-info in order to generate new SOURCES.txt
rm -rf neutron.egg-info


%build
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
    sed -ri "0,/^$name *=/{s!^$name *=.*!# $name = $value!}" etc/%{service}.conf
  else
    sed -ri "0,/^(#)? *$name *=/{s!^(#)? *$name *=.*!# $name = $value!}" etc/%{service}.conf
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
install -d -m 755 %{buildroot}%{_datarootdir}/%{service}/rootwrap
mv %{buildroot}/usr/etc/%{service}/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/%{service}/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}/usr/etc/%{service}/* %{buildroot}%{_sysconfdir}/%{service}
mv %{buildroot}%{_sysconfdir}/%{service}/api-paste.ini %{buildroot}%{_datadir}/%{service}/api-paste.ini
chmod 640 %{buildroot}%{_sysconfdir}/%{service}/plugins/*/*.ini

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
install -p -D -m 644 %{SOURCE19} %{buildroot}%{_unitdir}/neutron-mlnx-agent.service
install -p -D -m 644 %{SOURCE20} %{buildroot}%{_unitdir}/neutron-metering-agent.service
install -p -D -m 644 %{SOURCE21} %{buildroot}%{_unitdir}/neutron-sriov-nic-agent.service
install -p -D -m 644 %{SOURCE22} %{buildroot}%{_unitdir}/neutron-netns-cleanup.service
install -p -D -m 644 %{SOURCE28} %{buildroot}%{_unitdir}/neutron-dev-server.service
install -p -D -m 644 %{SOURCE29} %{buildroot}%{_unitdir}/neutron-rpc-server.service

# Install scripts for pacemaker support
install -p -D -m 755 %{SOURCE23} %{buildroot}%{_prefix}/lib/ocf/lib/neutron/neutron-netns-cleanup
install -p -D -m 755 %{SOURCE24} %{buildroot}%{_prefix}/lib/ocf/lib/neutron/neutron-ovs-cleanup
install -p -D -m 755 %{SOURCE25} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/NetnsCleanup
install -p -D -m 755 %{SOURCE26} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/OVSCleanup
install -p -D -m 755 %{SOURCE27} %{buildroot}%{_prefix}/lib/ocf/resource.d/neutron/NeutronScale

# Install README file that describes how to configure services with custom configuration files
install -p -D -m 755 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{service}/conf.d/README

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{service}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{service}
install -d -m 755 %{buildroot}%{_localstatedir}/run/%{service}

# Install dist conf
install -p -D -m 640 %{SOURCE30} %{buildroot}%{_datadir}/%{service}/%{service}-dist.conf

# Create and populate configuration directory for L3 agent that is not accessible for user modification
mkdir -p %{buildroot}%{_datadir}/%{service}/l3_agent
ln -s %{_sysconfdir}/%{service}/l3_agent.ini %{buildroot}%{_datadir}/%{service}/l3_agent/l3_agent.conf

# Create dist configuration directory for neutron-server (may be filled by advanced services)
mkdir -p %{buildroot}%{_datadir}/%{service}/server

# Create configuration directories for all services that can be populated by users with custom *.conf files
mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/common
for service in server dev-server rpc-server ovs-cleanup netns-cleanup; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service
done
for service in linuxbridge openvswitch dhcp l3 metadata mlnx metering sriov-nic; do
    mkdir -p %{buildroot}/%{_sysconfdir}/%{service}/conf.d/%{service}-$service-agent
done

# Kill hyperv agent since it's of no use for Linux
rm %{buildroot}/%{_bindir}/neutron-hyperv-agent


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


%preun
%systemd_preun neutron-dhcp-agent.service
%systemd_preun neutron-l3-agent.service
%systemd_preun neutron-metadata-agent.service
%systemd_preun neutron-server.service
%systemd_preun neutron-netns-cleanup.service
%systemd_preun neutron-ovs-cleanup.service


%postun
%systemd_postun_with_restart neutron-dhcp-agent.service
%systemd_postun_with_restart neutron-l3-agent.service
%systemd_postun_with_restart neutron-metadata-agent.service
%systemd_postun_with_restart neutron-server.service


%post linuxbridge
%systemd_post neutron-linuxbridge-agent.service
oldconf=%{_sysconfdir}/%{service}/plugins/linuxbridge/linuxbridge_conf.ini
newconf=%{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
if [ $1 -gt 1 ]; then
    if [ -e $oldconf ]; then
        # Imitate noreplace
        cp $newconf ${newconf}.rpmnew
        cp $oldconf $newconf
    fi
fi


%preun linuxbridge
%systemd_preun neutron-linuxbridge-agent.service


%postun linuxbridge
%systemd_postun_with_restart neutron-linuxbridge-agent.service


%post mellanox
%systemd_post neutron-mlnx-agent.service


%preun mellanox
%systemd_preun neutron-mlnx-agent.service


%postun mellanox
%systemd_postun_with_restart neutron-mlnx-agent.service


%post openvswitch
%systemd_post neutron-openvswitch-agent.service
oldconf=%{_sysconfdir}/%{service}/plugins/openvswitch/ovs_neutron_plugin.ini
newconf=%{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini
if [ $1 -gt 1 ]; then
    if [ -e $oldconf ]; then
        # Imitate noreplace
        cp $newconf ${newconf}.rpmnew
        cp $oldconf $newconf
    fi
fi


%preun openvswitch
%systemd_preun neutron-openvswitch-agent.service


%postun openvswitch
%systemd_postun_with_restart neutron-openvswitch-agent.service


%post metering-agent
%systemd_post neutron-metering-agent.service


%preun metering-agent
%systemd_preun neutron-metering-agent.service


%postun metering-agent
%systemd_postun_with_restart neutron-metering-agent.service


%post sriov-nic-agent
%systemd_post neutron-sriov-nic-agent.service


%preun sriov-nic-agent
%systemd_preun neutron-sriov-nic-agent.service


%postun sriov-nic-agent
%systemd_postun_with_restart neutron-sriov-nic-agent.service


%files
%license LICENSE
%{_bindir}/neutron-db-manage
%{_bindir}/neutron-debug
%{_bindir}/neutron-dhcp-agent
%{_bindir}/neutron-ipset-cleanup
%{_bindir}/neutron-keepalived-state-change
%{_bindir}/neutron-l3-agent
%{_bindir}/neutron-metadata-agent
%{_bindir}/neutron-netns-cleanup
%{_bindir}/neutron-ns-metadata-proxy
%{_bindir}/neutron-ovs-cleanup
%{_bindir}/neutron-pd-notify
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
%attr(-, root, %{service}) %{_datadir}/%{service}/api-paste.ini
%dir %{_datadir}/%{service}/l3_agent
%dir %{_datadir}/%{service}/server
%{_datadir}/%{service}/l3_agent/*.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/dhcp_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/l3_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/metadata_agent.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/policy.json
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-dhcp-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-l3-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-metadata-agent
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-server
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-netns-cleanup
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-ovs-cleanup


%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%files -n python-%{service}
%license LICENSE
%{python2_sitelib}/%{service}
%{python2_sitelib}/%{service}-*.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%files common
%license LICENSE
%doc README.rst
%{_bindir}/neutron-rootwrap
%{_bindir}/neutron-rootwrap-daemon
%{_bindir}/neutron-rootwrap-xen-dom0
%dir %{_sysconfdir}/%{service}
%{_sysconfdir}/%{service}/conf.d/README
%dir %{_sysconfdir}/%{service}/conf.d
%dir %{_sysconfdir}/%{service}/conf.d/common
%dir %{_sysconfdir}/%{service}/plugins
%attr(-, root, %{service}) %{_datadir}/%{service}/%{service}-dist.conf
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/%{service}.conf
%config(noreplace) %{_sysconfdir}/%{service}/rootwrap.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sudoers.d/%{service}
%dir %attr(0755, %{service}, %{service}) %{_sharedstatedir}/%{service}
%dir %attr(0750, %{service}, %{service}) %{_localstatedir}/log/%{service}
%dir %{_datarootdir}/%{service}
%dir %{_datarootdir}/%{service}/rootwrap
%{_datarootdir}/%{service}/rootwrap/debug.filters
%{_datarootdir}/%{service}/rootwrap/dhcp.filters
%{_datarootdir}/%{service}/rootwrap/ebtables.filters
%{_datarootdir}/%{service}/rootwrap/ipset-firewall.filters
%{_datarootdir}/%{service}/rootwrap/iptables-firewall.filters
%{_datarootdir}/%{service}/rootwrap/l3.filters


%files bigswitch
%license LICENSE
%{_bindir}/neutron-restproxy-agent
%dir %{_sysconfdir}/%{service}/plugins/bigswitch
%{_sysconfdir}/%{service}/plugins/bigswitch/ssl
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/bigswitch/*.ini


%files brocade
%license LICENSE
%doc %{service}/plugins/brocade/README.md
%dir %{_sysconfdir}/%{service}/plugins/brocade
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/brocade/*.ini
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/brocade/vyatta/*.ini


%files cisco
%license LICENSE
%dir %{_sysconfdir}/%{service}/plugins/cisco
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/cisco/*.ini


%files embrane
%license LICENSE
%doc %{service}/plugins/embrane/README
%dir %{_sysconfdir}/%{service}/plugins/embrane
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/embrane/*.ini


%files dev-server
%license LICENSE
%{_bindir}/neutron-dev-server
%{_unitdir}/neutron-dev-server.service
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-dev-server


%files linuxbridge
%license LICENSE
%{_bindir}/neutron-linuxbridge-agent
%{_unitdir}/neutron-linuxbridge-agent.service
%{_datarootdir}/%{service}/rootwrap/linuxbridge-plugin.filters
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-linuxbridge-agent


%files mellanox
%license LICENSE
%doc %{service}/plugins/ml2/drivers/mlnx/README
%{_bindir}/neutron-mlnx-agent
%{_unitdir}/neutron-mlnx-agent.service
%dir %{_sysconfdir}/%{service}/plugins/mlnx
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/mlnx/*.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-mlnx-agent


%files ml2
%license LICENSE
%doc %{service}/plugins/ml2/README
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/*.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/linuxbridge_agent.ini
%exclude %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini


%files nuage
%license LICENSE
%{python2_sitelib}/%{service}/plugins/nuage
%dir %{_sysconfdir}/%{service}/plugins/nuage
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/nuage/*.ini


%files ofagent
%license LICENSE


%files oneconvergence-nvsd
%license LICENSE
%doc %{service}/plugins/oneconvergence/README
%dir %{_sysconfdir}/%{service}/plugins/oneconvergence
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/oneconvergence/*.ini
%{_bindir}/neutron-nvsd-agent


%files opencontrail
%license LICENSE
#%doc %{service}/plugins/opencontrail/README
%dir %{_sysconfdir}/%{service}/plugins/opencontrail
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/opencontrail/*.ini


%files openvswitch
%license LICENSE
%{_bindir}/neutron-openvswitch-agent
%{_unitdir}/neutron-openvswitch-agent.service
%{_datarootdir}/%{service}/rootwrap/openvswitch-plugin.filters
%dir %{_sysconfdir}/%{service}/plugins/ml2
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ml2/openvswitch_agent.ini
%dir %{_sysconfdir}/%{service}/conf.d/%{service}-openvswitch-agent


%files ovsvapp
%license LICENSE
%{_bindir}/neutron-ovsvapp-agent
# TODO: add a systemd unit file
%dir %{_sysconfdir}/%{service}/plugins/ovsvapp
%config(noreplace) %attr(0640, root, %{service}) %{_sysconfdir}/%{service}/plugins/ovsvapp/*.ini


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


%changelog
