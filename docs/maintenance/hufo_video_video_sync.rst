mpv-sync - Synchronize Multiple mpv Instances via UDP Broadcast
===============================================================

Synchronisiert mehrere mpv-Instanzen über UDP Broadcast. Ein Master-Player steuert beliebig viele Slave-Player gleichzeitig.

Features
--------

* **UDP Broadcast**: Ein Master synchronisiert beliebig viele Slaves gleichzeitig
* **Dual Backend**: Unterstützt lua-socket UND socat (mit automatischem Fallback)
* **Adaptive Geschwindigkeitsanpassung**: Progressive Synchronisation ohne Oszillation
* **Manuelle Offset-Anpassung**: Feintuning in 5ms-Schritten mit Ö/Ä-Tasten
* **Hard Seeking**: Automatisches Springen bei großen Zeitunterschieden (>5s)
* **OSD-Anzeige**: Live-Sync-Info direkt im Player

Installation
------------

Voraussetzungen
~~~~~~~~~~~~~~~

**Option A: lua-socket** (funktioniert auf Debian 13, schneller)

.. code-block:: bash

   sudo apt install lua-socket

**Option B: socat** (funktioniert auf Debian 11, 12, 13)

.. code-block:: bash

   sudo apt install socat

**Empfehlung**: Beide installieren, Script wählt automatisch das beste Backend!

Script installieren
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Systemweit (für alle User):
   sudo cp mpv-sync-1.1.lua /usr/share/mpv/scripts/mpv-sync.lua

   # Oder pro User:
   mkdir -p ~/.config/mpv/scripts
   cp mpv-sync-1.1.lua ~/.config/mpv/scripts/mpv-sync.lua

Verwendung
----------

Einfachste Verwendung (empfohlen)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Master** (1x):

.. code-block:: bash

   mpv --script-opts=sync-role=master,sync-target=192.168.10.255:12345 video.mp4

**Slaves** (beliebig viele):

.. code-block:: bash

   mpv --script-opts=sync-role=slave,sync-target=192.168.10.255:12345 video.mp4

* Master sendet Commands über UDP Broadcast
* Alle Slaves auf dem gleichen Netzwerk empfangen automatisch
* Backend wird automatisch gewählt (lua-socket oder socat)

Backend explizit wählen
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Nur lua-socket verwenden:
   mpv --script-opts=sync-role=master,sync-backend=socket,sync-target=192.168.10.255:12345 video.mp4

   # Nur socat verwenden:
   mpv --script-opts=sync-role=master,sync-backend=socat,sync-target=192.168.10.255:12345 video.mp4

   # Auto-Modus (Standard - versucht socket, dann socat):
   mpv --script-opts=sync-role=master,sync-backend=auto,sync-target=192.168.10.255:12345 video.mp4

Master und Slaves mit verschiedenen Backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Funktioniert problemlos!** UDP-Pakete sind identisch, egal welches Backend:

.. code-block:: bash

   # Master mit lua-socket (Debian 13):
   mpv --script-opts=sync-role=master,sync-backend=socket video.mp4

   # Slave mit socat (Debian 12):
   mpv --script-opts=sync-role=slave,sync-backend=socat video.mp4

   # Slave mit auto (wählt bestes verfügbares):
   mpv --script-opts=sync-role=slave,sync-backend=auto video.mp4

Konfiguration
-------------

Alle Optionen via ``--script-opts=sync-OPTION=WERT``:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Option
     - Standard
     - Beschreibung
   * - ``role``
     - ``master``
     - ``master`` oder ``slave``
   * - ``target``
     - ``192.168.10.255:12345``
     - Broadcast-Adresse:Port (anpassen an dein Netzwerk!)
   * - ``backend``
     - ``auto``
     - ``auto``, ``socket`` oder ``socat``
   * - ``sync_interval``
     - ``0.5``
     - Sekunden zwischen Position-Updates
   * - ``seek_threshold``
     - ``5.0``
     - Sekunden Differenz für Hard Seek
   * - ``speed_adjust_threshold``
     - ``0.02``
     - Sekunden - unter 20ms = "in sync"
   * - ``max_speed_adjust``
     - ``0.5``
     - Maximale Geschwindigkeitsänderung (50%)
   * - ``initial_offset``
     - ``0.015``
     - Initialer Offset in Sekunden (15ms)
   * - ``show_osd``
     - ``true``
     - Sync-Info auf dem Bildschirm anzeigen

Beispiel mit Optionen
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   mpv --script-opts=sync-role=slave,sync-target=192.168.1.255:12345,sync-initial_offset=0.025,sync-show_osd=false video.mp4

Permanente Konfiguration
~~~~~~~~~~~~~~~~~~~~~~~~

Erstelle ``~/.config/mpv/script-opts/sync.conf``:

.. code-block:: ini

   role=slave
   target=192.168.10.255:12345
   backend=auto
   initial_offset=0.020
   show_osd=yes

Tastenbefehle (nur Slave)
-------------------------

* **Ö** (Shift+ö): Offset +5ms erhöhen (Slave läuft später)
* **Ä** (Shift+ä): Offset -5ms verringern (Slave läuft früher)

Nützlich für Audio/Video-Lippensync oder wenn verschiedene Hardware unterschiedliche Latenz hat.

Broadcast-Adresse finden
------------------------

.. code-block:: bash

   # Zeigt alle Netzwerk-Interfaces mit Broadcast-Adressen:
   ip addr show | grep -E "inet.*brd"

   # Typische Broadcast-Adressen:
   # 192.168.1.255 für Netzwerk 192.168.1.0/24
   # 192.168.10.255 für Netzwerk 192.168.10.0/24
   # 10.0.0.255 für Netzwerk 10.0.0.0/24

**Für lokale Tests:**

.. code-block:: text

   sync-target=127.0.0.1:12345

(nur auf dem gleichen Rechner, kein Broadcast)

Synchronisations-Algorithmus
----------------------------

Progressive Geschwindigkeitsanpassung
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Das Script verwendet adaptive Geschwindigkeitsanpassung ohne Oszillation:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Zeitdifferenz
     - Anpassung
     - Beschreibung
   * - < 20ms
     - Normal Speed
     - **IN SYNC** - keine Anpassung
   * - 20-50ms
     - ±5%
     - Ultra-feine Anpassung
   * - 50-200ms
     - ±10%
     - Feine Anpassung
   * - 200ms-1s
     - ±32%
     - Moderate Anpassung
   * - > 1s
     - ±50% (max)
     - Größere Anpassung
   * - > 5s
     - Hard Seek
     - Sofortiges Springen

**Vorteil**: Sanfte Konvergenz zum Sync-Punkt ohne "Überschwingen".

Wie funktioniert es?
~~~~~~~~~~~~~~~~~~~~

1. **Master sendet** alle 0.5s seine Position via UDP Broadcast
2. **Slaves empfangen** und vergleichen mit eigener Position
3. **Kleine Differenz** (< 5s): Geschwindigkeit anpassen
4. **Große Differenz** (> 5s): Hard Seek zur Master-Position
5. **In Sync** (< 20ms): Normale Geschwindigkeit

Fehlerbehebung
--------------

"No backend available!"
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Installiere mindestens eins:
   sudo apt install lua-socket  # Debian 13
   sudo apt install socat       # Debian 11, 12, 13

lua-socket: "unexpected symbol near char(127)"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Das ist ein bekanntes Problem auf Debian 12 - mpv's eingebautes Lua ist nicht mit der lua-socket Binary kompatibel.

**Lösung**: Script nutzt automatisch socat als Fallback!

.. code-block:: bash

   sudo apt install socat
   # Script automatisch wählt socat auf Debian 12

Slaves empfangen keine Nachrichten
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Firewall prüfen:**

.. code-block:: bash

   # UDP Port öffnen (z.B. 12345):
   sudo ufw allow 12345/udp

**Broadcast-Adresse prüfen:**

.. code-block:: bash

   # Deine Netzwerk-Info anzeigen:
   ip addr show

   # Beispiel Output:
   # inet 192.168.10.50/24 brd 192.168.10.255
   #                             ^^^^^^^^^^^^^^ <- Das ist deine Broadcast-Adresse!

**Test mit socat:**

.. code-block:: bash

   # Terminal 1 (Empfänger):
   socat UDP4-RECVFROM:12345,broadcast,fork STDOUT

   # Terminal 2 (Sender):
   echo "test" | socat - UDP4-DATAGRAM:192.168.10.255:12345,broadcast

   # Terminal 1 sollte "test" anzeigen

"Port already in use"
~~~~~~~~~~~~~~~~~~~~~

Nur ein Slave kann auf einem Port lauschen pro Rechner (mit lua-socket). Socat erlaubt mehrere.

**Lösung für mehrere Slaves auf einem Rechner:**

.. code-block:: bash

   # Alle Slaves lauschen auf gleichem Port mit socat:
   mpv --script-opts=sync-role=slave,sync-backend=socat video1.mp4 &
   mpv --script-opts=sync-role=slave,sync-backend=socat video2.mp4 &

Script wird nicht geladen
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Prüfen ob mpv das Script sieht:
   mpv --msg-level=all=debug video.mp4 2>&1 | grep sync

   # Sollte anzeigen:
   # [cplayer] Loading scripts...
   # [cplayer] Loading script: /path/to/mpv-sync.lua

Beispiel-Setups
---------------

Setup 1: Ein Master, 120 Slaves im LAN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Master (Debian 13 mit lua-socket):
   mpv --script-opts=sync-role=master,sync-target=192.168.1.255:12345 video.mp4

   # Alle Slaves (gemischte Debian-Versionen):
   for i in {1..120}; do
       ssh slave$i "mpv --script-opts=sync-role=slave,sync-target=192.168.1.255:12345 video.mp4" &
   done

Setup 2: Zwei Beamer, perfekter Sync
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Beamer 1 (Master):
   mpv --script-opts=sync-role=master --fs video.mp4

   # Beamer 2 (Slave mit 25ms Offset wegen Hardware-Latenz):
   mpv --script-opts=sync-role=slave,sync-initial_offset=0.025 --fs video.mp4

   # Live-Anpassung: Ö/Ä Tasten für Feintuning

Setup 3: Stereo-Audio mit zwei Lautsprechern
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Links (Master):
   mpv --script-opts=sync-role=master --audio-channels=stereo --lavfi-complex='[aid1]pan=stereo|c0=c0|c1=c0[ao]' video.mp4

   # Rechts (Slave):
   mpv --script-opts=sync-role=slave --audio-channels=stereo --lavfi-complex='[aid1]pan=stereo|c0=c1|c1=c1[ao]' video.mp4

Performance
-----------

lua-socket vs socat
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 25 25 25
   :header-rows: 1

   * - Backend
     - CPU
     - Latenz
     - Kompatibilität
   * - lua-socket
     - ~0.1%
     - ~1ms
     - Debian 13 ✓, Debian 12 ✗
   * - socat
     - ~0.5%
     - ~5ms
     - Debian 11/12/13 ✓

**Empfehlung**: Nutze ``backend=auto`` - Script wählt automatisch das beste!

Netzwerk-Traffic
~~~~~~~~~~~~~~~~

* **Master**: ~20 Bytes/s (Position-Updates alle 0.5s)
* **Pro Slave**: ~0 Bytes/s gesendet, ~20 Bytes/s empfangen
* **120 Slaves**: Immer noch nur ~20 Bytes/s vom Master (Broadcast!)

Technische Details
------------------

Nachrichten-Format
~~~~~~~~~~~~~~~~~~

Einfaches Text-Format über UDP:

.. code-block:: text

   play                    # Play
   pause                   # Pause
   seek|123.45             # Seek zu 123.45 Sekunden
   position|123.45         # Master Position (alle 0.5s)
   speed|1.5               # Geschwindigkeit geändert

Port-Nutzung
~~~~~~~~~~~~

* **Master**: Bindet an zufälligen Port (nur senden)
* **Slaves**: Binden an konfigurierten Port (z.B. 12345) zum Empfangen
* **Broadcast**: Alle Slaves auf dem Netzwerk empfangen gleichzeitig

Lizenz
------

Frei verwendbar für private und kommerzielle Zwecke.

Changelog
---------

Version 1.1
~~~~~~~~~~~

* Dual Backend: lua-socket + socat Support
* Automatisches Backend-Fallback (auto-Modus)
* Progressive Geschwindigkeitsanpassung ohne Oszillation
* Verbesserte Timing-Parameter (20ms Sync-Threshold)

Version 1.0
~~~~~~~~~~~

* Initial Release
* lua-socket Backend
* Basic Synchronisation

Support
-------

Bei Problemen:

1. Log-Output prüfen: ``mpv --msg-level=all=info video.mp4 2>&1 | grep sync``
2. Backend manuell wählen: ``sync-backend=socket`` oder ``sync-backend=socat``
3. Firewall/Netzwerk prüfen (siehe Fehlerbehebung)

**Script-Versionen**:

* ``mpv-sync-1.0.lua``: Nur lua-socket
* ``mpv-sync-1.1.lua``: Dual Backend (lua-socket + socat)
* ``mpv-sync-nc.lua``: Nur socat (deprecated, nutze 1.1!)
