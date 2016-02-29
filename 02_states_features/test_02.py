
# import some Python modules
import os.path

# import Simulator and Logger
import Simulator
import Logger

# import SECOND time definition
from ITimeKeeper import SECOND

# import unit test services
from tu_utils import tu_test_action, tu_test, tu_start_of_check, tu_end_of_check, \
                     tu_check_file, obj_dir, tu_make

# set unitary test information
tu_test("test_02", "K2 Tutorial", "States / Features", "States / Features example models")

# compile models
tu_make("Makefile")

# create Logger
tu_test_action("Create the Logger")
log_file  = os.path.join( obj_dir, "test_02.log" )
my_logger = Logger.Logger(log_file)
my_logger.SetDebugLog(True)

# create simulator and attach the Logger
tu_test_action("Create a simulator")
sim = Simulator.Simulator("test_states_features", "States / Features simulation example", my_logger)

# create 2 models instances (one model contains states and the other contains features)
tu_test_action("Create model instances in the simulator")
sim.CreateModelInstance("model_states", "model_states_1", "Model that contains a state")
sim.CreateModelInstance("model_features", "model_features_1", "Model that contains a feature")

# set time update periods for algorithms
tu_test_action("Set time update periods for algorithms")
sim["model_states_1.algo.update_states.period"    ] = 1 * SECOND / 2
sim["model_features_1.algo.update_features.period"] = 1 * SECOND

# run simulation for 10 seconds
tu_test_action("Run simulation for 10 seconds")
sim.Run(10 * SECOND)

# check results (log file against reference file)
tu_test_action("Check results (log file against reference file)")
tu_start_of_check()

log_file_ref = "test_02.log.ref"
tu_check_file("Comparing resulting log file", log_file, log_file_ref)

tu_end_of_check()
