#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_log import log as logging

from neutron.agent.ovsdb.native.commands import BaseCommand
from neutron.agent.ovsdb.native import idlutils
from neutron.i18n import _

LOG = logging.getLogger(__name__)


class AddLSwitchCommand(BaseCommand):
    def __init__(self, api, name, may_exist, **columns):
        super(AddLSwitchCommand, self).__init__(api)
        self.name = name
        self.columns = columns
        self.may_exist = may_exist

    def run_idl(self, txn):
        if self.may_exist:
            lswitch = idlutils.row_by_value(self.api.idl, 'Logical_Switch',
                                            'name', self.name, None)
            if lswitch:
                return
        row = txn.insert(self.api._tables['Logical_Switch'])
        row.name = self.name
        for col, val in self.columns.items():
            setattr(row, col, val)


class DelLSwitchCommand(BaseCommand):
    def __init__(self, api, name, if_exists):
        super(DelLSwitchCommand, self).__init__(api)
        self.name = name
        self.if_exists = if_exists

    def run_idl(self, txn):
        try:
            lswitch = idlutils.row_by_value(self.api.idl, 'Logical_Switch',
                                            'name', self.name)
        except idlutils.RowNotFound:
            if self.if_exists:
                return
            msg = _("Logical Switch %s does not exist") % self.name
            LOG.error(msg)
            raise RuntimeError(msg)

        self.api._tables['Logical_Switch'].rows[lswitch.uuid].delete()


class LSwitchSetExternalIdCommand(BaseCommand):
    def __init__(self, api, name, field, value):
        super(LSwitchSetExternalIdCommand, self).__init__(api)
        self.name = name
        self.field = field
        self.value = value

    def run_idl(self, txn):
        lswitch = idlutils.row_by_value(self.api.idl, 'Logical_Switch',
                                        'name', self.name)
        external_ids = getattr(lswitch, 'external_ids', {})
        external_ids[self.field] = self.value
        lswitch.external_ids = external_ids


class AddLogicalPortCommand(BaseCommand):
    def __init__(self, api, lport, lswitch, may_exist, **columns):
        super(AddLogicalPortCommand, self).__init__(api)
        self.lport = lport
        self.lswitch = lswitch
        self.may_exist = may_exist
        self.columns = columns

    def run_idl(self, txn):
        try:
            lswitch = idlutils.row_by_value(self.api.idl, 'Logical_Switch',
                                            'name', self.lswitch)
        except idlutils.RowNotFound:
            msg = _("Logical Switch %s does not exist") % self.lswitch
            LOG.error(msg)
            raise RuntimeError(msg)
        if self.may_exist:
            port = idlutils.row_by_value(self.api.idl,
                                         'Logical_Port', 'name',
                                         self.lport, None)
            if port:
                return

        port = txn.insert(self.api._tables['Logical_Port'])
        port.name = self.lport
        port.lswitch = lswitch
        for col, val in self.columns.items():
            setattr(port, col, val)


class SetLogicalPortCommand(BaseCommand):
    def __init__(self, api, lport, **columns):
        super(SetLogicalPortCommand, self).__init__(api)
        self.lport = lport
        self.columns = columns

    def run_idl(self, txn):
        try:
            port = idlutils.row_by_value(self.api.idl, 'Logical_Port',
                                         'name', self.lport)
        except idlutils.RowNotFound:
            msg = _("Logical Port %s does not exist") % self.lport
            LOG.error(msg)
            raise RuntimeError(msg)

        for col, val in self.columns.items():
            setattr(port, col, val)


class DelLogicalPortCommand(BaseCommand):
    def __init__(self, api, lport, if_exists):
        super(DelLogicalPortCommand, self).__init__(api)
        self.lport = lport
        self.if_exists = if_exists

    def run_idl(self, txn):
        try:
            lport = idlutils.row_by_value(self.api.idl, 'Logical_Port',
                                          'name', self.lport)
        except idlutils.RowNotFound:
            if self.if_exists:
                return
            msg = _("Port %s does not exist") % self.lport
            LOG.error(msg)
            raise RuntimeError(msg)

        self.api._tables['Logical_Port'].rows[lport.uuid].delete()


class CreateACLRuleCommand(BaseCommand):
    def __init__(self, api, lswitch_name, priority, match,
                 action, ext_ids_dict=None):
        super(CreateACLRuleCommand, self).__init__(api)
        self.lswitch_name = lswitch_name
        self.priority = priority
        self.match = match
        self.action = action
        self.ext_ids_dict = ext_ids_dict

    def run_idl(self, txn):
        try:
            lswitch = idlutils.row_by_value(self.api.idl, 'Logical_Switch',
                                            'name', self.lswitch_name)
        except idlutils.RowNotFound:
            msg = _("Logical Switch %s does not exist") % self.lswitch_name
            LOG.error(msg)
            raise RuntimeError(msg)

        row = txn.insert(self.api._tables['ACL'])
        row.lswitch = lswitch
        row.priority = self.priority
        row.match = self.match
        row.action = self.action
        row.external_ids = self.ext_ids_dict
