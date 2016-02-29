
/*****************************************************************************
 * K2_TME2                                                 
 *                                                                           
 * IDS_COUNT:                                                                
 * IDS_REFERENCE:                                                            
 * IDS_ISSUE:                                                                
 * IDS_REVISION:                                                                  
 *                    
 *                                                        
 * @file K2_TME2_constants.hpp                                        
 * @remarks Auto-generated from MELODY_CCM model                            
 *****************************************************************************/

#ifndef K2_TME2_CONSTANTS_HPP
#define K2_TME2_CONSTANTS_HPP

namespace K2_TME2
{
	/* String_Record */

	/* Feature_Record */
	const K2::ConstString COMMENT__Feature_Record__debug_level = "Model debug level";
	const K2::ConstString COMMENT__Feature_Record__RTS_IDENTIFIER = "Model identifier used to route the schedule activation";
	const K2::ConstString COMMENT__Feature_Record__TME2_MIN_VOLTAGE = "Minimum voltage to power ON";
	const K2::ConstString UNIT__Feature_Record__TME2_MIN_VOLTAGE = "V";
	const K2::ConstString COMMENT__Feature_Record__TME2_SEC_VOLTAGE_OFF = "Secondary voltage OFF value acquisition voltage";
	const K2::ConstString UNIT__Feature_Record__TME2_SEC_VOLTAGE_OFF = "V";
	const K2::ConstString COMMENT__Feature_Record__TME2_SEC_VOLTAGE_ON = "Secondary voltage ON value acquisition voltage";
	const K2::ConstString UNIT__Feature_Record__TME2_SEC_VOLTAGE_ON = "V";
	const K2::ConstString COMMENT__Feature_Record__TME2_OFF_TEMP = "OFF temperature";
	const K2::ConstString UNIT__Feature_Record__TME2_OFF_TEMP = "K";
	const K2::ConstString COMMENT__Feature_Record__TME2_ON_TEMP = "ON temperature";
	const K2::ConstString UNIT__Feature_Record__TME2_ON_TEMP = "K	";
	const K2::ConstString COMMENT__Feature_Record__TME2_ON_CONSUMPTION = "Power consumption in ON mode";
	const K2::ConstString UNIT__Feature_Record__TME2_ON_CONSUMPTION = "W";
	const K2::ConstString COMMENT__Feature_Record__TME2_OFF_CONSUMPTION = "Power consumption in OFF mode";
	const K2::ConstString UNIT__Feature_Record__TME2_OFF_CONSUMPTION = "W";
	const K2::ConstString COMMENT__Feature_Record__TME2_ON_DISSIPATION = "Dissipation in ON mode";
	const K2::ConstString UNIT__Feature_Record__TME2_ON_DISSIPATION = "W";
	const K2::ConstString COMMENT__Feature_Record__TME2_OFF_DISSIPATION = "Dissipation in OFF mode";
	const K2::ConstString UNIT__Feature_Record__TME2_OFF_DISSIPATION = "W";
	const K2::ConstString COMMENT__Feature_Record__FRAME_INPUT_LENGTH_MAX = "Max input TM frame length";
	const K2::ConstString COMMENT__Feature_Record__SEC_HEADER_SIZE = "Transfer Frame Secondary Header total  length";
	const K2::ConstString COMMENT__Feature_Record__DUMMY_PACKET_FIELD = "Value to insert in the packet data field of a dummy packet";

	/* Shared_Feature_Record */

	/* State_Record */
	const K2::ConstString COMMENT__State_Record__TME2_TEMP = "Temperature Telemetry";
	const K2::ConstString UNIT__State_Record__TME2_TEMP = "K";
	const K2::ConstString COMMENT__State_Record__TME2_STATUS = "ON OFF status";
	const K2::ConstString COMMENT__State_Record__TME2_SECONDARY_VOLTAGE = "Secondary voltage Telemetry";
	const K2::ConstString UNIT__State_Record__TME2_SECONDARY_VOLTAGE = "V";
	const K2::ConstString COMMENT__State_Record__TME2_DISSIPATION = "Dissipation";
	const K2::ConstString UNIT__State_Record__TME2_DISSIPATION = "W";
	const K2::ConstString COMMENT__State_Record__TME_ENABLE = "Telemetry Encoder Interface status of SCTMTC";
	const K2::ConstString COMMENT__State_Record__SEC_HEADER_VERSION = "Valeur sur 2 bits";
	const K2::ConstString COMMENT__State_Record__SEC_HEADER_DATA_FIELD = "Data field value (up to SEC_HEADER_SIZE-1)";
	const K2::ConstString COMMENT__State_Record__TME2_CONSUMPTION = "Power consumption ";
	const K2::ConstString UNIT__State_Record__TME2_CONSUMPTION = "W";
	const K2::ConstString COMMENT__State_Record__DUMMY_COUNTER_FRAME = "Generated frame Counter";
	const K2::ConstString COMMENT__State_Record__DUMMY_COUNTER_DPACKET = "Dummy packet Counter";
	const K2::ConstString COMMENT__State_Record__IDLE_FRAME = "Last Idle value for the pseudo-randomizer computation";

	/* State_Overload_Record */

	/* Input_Record */

	/* Output_Record */
	const K2::ConstString COMMENT__Output_Record__TME2_DISSIPATION = "Dissipation";
	const K2::ConstString UNIT__Output_Record__TME2_DISSIPATION = "W";

	/* CallPoint_Record */
	const K2::ConstString COMMENT__CallPoint_Record__TM_FRAME_OUT_CH1 = "TM frame channel 1";
	const K2::ConstString COMMENT__CallPoint_Record__TM_FRAME_OUT_CH2 = "TM frame channel 2";
	const K2::ConstString COMMENT__CallPoint_Record__TM_FRAME_OUT_AUX = "TM frame auxiliary";
	const K2::ConstString COMMENT__CallPoint_Record__TM_FRAME_OUT_TO_TME2 = "TM frame transmit to partner TME2 model ";

	/* Routine_Record */
	const K2::ConstString COMMENT__Routine_Record__RTM_SCHEDULING = "Bus Routine: RTS scheduling execution";
	const K2::ConstString COMMENT__Routine_Record__TM_FRAME_IN_FROM_SMU = "TM frame received from SMU";
	const K2::ConstString COMMENT__Routine_Record__TM_FRAME_IN_FROM_TME2 = "TM frame from other TME2";
	const K2::ConstString COMMENT__Routine_Record__TME_ENABLE = "Telemetry Encoder Interface relay status of SCTMTC";
	const K2::ConstString COMMENT__Routine_Record__TME2_POWER_3_3V = "TME2 power supply";

	/* Routine_Record */

	/* Algo_Record */
	const K2::ConstString COMMENT__Algo_Record___initialize_internal = "K2 algo '_initialize_internal'";
	const K2::ConstString COMMENT__Algo_Record___finalize_internal = "K2 algo '_finalize_internal'";
	const K2::ConstString COMMENT__Algo_Record___step_zero = "K2 algo '_step_zero'";
	const K2::ConstString COMMENT__Algo_Record___save_context = "K2 algo '_save_context'";
	const K2::ConstString COMMENT__Algo_Record___restore_context = "K2 algo '_restore_context'";
	const K2::ConstString COMMENT__Algo_Record__Update = "Update model's states";
}

#endif

/* End of file K2_TME2_constants.hpp */

