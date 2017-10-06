#! /usr/bin/python
# _*_ coding: utf-8 _*_

#
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: dellemc_idrac_location
short_description: Configure System location fields
version_added: "2.3"
description:
    - Configure System location fields
options:
  idrac_ip:
    required: False
    description:
      - iDRAC IP Address
    default: None
  idrac_user:
    required: False
    description:
      - iDRAC user name
    default: None
  idrac_pwd:
    required: False
    description:
      - iDRAC user password
    default: None
  idrac_port:
    required: False
    description:
      - iDRAC port
    default: None
  share_name:
    required: True
    description:
      - Network file share
  share_user:
    required: True
    description:
      - Network share user in the format user@domain
  share_pwd:
    required: True
    description:
      - Network share user password
  share_mnt:
    required: True
    description:
      - Local mount path of the network file share with read-write permission for ansible user
  data_center_name:
    required: False
    description:
      - Name of the Data Center where this system is located
    default: None
  aisle_name:
    required: False
    description:
      - Name of the Aisle in Data Center
    default: None
  rack_name:
    required: False
    description:
      - Rack Name
    default: None
  rack_slot:
    required: False
    description:
      - Rack slot number
    default: None
  room_name:
    required: False
    description:
      - Name of the Room in Data Center
    default: None

requirements: ['omsdk']
author: "anupam.aloke@dell.com"
'''

EXAMPLES = '''
# Configure System Location
- name: Configure System Location
    dellemc_idrac_location:
      idrac_ip:     "192.168.1.1"
      idrac_user:   "root"
      idrac_pwd:    "calvin"
      share_name:   "\\\\10.20.30.40\\share\\"
      share_user:   "user1"
      share_pwd:    "password"
      share_mnt:    "/mnt/share"
      data_center_name: "Data Center 1"
      aisle_name:   "Aisle 1"
      rack_name:    "Rack 1"
      rack_slot:    "Slot 1"
      room_name:    "Room 1"
'''

RETURN = '''
ElapsedTimeSinceCompletion:
  type: str
  description: Time elapsed since completion of the JOB
  returned: always
  sample: "0"
InstanceID:
  type: str
  description: 
  returned: always
  sample: "JID_064113236770"
JobStartTime:
  type: str
  description: Start time of the lifecycle controller JOB
  returned: always
  sample: "NA"
JobStatus:
  type: str
  description:
  returned: always
  sample: "Completed"
JobUntilTime:
  type: str
  description: Until time of the job
  returned: always
  sample: "NA"
Message:
  type: str
  description: The message text that is displayed to the user or logged as a result of the event
  returned: always
  sample: "Successfully imported and applied system configuration XML file"
MessageArguments:
  type: str
  description: Message arguments for the lifecycle job
  returned: always
  sample: "NA"
MessageID:
  type: str
  description: Unique alphanumeric identifier of the event 
  returned: always
  sample: "SYS053"
Name:
  type: str
  description: 
  returned: always
  sample: "Import Configurtion"
PercentComplete:
  type: str
  description: Percent completion of the JOB
  returned: always
  sample: "100"
Status:
  type: str
  description: Status
  returned: always
  sample: "Success"
file:
  type: str
  description: Server configuration profile (SCP) file path 
  returned: always
  sample: "\\\\192.168.10.10\\Share\\scpO3ZxL1.xml1"
retval:
  type: bool
  description: Return value
  returned: always
  sample: true

'''

from ansible.module_utils.dellemc_idrac import *
from ansible.module_utils.basic import AnsibleModule


def setup_idrac_location(idrac, module):
    """
    Setup iDRAC System Location

    Keyword arguments:
    idrac  -- iDRAC handle
    module -- Ansible module
    """

    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        idrac.config_mgr._sysconfig.System.ServerTopology.\
            DataCenterName_ServerTopology = module.params['data_center_name']
        idrac.config_mgr._sysconfig.System.ServerTopology.\
            AisleName_ServerTopology = module.params['aisle_name']
        idrac.config_mgr._sysconfig.System.ServerTopology.\
            RackName_ServerTopology = module.params['rack_name']
        idrac.config_mgr._sysconfig.System.ServerTopology.\
            RackSlot_ServerTopology = module.params['rack_slot']
        idrac.config_mgr._sysconfig.System.ServerTopology.\
            RoomName_ServerTopology = module.params['room_name']

        msg['changed'] = idrac.config_mgr._sysconfig.is_changed()

        if module.check_mode:
            # since it is running in check mode, reject the changes
            idrac.config_mgr._sysconfig.reject()
        else:
            msg['msg'] = idrac.config_mgr.apply_changes()

            if "Status" in msg['msg'] and msg['msg']['Status'] != "Success":
                msg['failed'] = True
                msg['changed'] = False

    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True

    return msg, err

# Main
def main():

    module = AnsibleModule (
            argument_spec = dict (

                # iDRAC handle
                idrac = dict (required = False, type = 'dict'),

                # iDRAC Credentials
                idrac_ip   = dict (required = True, type = 'str'),
                idrac_user = dict (required = True, type = 'str'),
                idrac_pwd  = dict (required = True, type = 'str', no_log = True),
                idrac_port = dict (required = False, default = 443, type = 'int'),

                # Network File Share
                share_name = dict (required = True, type = 'str'),
                share_user = dict (required = True, type = 'str'),
                share_pwd  = dict (required = True, type = 'str', no_log = True),
                share_mnt  = dict (required = True, type = 'path'),

                data_center_name = dict (required = False, default = None, type = 'str'),
                aisle_name = dict (required = False, default = None, type = 'str'),
                rack_name = dict (required = False, default = None, type = 'str'),
                rack_slot = dict (required = False, default = None, type = 'str'),
                room_name = dict (required = False, default = None, type = 'str')
                ),

            supports_check_mode = True)

    # Connect to iDRAC
    idrac_conn = iDRACConnection (module)
    idrac = idrac_conn.connect()

    # Setup network share as local mount
    if not idrac_conn.setup_nw_share_mount():
        module.fail_json(msg="Failed to setup network share local mount point")

    # Setup system topology
    msg, err = setup_idrac_location (idrac, module)

    # Disconnect from iDRAC
    idrac_conn.disconnect()

    if err:
        module.fail_json(**msg)
    module.exit_json(**msg)

if __name__ == '__main__':
    main()