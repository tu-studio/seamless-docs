# Setting up the System

This guide is specific to our installations of the SeamLess system at Humboldt-Forum or the TU


## Install Debian 12 on all rendering machines

In the Installer select or do the following
1. Language: English
2. Location: Germany
3. Locale: en_US.UTF-8
4. Keyboard: German
5. Select the correct network interface (you'll have to find out)
6. Hostname: kaoruXX for HuFo renderers (renderers)
7. Domain: the correct domain (empty in H0104/ak.tu-berlin.de in EN325/tu-ctrl at HuFo)
8. Root password: leave empty for automatic enabling of sudo/adding of the standard user to sudoers group
9. User: tu-studio
10. Full name: tu-studio
11. User password: use a good password here friend
12. Partitioning method: Manual (Guided partitioning manual)
  - /dev/nvme0n1
  - yes new partition table
  - 1.0 MB free space is done automatically
  - 512.0 MB EFI System Partition
    - Use as: EFI System Partition
    - Bootable flag: on
  - 850.0 GB brtfs / (root)
    - mount options: defaults
    - label: system
    - Bootable flag: off
  - 32 GB swap
    - Use as: swap area
    - Bootable flag: off
  - Finish partitioning and write changes to disk
13. wait for install of Base system
14. mirror country: Germany
15. select a mirror (deb.debian.org for example)
16. HTTP proxy: none (or the correct proxy at HuFo)
17. Participate in package usage survey: No
18. Software selection: SSH server, standard system utilities
19. Reboot

## Start Installations from remote host:

ansible playbooks for installation are run with this command:
`ansible-playbook -i <your_inventory>.yml <playbook_name>.yml`.
whenever doing something with just a `.yml` file is mentioned in the following, this should be done with the 

1. clone the [ansible repo](https://github.com/tu-studio/seamless-install-maintain/tree/main)
2. create `vars/vault.yml` from the `vars/vault.yml.template`, fill it in. if regularly switching between locations create multiple vault files, and just symlink them to the currently required one: `ln -sf vault_hufo.yml vars/vault.yml`
3. if you use a dante soundcard change the path in `vars/vars.yml` to the correct path to the driver directory
5. add host to ansible inventory file, follow the provided inventory files for guidance
   - hosts should be grouped into the sections `renderer`, `player`, `video_player` and `info_player`
   - hosts should contain the following variables (if used):
     - `ansible_host`: hostname
     - `ansible_user`: username 
     - `services` containing a list of services running on this machine, available services are `osc-kreuz`, `jack-connection-manager`, `audio-matrix`, `ambisonics`, `gui`, `showcontrol` and `twonder`
     - `location`: the location of this machine for use with the configs, at the moment one of `HUFO`, `EN325` or `H0104`
     - `audiodriver`: list of strings or single string of `dante` or `madi`
     - `n_twonders` only necessary if services contains `twonder`, sets up the `twonder.target` with the correct number of twonders
6. rollout your ssh key to pcs: `ansible-playbook mantain/rollout_ssh_key.yml --ask-pass -e "key=<path/to/public/key.pub>"`
7. if necessary install sudo: `install/install_sudo.yml`
8. setup btrfs subvolumes (don't do this more than once!): `install/setup_btrfs.yml -k`. This needs the `-k` option to ask for the ssh connection password, because the moving around of btrfs subvolumes briefly moves the `.ssh` directory somewhere else...
9. when in hufo: run hufo specific scripts:
   1. `install/hufo_setup_proxy_server.yml`
   2. `install/hufo_first_run.yml`
   3. `install/hufo_avm_user.yml`
10. start main install script: `install/full_install.yml`


### additional ansible scripts not run from full_install
- `install/install_jack-silence-detector`: debugging tool to discover longer silences (was used to debug reaper crashes)
- `install/reboot.yml`: used to reboot everything, sometimes used by services
- `install/remove_apt_cdrom_source.yml`: sometimes needed if installation of programs on fresh debian installs fails.
- `install/upgrade_system.yml`: performs a system upgrade

#### maintenance playbooks
- `pull_videos.yml`: pulls all videos from the video players to your local machine
- `rollout_info_text.yml`: roll out the video files of the desired piece to all video players