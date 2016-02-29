#! /bin/env python

import sys
import os
import os.path

from inspect import getsourcefile
from os.path import abspath

import vt.test
import vt.simulator
import vt.report

import time

from RTM_activation_explorer import STANDARD_SCHED;

# Routines Callbacks
tm_frame_parameters_ch1 = None
tm_frame_parameters_ch2 = None
tm_frame_parameters_aux = None
tm_frame_parameters_tme2 = None

def tm_set_parameters (tm_frame_parameters, parameters, results):

    tm_frame_parameters['cadu'] = parameters['cadu']
    tm_frame_parameters['cadu_size'] = parameters['cadu_size']
    tm_frame_parameters['tm_bit_rate'] = parameters['tm_bit_rate']
    tm_frame_parameters['simulation_time'] = parameters['simulation_time']

def tm_frame_routine_ch1(parameters, results):
    global tm_frame_parameters_ch1
    tm_frame_parameters_ch1 = {}
    tm_set_parameters(tm_frame_parameters_ch1, parameters, results)

def tm_frame_routine_ch2(parameters, results):
    global tm_frame_parameters_ch2
    tm_frame_parameters_ch2 = {}
    tm_set_parameters(tm_frame_parameters_ch2, parameters, results)

def tm_frame_routine_aux(parameters, results):
    global tm_frame_parameters_aux
    tm_frame_parameters_aux = {}
    tm_set_parameters(tm_frame_parameters_aux, parameters, results)

def tm_frame_routine_tme2(parameters, results):
    global tm_frame_parameters_tme2
    tm_frame_parameters_tme2 = {}
    tm_set_parameters(tm_frame_parameters_tme2, parameters, results)

# Common functions
def init_TME2 (instance_name) :
    # create_simulator
    test.do_action("Create %s instance" % (instance_name) )
    sim = test.new_simulator( instance_name = instance_name )

    sim.SetTraceFlag(True)
    sim.SetDebugFlag(True)
    sim.SetOverloadLog(True)
    sim.get_logger().SetInformationLog(True)
    sim.get_logger().SetDebugLog(True)
    sim.get_logger().SetWarningLog(True)
    sim.get_logger().SetErrorLog(True)
    

    # connect_callpoint_to_function
    sim.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_CH1" % (instance_name) , tm_frame_routine_ch1 )
    sim.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_CH2" % (instance_name) , tm_frame_routine_ch2 )
    sim.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_AUX" % (instance_name) , tm_frame_routine_aux )
    sim.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_TO_TME2" % (instance_name) , tm_frame_routine_tme2 )
   
    sim.InitializeInternal()
    return sim

def document(name,version,revision):
    test.do_action( "Applicable Document : %s / %s / %s" %(name,version,revision) )

def requirement(reqs):
    for req in reqs:
        test.do_action( "Requirement : %s" %(req) )

def call_activation_routine(sim, instance_name,routine,args):
    test.do_action( "Call routine %s with args %s" %(routine,str(args)) )
    return sim.CallActivationRoutine( "%s.routine.%s" % (instance_name,routine), args )

def call_tm_frame_from_smu_routine(sim, instance_name,message,args):

    global in_tm_bit_rate
    test.do_action( "Call routine TM_FRAME_IN_FROM_SMU with args (%s,%d,%d,2)" %(message,len(args),in_tm_bit_rate) )
    sim.CallActivationRoutine( "%s.routine.TM_FRAME_IN_FROM_SMU"%(instance_name), ( args + (0,) * (2048-len(args)), len(args), in_tm_bit_rate, 2 ) )

def call_tm_frame_from_tme2_routine(sim, instance_name,message,args):

    global in_tm_bit_rate
    test.do_action( "Call routine TM_FRAME_IN_FROM_TME2 with args (%s,%d,%d,2)" %(message,len(args),in_tm_bit_rate) )
    sim.CallActivationRoutine( "%s.routine.TM_FRAME_IN_FROM_TME2"%(instance_name), ( args + (0,) * (2048-len(args)), len(args), in_tm_bit_rate, 2 ) )

def set_state(sim, instance_name,state,value ):
    test.do_action( "Set %s.state.%s = " %(instance_name,state) + str(value))
    sim["%s.state.%s"%(instance_name,state)] = value

def set_feature( instance_name,feature,value ):
    test.do_action( "Set %s.feature.%s = %d" %(instance_name,feature,value) )
    sim["%s.feature.%s"%(instance_name,feature)] = value

def run( delta ):
    test.do_action( "Run simulator for %d ns" %(delta) )
    sim.Run(delta)

def check_feature_with_constant ( instance_name, feature_name, constant, sim):
    check.equal("Check %s.feature.%s == %d constant" % (instance_name,feature_name,constant), sim["%s.feature.%s"%(instance_name,feature_name)],  constant)
    
def check_state_with_constant ( instance_name, state_name, constant ,sim ):
    check.equal("Check %s.state.%s == " % (instance_name,state_name) + str(constant) + " constant", sim["%s.state.%s"%(instance_name,state_name)],  constant)

def check_output_with_constant ( instance_name, output_name, constant, sim ):
    check.equal("Check %s.output.%s == %f constant" % (instance_name,output_name,constant) , sim["%s.output.%s"%(instance_name,output_name)],  constant)

def check_output_with_state ( instance_name, output_name, state_name ):
    check.equal("Check %s.output.%s == %s state" % (instance_name,output_name,state_name) , sim["%s.output.%s"%(instance_name,output_name)],  sim["%s.state.%s"%(instance_name,state_name)])

def check_state_with_feature ( instance_name, state_name, feature_name ):
    check.equal("Check %s.state.%s == %s feature" % (instance_name,state_name,feature_name), sim["%s.state.%s"%(instance_name,state_name)],  sim["%s.feature.%s"%(instance_name,feature_name)])

def check_idle_frame (message, idle_cadu, res_asm_ph_sh, res_clcw, res_tm_bit_rate ):

    global max_CADU_length, out_GOODSIZE_frame_len, SIZE_asm_ph_sh, SIZE_tf_df, SIZE_clcw, SIZE_rs

    cadu_asm_ph_sh  = idle_cadu['cadu'][ 0                                                 :  SIZE_asm_ph_sh]
    cadu_clcw       = idle_cadu['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df )                   : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw)]
    cadu_0          = idle_cadu['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs): ]

    check.equal("TM frame has been propagated throughout %s : check ASM, PH, SH " % (message), cadu_asm_ph_sh, res_asm_ph_sh)
    check.equal("TM frame has been propagated throughout %s : check CLCW " % (message), cadu_clcw, res_clcw)
    check.equal("TM frame has been propagated throughout %s : check RS length " % (message), cadu_0, (0,)* (max_CADU_length - out_GOODSIZE_frame_len))
    check.equal("TM frame has been propagated throughout %s : check cadu size " % (message), idle_cadu['cadu_size'], out_GOODSIZE_frame_len)
    check.equal("TM frame has been propagated throughout %s : check tm bit rate " % (message), idle_cadu['tm_bit_rate'], res_tm_bit_rate)

def check_no_idle_frame (message, idle_cadu, res_asm_ph_sh, res_tf_df, res_clcw, res_tm_bit_rate ):

    global max_CADU_length, out_GOODSIZE_frame_len, SIZE_asm_ph_sh, SIZE_tf_df, SIZE_clcw, SIZE_rs

    cadu_asm_ph_sh = idle_cadu['cadu'][ 0                                                 :  SIZE_asm_ph_sh]
    cadu_tf_df     = idle_cadu['cadu'][ SIZE_asm_ph_sh                                    : (SIZE_asm_ph_sh + SIZE_tf_df)]
    cadu_clcw      = idle_cadu['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df)                      : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw)]
    cadu_0         = idle_cadu['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs): ]

    check.equal("TM frame has been propagated throughout %s : check ASM, PH, SH " % (message), cadu_asm_ph_sh, res_asm_ph_sh)
    check.equal("TM frame has been propagated throughout %s : check TF DATA FIELD " % (message), cadu_tf_df, res_tf_df)
    check.equal("TM frame has been propagated throughout %s : check CLCW " % (message), cadu_clcw, res_clcw)
    check.equal("TM frame has been propagated throughout %s : check RS length " % (message), cadu_0, (0,)* (max_CADU_length - out_GOODSIZE_frame_len))
    check.equal("TM frame has been propagated throughout %s : check cadu size " % (message), idle_cadu['cadu_size'], out_GOODSIZE_frame_len)
    check.equal("TM frame has been propagated throughout %s : check tm bit rate " % (message), idle_cadu['tm_bit_rate'], res_tm_bit_rate)

def save_simulator( sim ):
    test.do_action( "Saving simulator" )
    sim.SaveSimulator("ctx")
    sim.SaveData("ctx")
    
def restore_simulator(instance_name):
    test.do_action("Creating a new simulator instance and restoring simulator")
    sim2restore = test.new_simulator( instance_name = "MOCK")

    sim2restore.SetTraceFlag(True)
    sim2restore.SetDebugFlag(True)
    sim2restore.SetOverloadLog(True)
    sim2restore.get_logger().SetInformationLog(True)
    sim2restore.get_logger().SetDebugLog(True)
    sim2restore.get_logger().SetWarningLog(True)
    sim2restore.get_logger().SetErrorLog(True)
    
    sim2restore.RestoreSimulator("ctx")
    sim2restore.RestoreData("ctx")

    # connect_callpoint_to_function
    sim2restore.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_CH1" % (instance_name) , tm_frame_routine_ch1 )
    sim2restore.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_CH2" % (instance_name) , tm_frame_routine_ch2 )
    sim2restore.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_AUX" % (instance_name) , tm_frame_routine_aux )
    sim2restore.ConnectCallPointToFunction("%s.callpoint.TM_FRAME_OUT_TO_TME2" % (instance_name) , tm_frame_routine_tme2 )
   
    return sim2restore

# Time measurment
class Time_Measurment() :
    
    _test = None
    _max_time = 0
    _enter_time = 0
    
    def __init__(self, max_time, test ):
        self._max_time = max_time
        self._test = test

    def __enter__(self):
        self._test.do_action( "Starting monitoring time (max time = %.20f s)" % (self._max_time) )
        self._enter_time = time.time()
        
    def __exit__(self, *args ):
        elapsed_time = time.time() - self._enter_time
        self._test.new_check("").equal("Check elapsed time %.20f s =< %.20f s" % (elapsed_time,self._max_time), self._max_time - elapsed_time >= 0 , True)

MILLISECOND = 0.5
with vt.test.Test(accept_error=True) as test: 

     # Test
     with test.new_subtest( "[TEST_001] Test RTM_SCHEDULING activation routine" ):
         with Time_Measurment(MILLISECOND,test) as time_measurment:    
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "SCSIM-SRS_TME2-DES-008",
                "SCSIM-SRS_TME2-IF-010",
                "SCSIM-SRS_TME2-IF-011",
                "SCSIM-SRS_TME2-IF-012",
                "SCSIM-SRS_TME2-IF-013",
                "SCSIM-SRS_TME2-IF-014",
                "SCSIM-SRS_TME2-DISC-040"] )
                        
             sim = init_TME2("K2_SMU_TME2")
             
             #expected value
             NULL_SEC_HEADER_DATA_FIELD = (0,) * 63;

             with test.new_check("Values at initialization. Create and Initialize TME2 Model than check initial values") as check:
                 check_feature_with_constant("K2_SMU_TME2","debug_level",0, sim)
                 check_feature_with_constant("K2_SMU_TME2","RTS_IDENTIFIER",0, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_MIN_VOLTAGE",2.1, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_SEC_VOLTAGE_OFF",0, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_SEC_VOLTAGE_ON",3.3, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_OFF_TEMP",273.15, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_ON_TEMP",293.15, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_ON_CONSUMPTION",1.57, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_OFF_CONSUMPTION",0, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_ON_DISSIPATION",1.57, sim)
                 check_feature_with_constant("K2_SMU_TME2","TME2_OFF_DISSIPATION",0, sim)
                 check_feature_with_constant("K2_SMU_TME2","FRAME_INPUT_LENGTH_MAX",960, sim)
                 check_feature_with_constant("K2_SMU_TME2","SEC_HEADER_SIZE",34, sim)           
                 check_feature_with_constant("K2_SMU_TME2","DUMMY_PACKET_FIELD",0xE2, sim)           
                 check_state_with_constant("K2_SMU_TME2","TME2_TEMP",0, sim)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",False, sim)
                 check_state_with_constant("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE",0, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",False, sim)
                 check_state_with_constant("K2_SMU_TME2","TME2_DISSIPATION",0, sim)
                 check_state_with_constant("K2_SMU_TME2","SEC_HEADER_VERSION",0, sim)
                 check_state_with_constant("K2_SMU_TME2","SEC_HEADER_DATA_FIELD",NULL_SEC_HEADER_DATA_FIELD, sim)
                 check_state_with_constant("K2_SMU_TME2","TME2_CONSUMPTION",0, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",0, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",0, sim)
                 check_state_with_constant("K2_SMU_TME2","IDLE_FRAME",1, sim)
                 check_output_with_constant("K2_SMU_TME2","TME2_DISSIPATION",0, sim )
                
             with test.new_check("Set TME2 Power On. Set TME2_STATUS state to True and call RTM_SCHEDULING activation routine, than check states and output") as check:
                 set_state(sim, "K2_SMU_TME2","TME2_STATUS",True)
                 call_activation_routine(sim, "K2_SMU_TME2","RTM_SCHEDULING", (sim["%s.feature.RTS_IDENTIFIER" % ("K2_SMU_TME2")],STANDARD_SCHED,0))
                 check_state_with_feature("K2_SMU_TME2","TME2_CONSUMPTION", "TME2_ON_CONSUMPTION")
                 check_state_with_feature("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE", "TME2_SEC_VOLTAGE_ON")
                 check_state_with_feature("K2_SMU_TME2","TME2_TEMP", "TME2_ON_TEMP")
                 check_state_with_feature("K2_SMU_TME2","TME2_DISSIPATION", "TME2_ON_DISSIPATION")
                 check_output_with_state("K2_SMU_TME2","TME2_DISSIPATION","TME2_DISSIPATION")

             with test.new_check("Set TME2 Power Off. Set TME2_STATUS state to False and call RTM_SCHEDULING activation routine, than check states and output") as check:
                 set_state(sim, "K2_SMU_TME2","TME2_STATUS",False)
                 call_activation_routine(sim, "K2_SMU_TME2","RTM_SCHEDULING", (sim["%s.feature.RTS_IDENTIFIER" % ("K2_SMU_TME2")],STANDARD_SCHED,0))
                 check_state_with_feature("K2_SMU_TME2","TME2_CONSUMPTION", "TME2_OFF_CONSUMPTION")
                 check_state_with_feature("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE", "TME2_SEC_VOLTAGE_OFF")
                 check_state_with_feature("K2_SMU_TME2","TME2_TEMP", "TME2_OFF_TEMP")
                 check_state_with_feature("K2_SMU_TME2","TME2_DISSIPATION", "TME2_OFF_DISSIPATION")
                 check_output_with_state("K2_SMU_TME2","TME2_DISSIPATION","TME2_DISSIPATION")

     # Test
     with test.new_subtest( "[TEST_002] Test TME2 Power Line ON/OFF" ):
         with Time_Measurment(19 * MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "SCSIM-SRS_TME2-IF-011",
                "SCSIM-SRS_TME2-POW-015",
                "SCSIM-SRS_TME2-POW-016",
                "SCSIM-SRS_TME2-POW-017",
                "SCSIM-SRS_TME2-POW-018",
                "SCSIM-SRS_TME2-HPC-019",
                "SCSIM-SRS_TME2-FRAM-020",
                "SCSIM-SRS_TME2-FRAM-021",
                "SCSIM-SRS_TME2-FRAM-022",
                "SCSIM-SRS_TME2-FRAM-036",
                "SCSIM-SRS_TME2-FRAM-037",
                "SCSIM-SRS_TME2-FRAM-038",
                "SCSIM-SRS_TME2-FRAM-039",
                "SCSIM-SRS_TME2-DISC-040"] )
            
             sim = init_TME2("K2_SMU_TME2")

             from_smu_in_frame  = (1, 2, 3, 4, 5,) * 192 ; # 960
             from_tme2_in_frame = (1,) + (1, 2, 3, 4, 5, 6,) * 213; # 1279
             
             with test.new_check("Power OFF and TME disable: check states, outputs and equipment current") as check:
                 intensity = call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] - 0.01))
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",False, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",False, sim)
                 check_state_with_feature("K2_SMU_TME2","TME2_CONSUMPTION", "TME2_OFF_CONSUMPTION")
                 check_state_with_feature("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE", "TME2_SEC_VOLTAGE_OFF")
                 check_state_with_feature("K2_SMU_TME2","TME2_TEMP", "TME2_OFF_TEMP")
                 check_state_with_feature("K2_SMU_TME2","TME2_DISSIPATION", "TME2_OFF_DISSIPATION")
                 check_output_with_state("K2_SMU_TME2","TME2_DISSIPATION","TME2_DISSIPATION")
                 check.equal("Check equipment intensity = TME2_OFF_CONSUMPTION / VOLTAGE", abs(intensity[0] - sim["K2_SMU_TME2.feature.TME2_OFF_CONSUMPTION"] / (sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"]-0.01) ) < 0.01, True )
                
             with test.new_check("Power OFF and TME disable: call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 in_tm_bit_rate = 8192                
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","from_smu_in_frame",from_smu_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )
                 check.equal("TM frame has not been propagated throughout partner TME2", tm_frame_parameters_tme2,  None )

             with test.new_check("Power OFF and TME disable: call TM_FRAME_IN_FROM_TME2 activation routine") as check:
                 
                 in_tm_bit_rate = 10914
                 call_tm_frame_from_tme2_routine (sim, "K2_SMU_TME2","from_tme2_in_frame",from_tme2_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )

             with test.new_check("Power OFF and TME enable: check states, outputs and equipment current") as check:
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",False, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 
             with test.new_check("Power OFF and TME enable: call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 in_tm_bit_rate = 8192                
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","from_smu_in_frame",from_smu_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )
                 check.equal("TM frame has not been propagated throughout partner TME2", tm_frame_parameters_tme2,  None )
                 
             with test.new_check("Power OFF and TME enable: call TM_FRAME_IN_FROM_TME2 activation routine") as check:
                 in_tm_bit_rate = 10914
                 call_tm_frame_from_tme2_routine (sim, "K2_SMU_TME2","from_tme2_in_frame",from_tme2_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )

             with test.new_check("Power ON and TME disable: check states, outputs and equipment current") as check:
                 intensity = call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] + 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", False)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",False, sim)
                 check_state_with_feature("K2_SMU_TME2","TME2_CONSUMPTION", "TME2_ON_CONSUMPTION")
                 check_state_with_feature("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE", "TME2_SEC_VOLTAGE_ON")
                 check_state_with_feature("K2_SMU_TME2","TME2_TEMP", "TME2_ON_TEMP")
                 check_state_with_feature("K2_SMU_TME2","TME2_DISSIPATION", "TME2_ON_DISSIPATION")
                 check_output_with_state("K2_SMU_TME2","TME2_DISSIPATION","TME2_DISSIPATION")
                 check.equal("Check equipment intensity = TME2_ON_CONSUMPTION / VOLTAGE", abs(intensity[0] - sim["K2_SMU_TME2.feature.TME2_ON_CONSUMPTION"] / (sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"]-0.01) ) < 0.01, True )
                
             with test.new_check("Power ON and TME disable: call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 in_tm_bit_rate = 8192
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","from_smu_in_frame",from_smu_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )
                 check.equal("TM frame has not been propagated throughout partner TME2", tm_frame_parameters_tme2,  None )
                 
             with test.new_check("Power ON and TME disable: call TM_FRAME_IN_FROM_TME2 activation routine") as check:
                 in_tm_bit_rate = 10914
                 call_tm_frame_from_tme2_routine (sim, "K2_SMU_TME2","from_tme2_in_frame",from_tme2_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux, None );
                 check.equal("TM frame has been propagated throughout channel 1 : cadu", tm_frame_parameters_ch1['cadu'], from_tme2_in_frame + (0,) * (2048-len(from_tme2_in_frame)) );
                 check.equal("TM frame has been propagated throughout channel 1 : cadu_size", tm_frame_parameters_ch1['cadu_size'], len(from_tme2_in_frame) );
                 check.equal("TM frame has been propagated throughout channel 1 : tm_bit_rate", tm_frame_parameters_ch1['tm_bit_rate'], in_tm_bit_rate );
                 check.equal("TM frame has been propagated throughout channel 2", tm_frame_parameters_ch2, tm_frame_parameters_ch1 );
                 tm_frame_parameters_ch1 = None;
                 tm_frame_parameters_ch2 = None;

             with test.new_check("Power ON and TME enable: check states, outputs and equipment current") as check:
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 
             with test.new_check("Power ON and TME enable: call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 in_tm_bit_rate = 8192
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","from_smu_in_frame",from_smu_in_frame)
                 check.not_equal("TM frame has been propagated throughout auxiliary channel", tm_frame_parameters_aux, None );
                 check.not_equal("TM frame has been propagated throughout channel 1", tm_frame_parameters_ch1, None );
                 check.not_equal("TM frame has been propagated throughout channel 2", tm_frame_parameters_ch2, None );
                 check.not_equal("TM frame has been propagated throughout partner TME2", tm_frame_parameters_tme2,  None )
                 tm_frame_parameters_aux = None;
                 tm_frame_parameters_ch1 = None;
                 tm_frame_parameters_ch2 = None;
                 tm_frame_parameters_tme2 = None;
                 
             with test.new_check("Power ON and TME enable: call TM_FRAME_IN_FROM_TME2 activation routine") as check:
                 in_tm_bit_rate = 10914
                 call_tm_frame_from_tme2_routine (sim, "K2_SMU_TME2","from_tme2_in_frame",from_tme2_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux, None );
                 check.equal("TM frame has been propagated throughout channel 1 : cadu", tm_frame_parameters_ch1['cadu'], from_tme2_in_frame + (0,) * (2048-len(from_tme2_in_frame)) );
                 check.equal("TM frame has been propagated throughout channel 1 : cadu_size", tm_frame_parameters_ch1['cadu_size'], len(from_tme2_in_frame) );
                 check.equal("TM frame has been propagated throughout channel 1 : tm_bit_rate", tm_frame_parameters_ch1['tm_bit_rate'], in_tm_bit_rate );
                 check.equal("TM frame has been propagated throughout channel 2", tm_frame_parameters_ch2, tm_frame_parameters_ch1 );
                 tm_frame_parameters_ch1 = None;
                 tm_frame_parameters_ch2 = None;

             with test.new_check("Power OFF and TME disable: check states, outputs and equipment current") as check:
                 intensity = call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] - 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", False)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",False, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",False, sim)
                 check_state_with_feature("K2_SMU_TME2","TME2_CONSUMPTION", "TME2_OFF_CONSUMPTION")
                 check_state_with_feature("K2_SMU_TME2","TME2_SECONDARY_VOLTAGE", "TME2_SEC_VOLTAGE_OFF")
                 check_state_with_feature("K2_SMU_TME2","TME2_TEMP", "TME2_OFF_TEMP")
                 check_state_with_feature("K2_SMU_TME2","TME2_DISSIPATION", "TME2_OFF_DISSIPATION")
                 check_output_with_state("K2_SMU_TME2","TME2_DISSIPATION","TME2_DISSIPATION")
                 check.equal("Check equipment intensity = TME2_OFF_CONSUMPTION / VOLTAGE", abs(intensity[0] - sim["K2_SMU_TME2.feature.TME2_OFF_CONSUMPTION"] / (sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"]-0.01) ) < 0.01, True )
                
             with test.new_check("Power OFF and TME disable: call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 in_tm_bit_rate = 8192
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","from_smu_in_frame",from_smu_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )
                 check.equal("TM frame has not been propagated throughout partner TME2", tm_frame_parameters_tme2,  None )
                 
             with test.new_check("Power OFF and TME disable: call TM_FRAME_IN_FROM_TME2 activation routine") as check:
                 in_tm_bit_rate = 10914
                 call_tm_frame_from_tme2_routine (sim, "K2_SMU_TME2","from_tme2_in_frame",from_tme2_in_frame)
                 check.equal("TM frame has not been propagated throughout auxiliary channel", tm_frame_parameters_aux,  None )
                 check.equal("TM frame has not been propagated throughout channel 1", tm_frame_parameters_ch1,  None )
                 check.equal("TM frame has not been propagated throughout channel 2", tm_frame_parameters_ch2,  None )

     # Test
     with test.new_subtest( "[TEST_003] Test TM_FRAME_IN_FROM_SMU routine, check Generated frame Counter and Dummy packet Counter increment and reset" ):
         with Time_Measurment(12*MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "STEP2-SRD-TME2-010",
                "STEP2-SRD-TME2-011",
                "STEP2-SRD-TME2-013",
                "STEP2-SRD-TME2-015",] )
            
             sim = init_TME2("K2_SMU_TME2") 
            
             # frame length
             in_OVERSIZE_frame_len = 961;

             # frame bit_rate
             in_tm_bit_rate = 8192

             # frame composition :ASM
             ASM_pattern = (26, 207, 252, 29);
             # frame composition :Primary Header
             in_PH_idle_frame = (53, 102, 1, 4, 31, 254);
             in_PH_fhp_0_frame = (53, 102, 1, 1, 24, 0);
             in_PH_fhp_not0_frame = (53, 102, 1, 5, 24, 18);
             in_PH_error_frame = (53, 102, 1, 2, 31, 255);
             # frame composition : Data Field
             in_DF_idle_frame = (1,) * 946;
             in_DF_noidle_frame = (21,) + (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                              33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62) * 15; 
             # frame composition : Communications Link Control Word
             CLCW_pattern = (1, 60, 192, 0);

             # input frame:
             in_IDLE_frame =  ASM_pattern + in_PH_idle_frame + in_DF_idle_frame + CLCW_pattern;
             in_ERROR_frame =  ASM_pattern + in_PH_error_frame + in_DF_noidle_frame + CLCW_pattern;
             in_FHP_0_frame =  ASM_pattern + in_PH_fhp_0_frame + in_DF_noidle_frame + CLCW_pattern;
             in_FHP_not0_frame = ASM_pattern + in_PH_fhp_not0_frame + in_DF_noidle_frame + CLCW_pattern;          
             in_OVERSIZE_frame = (1,) * in_OVERSIZE_frame_len

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an idle frame") as check:
                 call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] + 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_IDLE_frame",in_IDLE_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",1, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",0, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine sending a valid frame with FHP equal to 0") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",2, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",1, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an error frame") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_ERROR_frame",in_ERROR_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",3, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",2, sim)
 
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an idle frame") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_IDLE_frame",in_IDLE_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",4, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",2, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an OVERSIZE frame") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_OVERSIZE_frame",in_OVERSIZE_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",4, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",2, sim)
                 
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine sending a valid frame with FHP different from 0") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_not0_frame",in_FHP_not0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",5, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",3, sim)
                 
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine to check Generated frame Counter reset") as check:
                 MOD32_COUNT_MAX = 2**31 -1 
                 set_state(sim, "K2_SMU_TME2", "DUMMY_COUNTER_FRAME", MOD32_COUNT_MAX)
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",0, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",4, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine after Generated frame Counter reset") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",1, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",5, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine to check Dummy Packet Counter reset") as check:
                 MOD32_COUNT_MAX = 2**31 -1 
                 set_state(sim, "K2_SMU_TME2", "DUMMY_COUNTER_DPACKET", MOD32_COUNT_MAX)
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",2, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",0, sim)
                
             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine after Dummy Packet Counter reset") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_FRAME",3, sim)
                 check_state_with_constant("K2_SMU_TME2","DUMMY_COUNTER_DPACKET",1, sim)
                 tm_frame_parameters_aux = None

     # Test
     with test.new_subtest( "[TEST_004] Test TM_FRAME_IN_FROM_SMU routine, the incoming frame is an idle frame" ):
         with Time_Measurment(6*MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "SCSIM-SRS_TME2-FRAM-023",
                "SCSIM-SRS_TME2-FRAM-026", 
                "SCSIM-SRS_TME2-FRAM-027", 
                "SCSIM-SRS_TME2-FRAM-028", 
                "SCSIM-SRS_TME2-FRAM-029", 
                "SCSIM-SRS_TME2-FRAM-030", 
                "SCSIM-SRS_TME2-FRAM-031", 
                "SCSIM-SRS_TME2-FRAM-032", 
                "SCSIM-SRS_TME2-FRAM-041",] )
            
             sim = init_TME2("K2_SMU_TME2") 
            
             # frame length
             in_OVERSIZE_frame_len = 961;
             in_GOODSIZE_frame_len = 960;
             out_GOODSIZE_frame_len = 1279
             max_CADU_length = 2048
            
             SIZE_asm_ph_sh = 44
             SIZE_tf_df     = 1071
             SIZE_clcw      = 4
             SIZE_rs        = 160

             # frame bit_rate
             in_tm_bit_rate = 8192
             out_tm_bit_rate = int(in_tm_bit_rate * out_GOODSIZE_frame_len / in_GOODSIZE_frame_len)

             # frame composition :ASM
             ASM_pattern = (26, 207, 252, 29);
             # frame composition :Primary Header
             in_PH_idle_frame = (53, 102, 1, 4, 31, 254);
             out_PH_idle_frame = (53, 103, 1, 4, 159, 254);
             in_PH_idle_frame_VC0 = (53, 102, 1, 0, 31, 254);
             out_PH_idle_frame_VC0 = (53, 103, 1, 0, 159, 254);
             # frame composition : Secondary Header
             default_SH = (33,) + (0,) * 33;
             # frame composition : Data Field
             in_DF_idle_frame = (1,) * 946;
             # frame composition : Communications Link Control Word
             CLCW_pattern = (1, 60, 192, 0);

             # input frame:
             in_OVERSIZE_frame = (1,) * in_OVERSIZE_frame_len
             in_IDLE_frame =  ASM_pattern + in_PH_idle_frame + in_DF_idle_frame + CLCW_pattern;
             in_IDLE_frame_VC0 =  ASM_pattern + in_PH_idle_frame_VC0 + in_DF_idle_frame + CLCW_pattern;

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an incoming OVERSIZE frame") as check:
                 call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] + 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_OVERSIZE_frame",in_OVERSIZE_frame)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 check.equal("TM frame has not been propagated ", tm_frame_parameters_aux,  None );

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an incoming idle frame") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_IDLE_frame",in_IDLE_frame)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 check_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_idle_frame  + default_SH, CLCW_pattern, out_tm_bit_rate)
                 idle1_tf = tm_frame_parameters_aux['cadu'][ SIZE_asm_ph_sh                           : (SIZE_asm_ph_sh + SIZE_tf_df)]
                 idle1_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 tm_frame_parameters_aux = None

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an idle frame for the second time") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_IDLE_frame",in_IDLE_frame)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 check_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_idle_frame  + default_SH, CLCW_pattern, out_tm_bit_rate)
                 idle2_tf = tm_frame_parameters_aux['cadu'][ SIZE_asm_ph_sh                           : (SIZE_asm_ph_sh + SIZE_tf_df)]
                 idle2_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 check.not_equal("Transfer Frame Data Field of TM idle frame 1 differs from Transfer Frame Data Field of output idle frame 2", idle1_tf, idle2_tf );
                 check.not_equal("Reed Solomon code of TM idle frame 1 differs from Reed Solomon code of output idle frame 2", idle1_RS, idle2_RS );
                 tm_frame_parameters_aux = None
                                                                                         

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine with an idle frame, VC counter has been restarted") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_IDLE_frame_VC0",in_IDLE_frame_VC0)
                 check_state_with_constant("K2_SMU_TME2","TME2_STATUS",True, sim)
                 check_state_with_constant("K2_SMU_TME2","TME_ENABLE",True, sim)
                 check_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_idle_frame_VC0  + default_SH, CLCW_pattern, out_tm_bit_rate)
                 idle3_tf = tm_frame_parameters_aux['cadu'][ SIZE_asm_ph_sh                           : (SIZE_asm_ph_sh + SIZE_tf_df)]
                 idle3_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 check.equal("Transfer Frame Data Field of output  idle frame3 is equal to Transfer Frame Data Field of output  idle frame 1", idle3_tf, idle1_tf );
                 check.not_equal("Reed Solomon code of output  idle frame 3 differs from Reed Solomon code of output  idle frame 1", idle3_RS, idle1_RS );
                 tm_frame_parameters_aux = None

     # Test
     with test.new_subtest( "[TEST_005] Test TM_FRAME_IN_FROM_SMU routine, the incoming frame is not an idle frame" ):
         with Time_Measurment(5*MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "STEP2-SRD-TME2-010",
                "STEP2-SRD-TME2-011",
                "STEP2-SRD-TME2-013",
                "STEP2-SRD-TME2-015",] )
            
             sim = init_TME2("K2_SMU_TME2") 
            
             # frame length
             in_GOODSIZE_frame_len = 960;
             out_GOODSIZE_frame_len = 1279
             max_CADU_length = 2048
            
             SIZE_asm_ph_sh = 44
             SIZE_tf_df     = 1071
             SIZE_clcw      = 4
             SIZE_rs        = 160

             # frame bit_rate
             in_tm_bit_rate = 8192
             out_tm_bit_rate = int(in_tm_bit_rate * out_GOODSIZE_frame_len / in_GOODSIZE_frame_len)

             # frame composition :ASM
             ASM_pattern = (26, 207, 252, 29);
             # frame composition :Primary Header
             fhp_not0 = 18;
             in_PH_fhp_0_frame = (53, 102, 1, 1, 24, 0);
             out_PH_fhp_0_frame = (53, 103, 1, 1, 152, 0);
             in_PH_fhp_not0_frame = (53, 102, 1, 2, 24, fhp_not0);
             out_PH_fhp_not0_frame = (53, 103, 1, 2, 152, fhp_not0);
             in_PH_error_frame = (53, 102, 1, 5, 31, 255);
             out_PH_error_frame = (53, 103, 1, 5, 159, 255);
             # frame composition : Secondary Header
             default_SH = (33,) + (0,) * 33;
             # frame composition : Data Field
             in_DF_noidle_frame = (21,) + (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                              33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62) * 15; 
             # frame composition : Dummy Packet
             dummy_pkg_1 = (3, 239,192, 0, 0, 118, 0, 0, 0, 1, 0, 0, 0, 1) + (226,)*111;
             dummy_pkg_2 = (3, 239,192, 0, 0, 118, 0, 0, 0, 2, 0, 0, 0, 2) + (226,)*111;
             dummy_pkg_3 = (3, 239,192, 0, 0, 118, 0, 0, 0, 3, 0, 0, 0, 3) + (226,)*111;
             # frame composition : Communications Link Control Word
             CLCW_pattern = (1, 60, 192, 0);

             # input frame:
             in_ERROR_frame =  ASM_pattern + in_PH_error_frame + in_DF_noidle_frame + CLCW_pattern;
             in_FHP_0_frame =  ASM_pattern + in_PH_fhp_0_frame + in_DF_noidle_frame + CLCW_pattern;
             in_FHP_not0_frame = ASM_pattern + in_PH_fhp_not0_frame + in_DF_noidle_frame + CLCW_pattern;          

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine sending a valid frame with FHP equal to 0 ") as check:
                 call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] + 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_no_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_fhp_0_frame  + default_SH, dummy_pkg_1 + in_DF_noidle_frame , CLCW_pattern, out_tm_bit_rate)
                 fhp_0_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 tm_frame_parameters_aux = None

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine sending a valid frame with FHP different from 0 ") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_not0_frame",in_FHP_not0_frame)
                 check_no_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_fhp_not0_frame  + default_SH, in_DF_noidle_frame[:18] + dummy_pkg_2 + in_DF_noidle_frame[18:] , CLCW_pattern, out_tm_bit_rate)
                 fhp_not0_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 check.not_equal("Reed Solomon code of TM frame with fhp = 0  differs from TM frame with fhp != 0 ", fhp_0_RS, fhp_not0_RS );
                 tm_frame_parameters_aux = None

             with test.new_check("Call TM_FRAME_IN_FROM_SMU activation routine sending an error frame") as check:
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_ERROR_frame",in_ERROR_frame)
                 check_no_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_error_frame + default_SH, in_DF_noidle_frame + dummy_pkg_3 , CLCW_pattern, out_tm_bit_rate)
                 fhp_error_RS = tm_frame_parameters_aux['cadu'][(SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw) : (SIZE_asm_ph_sh + SIZE_tf_df + SIZE_clcw + SIZE_rs)]
                 check.not_equal("Reed Solomon code of TM error frame differs from TM frame with fhp != 0 ", fhp_error_RS, fhp_not0_RS );
                 tm_frame_parameters_aux = None

     # Test
     with test.new_subtest( "[TEST_006] Test TM_FRAME_IN_FROM_SMU routine , secondary header use" ):
         with Time_Measurment(3*MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "SCSIM-SRS_TME2-FRAM-030"] )
            
             sim = init_TME2("K2_SMU_TME2") 
            
             # frame length
             in_GOODSIZE_frame_len = 960;
             out_GOODSIZE_frame_len = 1279
             max_CADU_length = 2048
             max_SEC_HEADER_DATA_FIELD_length = 64;
            
             SIZE_asm_ph_sh = 44
             SIZE_tf_df     = 1071
             SIZE_clcw      = 4
             SIZE_rs        = 160

             # frame bit_rate
             in_tm_bit_rate = 8192
             out_tm_bit_rate = int(in_tm_bit_rate * out_GOODSIZE_frame_len / in_GOODSIZE_frame_len)

             # frame composition :ASM
             ASM_pattern = (26, 207, 252, 29);
             # frame composition :Primary Header
             in_PH_fhp_0_frame = (53, 102, 1, 1, 24, 0);
             out_PH_fhp_0_frame = (53, 103, 1, 1, 152, 0);
             # frame composition : Secondary Header
             modify_DF_SH = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33);
             modify_SH = (225,) + modify_DF_SH;   #mod->state->SEC_HEADER_VERSION = 3
             # frame composition : Data Field
             in_DF_noidle_frame = (21,) + (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                              33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62) * 15; 
             # frame composition : Dummy Packet
             dummy_pkg_1 = (3, 239,192, 0, 0, 118, 0, 0, 0, 1, 0, 0, 0, 1) + (226,)*111;
             # frame composition : Communications Link Control Word
             CLCW_pattern = (1, 60, 192, 0);

             # input frame:
             in_FHP_0_frame =  ASM_pattern + in_PH_fhp_0_frame + in_DF_noidle_frame + CLCW_pattern;

             with test.new_check("Modify the states related to the Secondary Header and call TM_FRAME_IN_FROM_SMU activation routine") as check:
                 call_activation_routine(sim, "K2_SMU_TME2","TME2_POWER_3_3V", (True,sim["K2_SMU_TME2.feature.TME2_MIN_VOLTAGE"] + 0.01))
                 call_activation_routine(sim, "K2_SMU_TME2", "TME_ENABLE", True)
                 set_state(sim, "K2_SMU_TME2", "SEC_HEADER_VERSION",3)
                 set_state(sim, "K2_SMU_TME2", "SEC_HEADER_DATA_FIELD", modify_DF_SH + (0,) * (max_SEC_HEADER_DATA_FIELD_length - len(modify_DF_SH) -1))
                 call_tm_frame_from_smu_routine (sim, "K2_SMU_TME2","in_FHP_0_frame",in_FHP_0_frame)
                 check_no_idle_frame("auxiliary channel", tm_frame_parameters_aux, ASM_pattern + out_PH_fhp_0_frame  + modify_SH, dummy_pkg_1 + in_DF_noidle_frame , CLCW_pattern, out_tm_bit_rate)
                 tm_frame_parameters_aux = None

    # Test
     with test.new_subtest( "[TEST_007] Test Save/Restore" ):
         with Time_Measurment(6*MILLISECOND,test) as time_measurment:
             document( "TME 2 Model Specification for simulators",
               "200849534K",
               "01")
            
             requirement( [ "SCSIM-SRS_TME2-DES-003",
                "SCSIM-SRS_TME2-DES-004"] )
            
             sim2save = init_TME2("K2_SMU_TME2_SAVE") 

             # frame bit_rate
             in_tm_bit_rate = 8192
             max_SEC_HEADER_DATA_FIELD_length = 64;
            
             # frame composition :ASM
             ASM_pattern = (26, 207, 252, 29);
             # frame composition :Primary Header
             in_PH_idle_frame = (53, 102, 1, 4, 31, 254);
             in_PH_fhp_0_frame = (53, 102, 1, 1, 24, 0);
             # frame composition : Secondary Header
             modify_DF_SH = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33);
             # frame composition : Data Field
             in_DF_idle_frame = (1,) * 946;
             in_DF_noidle_frame = (21,) + (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 
                              33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62) * 15; 
             # frame composition : Communications Link Control Word
             CLCW_pattern = (1, 60, 192, 0);

             # input frame:
             in_FHP_0_frame =  ASM_pattern + in_PH_fhp_0_frame + in_DF_noidle_frame + CLCW_pattern;
             in_IDLE_frame =  ASM_pattern + in_PH_idle_frame + in_DF_idle_frame + CLCW_pattern;
             
             test.do_action("Put the model in a significant state, then save the context")
             call_activation_routine(sim2save, "K2_SMU_TME2_SAVE","TME2_POWER_3_3V", (True,sim2save["K2_SMU_TME2_SAVE.feature.TME2_MIN_VOLTAGE"] + 0.01))
             call_activation_routine(sim2save, "K2_SMU_TME2_SAVE","TME_ENABLE", True)
             
             call_tm_frame_from_smu_routine (sim2save, "K2_SMU_TME2_SAVE","in_FHP_0_frame",in_FHP_0_frame)
             call_tm_frame_from_smu_routine (sim2save, "K2_SMU_TME2_SAVE","in_IDLE_frame",in_IDLE_frame)
             
             set_state(sim2save, "K2_SMU_TME2_SAVE", "SEC_HEADER_VERSION",3)
             set_state(sim2save, "K2_SMU_TME2_SAVE", "SEC_HEADER_DATA_FIELD", modify_DF_SH + (0,) * (max_SEC_HEADER_DATA_FIELD_length - len(modify_DF_SH) -1))
              
             # save reference values 1
             REF_1__DEBUG_LEV = sim2save["K2_SMU_TME2_SAVE.feature.debug_level"]
             REF_1__RTS_IDENTIFIER = sim2save["K2_SMU_TME2_SAVE.feature.RTS_IDENTIFIER"]
             REF_1__MIN_VOLTAGE = sim2save["K2_SMU_TME2_SAVE.feature.TME2_MIN_VOLTAGE"]
             REF_1__SEC_VOLTAGE_OFF = sim2save["K2_SMU_TME2_SAVE.feature.TME2_SEC_VOLTAGE_OFF"]
             REF_1__SEC_VOLTAGE_ON = sim2save["K2_SMU_TME2_SAVE.feature.TME2_SEC_VOLTAGE_ON"]
             REF_1__TEMP_OFF = sim2save["K2_SMU_TME2_SAVE.feature.TME2_OFF_TEMP"]
             REF_1__TEMP_ON = sim2save["K2_SMU_TME2_SAVE.feature.TME2_ON_TEMP"]
             REF_1__CONSUMPTION_ON = sim2save["K2_SMU_TME2_SAVE.feature.TME2_ON_CONSUMPTION"]
             REF_1__CONSUMPTION_OFF = sim2save["K2_SMU_TME2_SAVE.feature.TME2_OFF_CONSUMPTION"]
             REF_1__DISSIPATION_ON = sim2save["K2_SMU_TME2_SAVE.feature.TME2_ON_DISSIPATION"]
             REF_1__DISSIPATION_OFF = sim2save["K2_SMU_TME2_SAVE.feature.TME2_OFF_DISSIPATION"]
             REF_1__FRAME_INP_LEN_MAX = sim2save["K2_SMU_TME2_SAVE.feature.FRAME_INPUT_LENGTH_MAX"]
             REF_1__SH_SIZE = sim2save["K2_SMU_TME2_SAVE.feature.SEC_HEADER_SIZE"]
             REF_1__DUMMY_PACKET_FIELD = sim2save["K2_SMU_TME2_SAVE.feature.DUMMY_PACKET_FIELD"]
             REF_1__TEMP = sim2save["K2_SMU_TME2_SAVE.state.TME2_TEMP"]
             REF_1__STATUS = sim2save["K2_SMU_TME2_SAVE.state.TME2_STATUS"]
             REF_1__SECONDARY_VOLTAGE = sim2save["K2_SMU_TME2_SAVE.state.TME2_SECONDARY_VOLTAGE"]
             REF_1__CONSUMPTION = sim2save["K2_SMU_TME2_SAVE.state.TME2_CONSUMPTION"]
             REF_1__DISSIPATION_STA = sim2save["K2_SMU_TME2_SAVE.state.TME2_DISSIPATION"]
             REF_1__ENABLE = sim2save["K2_SMU_TME2_SAVE.state.TME_ENABLE"]
             REF_1__SH_VERSION = sim2save["K2_SMU_TME2_SAVE.state.SEC_HEADER_VERSION"]
             REF_1__SH_DATA_FIELD = sim2save["K2_SMU_TME2_SAVE.state.SEC_HEADER_DATA_FIELD"]
             REF_1__DUMMY_COUNTER_FRAME = sim2save["K2_SMU_TME2_SAVE.state.DUMMY_COUNTER_FRAME"]
             REF_1__DUMMY_COUNTER_DPACKET = sim2save["K2_SMU_TME2_SAVE.state.DUMMY_COUNTER_DPACKET"]
             REF_1__IDLE_FRAME = sim2save["K2_SMU_TME2_SAVE.state.IDLE_FRAME"]
             REF_1__DISSIPATION_OUT = sim2save["K2_SMU_TME2_SAVE.output.TME2_DISSIPATION"]
             
             save_simulator(sim2save)
             
             test.do_action("Continue simulation after freeze action")
             call_tm_frame_from_smu_routine (sim2save, "K2_SMU_TME2_SAVE","in_FHP_0_frame",in_FHP_0_frame)
             REF__out_trame_1 = tm_frame_parameters_aux
             tm_frame_parameters_aux = None

             with test.new_check("Execute unfreeze action") as check:
                 sim2restore = restore_simulator("K2_SMU_TME2_SAVE")
                 check_feature_with_constant("K2_SMU_TME2_SAVE","debug_level", REF_1__DEBUG_LEV, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","RTS_IDENTIFIER", REF_1__RTS_IDENTIFIER, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_MIN_VOLTAGE", REF_1__MIN_VOLTAGE, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_SEC_VOLTAGE_OFF", REF_1__SEC_VOLTAGE_OFF, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_SEC_VOLTAGE_ON", REF_1__SEC_VOLTAGE_ON, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_OFF_TEMP", REF_1__TEMP_OFF, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_ON_TEMP", REF_1__TEMP_ON, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_ON_CONSUMPTION", REF_1__CONSUMPTION_ON, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_OFF_CONSUMPTION", REF_1__CONSUMPTION_OFF, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_ON_DISSIPATION", REF_1__DISSIPATION_ON, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","TME2_OFF_DISSIPATION", REF_1__DISSIPATION_OFF, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","FRAME_INPUT_LENGTH_MAX", REF_1__FRAME_INP_LEN_MAX, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","SEC_HEADER_SIZE", REF_1__SH_SIZE, sim2restore)
                 check_feature_with_constant("K2_SMU_TME2_SAVE","DUMMY_PACKET_FIELD", REF_1__DUMMY_PACKET_FIELD, sim2restore)
                 
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME2_TEMP", REF_1__TEMP , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME2_STATUS", REF_1__STATUS , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME2_SECONDARY_VOLTAGE", REF_1__SECONDARY_VOLTAGE , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME2_CONSUMPTION", REF_1__CONSUMPTION , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME2_DISSIPATION", REF_1__DISSIPATION_STA , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","TME_ENABLE", REF_1__ENABLE , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","SEC_HEADER_VERSION", REF_1__SH_VERSION , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","SEC_HEADER_DATA_FIELD", REF_1__SH_DATA_FIELD , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","DUMMY_COUNTER_FRAME", REF_1__DUMMY_COUNTER_FRAME, sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","DUMMY_COUNTER_DPACKET", REF_1__DUMMY_COUNTER_DPACKET , sim2restore)
                 check_state_with_constant("K2_SMU_TME2_SAVE","IDLE_FRAME", REF_1__IDLE_FRAME , sim2restore)
                 check_output_with_constant("K2_SMU_TME2_SAVE","TME2_DISSIPATION", REF_1__DISSIPATION_OUT , sim2restore)

             with test.new_check("Continue simulation after unfreeze action") as check:
                 call_tm_frame_from_smu_routine(sim2restore, "K2_SMU_TME2_SAVE","in_FHP_0_frame",in_FHP_0_frame)
                 check.equal("TM frame has been propagated , check with reference", tm_frame_parameters_aux, REF__out_trame_1)
                 

