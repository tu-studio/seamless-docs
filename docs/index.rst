SeamLess
========

SeamLess is the modular and distributed spatial audio rendering system powering the listening room at `Humboldt Forum <https://www.humboldtforum.org/en/>`_, Berlin and the `TU Studio <https://www.tu.berlin/ak/einrichtungen-services/tu-studio>`_.
In these locations WFS and Ambisonics playback is combined, although all kinds of spatialization are possible.

The key focus of the SeamLess system is distributed rendering on Linux Clusters to enable handling of a large amount of output channels, while keeping setup for artists to a minimum.

If you want to know more about the concept, continue :doc:`here <about>`.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   about
   maintenance/index
   archive/index

Software Components in the SeamLess System
------------------------------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1

   * - Name
     - Description
   * - `OSC-Kreuz <https://tu-studio.github.io/osc-kreuz/>`_
     - central interface for OSC messages, automatically translates incoming OSC messages to match expected formats of the rendering engines and distributes them to all connected receivers
   * - `Audio Matrix <https://tu-studio.github.io/audio-matrix/>`_
     - flexible multichannel DSP program written in C++, controllable with OSC, receiving gains and positional data from the OSC-Kreuz for Renderer Preprocessing and ambisonics encoding
   * - `Wonder <https://tu-studio.github.io/wonder/>`_
     - WFS rendering suite written in C++. for SeamLess only the actual renderer ``tWonder`` is used. Is able to run distributed and handles both focused and unfocused virtual sound sources
   * - `SeamLess Plugin Suite <https://github.com/tu-studio/seamless-plugin-suite>`_
     - Plugins for all common DAWs to control the SeamLess system during audio production
   * - `Jack-Connection-Manager <https://github.com/tu-studio/jack-connection-manager>`_
     - Python tool for managing connections in JACK setups with clients with high number of in/outputs while maintaining readable config files
   * - `Configs <https://github.com/tu-studio/seamless-configs>`_
     - Configuration files for all SeamLess setups maintained by the TU Studio Team, some tools for managing the speaker files required to create these configs can be found in `this repo <https://github.com/tu-studio/seamless-config-tools>`_
   * - `Ansible playbooks <https://github.com/tu-studio/seamless-install-maintain>`_
     - Playbooks for installation, management and maintenance of SeamLess clusters.

currently the system also relies on the following components for playback:

- `REAPER <https://reaper.fm>`_
  - used as playback system, remote controlled using OSC
- `IEM Plugin Suite <https://plugins.iem.at/>`_
  - the AllRADecoder and DistanceCompensator are used for ambisonics decoding, using a modified headless build found `here <https://github.com/tu-studio/IEMPluginSuite>`_

Installation of the System
--------------------------

Since all installations of the SeamLess system will vary wildly in setup it is hard to give a universal guide.
A specific guide to our installation of the SeamLess system at Humboldt-Forum or the TU can be found `here <https://github.com/tu-studio/seamless-install-maintain/blob/main/README.md>`_, that might serve as inspiration for your setup.

The core component to the SeamLess system is the OSC-Kreuz in combination with the Audio Matrix, different software for spatialization can be put behind them.

Developed and maintained by the TU Studio Team
----------------------------------------------

- *Fares Schulz*
- *Manolo Müller*

Previous Team-members
---------------------

- *Max Weidauer*
- *Henrik von Coler*
- *Paul Schuladen*
- *Nils Tonnätt*
