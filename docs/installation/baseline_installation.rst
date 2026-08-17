Baseline installation
=====================

This guide shows how to install our baseline software stack onto remote
machines. We assume familiarity with the use of Ansible playbooks, as
documented in :doc:``this guide <intro_to_ansible_playbooks>``.

1.  Create ``vars/vault.yml`` from the ``vars/vault.yml.template``, fill
    it in. If regularly switching between locations, create multiple
    vault files, and just symlink them to the currently required one:
    ``ln -sf vault_hufo.yml vars/vault.yml``
2.  If you use a Dante soundcard, change the path in ``vars/vars.yml``
    to the correct path to the driver directory.
3.  Add host to Ansible inventory file, follow the provided inventory
    files for guidance

    - Hosts should be grouped into the sections

      - ``renderer``
      - ``player``,
      - ``video_player``
      - ``info_player``

    - Hosts should contain the following variables (if used):

      - ``ansible_host``: hostname
      - ``ansible_user``: username
      - ``services``: containing a list of services running on this
        machine, available services are

        - ``osc-kreuz``
        - ``jack-connection-manager``
        - ``audio-matrix``
        - ``ambisonics``
        - ``gui``
        - ``showcontrol``
        - ``twonder``
        - ``location``: the location of this machine for use with the
          configs, at the moment one of ``HUFO``, ``EN325`` or ``H0104``

      - ``audiodriver``: list of strings or single string of ``dante``
        or ``madi``
      - ``n_twonders`` only necessary if services contains ``twonder``,
        sets up the ``twonder.target`` with the correct number of
        twonders

4.  Roll out your SSH key to PCs:
    ``ansible-playbook install/rollout_ssh_key.yml --ask-pass -e "key=<path/to/public/key.pub>"``.
    It might be necessary to install the ``sshpass`` package for your
    system.
5.  Change the SSH key in the ``ansible.cfg`` file to point to your
    private key.
6.  If necessary, install ``sudo``: ``install/install_sudo.yml``
7.  Set up btrfs subvolumes: ``install/setup_btrfs.yml -k``. This needs the
    ``-k`` option to ask for the SSH connection password, because moving around
    the btrfs subvolumes briefly moves the ``.ssh`` directory somewhere else…

.. warning:: Don't do this more than once!
   
8.  When in HuFo: run HuFo specific scripts:

   1.  ``install/hufo_setup_proxy_server.yml``
   2. ``install/hufo_first_run.yml``
   3. ``install/hufo_avm_user.yml``

9. Start main installation script: ``install/full_install.yml``

