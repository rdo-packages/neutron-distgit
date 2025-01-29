#!/bin/sh

# This script is triggered on every ovs agent start. Its intent is to make sure
# the firewall for bridged traffic is enabled before we start the agent that
# may atttempt to set firewall rules on a bridge (when iptables_hybrid firewall
# driver is used).

# before enabling the firewall, load the relevant module
/usr/sbin/modprobe bridge
/usr/sbin/modprobe br_netfilter

# now enable the firewall in case it's disabled (f.e. rhel 7.2 and earlier)
for proto in ip ip6; do
    /usr/sbin/sysctl -w net.bridge.bridge-nf-call-${proto}tables=1
done
