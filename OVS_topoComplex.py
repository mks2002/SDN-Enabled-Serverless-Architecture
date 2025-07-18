from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.log import setLogLevel
from mininet.cli import CLI

class ComplexTopo(Topo):
    def build(self):
        # Add switches (using Open vSwitch)
        s1 = self.addSwitch('s1', cls=OVSSwitch)
        s2 = self.addSwitch('s2', cls=OVSSwitch)
        s3 = self.addSwitch('s3', cls=OVSSwitch)

        # Add hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')
        h4 = self.addHost('h4', ip='10.0.0.4')
        h5 = self.addHost('h5', ip='10.0.0.5')

        # Add links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)

        # Add links between switches to create a more complex network
        self.addLink(s1, s2)  # Direct connection between s1 and s2
        self.addLink(s2, s3)  # Direct connection between s2 and s3
        self.addLink(s1, s3)  # Direct connection between s1 and s3 (forming a triangle)
       
        # Additional links between switches to form mesh
        self.addLink(s2, s1)
        self.addLink(s3, s1)

def run():
    # Create the custom topology
    topo = ComplexTopo()

    # Create the Mininet network, using the RemoteController (e.g., POX)
    net = Mininet(topo=topo, controller=RemoteController)

    # Start the network
    net.start()

    print("Complex topology running with Open vSwitch...")

    # Start the Mininet CLI for interactive commands
    CLI(net)

    # Stop the network when done
    net.stop()

if __name__ == '__main__':
    # Set log level to info to view some Mininet logs
    setLogLevel('info')
   
    # Run the network
    run()
