# Known Problems 
## (and workarounds and possible solutions for them)

## PCs don't always shutdown properly when restarting

If it takes a long time for the system to restart, hard reset the PC by holding its power button for some seconds.

Apparently that's a feature of these Dell PCs

## Sound cards are sometimes not recognized on cold boot

- might be fixed by changing BIOS power saving settings ("PCI Express Native Power Management" → Disable or something similar)
- what we tried: disable ASPM in grub (did not work, might need additional BIOS setting)
- restarting also works, but the current restart service has permission troubles

## SeamLess Plugins don't send out current position

- Will be fixed in next plugin version, current workaround: changing all relevant automation curves before moving them to the correct settings (urgh)

## no network directly after boot causes some services to fail

If a user-service needs network to function make it depend on the special user network online target:

```systemd
[Unit]
...
After=user-network-online.service
Wants=user-network-online.service
```

it is also necessary to enable `systemd-networkd.service` and configure systemd-networkd to manage network interfaces.
this is all taken care of by the `install_user_network_online_target.yml` ansible playbook

## reaper session not visible directly after boot

reaper still runs, the UI is just not visible, check the reaper systemd service
If you need the UI restart the service

## can't access dante device from dante controller, because it is in different subnet

change your ip to a static one in the dante devices subnet, then change its ip to the correct subnet (or, better yet, make it dynamic by enabling DHCP)
