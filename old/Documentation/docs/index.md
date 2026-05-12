# SeamLess

SeamLess is the modular and distributed spatial audio rendering system powering the listening room at [Humboldt Forum](https://www.humboldtforum.org/en/), Berlin and the [TU Studio](https://www.tu.berlin/ak/einrichtungen-services/tu-studio).
In these locations WFS and Ambisonics playback is combined, although all kinds of spatialization are possible.


**If you want to know more about the concept, continue [here](about/)** 

<!-- **If you want to get started setting up the SeamLess system for your system go [here](technical/)** -->

<!-- **If you are interested in using the system from a Reaper session, continue here:** [Reaper Userguide](reaper/) -->

## Software Components in the SeamLess System

| Name | Description |
| --- | ---|
| [OSC-Kreuz]() | central interface for OSC messages, automatically translates incoming OSC messages to match expected formats of the rendering engines and distributes them to all connected receivers |
| [Audio Matrix]() | |
| [Wonder]() | |
| [SeamLess Plugin Suite]() | |
| [Jack-Connection-Manager]() | |
| [Configs]() | |
| [Ansible]() | Playbooks for installation, management and maintenance of SeamLess clusters. |

currently the system also relies on the following components for playback:

- [REAPER](https://reaper.fm)
- [IEM Plugin Suite](https://https://plugins.iem.at/)

----

  **2021 - TU Studio Team:**    
  *Henrik von Coler*  
  *Paul Schuladen*  
  *Nils Tonnätt*  
