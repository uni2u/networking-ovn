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

from oslo_config import cfg

ovn_opts = [
    cfg.StrOpt('ovsdb_connection',
               default='tcp:127.0.0.1:6640',
               help=_('The connection string for the native OVSDB backend')),
    cfg.IntOpt('ovsdb_connection_timeout',
               default=10,
               help=_('Timeout in seconds for the OVSDB '
                      'connection transaction')),
    cfg.StrOpt('neutron_sync_mode',
               default='log',
               help=_('The synchronization mode of OVN with Neutron DB. \n'
                      'off - synchronization is off \n'
                      'log - during neutron-server startup, '
                      'check to see if OVN is in sync with '
                      'the Neutron database. '
                      ' Log warnings for any inconsistencies found so'
                      ' that an admin can investigate \n'
                      'repair - during neutron-server startup, automatically'
                      ' create resources found in Neutron but not in OVN.'
                      ' Also remove resources from OVN'
                      ' that are no longer in Neutron.')),
]

cfg.CONF.register_opts(ovn_opts, 'ovn')


def get_ovn_ovsdb_connection():
    return cfg.CONF.ovn.ovsdb_connection


def get_ovn_ovsdb_timeout():
    return cfg.CONF.ovn.ovsdb_connection_timeout


def get_ovn_neutron_sync_mode():
    return cfg.CONF.ovn.neutron_sync_mode
