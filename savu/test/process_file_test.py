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
.. module:: framework_test
   :platform: Unix
   :synopsis: unittest test class for plugin utils

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""

import unittest
import tempfile

from savu.data.plugin_info import PluginList

from savu.core import process
from savu.plugins import utils as pu
from savu.test import test_utils as tu

base_class_name = "savu.plugins.plugin"


class FrameworkTest(unittest.TestCase):

    def setUp(self):
        self.process_filename = None

    @unittest.skip("This is superceeded by the new plugin runner, and should be migrated")
    def test_pipeline(self):
        if self.process_filename is None:
            return

        print self.process_filename
        temp_dir = tempfile.gettempdir()
        plugin_list = PluginList()
        plugin_list.populate_plugin_list(self.process_filename)

        first_plugin = pu.load_plugin(plugin_list.plugin_list[0]['id'])
        input_data = tu.get_appropriate_input_data(first_plugin)[0]

        try :
            process.run_plugin_list(input_data, plugin_list, temp_dir)
        except ImportError as e:
            print("Failed to run plugin test as libraries not available (%s), passing test" % (e))
            pass

class Process01Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process01.nxs')


class Process02Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process02.nxs')


class Process03Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process03.nxs')


class Process04Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process04.nxs')


class Process05Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process05.nxs')


class Process06Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process06.nxs')


class Process07Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process07.nxs')


class Process08Test(FrameworkTest):

    def setUp(self):
        self.process_filename = tu.get_test_data_path('process08.nxs')

if __name__ == "__main__":
    unittest.main()
