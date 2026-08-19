Debian installation
===================

Install Debian 12 on all machines. At the moment, this is a manual
process. In the installer select or do the following:

.. hint:: The subheaders of this document are just for orientation and do not
   correspond by name to steps in the actual Debian installer.

Basics
------

1. Language: English
2. Location: Germany
3. Locale: en_US.UTF-8
4. Keyboard: German

Network setup
-------------

1. Select the correct network interface (you’ll have to find out)
2. Hostname: kaoruXX for HuFo renderers (renderers)
3. Domain: the correct domain

   - H0104: empty
   - EN325: ``ak.tu-berlin.de``
   - HuFo: ``tu-ctrl``

.. warning::
   If there is a DHCP configuration error, your device might need to be
   whitelisted in your current network. This means asking a system
   administrator to help you do that or using a network adapter/dongle with
   a whitelisted MAC address.

.. hint::
   The whitelisted adapter **must** be the final physical device of your
   carefully frankensteined adapter chain, e.g. putting a USB-C-to-USB-B adapter
   in front of the whitelisted Ethernet-to-USB-B adapter **will not work**. Go
   look for a whitelisted Ethernet-to-USB-B adapter instead.

User setup
----------

1. Root password: leave empty for automatic enabling of sudo. The
   standard user will be added to the sudoers group automatically. If
   you are prompted a ``sudo`` password while using the system, just use
   the one you set in step 11.
2. User: tu-studio
3. Full name: tu-studio
4. User password: use a good password here friend

Partitioning
------------

1. In the menu ‘Partition disks’, choose ‘Manual’
2. Partition the drives according to the following layout:

- New partition table: yes
- 1.0 MB free space is done automatically
- 512.0 MB EFI System Partition

  - Use as: EFI System Partition
  - Bootable flag: on

- 900.0 GB brtfs / (root)

  - mount options: defaults
  - label: system
  - Bootable flag: off

- 32 GB swap

  - Use as: swap area
  - Bootable flag: off

- Finish partitioning and write changes to disk

Finishing up
------------

1. Wait for install of base system
2. Select mirror country: Germany
3. Select a mirror (e.g. ``deb.debian.org``)
4. HTTP proxy: none (or the correct proxy at HuFo)
5. Participate in package usage survey: No
6. Software selection:

   - SSH server
   - Standard system utilities
   - On player, video and info PC: choose a desktop environment,
     currently we use KDE (but that might be overkill)

7. Reboot
