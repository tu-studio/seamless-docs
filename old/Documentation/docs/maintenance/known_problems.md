# Known Problems 

## (and workarounds and possible solutions for them)

## Dell PCs don't always shutdown properly when restarting

If it takes a long time for the system to restart, hard reset the PC by
holding its power button for some seconds. This is a known bug in the Dell
units, which might also affect Wake-On-LAN. The bug is known to cause the
servers to hang on reboot, leaving them dead in the water. As of 24.6.026,
it was decided to add a power distribution unit to cut power to the
machines in the evening. 

## Sound cards are sometimes not recognized on cold boot

- might be fixed by changing BIOS power saving settings ("PCI Express Native
  Power Management" → Disable or something similar)
- what we tried: disable ASPM in grub (did not work, might need additional BIOS
  setting)
- restarting also works, but the current restart service has permission
  troubles

## no network directly after boot causes some services to fail

If a user-service needs network to function make it depend on the special user
network online target:

```systemd
[Unit]
...
After=user-network-online.service
Wants=user-network-online.service
```

it is also necessary to enable `systemd-networkd.service` and configure
systemd-networkd to manage network interfaces. This is all taken care of by the
`install_user_network_online_target.yml` ansible playbook

## reaper session not visible directly after boot

Reaper still runs, the UI is just not visible, check the reaper systemd
service. If you need the UI restart the service.

## can't access dante device from dante controller, because it is in different subnet

Change your IP to a static one in the dante devices subnet, then change its IP
to the correct subnet (or, better yet, make it dynamic by enabling DHCP).
