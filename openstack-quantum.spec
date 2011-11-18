Name:		openstack-quantum
Version:	2011.3
Release:	1%{?dist}
Summary:	Virtual network service for OpenStack (quantum)

Group:		Applications/System
License:	ASL 2.0
URL:		http://launchpad.net/quantum/
Source0:	http://launchpad.net/quantum/diablo/2011.3/+download/quantum-%{version}.tar.gz
Source1:	openstack-quantum.service
Source2:	quantum.logrotate

BuildArch:	noarch

BuildRequires:	python-setuptools
BuildRequires:	systemd-units
BuildRequires:	dos2unix

Requires:	python-quantum = %{version}-%{release}
Requires:	python-cheetah

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

mv quantum/plugins/cisco/README README-cisco
chmod 644 README-cisco
dos2unix README-cisco
mv quantum/plugins/openvswitch/README README-openvswitch

# Relocate top-level packages underneath quantum
mv extensions quantum/extensions
find quantum/extensions -name \*.py -exec sed -i 's/from extensions import/from quantum.extensions import/g' {} \;
mv tests quantum/tests
find quantum/tests/unit -name \*.py -exec sed -i 's/ tests.unit/ quantum.tests.unit/g' {} \;


%build
%{__python} setup.py build


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Remove docs since they don't build
rm -rf %{buildroot}%{python_sitelib}/doc

# Install execs with reasonable names
install -p -D -m 755 bin/quantum %{buildroot}%{_bindir}/quantum-server
install -p -D -m 755 bin/cli %{buildroot}%{_bindir}/quantum-cli

# Install config files, relocating ini files to /etc/quantum
install -p -D -m 644 etc/quantum.conf %{buildroot}%{_sysconfdir}/quantum/quantum.conf
sed -i 's|api_extensions_path = extensions|api_extensions_path = %{python_sitelib}/quantum/extensions|' %{buildroot}%{_sysconfdir}/quantum/quantum.conf
install -p -D -m 644 quantum/plugins.ini %{buildroot}%{_sysconfdir}/quantum/plugins.ini
ln -s ../../../../..%{_sysconfdir}/quantum/plugins.ini %{buildroot}%{python_sitelib}/quantum/plugins.ini
mkdir %{buildroot}%{python_sitelib}/quantum/plugins/cisco/conf
for f in credentials.ini db_conn.ini l2network_plugin.ini nexus.ini plugins.ini ucs.ini ucs_inventory.ini; do
    install -p -D -m 644 quantum/plugins/cisco/conf/$f %{buildroot}%{_sysconfdir}/quantum/cisco-plugin/$f
    ln -s ../../../../../../../..%{_sysconfdir}/quantum/cisco-plugin/$f %{buildroot}%{python_sitelib}/quantum/plugins/cisco/conf/$f
done
install -p -D -m 644 quantum/plugins/openvswitch/ovs_quantum_plugin.ini %{buildroot}%{_sysconfdir}/quantum/openvswitch-plugin/ovs_quantum_plugin.ini
ln -s ../../../../../../..%{_sysconfdir}/quantum/openvswitch-plugin/ovs_quantum_plugin.ini %{buildroot}%{python_sitelib}/quantum/plugins/openvswitch/ovs_quantum_plugin.ini

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
%doc LICENSE
%doc README
%doc README-cisco
%doc README-openvswitch
%{_bindir}/*
%{_unitdir}/*
%dir %{_sysconfdir}/quantum
%config(noreplace) %{_sysconfdir}/quantum/*
%config(noreplace) %{_sysconfdir}/logrotate.d/*
%{python_sitelib}/quantum/plugins.ini
%{python_sitelib}/quantum/plugins/cisco/conf/*.ini
%{python_sitelib}/quantum/plugins/openvswitch/ovs_quantum_plugin.ini
%dir %attr(0755, quantum, quantum) %{_sharedstatedir}/quantum
%dir %attr(0755, quantum, quantum) %{_localstatedir}/log/quantum


%files -n python-quantum
%doc LICENSE
%{python_sitelib}/quantum
%exclude %{python_sitelib}/quantum/plugins.ini
%exclude %{python_sitelib}/quantum/plugins/cisco/conf/*.ini
%exclude %{python_sitelib}/quantum/plugins/openvswitch/ovs_quantum_plugin.ini
#should be %%{python_sitelib}/quantum-%%{version}-*.egg-info
%{python_sitelib}/Quantum-*.egg-info
%{python_sitelib}/Quantum-*-nspkg.pth


%changelog
* Thu Nov  18 2011 Robert Kukura <rkukura@redhat.com> - 2011.3-1
- Initial package for Fedora
