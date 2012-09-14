#
# This is 2012.2 folsom rc1
#

Name:		openstack-quantum
Version:	2012.2
Release:	0.7.rc1%{?dist}
Summary:	Virtual network service for OpenStack (quantum)

Group:		Applications/System
License:	ASL 2.0
URL:		http://launchpad.net/quantum/

Source0:	https://launchpad.net/quantum/folsom/folsom-rc1/+download/quantum-2012.2~rc1.tar.gz
Source1:	quantum.logrotate
Source2:	quantum-sudoers
Source4:	quantum-server-setup
Source5:	quantum-node-setup
Source6:	quantum-dhcp-setup
Source7:	quantum-l3-setup

Source10:	quantum-server.service
Source11:	quantum-linuxbridge-agent.service
Source12:	quantum-openvswitch-agent.service
Source13:	quantum-ryu-agent.service
Source14:	quantum-nec-agent.service
Source15:	quantum-dhcp-agent.service
Source16:	quantum-l3-agent.service


# Remove #!/bin/python (https://bugs.launchpad.net/quantum/+bug/1050053)
Patch0001: quantum.git-12e2afc113add0150f3f6f5d2975929367854880.patch

# Fix filters_path (https://bugs.launchpad.net/quantum/+bug/1050062)
Patch0002: quantum.git-713d92e7b1397386be8fbca3a29eaa492e28f2b6.patch

# Missing quantum-nec-agent executable (https://bugs.launchpad.net/quantum/+bug/1050047)
Patch0003: quantum.git-7e2db08e6f4ed5f0d640b4c07189a8edd0b28b28.patch

# Install rootwrap files (https://bugs.launchpad.net/quantum/+bug/1050045)
Patch0004: quantum.git-39cce9beddc6d3ed78c8c55bd972465a7af69420.patch


BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	systemd-units

Requires:	python-quantum = %{version}-%{release}
Requires:	openstack-utils

Requires(pre):	shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
Quantum is a virtual network service for Openstack. Just like
OpenStack Nova provides an API to dynamically request and configure
virtual servers, Quantum provides an API to dynamically request and
configure virtual networks. These networks connect "interfaces" from
other OpenStack services (e.g., virtual NICs from Nova VMs). The
Quantum API supports extensions to provide advanced network
capabilities (e.g., QoS, ACLs, network monitoring, etc.)


%package -n python-quantum
Summary:	Quantum Python libraries
Group:		Applications/System

Requires:	MySQL-python
Requires:	python-amqplib
Requires:	python-anyjson
Requires:	python-eventlet
Requires:	python-greenlet
Requires:	python-httplib2
Requires:	python-iso8601
Requires:	python-kombu
Requires:	python-lxml
Requires:	python-netaddr
Requires:	python-paste-deploy
Requires:	python-qpid
Requires:	python-quantumclient >= 2.0.22
Requires:	python-routes
Requires:	python-sqlalchemy
Requires:	python-webob
Requires:	sudo



%description -n python-quantum
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum Python library.


%package -n openstack-quantum-cisco
Summary:	Quantum Cisco plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}
Requires:	python-configobj


%description -n openstack-quantum-cisco
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Cisco UCS and Nexus.


%package -n openstack-quantum-linuxbridge
Summary:	Quantum linuxbridge plugin
Group:		Applications/System

Requires:	bridge-utils
Requires:	openstack-quantum = %{version}-%{release}
Requires:	python-pyudev


%description -n openstack-quantum-linuxbridge
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks as VLANs using Linux bridging.


%package -n openstack-quantum-nicira
Summary:	Quantum Nicira plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-nicira
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Nicira NVP.


%package -n openstack-quantum-openvswitch
Summary:	Quantum openvswitch plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}
Requires:	openvswitch


%description -n openstack-quantum-openvswitch
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using Open vSwitch.


%package -n openstack-quantum-ryu
Summary:	Quantum Ryu plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-ryu
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using the Ryu Network Operating System.


%package -n openstack-quantum-nec
Summary:	Quantum NEC plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-nec
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using the NEC OpenFlow controller.


%package -n openstack-quantum-metaplugin
Summary:	Quantum meta plugin
Group:		Applications/System

Requires:	openstack-quantum = %{version}-%{release}


%description -n openstack-quantum-metaplugin
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum plugin that implements virtual
networks using multiple other quantum plugins.


%prep
%setup -q -n quantum-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1

find quantum -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;

chmod 644 quantum/plugins/cisco/README

# Adjust configuration file content
sed -i 's/debug = True/debug = False/' etc/quantum.conf
sed -i 's/\# auth_strategy = keystone/auth_strategy = noauth/' etc/quantum.conf

# Remove unneeded dependency
sed -i '/setuptools_git/d' setup.py


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/bin
rm -rf %{buildroot}%{python_sitelib}/doc
rm -rf %{buildroot}%{python_sitelib}/tools
rm -rf %{buildroot}%{python_sitelib}/quantum/tests
rm -rf %{buildroot}%{python_sitelib}/quantum/plugins/*/tests
rm -f %{buildroot}%{python_sitelib}/quantum/plugins/*/run_tests.*
rm %{buildroot}/usr/etc/init.d/quantum-server

# Install execs (using hand-coded rather than generated versions)
install -p -D -m 755 bin/quantum-debug %{buildroot}%{_bindir}/quantum-debug
install -p -D -m 755 bin/quantum-dhcp-agent %{buildroot}%{_bindir}/quantum-dhcp-agent
install -p -D -m 755 bin/quantum-dhcp-agent-dnsmasq-lease-update %{buildroot}%{_bindir}/quantum-dhcp-agent-dnsmasq-lease-update
install -p -D -m 755 bin/quantum-l3-agent %{buildroot}%{_bindir}/quantum-l3-agent
install -p -D -m 755 bin/quantum-linuxbridge-agent %{buildroot}%{_bindir}/quantum-linuxbridge-agent
install -p -D -m 755 bin/quantum-nec-agent %{buildroot}%{_bindir}/quantum-nec-agent
install -p -D -m 755 bin/quantum-netns-cleanup %{buildroot}%{_bindir}/quantum-netns-cleanup
install -p -D -m 755 bin/quantum-openvswitch-agent %{buildroot}%{_bindir}/quantum-openvswitch-agent
install -p -D -m 755 bin/quantum-rootwrap %{buildroot}%{_bindir}/quantum-rootwrap
install -p -D -m 755 bin/quantum-ryu-agent %{buildroot}%{_bindir}/quantum-ryu-agent
install -p -D -m 755 bin/quantum-server %{buildroot}%{_bindir}/quantum-server

# Move rootwrap files to proper location
install -d -m 755 %{buildroot}%{_datarootdir}/quantum/rootwrap
mv %{buildroot}/usr/etc/quantum/rootwrap.d/*.filters %{buildroot}%{_datarootdir}/quantum/rootwrap

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/quantum
mv %{buildroot}/usr/etc/quantum/* %{buildroot}%{_sysconfdir}/quantum
chmod 640  %{buildroot}%{_sysconfdir}/quantum/plugins/*/*.ini

# Install files missing from setup.py (https://bugs.launchpad.net/quantum/+bug/1050045)
install -p -D -m 640 etc/l3_agent.ini %{buildroot}%{_sysconfdir}/quantum/l3_agent.ini

# Configure agents to use quantum-rootwrap
for f in %{buildroot}%{_sysconfdir}/quantum/plugins/*/*.ini %{buildroot}%{_sysconfdir}/quantum/*_agent.ini; do
    sed -i 's/^root_helper.*/root_helper = sudo quantum-rootwrap \/etc\/quantum\/rootwrap.conf/g' $f
done

# Configure quantum-dhcp-agent state_path
sed -i 's/state_path = \/opt\/stack\/data/state_path = \/var\/lib\/quantum/' %{buildroot}%{_sysconfdir}/quantum/dhcp_agent.ini

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-quantum

# Install sudoers
install -p -D -m 440 %{SOURCE2} %{buildroot}%{_sysconfdir}/sudoers.d/quantum

# Install systemd units
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/quantum-server.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/quantum-linuxbridge-agent.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/quantum-openvswitch-agent.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/quantum-ryu-agent.service
install -p -D -m 644 %{SOURCE14} %{buildroot}%{_unitdir}/quantum-nec-agent.service
install -p -D -m 644 %{SOURCE15} %{buildroot}%{_unitdir}/quantum-dhcp-agent.service
install -p -D -m 644 %{SOURCE16} %{buildroot}%{_unitdir}/quantum-l3-agent.service

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/quantum
install -d -m 755 %{buildroot}%{_localstatedir}/log/quantum

# Install setup helper scripts
install -p -D -m 755 %{SOURCE4} %{buildroot}%{_bindir}/quantum-server-setup
install -p -D -m 755 %{SOURCE5} %{buildroot}%{_bindir}/quantum-node-setup
install -p -D -m 755 %{SOURCE6} %{buildroot}%{_bindir}/quantum-dhcp-setup
install -p -D -m 755 %{SOURCE7} %{buildroot}%{_bindir}/quantum-l3-setup


%pre
getent group quantum >/dev/null || groupadd -r quantum --gid 164
getent passwd quantum >/dev/null || \
    useradd --uid 164 -r -g quantum -d %{_sharedstatedir}/quantum -s /sbin/nologin \
    -c "OpenStack Quantum Daemons" quantum
exit 0


%post
if [ $1 -eq 1 ] ; then
    # Initial installation
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi


%preun
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable quantum-server.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-server.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable quantum-dhcp-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-dhcp-agent.service > /dev/null 2>&1 || :
    /bin/systemctl --no-reload disable quantum-l3-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-l3-agent.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart quantum-server.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart quantum-dhcp-agent.service >/dev/null 2>&1 || :
    /bin/systemctl try-restart quantum-l3-agent.service >/dev/null 2>&1 || :
fi


%preun -n openstack-quantum-linuxbridge
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable quantum-linuxbridge-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-linuxbridge-agent.service > /dev/null 2>&1 || :
fi


%postun -n openstack-quantum-linuxbridge
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart quantum-linuxbridge-agent.service >/dev/null 2>&1 || :
fi


%preun -n openstack-quantum-openvswitch
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable quantum-openvswitch-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-openvswitch-agent.service > /dev/null 2>&1 || :
fi


%postun -n openstack-quantum-openvswitch
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart quantum-openvswitch-agent.service >/dev/null 2>&1 || :
fi


%preun -n openstack-quantum-ryu
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable quantum-ryu-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-ryu-agent.service > /dev/null 2>&1 || :
fi


%postun -n openstack-quantum-ryu
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart quantum-ryu-agent.service >/dev/null 2>&1 || :
fi


%preun -n openstack-quantum-nec
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable quantum-nec-agent.service > /dev/null 2>&1 || :
    /bin/systemctl stop quantum-nec-agent.service > /dev/null 2>&1 || :
fi


%postun -n openstack-quantum-nec
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart quantum-nec-agent.service >/dev/null 2>&1 || :
fi


%files
%doc LICENSE
%doc README
%{_bindir}/quantum-debug
%{_bindir}/quantum-dhcp-agent
%{_bindir}/quantum-dhcp-agent-dnsmasq-lease-update
%{_bindir}/quantum-dhcp-setup
%{_bindir}/quantum-l3-agent
%{_bindir}/quantum-l3-setup
%{_bindir}/quantum-netns-cleanup
%{_bindir}/quantum-node-setup
%{_bindir}/quantum-rootwrap
%{_bindir}/quantum-server
%{_bindir}/quantum-server-setup
%{_unitdir}/quantum-dhcp-agent.service
%{_unitdir}/quantum-l3-agent.service
%{_unitdir}/quantum-server.service
%dir %{_sysconfdir}/quantum
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/api-paste.ini
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/dhcp_agent.ini
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/l3_agent.ini
%config(noreplace) %{_sysconfdir}/quantum/policy.json
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/quantum.conf
%config(noreplace) %{_sysconfdir}/quantum/rootwrap.conf
%dir %{_sysconfdir}/quantum/plugins
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%config(noreplace) %{_sysconfdir}/sudoers.d/quantum
%dir %attr(0755, quantum, quantum) %{_sharedstatedir}/quantum
%dir %attr(0755, quantum, quantum) %{_localstatedir}/log/quantum
%dir %{_datarootdir}/quantum
%dir %{_datarootdir}/quantum/rootwrap
%{_datarootdir}/quantum/rootwrap/dhcp.filters
%{_datarootdir}/quantum/rootwrap/iptables-firewall.filters
%{_datarootdir}/quantum/rootwrap/l3.filters


%files -n python-quantum
%doc LICENSE
%doc README
%{python_sitelib}/quantum
%exclude %{python_sitelib}/quantum/extensions/_credential_view.py*
%exclude %{python_sitelib}/quantum/extensions/portprofile.py*
%exclude %{python_sitelib}/quantum/extensions/novatenant.py*
%exclude %{python_sitelib}/quantum/extensions/credential.py*
%exclude %{python_sitelib}/quantum/extensions/_novatenant_view.py*
%exclude %{python_sitelib}/quantum/extensions/multiport.py*
%exclude %{python_sitelib}/quantum/extensions/_pprofiles.py*
%exclude %{python_sitelib}/quantum/extensions/qos.py*
%exclude %{python_sitelib}/quantum/extensions/_qos_view.py*
%exclude %{python_sitelib}/quantum/plugins/cisco
%exclude %{python_sitelib}/quantum/plugins/linuxbridge
%exclude %{python_sitelib}/quantum/plugins/metaplugin
%exclude %{python_sitelib}/quantum/plugins/nec
%exclude %{python_sitelib}/quantum/plugins/nicira
%exclude %{python_sitelib}/quantum/plugins/openvswitch
%exclude %{python_sitelib}/quantum/plugins/ryu
%{python_sitelib}/quantum-%%{version}-*.egg-info


%files -n openstack-quantum-cisco
%doc LICENSE
%doc quantum/plugins/cisco/README
%{python_sitelib}/quantum/extensions/_credential_view.py*
%{python_sitelib}/quantum/extensions/portprofile.py*
%{python_sitelib}/quantum/extensions/novatenant.py*
%{python_sitelib}/quantum/extensions/credential.py*
%{python_sitelib}/quantum/extensions/_novatenant_view.py*
%{python_sitelib}/quantum/extensions/multiport.py*
%{python_sitelib}/quantum/extensions/_pprofiles.py*
%{python_sitelib}/quantum/extensions/qos.py*
%{python_sitelib}/quantum/extensions/_qos_view.py*
%{python_sitelib}/quantum/plugins/cisco
%dir %{_sysconfdir}/quantum/plugins/cisco
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/cisco/*.ini


%files -n openstack-quantum-linuxbridge
%doc LICENSE
%doc quantum/plugins/linuxbridge/README
%{_bindir}/quantum-linuxbridge-agent
%{_unitdir}/quantum-linuxbridge-agent.service
%{python_sitelib}/quantum/plugins/linuxbridge
%{_datarootdir}/quantum/rootwrap/linuxbridge-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/linuxbridge
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/linuxbridge/*.ini


%files -n openstack-quantum-nicira
%doc LICENSE
%doc quantum/plugins/nicira/nicira_nvp_plugin/README
%{python_sitelib}/quantum/plugins/nicira
%dir %{_sysconfdir}/quantum/plugins/nicira
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/nicira/*.ini


%files -n openstack-quantum-openvswitch
%doc LICENSE
%doc quantum/plugins/openvswitch/README
%{_bindir}/quantum-openvswitch-agent
%{_unitdir}/quantum-openvswitch-agent.service
%{python_sitelib}/quantum/plugins/openvswitch
%{_datarootdir}/quantum/rootwrap/openvswitch-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/openvswitch
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/openvswitch/*.ini


%files -n openstack-quantum-ryu
%doc LICENSE
%doc quantum/plugins/ryu/README
%{_bindir}/quantum-ryu-agent
%{_unitdir}/quantum-ryu-agent.service
%{python_sitelib}/quantum/plugins/ryu
%{_datarootdir}/quantum/rootwrap/ryu-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/ryu
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/ryu/*.ini


%files -n openstack-quantum-nec
%doc LICENSE
%doc quantum/plugins/nec/README
%{_bindir}/quantum-nec-agent
%{_unitdir}/quantum-nec-agent.service
%{python_sitelib}/quantum/plugins/nec
%{_datarootdir}/quantum/rootwrap/nec-plugin.filters
%dir %{_sysconfdir}/quantum/plugins/nec
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/nec/*.ini


%files -n openstack-quantum-metaplugin
%doc LICENSE
%doc quantum/plugins/metaplugin/README
%{python_sitelib}/quantum/plugins/metaplugin
%dir %{_sysconfdir}/quantum/plugins/metaplugin
%config(noreplace) %attr(0640, root, quantum) %{_sysconfdir}/quantum/plugins/metaplugin/*.ini


%changelog
* Thu Sep 13 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.7.rc1
- Fix various issues in setup scripts
- Configure quantum-dhcp-agent to store files under /var/lib/quantum
- Make config files with passwords world-unreadable
- Replace bug workarounds with upstream patches

* Wed Sep 12 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.6.rc1
- Require python-quantumclient >= 2.0.22
- Add bug references for work-arounds
- Use /usr/share/quantum/rootwrap instead of /usr/share/quantum/filters

* Wed Sep 12 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.5.rc1
- Update to folsom rc1
- Fix command lines in agent systemd units
- Fix setup scripts
- Fix configuration of agents to use quantum-rootwrap
- Set "debug = False" and "auth_strategy = noauth" in quantum.conf
- Symlink /etc/quantum/plugin.ini to plugin's config file
- Add "--config-file /etc/quantum/plugin.ini" to ExecStart in quantum-server.service

* Tue Sep 11 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.4.rc1.20120911.1224
- Update to folsom rc1 snapshot
- Add support for new agents, plugins and rootwrap

* Wed Aug 22 2012 Pádraig Brady <P@draigBrady.com> - 2012.2-0.3.f2
- Fix helper scripts to setup the database config correctly (#847785)

* Tue Aug  7 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.2.f2
- Include quantum module no longer provided by python-quantumclient
- Update description text
- Disable setuptools_git dependency

* Tue Aug  7 2012 Robert Kukura <rkukura@redhat.com> - 2012.2-0.1.f2
- Update to folsom milestone 2

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Pádraig Brady <P@draigBrady.com> - 2012.1-2
- Fix helper scripts to use the always available openstack-config util

* Mon Apr  9 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-1
- Update to essex release

* Thu Apr  5 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.7.rc2
- Update to essex rc2 milestone
- Use PrivateTmp for services

* Wed Mar 21 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.6.rc1
- Update to official essex rc1 milestone
- Add quantum-server-setup and quantum-node-setup scripts
- Use hand-coded agent executables rather than easy-install scripts
- Make plugin config files mode 640 and group quantum to protect passwords

* Mon Mar 19 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.5.e4
- Update to essex possible RC1 tarball
- Remove patches incorporated upstream
- Don't package test code
- Remove dependencies only needed by test code

* Wed Mar 14 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.4.e4
- Upstream patch: add root_helper to quantum agents
- Add sudoers file enabling quantum-rootwrap for quantum user
- Configure plugin agents to use quantum-rootwrap
- Run plugin agents as quantum user

* Fri Mar  9 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.3.e4
- Add upstream patch: remove pep8 and strict lxml version from setup.py
- Remove old fix for pep8 dependency
- Add upstream patch: Bug #949261 Removing nova drivers for Linux Bridge Plugin
- Add openvswitch dependency

* Mon Mar  5 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.2.e4
- Update to essex milestone 4
- Move plugins to sub-packages
- Systemd units for agents

* Mon Jan 31 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.1.e3
- Update to essex milestone 3 for F17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  18 2011 Robert Kukura <rkukura@redhat.com> - 2011.3-1
- Initial package for Fedora
