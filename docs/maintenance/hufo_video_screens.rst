Betriebsdokumentation — Kiosk-Videoplayer
==========================================

Alle 8 PCs wurden automatisiert installiert: Debian Preseed für das
Grundsystem, anschließend ``firstrun.sh`` für die Kiosk-Konfiguration
(STM-Installer). Die Systeme sind identisch aufgesetzt.

1. Überblick
------------

Diese Systeme sind Kiosk-Videoplayer auf Basis von Debian Trixie (13).
Jeder PC startet automatisch einen MPV-Player im Vollbild.

Es gibt zwei Gruppen:

* **PC 1–6** — Video-Playback mit synchronisierter Wiedergabe (mpv-sync.lua, Master/Slave)
* **PC 7–8** — Statische Bilder aus einer Playlist (kein Sync)

Die PCs wurden mit dem STM-Installer aufgesetzt (``firstrun.sh`` nach Preseed-Installation).

Netzwerk
~~~~~~~~

Die Installation läuft aktuell noch im alten Netz ``172.25.18.0/22``. Die PCs bekommen demnächst ein eigenes VLAN mit neuen Adressen — Broadcast-Adressen in ``mpv.conf`` und Bridge-Service müssen dann angepasst werden.

.. list-table::
   :widths: 10 30 60
   :header-rows: 1

   * - PC
     - Hostname
     - IP (aktuell, DHCP)
   * - 1
     - ``3910-pc-01.asg``
     - ``172.25.18.171``
   * - 2
     - ``3910-pc-02.asg``
     - ``172.25.18.172``
   * - 3
     - ``3910-pc-03.asg``
     - ``172.25.18.173``
   * - 4
     - ``3910-pc-04.asg``
     - ``172.25.18.174``
   * - 5
     - ``3910-pc-05.asg``
     - ``172.25.18.175``
   * - 6
     - ``3910-pc-06.asg``
     - ``172.25.18.176``
   * - 7
     - ``3910-pc-07.asg``
     - ``172.25.18.177``
   * - 8
     - ``3910-pc-08.asg``
     - ``172.25.18.178``

.. note::
   **Bei VLAN-Umzug anpassen:**

   * Broadcast-Adresse in ``mpv.conf`` (``sync-target=172.25.19.255:...``)
   * Broadcast-Adresse im Bridge-Service (``mpv-udp-bridge.service``)

2. Benutzer
-----------

.. list-table::
   :widths: 15 45 40
   :header-rows: 1

   * - User
     - Zweck
     - Login
   * - ``kiosk``
     - Kiosk-Betrieb, startet den Player automatisch
     - Auto-Login via LightDM
   * - ``avm``
     - Administration (AVM-Team)
     - SSH, VNC, sudo (mit Passwort)
   * - ``tu``
     - Administration (TU Berlin)
     - SSH, VNC, sudo (mit Passwort)

Alle drei User gehören zur Gruppe ``avm`` — können gegenseitig Dateien lesen und schreiben.
SSH-Keys sind für ``avm`` und ``kiosk`` hinterlegt. Für ``tu`` müssen die SSH-Keys des TU-Teams noch eingetragen werden (``/home/tu/.ssh/authorized_keys``).

3. Verzeichnisstruktur
----------------------

Alle benutzerbezogenen Dateien liegen unter ``/home/kiosk/content/``:

.. code-block:: text

   /home/kiosk/content/
   ├── startup.sh              # Autostart-Script (wird bei kiosk-Login ausgeführt)
   ├── mpv.conf                # MPV-Konfiguration (Lautstärke, Mute, Video-Optionen)
   ├── mpv-sync.lua            # Sync-Script für Multi-Player-Betrieb
   ├── watchlater_files/       # MPV Wiedergabepositionen (automatisch)
   ├── userconfig.txt          # Konfiguration für die Humboldt-Probe (MQTT)
   ├── README-mpv-sync.md      # Doku zum Sync-Script
   └── (Videos / Playlisten)   # Hier eigene Inhalte ablegen

Die MPV-Hauptkonfiguration unter ``~/.config/mpv/mpv.conf`` inkludiert automatisch ``/home/kiosk/content/mpv.conf`` — dort Änderungen vornehmen.

mpv.conf — PC 1–6 (Video mit Sync)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Einer der PCs ist Master, die restlichen sind Slaves. Die Konfiguration ist identisch bis auf die ``script-opts``-Zeile:

.. code-block:: ini

   vo=gpu-next
   hwdec=vaapi
   profile=gpu-hq
   fullscreen
   input-ipc-server=/tmp/mpvsocket
   pause                          # Startet pausiert (wird per Bridge/Sync gestartet)
   reset-on-next-file=pause       # Bei Playlist-Wechsel wieder pausieren
   loop-playlist                  # Gesamte Playlist in Schleife

   script=~/content/mpv-sync.lua
   # Master (genau ein PC):
   script-opts=sync-backend=socat,sync-role=master,sync-target=172.25.19.255:12338,sync-interval=0.5,sync-show_osd=no
   # Slaves (alle anderen):
   #script-opts=sync-backend=socat,sync-role=slave,sync-target=172.25.19.255:12338,sync-initial_offset=0.015,sync-show_osd=no

mpv.conf — PC 7–8 (Statische Bilder)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

   vo=gpu-next
   hwdec=vaapi
   profile=gpu-hq
   fullscreen
   input-ipc-server=/tmp/mpvsocket
   pause
   reset-on-next-file=pause
   loop                           # Aktuellen Eintrag loopen (nicht die Playlist)

Kein Sync-Script. ``loop`` (statt ``loop-playlist``) sorgt dafür, dass das aktuell angezeigte Bild dauerhaft gehalten wird.

4. MPV-Steuerung
----------------

mpv_control Script
~~~~~~~~~~~~~~~~~~

Das Script ``/usr/bin/mpv_control`` steuert MPV über den IPC-Socket ``/tmp/mpvsocket``:

.. code-block:: text

   mpv_control play              # Wiedergabe starten
   mpv_control pause             # Pausieren
   mpv_control play-pause        # Umschalten Play/Pause
   mpv_control next              # Nächster Titel
   mpv_control prev              # Vorheriger Titel
   mpv_control skip_plus         # 60 Sekunden vorspringen
   mpv_control skip_minus        # 60 Sekunden zurückspringen
   mpv_control playlist_index N  # Titel N aus der Playlist spielen
   mpv_control vol_get           # Aktuelle Lautstärke abfragen
   mpv_control vol_plus          # Lautstärke +5
   mpv_control vol_minus         # Lautstärke -5
   mpv_control get_mute          # Mute-Status abfragen (0/1)
   mpv_control set_mute 1        # Muten
   mpv_control set_mute 0        # Unmuten
   mpv_control get_filename      # Aktuellen Dateinamen abfragen
   mpv_control get_playlist_index    # Aktuelle Position in der Playlist
   mpv_control get_playlist_count    # Anzahl Titel in der Playlist
   mpv_control file_pos_percent      # Wiedergabeposition in Prozent
   mpv_control file_pos_sec          # Wiedergabeposition in Sekunden
   mpv_control file_duration_sec     # Gesamtlänge in Sekunden

Lautstärke- und Mute-Änderungen über ``mpv_control`` werden automatisch in ``mpv.conf`` persistiert.

Fernsteuerung (mpv-udp-bridge)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Der Service ``mpv-udp-bridge.service`` empfängt UDP-Broadcast-Befehle und leitet ``play``/``pause``-Kommandos an den MPV-Socket weiter.

**Ports:**

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - PCs
     - UDP-Port
   * - 1–6
     - 12339
   * - 7–8
     - 12340

Der Bridge-Befehl (exemplarisch PC 1–6):

.. code-block:: bash

   /usr/bin/socat -u UDP4-RECVFROM:12339,broadcast,fork,reuseaddr \
     SYSTEM:"/bin/grep -E 'play|pause' | socat - /tmp/mpvsocket"

Damit kann MPV von einem anderen Rechner gesteuert werden:

.. code-block:: bash

   # Play an alle PCs 1-6 senden:
   echo '{ "command": ["set", "pause", "no"] }' | socat - UDP4-DATAGRAM:172.25.19.255:12339,broadcast

   # Pause an PC 7-8:
   echo '{ "command": ["set", "pause", "yes"] }' | socat - UDP4-DATAGRAM:172.25.19.255:1240,broadcast

.. note::
   Die Bridge filtert auf ``play`` und ``pause`` — andere Befehle werden verworfen. Für volle MPV-Steuerung direkt per SSH und ``mpv_control`` arbeiten.

.. warning::
   **mmm:** Der Befehl, den wir brauchen, um ein bestimmtes Video zu schicken, ist ``playlist-play-index``. Das funktioniert nur, weil ``grep -E play|pause`` aus Versehen auch ``playlist-play-index`` matcht lol. Die Filterung könnte also robuster sein, da das Ganze vielleicht randomly breakt/nur aus Versehen funktioniert.

5. MPV-Sync (Multi-Player-Synchronisation)
------------------------------------------

Das Script ``mpv-sync.lua`` synchronisiert die Wiedergabe mehrerer MPV-Instanzen über UDP-Broadcast.

Konzept
~~~~~~~

* **Master** sendet regelmäßig seine Wiedergabeposition per UDP-Broadcast
* **Slaves** empfangen die Position und gleichen sich an (Geschwindigkeitsanpassung oder Seek)
* Backend: ``socat`` (lua-socket ist inkompatibel mit MPV in Debian 13)

Aktuelle Konfiguration (PC 1–6)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sync ist aktiv. In der ``mpv.conf`` von PC 1–6:

.. code-block:: ini

   #

Für Slaves die Rolle ändern:

.. code-block:: ini

   script-opts=sync-backend=socat,sync-role=slave,sync-target=172.25.19.255:12338,sync-initial_offset=0.015,sync-show_osd=no

Parameter
~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1

   * - Parameter
     - Beschreibung
   * - ``sync-backend``
     - ``socat`` (empfohlen für Debian 13)
   * - ``sync-role``
     - ``master`` oder ``slave``
   * - ``sync-target``
     - Broadcast-Adresse:Port (``172.25.19.255:12338``)
   * - ``sync-interval``
     - Sendeintervall Master in Sekunden (Standard: 0.5)
   * - ``sync-initial_offset``
     - Zeitversatz Slave in Sekunden (Feintuning)
   * - ``sync-show_osd``
     - OSD-Anzeige (``yes``/``no``)

Detaillierte Dokumentation: ``/home/kiosk/content/README-mpv-sync.md``

6. Fernzugriff
--------------

SSH
~~~

.. code-block:: bash

   ssh avm@HOSTNAME      # Admin-Zugang AVM (sudo möglich)
   ssh tu@HOSTNAME       # Admin-Zugang TU Berlin (sudo möglich)
   ssh kiosk@HOSTNAME    # Direkter Zugriff auf Kiosk-User

VNC
~~~

**x11vnc** — Zugriff auf das laufende Kiosk-Display (Port 5900):

.. code-block:: bash

   # Nur über SSH-Tunnel (x11vnc bindet auf localhost):
   ssh -L 5900:localhost:5900 avm@HOSTNAME
   # Dann VNC-Viewer auf localhost:5900 verbinden

**TigerVNC** — Eigene Desktop-Session als avm- oder tu-User:

.. code-block:: bash

   # Auf dem Zielrechner:
   tigervncserver        # Startet Session auf :1 (Port 5901)

   # Vom eigenen Rechner:
   ssh -L 5901:localhost:5901 tu@HOSTNAME
   # VNC-Viewer auf localhost:5901

VNC-Passwort: ``avm`` (User avm) / ``tu2026!`` (User tu)

7. Systemdienste
----------------

.. list-table::
   :widths: 35 65
   :header-rows: 1

   * - Service
     - Beschreibung
   * - ``mpv-udp-bridge.service``
     - UDP→Socket-Bridge für MPV-Fernsteuerung (Port 12339/12340)
   * - ``humboldt-probe.service``
     - MQTT-Monitoring (Ping, Temperatur, Mute-Status etc.)
   * - ``wolfix.service``
     - Wake-on-LAN Fix für Dell Optiplex (oneshot)
   * - ``lightdm``
     - Display-Manager, Auto-Login für kiosk

Humboldt-Probe
~~~~~~~~~~~~~~

MQTT-basiertes Monitoring-System unter ``/home/kiosk/humboldt_probe/``.
Konfiguration: ``/home/kiosk/content/userconfig.txt``
Broker: ``srv-control-avm`` (TLS mit Client-Zertifikaten)

8. Kurzreferenz — Wichtige Befehle
----------------------------------

System
~~~~~~

.. code-block:: bash

   sudo reboot                               # Neustart
   sudo shutdown -h now                      # Herunterfahren

MPV steuern
~~~~~~~~~~~

.. code-block:: bash

   mpv_control play                          # Abspielen
   mpv_control pause                         # Pause
   mpv_control next                          # Nächster Titel
   mpv_control vol_plus                      # Lauter (+5)
   mpv_control set_mute 1                    # Stumm schalten

Logs ansehen
~~~~~~~~~~~~

.. code-block:: bash

   journalctl -u mpv-udp-bridge -f           # Bridge-Log live
   journalctl -u humboldt-probe -f           # Probe-Log live
   journalctl -t mpv -f                      # MPV-Log (wenn über systemd-cat gestartet)

Services
~~~~~~~~

.. code-block:: bash

   systemctl status mpv-udp-bridge           # Status prüfen
   systemctl restart mpv-udp-bridge          # Neustarten
   systemctl status humboldt-probe

Kiosk-Session neustarten
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Als avm-User:
   sudo systemctl restart lightdm            # Startet kiosk-Session komplett neu
