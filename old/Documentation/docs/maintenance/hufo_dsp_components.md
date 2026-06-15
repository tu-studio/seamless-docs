# DSP Components at HuFo

## QSC

DSP processor, function currently unknown. Runs a 'design file', which has
eluded some attempts at inspection.

- Hostname: 3900-ZG-AD-01
- IP: 10.30.80.100

### QSC Core Web interface

The web interface is reachable over a separate IP address (no hostname as
of 15.6.2026) but does not offer any useful functionality.

- IP: 10.30.70.208
- login: tu-studio

## HD2

Every single WFS panel features a DSP unit by HD2. They are accessible on
the `tu-dante` network. Configuration is done using the Windows-only
program [HD2Control](https://www.four-audio.com/downloads-de/). Use Wine
on Linux and Whisky on macOS to get it running. It is recommended to turn
off Wi-Fi before connecting, as the software might get confused if it's
on.

As of writing (9.6.2026), every panel features the same EQ curve.
