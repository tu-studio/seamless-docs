# Dante at Humboldt-Forum

The Dante network is in its own VLAN on the HuFo network. The network is
managed with a DHCP server, static ips are therefore not needed. There is also
no longer a Dante Domain Manager involved.

## Connect to the Dante Network and Authenticate

In order to connect to the Dante Network and see its connections you need to
use the software Dante Controller. There you select the desired network device.
First you need to select which network device should be used. There are two
main options of connecting:

### connecting using an ethernet dongle

If you are using our normal ethernet dongle just connect it to the dante
network port (service 1 or 2). DHCP takes care of the IP, everything is eazy
peazy lemon squeazy

### connecting using the ethernet bridge of the danteface

The RME Digiface Dante has multiple MAC-Adresses/IP adresses. The IP being used
for Dante is setup using the Dante Controller (and/or DHCP). The ip we can use
for accessing the dante network for use with the dante controller is a seperate
one. It is also being assigned using DHCP. As of writing (9.6.2026), the
ethernet bridge unfortunately does not work on any computers the author was
able to get their hands on. Therefore, it is recommended to always connect by
ethernet dongle. It used to work on the studio MacBook in the following manner:

For the danteface 1 (3900-aio-dante-01 or something like that) select "use
shared interface" and select feth1001. For the Danteface 2 (the one usually
only used by the hufo people, 3900-aio-dante-02) do not select "use shared
interface", the interface is shown as en26 or something similar.

If some devices are not shown enable "show hidden devices" in the View settings
of the dante controller.
