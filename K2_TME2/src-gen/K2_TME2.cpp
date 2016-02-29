
/*****************************************************************************
 * K2_TME2                                                 
 *                                                                           
 * IDS_COUNT:                                                                
 * IDS_REFERENCE:                                                            
 * IDS_ISSUE:                                                                
 * IDS_REVISION:                                                                  
 *                   
 * TME2 is an option of Satellite Management Unit. 
 * TME2 Model will complement the existing SCTMTC Model available in SMU Numerical Model.
 * The main activity of this TME2 Model is to give the capability to simulate the insertion of a secondary frame header of fixed length in the Telemetry Transfer Frame.    
 *                                                        
 * @file K2_TME2.cpp                                        
 * @remarks Auto-generated from MELODY_CCM model                            
 *****************************************************************************/

/* default Includes  */
#include "K2_TME2.hpp"
#include "K2_TME2_internal.hpp"
//#include "k2macros.hpp"

/* User Includes */
// V V V V V V V V V V V V V V V V V V V V V V V V V
// Start of user code : User Includes
//#include "ccsds.h"

// End of user code
// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

namespace K2_TME2
{

	// V V V V V V V V V V V V V V V V V V V V V V V V V
	// Start of user code : Local Functions
/*
 * 						INPUT FRAME STRUCTURE
 *
|| ASM	||   Telemetry Transfer Frame ( = 956 Bytes)	||
==========================================================
||		|| PH | SH	| 		TF Data Field	|    CLCW	||
----------------------------------------------------------
||  4	|| 6  |  0  |  		   946       	|	  4		||
==========================================================
 *

 * 						OUPUT FRAME STRUCTURE
 *
|| ASM	||  Telemetry Transfer Frame ( = 1115 Bytes)	|| RS  ||
=================================================================
||		|| PH | SH	| 		TF Data Field	|    CLCW	||	   ||
-----------------------------------------------------------------
||  4	|| 6  |  34 |  		   1071        	|	  4		|| 160 ||
=================================================================
 */

	const K2::UInt16 	ONE_BIT_LENGTH = 8;

	// All index are expressed in bit
	const K2::UInt16    ASM_STD_LENGTH            =   4;  //  Attached Sync Marker length (octets)

	const K2::UInt16	PH_VERSION_INX            =   1 + ASM_STD_LENGTH * ONE_BIT_LENGTH;  // Transfer Frame Primary Header - Master Channel identifier - Transfer frame version number
	const K2::UInt16	PH_OPCF_FLAG_INX          =  15 +(ASM_STD_LENGTH * ONE_BIT_LENGTH);  // Transfer Frame Primary Header - Operation Control Field Flag
	const K2::UInt16	PH_VC_FC_INX              =  24 +(ASM_STD_LENGTH * ONE_BIT_LENGTH);  // Transfer Frame Primary Header - Virtual Channel Frame Count
	const K2::UInt16	PH_SH_FLAG_INX            =  32 +(ASM_STD_LENGTH * ONE_BIT_LENGTH);  // Transfer Frame Primary Header - Transfer Frame Data Field Status - Secondary Header Flag
	const K2::UInt16	PH_SYNCH_FLAG_INX         =  33 +(ASM_STD_LENGTH * ONE_BIT_LENGTH);  // Transfer Frame Primary Header - Transfer Frame Data Field Status - Synchronization Flag
	const K2::UInt16	PH_FIRST_HEAD_POINTER_INX =  37 +(ASM_STD_LENGTH * ONE_BIT_LENGTH);  // Transfer Frame Primary Header - Transfer Frame Data Field Status - First Header Pointer
	const K2::UInt16	FIRST_HEAD_POINTER_IDLE   =  0x7FE;     // First Header Pointer value in idle frame
	const K2::UInt16	FIRST_HEAD_POINTER_ERR    =  0x7FF;     // First Header Pointer value in error frame
	const K2::UInt16	PH_STD_LENGTH             =   6;        // Transfer Frame Primary Header length (octets)

	const K2::UInt16	SH_VERSION_INX_OCT        =  1 + (ASM_STD_LENGTH+PH_STD_LENGTH) * ONE_BIT_LENGTH;  // Transfer Frame Secondary Header - Transfer Frame SH identifier - Transfer frame SH version number
	const K2::UInt16	SH_DATA_FIELD_INX         =  8 + (ASM_STD_LENGTH+PH_STD_LENGTH) * ONE_BIT_LENGTH;  // Transfer Frame Secondary Header - Transfer Frame SH Data Field

	const K2::UInt16	RS_CODEBLOCK_LENGTH       = 160;  // Reed Solomon Code Block size (octets)
	const K2::UInt16    CLCW_STD_LENGTH           =   4;  // Communication Link Control Word length (octets)
	const K2::UInt16    RS_E16_I5_MAX_LENGTH      = 1115; // Maximum frame lengths compatible with Reed Solomon coding (for E=16 I=5)
	const K2::UInt16 	RS_Interleaving   		  = 5;    // Reed Solomon Iterleaving parameter
	const K2::UInt16  	RS_rsData 				  = 223;  // Number of information R-S symbols in each codeword.


/*                                 DUMMY PACKET STRUCTURE
 *
|| Packet Identification	                      ||Packet Sequence Control	 ||Packet Length||	         Packet Data Field			 ||
=======================================================================================================================================
||Dummy Packet   | Type	|Data Field  |Application ||Segmentation |	 Source  ||    Packet   ||	 Packet  |	  Packet  |   Packet     ||
||Version Number |		|Header Flag |Process ID  ||    Flags	 | Seq Count ||    Length   ||Data Field | Data Field |  Data Field  ||
---------------------------------------------------------------------------------------------------------------------------------------
||  bit 0 to 2	| bit 3	|    bit 4	 |bit 5 to 15 ||bit 0 to 1	 |bit 2 to 15|| bit 0 to 15 ||bit 0 to 31|bit 32 to 63|	bit 64 to 951||
|| 				2 octets						  ||	  2 octets			 ||  2 octets	|| 4 octets	 |  4 octets  |	 111 octets  ||
=======================================================================================================================================
*/
	const K2::UInt16	DUMMY_PKG_VERSION		  = 0; 	  // Default value of Dummy Packet Version Number 	(bit 0 to 2)
	const K2::UInt16	DUMMY_PKG_VERSION_INX	  = 2; 	  // Position Dummy Packet Version Number
	const K2::UInt16	DUMMY_TYPE		          = 0; 	  // Default value of Type 	(bit 3)
	const K2::UInt16	DUMMY_TYPE_INX	          = 3; 	  // Position of Packet Type
	const K2::UInt16	DUMMY_DATA_FH_FLAG		  = 0; 	  // Default value of Data Field Header Flag  	(bit 4)
	const K2::UInt16	DUMMY_DATA_FH_FLAG_INX	  = 4; 	  // Position of Data Field Header Flag
	const K2::UInt16	DUMMY_APP_ID		      = 1007; // Default value of Application Process Identifier (bit 5 to 15)
	const K2::UInt16	DUMMY_SEG_FLAG		      = 3; 	  // Default value of Segmentation Flags (bit 0 to 1)
	const K2::UInt16	DUMMY_SEG_FLAG_INX	      = 1;    // Position of Segmentation Flags
	const K2::UInt16	DUMMY_SRC_SQ_COUNT	      = 0; 	  // Default value of Source Sequence Count (bit 2 to 15)
	const K2::UInt16    DUMMY_PKG_TOTAL_LENGTH = 125;
	const K2::UInt16    DUMMY_PKG_LENGTH_VALUE = 118;	  // Packet Length (bit 0 to 15)

//Other constant value:l
	const K2::UInt16 ONE_BIT_LAST_INX = 7;
	const K2::UInt16 MASK_0_TO_3_BIT = 7;
	const K2::UInt16 MASK_0_BIT = 1;
	const K2::UInt16 MASK_0_TO_7_BIT = 255;
	const K2::UInt16 SHIFT_FOR_9TH_BIT = 0;
	const K2::UInt16 SHIFT_FOR_4TH_BIT = 5;
	const K2::UInt16 SHIFT_ONE_INX = 1;
	const K2::UInt32 MAX_MOD_32_COUNT = 2147483647; // 2^31  - 1;
	const K2::UInt16 SIZE_OF_BASE_MOD_9 = 9;
	const K2::UInt16 DUMMY_DF_4TH_oct_inx = 3;


	K2::UInt16 random_LFSR(K2::UInt8 initial_value, K2::UInt8 * result_array, K2::UInt16 array_length)
	{

		// Declare and initialize rnd_array
		K2::UInt8 rnd_array[array_length];

		for (unsigned int n = 0; n < array_length; n++) {
			rnd_array[n] = 0;
		}

		// Declare and initialize counter and polynomial input/output

		K2::UInt16 k = 0;
		K2::UInt16 rand_input = initial_value;
		K2::UInt16 rand_output = rand_input;

		while ( k < (array_length-1) ) {

			// Calculate output (9 bit length)
			rand_output = (rand_input >> SHIFT_ONE_INX) | ((((rand_input >> SHIFT_FOR_9TH_BIT) ^ (rand_input >> SHIFT_FOR_4TH_BIT)) & MASK_0_BIT) << ONE_BIT_LENGTH );

			//write output on unsigned char ( 8 bit length)
			rnd_array[k] = rand_output & MASK_0_TO_7_BIT;

			// update input value
			rand_input = rand_output;
			k ++;
		}

		memcpy( result_array , rnd_array ,array_length);

		return rand_output;
	}

	void insert_dummy_packet(K2::UInt8 * cadu_array, K2::UInt16 dummy_pck_start, K2::UInt16 dummy_count_frame, K2::UInt16 dummy_count_dpck, K2::UInt16 dummy_pck_df_value)
	{
		// Insert Packet identification
		K2::UInt16 i = 0;

		cadu_array[dummy_pck_start +i] = (DUMMY_PKG_VERSION << (ONE_BIT_LAST_INX - DUMMY_PKG_VERSION_INX)) +
													(DUMMY_TYPE << (ONE_BIT_LAST_INX-DUMMY_TYPE_INX)) +
													(DUMMY_DATA_FH_FLAG << (ONE_BIT_LAST_INX - DUMMY_DATA_FH_FLAG_INX)) +
													(DUMMY_APP_ID >> ONE_BIT_LENGTH);
		i++;

		cadu_array[dummy_pck_start + i] = DUMMY_APP_ID & MASK_0_TO_7_BIT;
		i++;

		// Insert Packet Sequence Control
		cadu_array[dummy_pck_start + i] = (DUMMY_SEG_FLAG << (ONE_BIT_LAST_INX - DUMMY_SEG_FLAG_INX)) +
													(DUMMY_SRC_SQ_COUNT >> ONE_BIT_LENGTH);
		i++;

		cadu_array[dummy_pck_start + i] = DUMMY_SRC_SQ_COUNT & MASK_0_TO_7_BIT;
		i++;

		// Insert Packet Length
		cadu_array[dummy_pck_start + i] = DUMMY_PKG_LENGTH_VALUE  >> ONE_BIT_LENGTH;
		i++;

		cadu_array[dummy_pck_start + i] = DUMMY_PKG_LENGTH_VALUE  & MASK_0_TO_7_BIT;
		i++;

		// Insert Packet Data Field (bit 0 to 31)
		for (int k = DUMMY_DF_4TH_oct_inx; k>=0; k--) {
			cadu_array[dummy_pck_start + i] = (dummy_count_frame >> (ONE_BIT_LENGTH * k)) & MASK_0_TO_7_BIT ;
			i++;
		}

		// Insert Packet Data Field (bit 32 to 63)
		for (int k = DUMMY_DF_4TH_oct_inx; k>=0; k--) {
			cadu_array[dummy_pck_start + i] = (dummy_count_dpck >> (ONE_BIT_LENGTH * k)) & MASK_0_TO_7_BIT ;
			i++;
		}

		// Insert Packet Data Field (bit 34 to 951)
		while (i < DUMMY_PKG_TOTAL_LENGTH) {
			cadu_array[dummy_pck_start + i] = dummy_pck_df_value ;
			i++;
		}

	}

	void update_primary_frame_header(K2::UInt8 * cadu_array)
	{
		// Set Operation Control Field Flag to present
		K2::UInt16 bit_inx = PH_OPCF_FLAG_INX % ONE_BIT_LENGTH;
		K2::UInt16 oct_inx = PH_OPCF_FLAG_INX / ONE_BIT_LENGTH;

		cadu_array[oct_inx] = (cadu_array[oct_inx] | (1 << (ONE_BIT_LAST_INX - bit_inx)));

		// Set Secondary Header Flag to present
		bit_inx = PH_SH_FLAG_INX % ONE_BIT_LENGTH;
		oct_inx = PH_SH_FLAG_INX / ONE_BIT_LENGTH;

		cadu_array[oct_inx] = (cadu_array[oct_inx] | (1 << (ONE_BIT_LAST_INX - bit_inx)));
	}

	void add_secondary_frame_header(K2::UInt8 * cadu_array, K2::UInt16 SH_size, K2::UInt16 SH_version, K2::UInt8 * SH_data_field)
	{
		// Fill first octet
		K2::UInt16 oct_inx = SH_VERSION_INX_OCT / ONE_BIT_LENGTH;
		K2::UInt16 bit_inx = SH_VERSION_INX_OCT % ONE_BIT_LENGTH;
		cadu_array[oct_inx] = (SH_version << (ONE_BIT_LAST_INX - bit_inx)) + (SH_size - 1);

		// Fill remaining octets
		oct_inx = SH_DATA_FIELD_INX / ONE_BIT_LENGTH;
		for (int i = 0; i < (SH_size - 1); i++) {
			cadu_array[oct_inx + i] = SH_data_field[i];
		}
	}

	void shift_right_pck(K2::UInt8 * cadu_array, K2::UInt16 idx_start, K2::UInt16 idx_end, K2::UInt16 delta_idx)
	{
		for (unsigned int i = (idx_start -1); i >= idx_end; i--) {
			cadu_array[i + delta_idx] = cadu_array[i];
		}
	}

	// End of user code
	// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : _initialize_internal__algo

		LOG_DEBUG(10, "_initialize_internal__algo");

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : _finalize_internal__algo

		LOG_DEBUG(10, "_finalize_internal__algo");

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : _step_zero__algo

		LOG_DEBUG(10, "_step_zero__algo");

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : _save_context__algo

		LOG_DEBUG(10, "_save_context__algo");

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : _restore_context__algo

		LOG_DEBUG(10, "_restore_context__algo");

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						void                         * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : Update__algo

		LOG_DEBUG(10, "Update__algo");

		if ( mod->state->TME2_STATUS == 0)
		{
			mod->state->TME2_CONSUMPTION = mod->feature->TME2_OFF_CONSUMPTION;
			mod->state->TME2_DISSIPATION = mod->feature->TME2_OFF_DISSIPATION;
			mod->state->TME2_TEMP = mod->feature->TME2_OFF_TEMP;
			mod->state->TME2_SECONDARY_VOLTAGE = mod->feature->TME2_SEC_VOLTAGE_OFF;
		}
		else
		{
			mod->state->TME2_CONSUMPTION = mod->feature->TME2_ON_CONSUMPTION;
			mod->state->TME2_DISSIPATION = mod->feature->TME2_ON_DISSIPATION;
			mod->state->TME2_TEMP = mod->feature->TME2_ON_TEMP;
			mod->state->TME2_SECONDARY_VOLTAGE = mod->feature->TME2_SEC_VOLTAGE_ON;
		}

		mod->output->TME2_DISSIPATION = mod->state->TME2_DISSIPATION;

		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}



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
						RTM_activation::Result_Record     * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : RTM_SCHEDULING__routine
		LOG_DEBUG(10, "RTM_SCHEDULING__routine");

		Update__algo(kernelServices, mod, NULL, NULL);
		return true; // true means the routine responds and can be traced
 
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						SBDL_TM_activation::Result_Record     * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : TM_FRAME_IN_FROM_SMU__routine

		LOG_DEBUG(10, "TM_FRAME_IN_FROM_SMU__routine");

		if (mod->state->TME2_STATUS == 1 &&
				mod->state->TME_ENABLE == 1) {

			// check the length of the frame received
			if (parameters->cadu_size > mod->feature->FRAME_INPUT_LENGTH_MAX) {
				LOG_ERROR
					("Receiving frame length differs from the expected one");
			}

			// check the total length of the frame
			else if ((parameters->cadu_size - ASM_STD_LENGTH + mod->feature->SEC_HEADER_SIZE + DUMMY_PKG_TOTAL_LENGTH ) > RS_E16_I5_MAX_LENGTH) {
				LOG_ERROR
					("The frame length would exceed the maximum size compatible with Reed Solomon coding. Check Secondary Header size");
			}

			else {

				// START FRAME PROCESSING:
				// Identify incoming frame

				K2::UInt16 IN_TF_DATA_FIELD_LENGTH = parameters->cadu_size - ASM_STD_LENGTH - PH_STD_LENGTH - CLCW_STD_LENGTH;
				K2::UInt16 IN_CADU_SIZE = parameters->cadu_size;
				K2::UInt16 IN_BIT_RATE = parameters->tm_bit_rate;
				K2::UInt16 TF_DATA_FIELD_START = ASM_STD_LENGTH + PH_STD_LENGTH + mod->feature->SEC_HEADER_SIZE;

				// Read First Header Pointer and calculate the position to insert the dummy packet
				K2::Boolean IDLE_FRAME = false;
				K2::UInt16  TF_DUMMY_PACKET_START = TF_DATA_FIELD_START;

				// Read First Header Pointer : it is 11 bits length => 3 + 8
				K2::UInt16 oct_inx = PH_FIRST_HEAD_POINTER_INX / ONE_BIT_LENGTH;
				K2::UInt16 PH_FIRST_HEAD_POINTER_VALUE = ((parameters->cadu[oct_inx] & MASK_0_TO_3_BIT) << ONE_BIT_LENGTH) + parameters->cadu[oct_inx + 1];

				// Idle frame : if First Header Pointer == 111 11111110
				if (PH_FIRST_HEAD_POINTER_VALUE == FIRST_HEAD_POINTER_IDLE) {
					IDLE_FRAME = true;
					TF_DUMMY_PACKET_START += IN_TF_DATA_FIELD_LENGTH;
					}

				// Error case on Frame - no packet starts in this frame : if First Header Pointer == 111 11111111
				else if (PH_FIRST_HEAD_POINTER_VALUE == FIRST_HEAD_POINTER_ERR)
					TF_DUMMY_PACKET_START += IN_TF_DATA_FIELD_LENGTH;

				// Frame with 0 <= PH_FIRST_HEAD_POINTER_VALUE <  IN_TF_DATA_FIELD_LENGTH
				else
					TF_DUMMY_PACKET_START += PH_FIRST_HEAD_POINTER_VALUE;


				// Shift packets in range : TF_DUMMY_PACKET_START - IN_CADU_SIZE (at least CLCW shall be shifted)
				shift_right_pck(parameters->cadu, IN_CADU_SIZE, (TF_DUMMY_PACKET_START - mod->feature->SEC_HEADER_SIZE) , (mod->feature->SEC_HEADER_SIZE + DUMMY_PKG_TOTAL_LENGTH) );

				// Process frame depending on its type
				mod->state->DUMMY_COUNTER_FRAME = (mod->state->DUMMY_COUNTER_FRAME == MAX_MOD_32_COUNT) ?
													0 : (mod->state->DUMMY_COUNTER_FRAME + 1);

				// Idle Frame
				if (IDLE_FRAME) {
					//Dummy packet is not created, but generate a new idle package 1071 bytes length

					//Create and insert the idle package
					K2::UInt16 TF_DATA_FIELD_END = TF_DATA_FIELD_START + IN_TF_DATA_FIELD_LENGTH + DUMMY_PKG_TOTAL_LENGTH;
					K2::UInt16 random_LFSR_input;

					oct_inx = PH_VC_FC_INX / ONE_BIT_LENGTH;
					random_LFSR_input =  (parameters->cadu[oct_inx] == 0) ?
											1	: mod->state->IDLE_FRAME;

					mod->state->IDLE_FRAME = random_LFSR (random_LFSR_input, &(parameters->cadu[TF_DATA_FIELD_START]) , (TF_DATA_FIELD_END - TF_DATA_FIELD_START) );

				}

				// Other frame
				else {
					
					mod->state->DUMMY_COUNTER_DPACKET = (mod->state->DUMMY_COUNTER_DPACKET == MAX_MOD_32_COUNT ) ?
															0 : mod->state->DUMMY_COUNTER_DPACKET +1;


					insert_dummy_packet(parameters->cadu, TF_DUMMY_PACKET_START, mod->state->DUMMY_COUNTER_FRAME, mod->state->DUMMY_COUNTER_DPACKET , mod->feature->DUMMY_PACKET_FIELD);


					// Shift remaining data : range TF_DATA_FIELD_START - TF_DUMMY_PACKET_START
					shift_right_pck(parameters->cadu, (TF_DUMMY_PACKET_START - mod->feature->SEC_HEADER_SIZE) , (TF_DATA_FIELD_START - mod->feature->SEC_HEADER_SIZE), mod->feature->SEC_HEADER_SIZE );

				}


				// CONTINUE FRAME PROCESSING:

				// Add 34 Bytes Secondary Frame Header
				add_secondary_frame_header(parameters->cadu, mod->feature->SEC_HEADER_SIZE, mod->state->SEC_HEADER_VERSION, mod->state->SEC_HEADER_DATA_FIELD);


				// Update Primary Frame Header: Secondary Header Flag, Operation Control Field Flag
				update_primary_frame_header(parameters->cadu);


				// CONCLUDE FRAME PROCESSING :

				// Insert Reed-Solomon Code
				K2::UInt16  RS_CHECK_SYMBOL_INX  = IN_CADU_SIZE + mod->feature->SEC_HEADER_SIZE + DUMMY_PKG_TOTAL_LENGTH;

				rsEncode (&(parameters->cadu[ASM_STD_LENGTH]), &(parameters->cadu[RS_CHECK_SYMBOL_INX]), RS_Interleaving, RS_rsData );
				
				// modify cadu_size
				parameters->cadu_size = IN_CADU_SIZE + mod->feature->SEC_HEADER_SIZE + DUMMY_PKG_TOTAL_LENGTH +  RS_CODEBLOCK_LENGTH ;

				// modify bit rate
				parameters->tm_bit_rate = IN_BIT_RATE * (1.0 *(IN_CADU_SIZE + mod->feature->SEC_HEADER_SIZE + DUMMY_PKG_TOTAL_LENGTH +  RS_CODEBLOCK_LENGTH ) / IN_CADU_SIZE);

				// SEND CALL POINT:
				SBDL_TM_activation::Call(
								mod->callpoint->TM_FRAME_OUT_CH1,
								kernelServices,
								parameters->cadu,
								parameters->cadu_size,
								parameters->tm_bit_rate,
								kernelServices->GetSimulationTime());

				SBDL_TM_activation::Call(
								mod->callpoint->TM_FRAME_OUT_CH2,
								kernelServices,
								parameters->cadu,
								parameters->cadu_size,
								parameters->tm_bit_rate,
								kernelServices->GetSimulationTime());

				SBDL_TM_activation::Call(
								mod->callpoint->TM_FRAME_OUT_TO_TME2,
								kernelServices,
								parameters->cadu,
								parameters->cadu_size,
								parameters->tm_bit_rate,
								kernelServices->GetSimulationTime());

				SBDL_TM_activation::Call(
								mod->callpoint->TM_FRAME_OUT_AUX,
								kernelServices,
								parameters->cadu,
								parameters->cadu_size,
								parameters->tm_bit_rate,
								kernelServices->GetSimulationTime());
			}



		}

		return true; // true means the routine responds and can be traced
 
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						SBDL_TM_activation::Result_Record     * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : TM_FRAME_IN_FROM_TME2__routine

		LOG_DEBUG(10, "TM_FRAME_IN_FROM_TME2__routine");

		if (mod->state->TME2_STATUS == 1 ) {

			SBDL_TM_activation::Call(
							mod->callpoint->TM_FRAME_OUT_CH1,
							kernelServices,
							parameters->cadu,
							parameters->cadu_size,
							parameters->tm_bit_rate,
							kernelServices->GetSimulationTime()	);

			SBDL_TM_activation::Call(
							mod->callpoint->TM_FRAME_OUT_CH2,
							kernelServices,
							parameters->cadu,
							parameters->cadu_size,
							parameters->tm_bit_rate,
							kernelServices->GetSimulationTime()	);
		}

		return true; // true means the routine responds and can be traced
 
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						Isis_HighPowerCommand_activation::Result_Record     * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : TME_ENABLE__routine

		LOG_DEBUG(10, "TME_ENABLE__routine");

		if (parameters->type == true) {

			mod->state->TME_ENABLE = true;
		}
		else {

			mod->state->TME_ENABLE = false;
		}

		return true; // true means the routine responds and can be traced
 
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}

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
						Isis_PowerLine_activation::Result_Record     * results )
	{
		// V V V V V V V V V V V V V V V V V V V V V V V V V
		// Start of user code : TME2_POWER_3_3V__routine

		LOG_DEBUG(10, "TME2_POWER_3_3V__routine");

		if (parameters->voltage >= mod->feature->TME2_MIN_VOLTAGE)
		{
			mod->state->TME2_STATUS = true;
		}
		else {
			mod->state->TME2_STATUS = false;
		}

		Update__algo(kernelServices, mod, NULL, NULL);

		if (parameters->voltage != 0.0)
		{
			results->intensity = mod->state->TME2_CONSUMPTION / parameters->voltage;
		}
		else
		{
			results->intensity = 0;
		}


		return true; // true means the routine responds and can be traced
 
		// End of user code
		// ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
	}



}

/* End of file K2_TME2.cpp */

