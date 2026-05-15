# Migration of old pieces
## Coordinate Transformation

During the consolidation of the seamless system into seamless v2 the coordinate system was changed.
The x-Axis runs along the default viewing direction of the listener.
The coordinate systems were normalized

### Automatic
For pieces composed for the EN325 or the HuFo his can be done using the reascripts in this [repo](https://github.com/TU-Studio/ReaScripts).
1. open reaper-session of the piece that should be rotated (best to do it in a copy) on a computer with both the old and the new seamless client installed
2. load the reascripts (`Actions->Show Action List->New Action->Load ReaScript`)
3. open the script `migrate_seamless_plugins.lua` for editing
4. set the value for `scaling_factor` to $6.046$ for the EN325 or to $12.108$ if its a HuFo piece
5. set `rotate` to `false` for the EN325 or to `true` for the HuFo
6. run the script
7. if each source track has both plugins on it and the transformed automation lanes exist (and were opened) this was a success. yay!
8. run `delete_old_plugins.lua`, you can probably guess what it does
9. Yay! Yippee


### Manual


#### 1. rotation of the coordinate system

For Pieces for the H0104 or HuFo
first rotate the coordinate system:

$$
x_\text{rotated} = - y_\text{old}\\
y_\text{rotated} = x_\text{old}
$$

#### 2. move coordinate origin (H0104 only)

$$
x_\text{offset} = 12.9246\\
y_\text{offset} = 0.0855
$$

then move the coordinate origin:

$$
x_{\text{recentered}} = x_{\text{rotated}} + x_\text{offset} \\
y_{\text{recentered}} = y_{\text{rotated}} + y_\text{offset}
$$

#### 3. apply scaling

Scaling factor $S$

$$
S_{\text{H0104}} = 25.4492 \\
S_{\text{EN325}} = 6.046 \\
S_{\text{HUFO}} = 12.108
$$

$$
x_\text{scaled} = x_\text{recentered}/{S}\\
y_\text{scaled} = y_\text{recentered}/{S}\\
z_\text{scaled} = z/{S}
$$

#### 4. Apply flip of axis (H0104 only)

flip y axis

$$
y_\text{flipped} = -y_\text{scaled}
$$


## change channel routing

There is only one 3rd order ambisonics decoder now, so the output channels have to be adjusted:

- 1st order ambi: channel 33-36
- 3rd order ambi: channel 33-48
- omni: channel 33
- lfe: channel 50

The SeamLess source channels (1-32) stay the same.