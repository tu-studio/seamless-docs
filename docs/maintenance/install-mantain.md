# Varia

## Specify program versions

Desired versions are specified in `vars/program_versions.yml`, these correspond
to GitHub tags/branches/commits.

To overwrite the version of a specific program pass it to the
`ansible-playbook` call as `-e "<program>_version=X"`

## Encrypt variable

```bash
ansible-vault encrypt_string --name "variable_name"
```

## Additional Ansible scripts not run from full_install

- `install/install_jack-silence-detector`: debugging tool to discover longer
  silences (was used to debug reaper crashes)
- `install/reboot.yml`: used to reboot everything, sometimes used by services
- `install/remove_apt_cdrom_source.yml`: sometimes needed if installation of
  programs on fresh debian installs fails.
- `install/upgrade_system.yml`: performs a system upgrade

## Maintenance playbooks

- `maintain/pull_videos.yml`: pulls all videos from the video players to your
  local machine
- `maintain/rollout_videos.yml`/`maintain/rollout_info_text.yml`: roll out the
  video/info video files of the desired piece to all video/info players, has to
  be modified before use:
  1. Add video file name to `maintain/templates/playlist.txt.j2`, `{{ video_id
     }}` will be replaced with the index of this video player (1-6).
  2. Change `project_source` to point to the folder containing the videos on
     your local machine.
  3. Add a block like this to the tasks in `rollout_videos.yml`:
    ``` yaml
        - name: "Copy <new_project> onto the server"
        copy:
            src: "{{ project_source }}/<new_project>/cool_filename-0{{ video_id }}.mp4"
            dest: "{{ target_content_dir  }}"
            owner: kiosk
            group: avm
            mode: "u=rwx,g=rwx,o=rx"
    ```

