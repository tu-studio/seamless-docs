Jacktrip Connection
===================

to connect via jacktrip (for example to play audio from linux machine)

on the playstation run `jacktrip -S`
on the client run `jacktrip --receivechannels 1 --sendchannels 8 -C 3900-ZG-PS-01.tu-ctrl -K jacktrip_client -D`, if you run it on a pipewire system prepend the command with `PIPEWIRE_LATENCY="2048/48000"`

on your client connect the desired inputs to the jacktrip client. they are mapped to the seamless system starting from channel 0

at 2048 buffersize only 16 channels total (ins+outs) are possible
