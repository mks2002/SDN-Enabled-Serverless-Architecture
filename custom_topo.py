from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel

class MyTopo(Topo):
    def build(self):
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')

        # Add links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(s1, s2)
        self.addLink(h3, s2)
        self.addLink(h4, s2)


'''
def run():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()
    print("Custom topology running...")
    net.pingAll()
    CLI(net)
    net.stop()
'''


from mininet.cli import CLI

def run():
    topo = MyTopo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()
    print("Custom topology running...")
    CLI(net)  # <- lets you enter Mininet CLI
    net.stop()



if __name__ == '__main__':
    from mininet.cli import CLI
    setLogLevel('info')
    run()

