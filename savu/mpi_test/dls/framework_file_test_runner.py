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
.. module:: mpi_runner
   :platform: Unix
   :synopsis: runner for tests using the MPI framework

.. moduleauthor:: Mark Basham <scientificsoftware@diamond.ac.uk>

"""

import logging
import optparse
import socket

from itertools import chain

from mpi4py import MPI
from savu.core import process

from savu.data.plugin_info import PluginList
from savu.core.utils import logfunction

import savu.plugins.utils as pu
import savu.test.test_utils as tu



@logfunction
def call_mpi_barrier():
    logging.debug("Waiting at the barrier")
    MPI.COMM_WORLD.barrier()


if __name__ == '__main__':

    usage = "%prog [options]"
    version = "%prog 0.1"
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option("-n", "--names", dest="names", help="Process names",
                      default="CPU1,CPU2,CPU3,CPU4,CPU5,CPU6,CPU7,CPU8",
                      type='string')
    parser.add_option("-f", "--filename", dest="process_filename",
                      help="The filename of the process file",
                      default="process01.nxs",
                      type='string')
    parser.add_option("-d", "--dir", dest="directory",
                      help="Temp direcotry name",
                      default="/dls/tmp/nic_savu/cluster",
                      type='string')
    (options, args) = parser.parse_args()

    RANK_NAMES = options.names.split(',')

    RANK = MPI.COMM_WORLD.rank
    SIZE = MPI.COMM_WORLD.size
    RANK_NAMES_SIZE = len(RANK_NAMES)
    if RANK_NAMES_SIZE > SIZE:
        RANK_NAMES_SIZE = SIZE
    MACHINES = SIZE/RANK_NAMES_SIZE
    MACHINE_RANK = RANK/MACHINES
    MACHINE_RANK_NAME = RANK_NAMES[MACHINE_RANK]
    MACHINE_NUMBER = RANK % MACHINES
    MACHINE_NUMBER_STRING = "%03i" % (MACHINE_NUMBER)
    ALL_PROCESSES = [[i]*MACHINES for i in RANK_NAMES]
    ALL_PROCESSES = list(chain.from_iterable(ALL_PROCESSES))

    logging.basicConfig(level=0, format='L %(relativeCreated)12d M' +
                        MACHINE_NUMBER_STRING + ' ' + MACHINE_RANK_NAME +
                        ' %(levelname)-6s %(message)s', datefmt='%H:%M:%S')

    MPI.COMM_WORLD.barrier()

    logging.info("Starting the test process")

    logging.debug("Rank : %i - Size : %i", RANK, SIZE)

    IP = socket.gethostbyname(socket.gethostname())

    logging.debug("ip address is : %s", IP)

    call_mpi_barrier()

    import os
    logging.debug(os.getenv('LD_LIBRARY_PATH'))

    call_mpi_barrier()

    process_filename = tu.get_test_data_path(options.process_filename)

    process_list = PluginList()
    process_list.populate_process_list(process_filename)

    first_plugin = pu.load_plugin(process_list.process_list[0]['id'])
    input_data = tu.get_appropriate_input_data(first_plugin)[0]

    process.run_process_list(input_data, process_list, options.directory,
                             mpi=True, processes=ALL_PROCESSES,
                             process=RANK)

    call_mpi_barrier()

    
