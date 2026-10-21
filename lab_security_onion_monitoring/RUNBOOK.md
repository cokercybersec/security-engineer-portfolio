# Runbook: network monitoring lab

Steps to repeat the lab, and to clean it up. Check the current Security Onion documentation for exact requirements and install screens, because they change between versions.

## Before you start

1. Read the hardware page in the Security Onion documentation. A standalone deployment lists a minimum of 4 CPU cores, 24 GB of RAM, 200 GB of storage and 2 network interfaces, and suggests more RAM if you monitor real traffic.
2. Confirm you have a managed switch that supports port mirroring, and a USB gigabit network adapter for the monitoring interface.
3. Only monitor networks you own or are authorized to monitor.

## Build

1. Create the virtual machine in VirtualBox with the resources from the documentation.
2. Give it two network adapters. Adapter one is the management interface. Adapter two is bound to the USB network adapter.
3. On the monitoring adapter, set promiscuous mode to Allow All in the VirtualBox network settings.
4. Install Security Onion from the official installer and choose a standalone deployment.
5. During setup, give the management interface a static address on a dedicated management network, and leave the monitoring interface without an address.
6. On the switch, set port mirroring so traffic from the uplink you want to watch is copied to the port connected to the USB adapter.

## Verify

1. Log in to the web console from the management network.
2. Confirm that network metadata and alerts are arriving.
3. Compare what you see against a device you know is active. If it is missing, check the path it takes to the internet and where the mirror is attached.
4. Write down every device or segment that is not covered.

## Operate

1. Review alerts on a schedule, weekly to start.
2. Group alerts into categories and decide for each whether it is expected, needs a fix or needs more data.
3. Record the decision and the date.
4. After a fix, confirm the alert stops.

## Clean up

1. Shut down the virtual machine, or remove it if you no longer need it.
2. Disable port mirroring on the switch.
3. Remove or reset the monitoring adapter settings in VirtualBox.
4. Delete stored captures and logs you no longer need, since they contain details of your network.
