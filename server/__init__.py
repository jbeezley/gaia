#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################
import os
from girder.utility.config import _mergeConfig
from girder.plugins.gaia.rest import geoprocess
from girder.plugins.gaia.geoservice_proxy import GeoserviceProxy
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

# Read the configuration files
_cfgs = ('gaia.dist.cfg', 'gaia.local.cfg')
for f in _cfgs:
    configPath = os.path.join(PACKAGE_DIR, '../gaia/conf', f)
    if os.path.exists(configPath):
        _mergeConfig(configPath)


def load(info):
    info['serverRoot'].geo = GeoserviceProxy()
    info['apiRoot'].geoprocess = geoprocess.GeoProcess()
