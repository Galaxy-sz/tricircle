# Copyright 2017 Huawei Technologies Co., Ltd.
# All Rights Reserved
#
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


import migrate
import sqlalchemy as sql


def upgrade(migrate_engine):
    meta = sql.MetaData()
    meta.bind = migrate_engine

    shadow_agents = sql.Table(
        'shadow_agents', meta,
        sql.Column('id', sql.String(length=36), primary_key=True),
        sql.Column('pod_id', sql.String(length=64), nullable=False),
        sql.Column('host', sql.String(length=255), nullable=False),
        sql.Column('type', sql.String(length=36), nullable=False),
        sql.Column('tunnel_ip', sql.String(length=48), nullable=False),
        migrate.UniqueConstraint(
            'pod_id', 'host', 'type',
            name='pod_id0host0type'),
        mysql_engine='InnoDB',
        mysql_charset='utf8')
    shadow_agents.create()

    pods = sql.Table('pods', meta, autoload=True)
    fkey = {'columns': [shadow_agents.c.pod_id],
            'references': [pods.c.pod_id]}
    migrate.ForeignKeyConstraint(columns=fkey['columns'],
                                 refcolumns=fkey['references'],
                                 name=fkey.get('name')).create()


def downgrade(migrate_engine):
    raise NotImplementedError('downgrade not support')
