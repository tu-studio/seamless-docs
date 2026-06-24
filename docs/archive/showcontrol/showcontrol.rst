Showcontrol
===========

Showcontrol is the scheduler powering automated playback in the humboldt-forum. The preferred way of control is using the webinterface, alternatively the api can be used directly.

SystemD services
----------------

ShowControl usually starts as a systemd user service.

* __showcontrol__: Scheduler, OSC server, Web Interface

OSC Commands
------------

``/showcontrol/pause f``

   **1.0**: Sends stop and mute message to Reaper and jumps to first video to get a black image
   **0.0**: Resumes schedule

``/showcontrol/track i``

   **track number**: Pause schedule, unmute reaper and play track number **track number**

``/play f``

   Receives playing state from Reaper. This is only meant as a callback.
   It's not supposed to be used directly.

   **1.0**: Set playing state to True and resume video players
   **0.0**: Set playing state to False and pause video players

``/showcontrol/reboot f``

   **Not tested yet!** Doesn't work probably because the showcontrol machine
   is part of this is list, but it doesn't make sure that itself is the last one.

   **1.0**: Reboots all system machines from showcontrol_config.yml

ShowControl YAML Syntax
-----------------------

Filename: ``_showcontrol_config.yml_``

The ShowControl config file set ip and port of Reaper's and
of ShowControl's OSC servers. Every machine of the seamless installation
is listed with name, ip, user and used services.

For the specifics of the syntax look at the Humboldt Forum configuration.

Schedule YAML Syntax
--------------------

Filename: ``_schedule.yml_``

The schedule file consists of events with following structure:

.. code-block:: yaml

   - audio_index: 1
     command: play
     day_of_week: 0,1,2,3,4,5,6
     hour: 9
     minute: 0
     second: 0
     video_index: 0

The _schedule.yml_ can be generated from a _blockplan.yml_, blocks and tracks
files with the _schedule\_generator.py_ script.

Tracks
^^^^^^

All tracks are found in the _tracks_ directory. Beside the
scheduling information like audio and video indices and duration, there
are descriptive information like the title in German and English
and a description. This information is to be used for the generation
of the infopanel SVGs.

Track example file:

.. code-block:: yaml

   brunnen:
     title: Brunnen der Sonne
     title_en: Well of the Sun
     audio_index: 2
     video_index: 1
     duration:
       minutes: 16
       seconds: 14
     description: >
       Brunnen description text

Blocks
^^^^^^

Tracks are grouped in blocks. Blocks have a overall length
in minutes and a track padding in seconds.

Example block file:

.. code-block:: yaml

   default:
     length: 80
     track_padding: 10
     tracks:
       1: trailer
       2: brunnen
       3: sufi
       4: trailer
       5: oksus
       6: datenerhebung

Blockplan
^^^^^^^^^

There's only one blockplan.yml in use currently.
It's just a list of blocks.

Blockplan file:

.. code-block:: yaml

   default:
     blocks:
       1: default
       2: default
       3: default
       4: default
