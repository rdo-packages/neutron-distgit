#
# This is 2012.1 essex-3 milestone
#
%global release_name essex
%global release_letter e
%global milestone 3

Name:		openstack-quantum
Version:	2012.1
Release:	0.1.%{release_letter}%{milestone}%{?dist}
Summary:	Virtual network service for OpenStack (quantum)

Group:		Applications/System
License:	ASL 2.0
URL:		http://launchpad.net/quantum/
Source0:	http://launchpad.net/quantum/%{release_name}/%{release_name}-%{milestone}/+download/quantum-%{version}~%{release_letter}%{milestone}.tar.gz
Source1:	openstack-quantum.service
Source2:	quantum.logrotate

BuildArch:	noarch

BuildRequires:	python2-devel
BuildRequires:	python-setuptools
BuildRequires:	systemd-units
#BuildRequires:	dos2unix

Requires:	python-quantum = %{version}-%{release}

Requires(pre):	shadow-utils
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units


%description
Quantum is a virtual network service for Openstack, and a part of
Netstack. Just like OpenStack Nova provides an API to dynamically
request and configure virtual servers, Quantum provides an API to
dynamically request and configure virtual networks. These networks
connect "interfaces" from other OpenStack services (e.g., virtual NICs
from Nova VMs). The Quantum API supports extensions to provide
advanced network capabilities (e.g., QoS, ACLs, network monitoring,
etc.)


%package -n python-quantum
Summary:	Quantum Python libraries
Group:		Applications/System

Requires:	python-quantumclient
Requires:	MySQL-python
Requires:	python-configobj
Requires:	python-eventlet
Requires:	python-gflags
Requires:	python-anyjson
Requires:	python-nose
Requires:	python-paste-deploy
Requires:	python-routes
Requires:	python-sqlalchemy
Requires:	python-webob
Requires:	python-webtest


%description -n python-quantum
Quantum provides an API to dynamically request and configure virtual
networks.

This package contains the quantum Python library.


%prep
%setup -q -n quantum-%{version}

find quantum -name \*.py -exec sed -i '/\/usr\/bin\/env python/d' {} \;

#mv quantum/plugins/cisco/README README-cisco
#chmod 644 README-cisco
#dos2unix README-cisco
#mv quantum/plugins/openvswitch/README README-openvswitch


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove unused files
rm -rf %{buildroot}%{python_sitelib}/bin
rm -rf %{buildroot}%{python_sitelib}/doc
rm -rf %{buildroot}%{python_sitelib}/tools
rm %{buildroot}%{_bindir}/quantum
rm %{buildroot}/usr/etc/quantum/quantum.conf.test
rm %{buildroot}/usr/etc/init.d/quantum-server

# Install execs
install -p -D -m 755 bin/quantum-server %{buildroot}%{_bindir}/quantum-server

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/quantum
mv %{buildroot}/usr/etc/quantum/* %{buildroot}%{_sysconfdir}/quantum

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-quantum.service

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-quantum

# Setup directories
install -d -m 755 %{buildroot}%{_sharedstatedir}/quantum
install -d -m 755 %{buildroot}%{_localstatedir}/log/quantum


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
    /bin/systemctl --no-reload disable openstack-quantum.service > /dev/null 2>&1 || :
    /bin/systemctl stop openstack-quantum.service > /dev/null 2>&1 || :
fi


%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart openstack-quantum.service >/dev/null 2>&1 || :
fi


%files
#%%doc LICENSE
%doc README
#%%doc README-cisco
#%%doc README-openvswitch
%{_bindir}/quantum-server
%{_unitdir}/openstack-quantum.service
%dir %{_sysconfdir}/quantum
%config(noreplace) %{_sysconfdir}/quantum/quantum.conf
%config(noreplace) %{_sysconfdir}/quantum/plugins.ini
%dir %{_sysconfdir}/quantum/plugins
%dir %{_sysconfdir}/quantum/plugins/cisco
%config(noreplace) %{_sysconfdir}/quantum/plugins/cisco/*.ini
%dir %{_sysconfdir}/quantum/plugins/openvswitch
%config(noreplace) %{_sysconfdir}/quantum/plugins/openvswitch/*.ini
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%dir %attr(0755, quantum, quantum) %{_sharedstatedir}/quantum
%dir %attr(0755, quantum, quantum) %{_localstatedir}/log/quantum


%files -n python-quantum
# note that %%{python_sitelib}/quantum is owned by python-quantumclient
#%%doc LICENSE
%doc README
%{python_sitelib}/quantum/*
%exclude %{python_sitelib}/quantum/__init__.*
%{python_sitelib}/quantum-%%{version}-*.egg-info


%changelog
* Mon Jan 31 2012 Robert Kukura <rkukura@redhat.com> - 2012.1-0.1.e3
- Update to essex milestone 3 for F17

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2011.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov  18 2011 Robert Kukura <rkukura@redhat.com> - 2011.3-1
- Initial package for Fedora
