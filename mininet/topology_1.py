#!/usr/bin/env python2

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Intf, TCLink
from mininet.node import Node
from p4_mininet import P4Switch, P4Host

import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Use Case 1')
parser.add_argument('--behavioral-exe', help='Path to behavioral executable',
                    type=str, action="store", required=True)
parser.add_argument('--thrift-port', help='Thrift server port for table updates',
                    type=int, action="store", default=9090)
parser.add_argument('--json', help='Path to JSON config file',
                    type=str, action="store", required=True)
parser.add_argument('--pcap-dump', help='Dump packets on interfaces to pcap files',
                    type=str, action="store", required=False, default=False)

args = parser.parse_args()


class SingleSwitchTopo(Topo):
    def __init__(self, sw_path, json_path, thrift_port, pcap_dump, num_switches, num_hosts, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        # Adding switches
        switches = []
        for i in xrange(num_switches):
            switch = self.addSwitch('s%d' % (i + 1),
                                    sw_path = sw_path,
                                    json_path = json_path,
                                    thrift_port = thrift_port + i,
                                    pcap_dump = pcap_dump,
                                    device_id = i)
            switches.append(switch)


        # Adding hosts
        hosts = []
        for h in xrange(num_hosts):
			if h==0:
				host = self.addHost('h%d' % (h + 1), ip = "10.0.%d.10/24" % (h + 1), mac = '00:04:00:00:00:%02x' %(h+1))#, inNamespace=False)
				
			else:
				host = self.addHost('h%d' % (h + 1),ip = "10.0.%d.10/24" % (h + 1),mac = '00:04:00:00:00:%02x' %(h+1))
			hosts.append(host)

	
        self.addLink(hosts[0], switches[0], intfName2 = 's1-eth1', addr2 = "00:04:00:00:00:11", delay = "0ms");
        self.addLink(hosts[1], switches[0], intfName2 = 's1-eth2', addr2 = "00:04:00:00:00:12", delay = "0ms");
        self.addLink(hosts[2], switches[1], intfName2 = 's2-eth1', addr2 = "00:04:00:00:00:21", delay = "0ms");
        self.addLink(hosts[3], switches[2], intfName2 = 's3-eth1', addr2 = "00:04:00:00:00:31", delay = "0ms");
        self.addLink(hosts[4], switches[2], intfName2 = 's3-eth2', addr2 = "00:04:00:00:00:32", delay = "0ms");

        self.addLink(switches[1], switches[2], intfName1 = 's2-eth2', intfName2 = 's3-eth3', addr1 = "00:04:00:00:00:22", addr2 = "00:04:00:00:00:33", delay = "0ms");
        self.addLink(switches[0], switches[1], intfName1 = 's1-eth3', intfName2 = 's2-eth3', addr1 = "00:04:00:00:00:13", addr2 = "00:04:00:00:00:23", delay = "0ms");
        self.addLink(switches[0], switches[2], intfName1 = 's1-eth4', intfName2 = 's3-eth4', addr1 = "00:04:00:00:00:14", addr2 = "00:04:00:00:00:34", delay="0ms");



	#self.addNode('root', inNamespace=False)
	#intf = self.addLink('root', hosts[0])

def main():
    num_hosts = 5
    num_switches = 3

    topo = SingleSwitchTopo(args.behavioral_exe,
                            args.json,
                            args.thrift_port,
                            args.pcap_dump,
                            num_switches,
                            num_hosts
                            )
    net = Mininet(topo = topo,
                  link = TCLink,
                  host = P4Host,
                  switch = P4Switch,
                  controller = None)
    sleep(1)

    net.start()

   # h = net.get('root')
    #h.setIP("10.0.7.11/24")
    

    # Assigning IP address to switches

    s = net.get('s1')
    s.setIP("10.0.1.1/24", intf = 's1-eth1')
    s.setIP("10.0.2.1/24", intf = 's1-eth2')
    s.setIP("10.0.6.1/30", intf = 's1-eth3')
    s.setIP("10.0.6.5/30", intf = 's1-eth4')
    s.intf('s1-eth3').config(delay="24ms")   # t_5
    s.intf('s1-eth4').config(delay="8ms")   # t_1



    s = net.get('s2')
    s.setIP("10.0.3.1/24", intf = 's2-eth1')
    s.setIP("10.0.6.10/30", intf = 's2-eth2')
    s.setIP("10.0.6.2/30", intf = 's2-eth3')
    s.intf('s2-eth2').config(delay="24ms")   # t_6
    s.intf('s2-eth3').config(delay="8ms")   # t_4


    s = net.get('s3')
    s.setIP("10.0.4.1/24", intf = 's3-eth1')
    s.setIP("10.0.5.1/24", intf = 's3-eth2')
    s.setIP("10.0.6.9/30", intf = 's3-eth3')
    s.setIP("10.0.6.6/30", intf = 's3-eth4')

    s.intf('s3-eth4').config(delay="32ms")  # t_2
    s.intf('s3-eth3').config(delay="3ms")   # t_3

    def get_mac(x):
        if x == 1:
            return 11
        if x == 2:
            return 12
        if x == 3:
            return 21
        if x == 4:
            return 31
        if x == 5:
            return 32

    for n in xrange(num_hosts):
        h = net.get('h%d' % (n + 1))
        if num_hosts==0:
            h.cmd("")
        h.cmd("route add default gw 10.0.%d.1" % (n + 1))
        h.setARP('10.0.%d.1' % (n + 1), '00:04:00:00:00:%d' % get_mac(n+1))
        h.describe()

    sleep(1)

    print "Ready!"

    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    main()
