# Big Data

## Hardware

#### CPU (Central Processing Unit)
- The CPU is the "brain" of the computer.
- Every process on your computer is eventually handled by your CPU.
  * This includes calculations and also instructions for the other components of the compute.
- The CPU can also store small amounts of data inside itself in what are called **registers**. These registers hold data that the CPU is working with at the moment.
  * The registers make computations more efficient: the registers avoid having to send data unnecessarily back and forth between memory (RAM) and the CPU.


#### Memory (RAM)
- When your program runs, data gets temporarily stored in memory before getting sent to the CPU
- Memory is **ephemeral storage** - when your computer shuts down, the data in the memory is lost.

What are the potential trade offs of creating one computer with a lots of CPUs and memory?
- it is very efficient, but...
- **ephemeral**: we lose our data every time we shut down the machines
- **expensive**

alternative: **distributed systems**
- e.g. rather than relying on lots of memory, Google leveraged **long-term storage** on cheap, pre-used hardware.

#### Storage (SSD or Magnetic Disk)
- Storage is used for keeping data over long periods of time.
- When a program runs, the CPU will direct the memory to temporarily load data from long-term storage.

#### Network (LAN or the Internet)
- Network is the gateway for anything that you need that isn't stored on your computer.
- The network could connect to other computers in the same room (a **Local Area Network**) or to a computer on the other side of the world, connected over the internet.

The *speed of our network* has lagged behind the improvments in CPU memory and storage
- moving data across the network from one machine to another is the most common **bottleneck** when working w/ big data.
- for this reason, distributed systems try to **minimize shuffling** data back and forth across different machines

**Other Numbers to Know?**
- check out [Peter Norvig's original blog post](http://norvig.com/21-days.html) from a few years ago;
- and [an interactive version](https://colin-scott.github.io/personal_website/research/interactive_latency.html) for today's current hardware.

**Key Ratios**
- Fastest: CPU - 200x faster than memory
- Memory - 15x faster than SSD
- SSD - 20x faster than network
- Slowest: Network

