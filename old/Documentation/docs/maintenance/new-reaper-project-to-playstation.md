# 1: New Piece to main project

**Projects On MacBook**

Copy most recent project from Playstation
`rsync tu-studio@hufo_playstation:showcontrol_project/reaper_projects/<YYYY-MM-DD>_hufo_show.RPP ak/showcontrol_project/reaper_projects/<YYYY-MM-DD>_hufo_show.RPP`

move audio files to Users/humboldt-forum/hufo_show_projects/audiofiles (?)

open production project and hufo_show project as separate project tabs in Reaper

### In the production project

TODO: instructions for cleaning up production project ..

- Arrange session to have exact same layout/channel structure as the hufo_show_project
  - Some tracks might be hidden and can be shown in the Track Manager (Menu: View->Track Manager) by clicking on the fields in the TCP and MCP columns
- Every Automation Lane for every plugin (on a channel that contains audio) needs at least one automation point:
  - Action: "Envelope: Show all envelopes for all tracks"
  - Insert help marker shortly before the start of the first media item and
  - move transport to marker
  - Bind action "Envelope: Insert new point at current position (do not remove
  - nearby points)" to a key combination such as Opt+.
  - Select any envelope in the track control panel and execute key combination
  - Repeat last step for every envelope (it is currently not possible to automatically select the next envelope)
- Use **razor editing** to select all media items including automation points
  - Also include MASTER_DCA in the selection, even if its empty
- Regularly copy the selected razor edit (CMD+C)

### In the hufo_show project

- Move playback position to some minutes after the last piece in the project
- Ensure MASTER_DCA is selected in the track control panel by clicking on it
- Paste
- Set time selection to length of piece, including the extra seconds for opening and closing credits
- Ensure MASTER_DCA is selected in the track control panel by clicking on it
- Menu: Insert->New MIDI Item
- Menu: Insert->Region (from time selection)
  - **NB**: The automation points previously inserted need to be AFTER the start of the region, transport needs to move over these points for the plugin to get the value
- Name the region (does not have to be exact, only for reference)
- Add end marker
  - Move time selection to end of region
  - Menu: Insert->Marker (prompt for name)
  - Name: !1016
  - ID: one bigger than end marker of last piece
  - IMPORTANT: this has to be the same id as audio_index in the seamless-config!
- Check proper IP address in SeamLess Plugins
- place the time cursor at the beginning of the trailer to make sure plugins are initialized with zeros

# 2: MAIN PROJECT TO PLAYSTATION

##### 1: Copy Files to Playstation

rsync is used instead of ansible because it gives progress feedback and is faster

```bash
# rsync new project
rsync -Purtz ak/showcontrol_project/reaper_projects/YYYY-MM-DD_hufo_show.RPP hufo_playstation:showcontrol_project/reaper_projects

#sync new audio
export new_project="<NEW_PROJECT_NAME>"
rsync -Purtz ak/showcontrol_project/audiofiles/$new_project/ hufo_playstation:showcontrol_project/audiofiles/$new_project
```

##### 2: open new project in reaper

Reaper will always open the last opened project on boot.

❗IMPORTANT❗ : save the project after opening it, if there was a dialog saying that files could not be found.

Sometimes the kvm switch does not work then restart the playstation

# 3: Add new Piece to ShowControl

### **Add track file (yml)**

- in seamless configs repo: `HUFO/showcontrol/config/tracks/`
- copy other yml, fill with necessary infos, video indices are 0 based, audio indices 1 based
- make sure the "name" field contains a unique id for this track
- commit and push afterwards

### **Update schedules**

In the showcontrol repo. Install the python package:

```bash
pip install -e .
```

Then use the following commands to generate the schedule and human readable text file in the seamless configs repo

```bash
showcontrol_schedule_generator -c ../seamless-configs/HUFO/showcontrol/config/ -o ../seamless-configs/HUFO/showcontrol/config/schedule.yml -r ../seamless-configs/HUFO/showcontrol/readable_schedules
```

- check file the readable schedule and the `schedule.yml` in the seamless-configs repo and verify if everything looks good
- commit and push both repos

### **Apply changes on PlayStation**

1. Update Configs on playstation:

```bash
ansible-playbook -i HUFO_inventory.yml install/install_configs.yml -l "playstation"

# if you want to install something else than the main config branch specify the desired branch/tag/commit using the -e option

ansible-playbook -i HUFO_inventory.yml install/install_configs.yml -l "playstation" -e "config_version=<branch_name>"
```

1. Restart Showcontrol Service on playstation run
   1. `systemctl --user restart showcontrol.service`

# 4: Upload VIDEOs

videos are rolled out using ansible playbooks. The video files have to be placed on the machines, and the filename has to be placed in the playlist.txt.
`maintain/rollout_videos.yml` is used, however it has to be modified before use:

1. add video file name to `maintain/templates/playlist.txt.j2`, {{ video_id }} will be filled with the index of this video player (1-6)
2. put the video files into the `project_source` directory (or change the `project_source` directory to your video directory, whatever makes you happy)
3. add a block like this to the tasks in `rollout_videos.yml`:
  block:
  ```yaml
      - name: "Copy <new_project> onto the server"
      copy:
          src: "{{ project_source }}/<new_project>/cool_filename-0{{ video_id }}.mp4"
          dest: "{{ target_content_dir  }}"
          owner: kiosk
          group: avm
          mode: "u=rwx,g=rwx,o=rx"
  ```

4. run the playbook
5. restart the video players
