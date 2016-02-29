/*****************************************************************************
 * K2_TME2                                                 
 *                                                                           
 * IDS_COUNT:                                                                
 * IDS_REFERENCE:                                                            
 * IDS_ISSUE:                                                                
 * IDS_REVISION:                                                             
 *                                                                           
 *                 !!! THIS FILE SHALL NOT BE MODIFIED !!!   
 *
 * TME2 is an option of Satellite Management Unit. 
 * TME2 Model will complement the existing SCTMTC Model available in SMU Numerical Model.
 * The main activity of this TME2 Model is to give the capability to simulate the insertion of a secondary frame header of fixed length in the Telemetry Transfer Frame.                    
 *                                                                           
 * @file K2_TME2.hpp                                        
 * @remarks Auto-generated from MELODY_CCM model                            
 *****************************************************************************/

#ifndef K2_TME2__HPP
#define K2_TME2__HPP

/* Default Includes */
/* #include "IModel.hpp"
#include "Input.hpp"
#include "IKernelServices.hpp"
#include "DataOverload.hpp"
#include "DerivedTypes.hpp"

/* Other Includes */

/* #include "SimpleTypes.hpp"
#include "Isis_HighPowerCommand_activation.hpp"
#include "Isis_PowerLine_activation.hpp"
#include "RTM_activation.hpp"
#include "SBDL_TM_activation.hpp"  */ 



// V V V V V V V V V V V V V V V V V V V V V V V V V
// Start of user code : User Addons code

// End of user code
// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

namespace K2_TME2
{
	// V V V V V V V V V V V V V V V V V V V V V V V V V
 	// Start of user code : User Addons code in namespace

 	// End of user code
 	// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

	/* Array Sizes */
	

	/* Types */
	

	/* Model string features */
	struct String_Record
	{
	
		/* String Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : String Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	
	/* Default string feature values */
	const String_Record default_string =
	{
	};
	

	/* Model features */
	struct Feature_Record
	{
		/* Model debug level */
		K2::UInt32 debug_level;
		/* Model identifier used to route the schedule activation */
		K2::UInt16 RTS_IDENTIFIER;
		/* Minimum voltage to power ON */
		K2::Double TME2_MIN_VOLTAGE;
		/* Secondary voltage OFF value acquisition voltage */
		K2::Double TME2_SEC_VOLTAGE_OFF;
		/* Secondary voltage ON value acquisition voltage */
		K2::Double TME2_SEC_VOLTAGE_ON;
		/* OFF temperature */
		K2::Double TME2_OFF_TEMP;
		/* ON temperature */
		K2::Double TME2_ON_TEMP;
		/* Power consumption in ON mode */
		K2::Double TME2_ON_CONSUMPTION;
		/* Power consumption in OFF mode */
		K2::Double TME2_OFF_CONSUMPTION;
		/* Dissipation in ON mode */
		K2::Double TME2_ON_DISSIPATION;
		/* Dissipation in OFF mode */
		K2::Double TME2_OFF_DISSIPATION;
		/* Max input TM frame length */
		K2::UInt16 FRAME_INPUT_LENGTH_MAX;
		/* Transfer Frame Secondary Header total  length */
		K2::UInt16 SEC_HEADER_SIZE;
		/* Value to insert in the packet data field of a dummy packet */
		K2::UInt8 DUMMY_PACKET_FIELD;
	
		/* Feature Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Feature Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Default feature values */
	const Feature_Record default_feature =
	{
		/* Default value of debug_level */
		0,
		/* Default value of RTS_IDENTIFIER */
		0,
		/* Default value of TME2_MIN_VOLTAGE */
		2.1,
		/* Default value of TME2_SEC_VOLTAGE_OFF */
		0,
		/* Default value of TME2_SEC_VOLTAGE_ON */
		3.3,
		/* Default value of TME2_OFF_TEMP */
		273.15,
		/* Default value of TME2_ON_TEMP */
		293.15,
		/* Default value of TME2_ON_CONSUMPTION */
		1.57,
		/* Default value of TME2_OFF_CONSUMPTION */
		0,
		/* Default value of TME2_ON_DISSIPATION */
		1.57,
		/* Default value of TME2_OFF_DISSIPATION */
		0,
		/* Default value of FRAME_INPUT_LENGTH_MAX */
		960,
		/* Default value of SEC_HEADER_SIZE */
		34,
		/* Default value of DUMMY_PACKET_FIELD */
		0xE2
	};
	
	

	/* Model shared features */
	struct Shared_Feature_Record
	{
	
		/* Shared Feature Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Shared Feature Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Model states */
	struct State_Record
	{
		/* Temperature Telemetry */
		K2::Double TME2_TEMP;
		/* ON OFF status */
		K2::Boolean TME2_STATUS;
		/* Secondary voltage Telemetry */
		K2::Double TME2_SECONDARY_VOLTAGE;
		/* Dissipation */
		K2::Double TME2_DISSIPATION;
		/* Telemetry Encoder Interface status of SCTMTC */
		K2::Boolean TME_ENABLE;
		/* Valeur sur 2 bits */
		K2::UInt16 SEC_HEADER_VERSION;
		/* Data field value (up to SEC_HEADER_SIZE-1) */
		K2::UInt8 SEC_HEADER_DATA_FIELD[63];
		/* Power consumption */
		K2::Double TME2_CONSUMPTION;
		/* Generated frame Counter */
		K2::UInt32 DUMMY_COUNTER_FRAME;
		/* Dummy packet Counter */
		K2::UInt32 DUMMY_COUNTER_DPACKET;
		/* Last Idle value for the pseudo-randomizer computation */
		K2::UInt16 IDLE_FRAME;
	
		/* State Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : State Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Default state values */
	const State_Record default_state =
	{
		/* Default value of TME2_TEMP */
		0,
		/* Default value of TME2_STATUS */
		false,
		/* Default value of TME2_SECONDARY_VOLTAGE */
		0,
		/* Default value of TME2_DISSIPATION */
		0,
		/* Default value of TME_ENABLE */
		0,
		/* Default value of SEC_HEADER_VERSION */
		0,
		/* Default value of SEC_HEADER_DATA_FIELD */
		{0},
		/* Default value of TME2_CONSUMPTION */
		0,
		/* Default value of DUMMY_COUNTER_FRAME */
		0,
		/* Default value of DUMMY_COUNTER_DPACKET */
		0,
		/* Default value of IDLE_FRAME */
		1
	};
	

	/* Model states overloads */
	struct State_Overload_Record
	{
	
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : State Overload Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Default state overloads values */
	const State_Overload_Record default_state_overload =
	{
	};
	

	/* Model inputs */
	struct Input_Record
	{
	
		/* Input Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Input Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};

	/* Model outputs */
	struct Output_Record
	{
		/* Dissipation */
		K2::Double TME2_DISSIPATION;
	
		/* Output Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Output Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Default output values */
	const Output_Record default_output =
	{
		/* Default value of TME2_DISSIPATION */
		0
	};
	

    #ifdef SWIG
    struct Internal_Record {};
    #else
    struct Internal_Record;
    #endif

	/* Model Call Points */
	struct CallPoint_Record
	{
		/* TM frame channel 1 */
		SBDL_TM_activation::ACP * TM_FRAME_OUT_CH1;
		/* TM frame channel 2 */
		SBDL_TM_activation::ACP * TM_FRAME_OUT_CH2;
		/* TM frame auxiliary */
		SBDL_TM_activation::ACP * TM_FRAME_OUT_AUX;
		/* TM frame transmit to partner TME2 model */
		SBDL_TM_activation::ACP * TM_FRAME_OUT_TO_TME2;
	
		/* Callpoint Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Callpoint Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};
	
	/* Model Routines */
	struct Routine_Record
	{
		/* Bus Routine: RTS scheduling execution */
		RTM_activation::AR * RTM_SCHEDULING;
		/* TM frame received from SMU */
		SBDL_TM_activation::AR * TM_FRAME_IN_FROM_SMU;
		/* TM frame from other TME2 */
		SBDL_TM_activation::AR * TM_FRAME_IN_FROM_TME2;
		/* Telemetry Encoder Interface relay status of SCTMTC */
		Isis_HighPowerCommand_activation::AR * TME_ENABLE;
		/* TME2 power supply */
		Isis_PowerLine_activation::AR * TME2_POWER_3_3V;
	
		/* Routine Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Routine Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};

	/* Model Algorithms */
	struct Algo_Record
	{
		/* K2 algo '_initialize_internal' */
		K2::Kernel::IAlgo * _initialize_internal;
		/* K2 algo '_finalize_internal' */
		K2::Kernel::IAlgo * _finalize_internal;
		/* K2 algo '_step_zero' */
		K2::Kernel::IAlgo * _step_zero;
		/* K2 algo '_save_context' */
		K2::Kernel::IAlgo * _save_context;
		/* K2 algo '_restore_context' */
		K2::Kernel::IAlgo * _restore_context;
		/* Update model's states */
		K2::Kernel::IAlgo * Update;
	
		/* Algo Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Algo Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};

	/* Model Extensions */
	struct Extension_Record
	{
	// V V V V V V V V V V V V V V V V V V V V V V V V V
	// Start of user code : User Extensions
	
	// Sample 
	// K2::Extension::XmlTransFuncService::XmlTransFunc * transfer_functions;

	// End of user code
	// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};

	/* Model Structures */
	struct Model_Record
	{
		K2::Kernel::IModel    * model;
		String_Record         * string;
		Feature_Record        * feature;
		Input_Record          * input;
		State_Record          * state;
		Output_Record         * output;
		Internal_Record       * internal;
		CallPoint_Record      * callpoint;
		Routine_Record        * routine;
		Algo_Record           * algo;
		Extension_Record      * extension;
		Shared_Feature_Record * shared_feature;
		State_Overload_Record * state_overload;

		/* Model Functions */
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Model Functions
		
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	};

	/*****************************************************************************
	 * K2 algo '_initialize_internal'
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void _initialize_internal__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );

	/*****************************************************************************
	 * K2 algo '_finalize_internal'
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void _finalize_internal__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );

	/*****************************************************************************
	 * K2 algo '_step_zero'
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void _step_zero__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );

	/*****************************************************************************
	 * K2 algo '_save_context'
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void _save_context__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );

	/*****************************************************************************
	 * K2 algo '_restore_context'
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void _restore_context__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );

	/*****************************************************************************
	 * Update model's states
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Unused                                          
	 * @param results            Unused                                          
	 *****************************************************************************/
	void Update__algo (
						K2::Kernel::IKernelServices  * kernelServices,
						Model_Record                 * mod,
						void                         * parameters,
						void                         * results );


	/*****************************************************************************
	 * Bus Routine: RTS scheduling execution	
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Pointer on routine parameters                   
	 * @param results            Pointer on routine results                      
	 *****************************************************************************/
	K2::Boolean RTM_SCHEDULING__routine (
						K2::Kernel::IKernelServices  * kernelServices,
 						Model_Record                 * mod,
						RTM_activation::Parameter_Record  * parameters,
						RTM_activation::Result_Record     * results );

	/*****************************************************************************
	 * TM frame received from SMU	
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Pointer on routine parameters                   
	 * @param results            Pointer on routine results                      
	 *****************************************************************************/
	K2::Boolean TM_FRAME_IN_FROM_SMU__routine (
						K2::Kernel::IKernelServices  * kernelServices,
 						Model_Record                 * mod,
						SBDL_TM_activation::Parameter_Record  * parameters,
						SBDL_TM_activation::Result_Record     * results );

	/*****************************************************************************
	 * TM frame from other TME2	
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Pointer on routine parameters                   
	 * @param results            Pointer on routine results                      
	 *****************************************************************************/
	K2::Boolean TM_FRAME_IN_FROM_TME2__routine (
						K2::Kernel::IKernelServices  * kernelServices,
 						Model_Record                 * mod,
						SBDL_TM_activation::Parameter_Record  * parameters,
						SBDL_TM_activation::Result_Record     * results );

	/*****************************************************************************
	 * Telemetry Encoder Interface relay status of SCTMTC	
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Pointer on routine parameters                   
	 * @param results            Pointer on routine results                      
	 *****************************************************************************/
	K2::Boolean TME_ENABLE__routine (
						K2::Kernel::IKernelServices  * kernelServices,
 						Model_Record                 * mod,
						Isis_HighPowerCommand_activation::Parameter_Record  * parameters,
						Isis_HighPowerCommand_activation::Result_Record     * results );

	/*****************************************************************************
	 * TME2 power supply	
	 * @param kernelServices     Pointer on K2 services                          
	 * @param mod                Pointer on model record                         
	 * @param parameters         Pointer on routine parameters                   
	 * @param results            Pointer on routine results                      
	 *****************************************************************************/
	K2::Boolean TME2_POWER_3_3V__routine (
						K2::Kernel::IKernelServices  * kernelServices,
 						Model_Record                 * mod,
						Isis_PowerLine_activation::Parameter_Record  * parameters,
						Isis_PowerLine_activation::Result_Record     * results );



	// V V V V V V V V V V V V V V V V V V V V V V V V V
	// Start of user code : User Addons code at end of namespace
		
	// End of user code
	// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
}

#endif
/* End of file K2_TME2.hpp */

