# LXC Helpers
A collection of functions that I use when working with LXC as shortcuts for some otherwise more complicated commands.

![LXC Logo](https://github.com/AncientAbysswalker/Server-Scripts/blob/main/.readme/lxc.png?raw=true "LXC Logo")

# Function Definitions:
##lxc_cd_rootfs
Used to directly access the root filesystem of an LXC container. This allows direct access to the files inside from the external Linux system. Any commands run will be done by the user external to the container.

```Shell
# Usage
lxc_cd_rootfs container_name

# Params
container_name: Name of the container
```

word
##lxc_conn

Used to connect to and enter an LXC container. This operates exactly like a standard ```lxc exec``` command, except there is an optional flag to maintain the session after the terminal is closed. Normally, when the terminal being used on the container is closed any running processes will also close. This command makes it easy to close a session without losing work and to hop into a pre-existing session where you left off.

```shell
# Usage
lxc_conn -t container_name

# Params
-t [Optional] : Maintain session after closing terminal
container_name : Name of the container
```

##lxc_port_ls
List port forwarding rules associated with a container

```Shell
# Usage
lxc_port_ls container_name

# Params
container_name : Name of the container
```

##lxc_port_open
Create a new port forwarding rule associated with a container

```Shell
# Usage
lxc_port_open container_name port_number

# Params
container_name : Name of the container
port_number : Port number to forward into the container
```

##lxc_port_close
Remove a port forwarding rule associated with a container

```Shell
# Usage
lxc_port_close container_name port_number

# Params
container_name : Name of the container
port_number : Port number to forward into the container
```
