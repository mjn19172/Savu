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
.. module:: tomo_recon
   :platform: Unix
   :synopsis: runner for tests using the MPI framework

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""
import unittest
import tempfile
from savu.test import test_utils as tu

from savu.core.plugin_runner import PluginRunner


class PyfaiAzimuthalIntegrationTestFull(unittest.TestCase):

    @unittest.skip("Local files in test data, needs to be fixed")
    def test_Pyfai(self):
        options = {
            "transport": "hdf5",
            "process_names": "CPU0",
            "data_file": '/media/My Passport/Steve_data/xrd_tester2.nxs',
            "process_file": tu.get_test_data_path('PyFAI_azimuth_test.nxs'),
            "out_path": tempfile.mkdtemp()
            }
        try:
            PluginRunner(options)
        except ImportError as e:
            print("Failed to run test as libraries not available (%s)," % (e) +
                  " passing test")
            pass

if __name__ == "__main__":
    unittest.main()
