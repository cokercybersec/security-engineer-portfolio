# Lessons learned

Five lessons from building a home network monitor, written so they apply to any small network.

## 1. Count your routers

My network has two routers in a row. A monitor only sees the traffic that crosses the place it is attached to, so with two routers in a row a lot of traffic never reached my sensor the way I first expected. The fix was not a setting inside Security Onion. It was moving where the traffic is copied from. Before you build a monitor, draw the path a device's traffic takes to the internet and mark every device it crosses.

## 2. A sensor needs a copy of the traffic

A switch normally sends traffic only to the port that needs it, so a sensor plugged in like any other computer sees almost nothing. A managed switch with port mirroring copies traffic to a chosen port. I paired that with a dedicated USB network adapter so the monitoring interface has no IP address and does nothing except listen, while a separate interface handles management.

## 3. Write down your blind spots

Some devices on my network connect through the internet provider router WiFi, outside the part of the network my sensor could see. A monitoring project that does not list what it cannot see gives a false sense of coverage. The blind spot list is as useful as the alert list, because it tells you where to extend coverage next.

## 4. Expect noise

My first alerts were noisy. That is normal. I treated the first period as a baseline: group alerts into categories, decide which are expected on my network, and write down why. After that, the alerts that mattered stood out.

## 5. Close the loop

Alert review found a weakness on my own network that was worth fixing. I fixed it and checked that the alert stopped. Detection is only valuable when it ends in a decision or a change, and recording that decision is what makes the work auditable.

## What I would do next

Extend coverage to the devices outside the mirror, write the alert review into a weekly routine, and keep a short register of decisions about what is normal.
