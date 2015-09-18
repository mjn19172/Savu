# Copyright 2014 Diamond Light Source Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
.. module:: utils
   :platform: Unix
   :synopsis: Utilities for plugin management

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""

import sys
import os
import logging
import re

import numpy as np

from savu.data.structures import Data, PassThrough
from savu.data.structures import RawTimeseriesData, ProjectionData, VolumeData

plugins = {}


def register_plugin(clazz):
    """decorator to add logging information around calls for use with ."""
    plugins[clazz.__name__] = clazz
    return clazz


def load_plugin(plugin_name):
    """Load a plugin.

    :param plugin_name: Name of the plugin to import /path/loc/then.plugin.name
                    if there is no path, then the assumptiuon is an internal
                    plugin
    :type plugin_name: str.
    :returns:  An instance of the class described by the named plugin

    """
    #logging.debug("Running load_plugin")
    path, name = os.path.split(plugin_name)
    #logging.debug("Path is : %s", path)
    #logging.debug("Name is : %s", name)
    if (path is not '') and (path not in sys.path):
        #logging.debug("Appending path")
        sys.path.append(path)
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    clazz = getattr(mod, module2class(name.split('.')[-1]))
    instance = clazz()
    instance.populate_default_parameters()
    return instance


def module2class(module_name):
    """
    Converts a module name to a class name

    :param module_name: The lowercase_module_name of the module
    :type module_name: str
    :returns:  the module name in CamelCase
    """
    return ''.join(x.capitalize() for x in module_name.split('_'))


def find_args(dclass):
    """
    Finds the parameters list from the docstring
    """
    if not dclass.__doc__:
        return []
    lines = dclass.__doc__.split('\n')
    param_regexp = re.compile('^:param (?P<param>\w+):\s?(?P<doc>\w.*[^ ])\s' +
                              '?Default:\s?(?P<default>.*[^ ])$')
    args = [param_regexp.findall(line.strip(' .')) for line in lines]
    args = [arg[0] for arg in args if len(arg)]
    return [{'dtype': type(value),
             'name': a[0], 'desc': a[1],
             'default': value} for a in args for value in [eval(a[2])]]


def load_raw_data(filename):
    data = RawTimeseriesData()
    data.populate_from_nx_tomo(filename)
    return data


def get_raw_data(input_data, file_name, group_name, mpi=False, new_shape=None):
    """
    Gets a file backed, Raw data object

    :returns:  a RawTimeseriesData Object containing the example data.
    """
    data = RawTimeseriesData()
    data.create_backing_h5(file_name, group_name, input_data, mpi, new_shape)
    return data


def get_projection_data(input_data, file_name, group_name,
                        mpi=False, new_shape=None):
    """
    Gets a file backed, Raw data object

    :returns:  a RawTimeseriesData Object containing the example data.
    """
    data = ProjectionData()
    data.create_backing_h5(file_name, group_name, input_data, mpi, new_shape)
    return data


def get_volume_data(input_data, file_name, group_name, mpi=False,
                    new_shape=None):
    """
    Gets a file backed, Raw data object

    :returns:  a RawTimeseriesData Object containing the example data.
    """
    data = VolumeData()
    data_shape = new_shape
    if data_shape is None:
        data_shape = (input_data.data.shape[2], input_data.data.shape[1],
                      input_data.data.shape[2])
    data_type = np.double
    data.create_backing_h5(file_name, group_name, data_shape,
                           data_type, mpi)
    return data


def create_output_data(plugin, input_data, file_name, group_name, mpi=False,
                       new_shape=None):
    """Creates an output file of the appopriate type for a specified plugin

    :param plugin: The plugin for which the data is being created.
    :type plugin: savu.plugins.Plugin
    :param input_data: The data which is being passed to the plugin
    :type input_data: savu.structure.Data
    :param file_name: The file name of the new output file
    :type file_name: path
    :param group_name: the group name which all the data will be put into
    :type group_name: str
    :param mpi: Whether this is running in the MPI environment
    :type mpi: bool
    :returns:  The output data object
    """
    if plugin.output_data_type() == PassThrough:
        return input_data
    if plugin.output_data_type() == RawTimeseriesData:
        return get_raw_data(input_data, file_name,
                            group_name, mpi, new_shape)

    elif plugin.output_data_type() == ProjectionData:
        return get_projection_data(input_data, file_name,
                                   group_name, mpi, new_shape)

    elif plugin.output_data_type() == VolumeData:
        return get_volume_data(input_data, file_name,
                               group_name, mpi, new_shape)

    elif plugin.output_data_type() == Data:
        if isinstance(input_data, RawTimeseriesData):
            return get_raw_data(input_data, file_name,
                                group_name, mpi, new_shape)

        elif isinstance(input_data, ProjectionData):
            return get_projection_data(input_data, file_name,
                                       group_name, mpi, new_shape)

        elif isinstance(input_data, VolumeData):
            return get_volume_data(input_data, file_name,
                                   group_name, mpi, new_shape)
