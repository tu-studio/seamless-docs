Playback system installation
============================

This guide shows you how to get the playback system up and running on the
dedicated playback PC. We assume familiarity with the use of Ansible playbooks,
as documented in :doc:``this guide <intro_to_ansible_playbooks>``.

Setting up the playback machine
-------------------------------

REAPER will already have been installed in the previous steps outlined in
:doc:`this guide <baseline_installation>`. Now we need to add some more components.

.. hint:: The REAPER version is specified in ``program_versions.yml``,
    consequently it can be overwritten using ``-e`` for both
    ``reaper_archive_name`` and ``reaper_url``

1. Download the x64 Linux version of the SWS extension for REAPER from
   `here <https://sws-extension.org/>`__ onto your local machine.
2. Run these playbooks:

   1. ``install/setup_player_autologin_and_desktop.yml``
   2. ``install/setup_player_reaper.yml -e "sws_archive=<path/to/your/sws-x.xx.x.x-Linux-x86_64.tar.xz>"``
   3. ``install/install_player_showcontrol.yml``
   4. ``install/install_player_seamless-plugin-suite.yml``
   5. Only in ``H0104``: ``install/setup_player_dante_bridge.yml``
   6. Should you have problems with NVIDIA graphics cards and Wayland:
      ``install/setup_player_nvidia_drivers.yml``

Some steps in REAPER need to be performed manually in the GUI:

Set up REAPER remote control
----------------------------

Some steps need to be performed manually in the GUI on the playback PC:

- In REAPER go to ``options->Preferences->Control/OSC/web``
- Press “add” to add a new OSC control surface
- Device Name: “Showcontrol” or something like that
- Pattern Config:

  - Select ``(open config directory)``
  - Copy ``HufoShowControl.ReaperOSC`` from the `showcontrol
    repo <https://github.com/tu-studio/showcontrol>`__ to the folder
  - Select ``(refresh list)``
  - Select ``HufoShowControl``

- Mode: ``Local port [receive only]``

  - Local listen port: ``8000``
  - Local IP: ``0.0.0.0``

Set up REAPER channels
----------------------

The number of output channels in REAPER must be set to 64.

Set up remote desktop
---------------------

VNC with the help of ``krfb`` will have already been installed using the
playbook ``install/setup_player_autologin_and_desktop.yml``. This,
however, does not start it automatically.

Configure ``krfb`` on the desktop: System Settings > Sharing > Desktop
Sharing > Configure
