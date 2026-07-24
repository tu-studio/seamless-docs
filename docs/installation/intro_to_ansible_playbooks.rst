Intro to Ansible playbooks
==========================

This (very) short guide shows how to install our software stack onto
remote machines using Ansible playbooks. These playbooks are ran on your
local machine but execute on the remote ones.

Getting started
---------------

1. Clone the
   `seamless-install-maintain <https://github.com/tu-studio/seamless-install-maintain/tree/main>`__
   repo.
2. Follow the repo ``README.md`` there to get Ansible up and running.

Convention
----------

Ansible playbooks for installation are run with this command:

.. code:: bash

   ansible-playbook -i <your_inventory>.yml <playbook_name>.yml

.. hint:: Whenever a ``install/*.yml`` file is mentioned in any other guide, it
   should be executed using the command above.
