COMPONENT_NAME=K2_SMU_TME2


# ===========================================
# Model specfic variables
# ===========================================

ACTIVATIONS+=Isis_HighPowerCommand_activation
ACTIVATIONS+=Isis_PowerLine_activation
ACTIVATIONS+=RTM_activation
ACTIVATIONS+=SBDL_TM_activation

# V V V V V V V V V V V V V V V V V V V V V V V V V
# Start of user code : User variable modification
#

# # specify preprocessor flags with USER_DEFINES variable : will be applyed on model algo and addons
# USER_DEFINES += -Darch32bits -DDEBUG_LEVEL=3

# # specify preprocessor flags with USER_DEFINES_ADDONS variable : will be applyed ONLY on addons
# USER_DEFINES_ADDONS += -DADDONS_DEF

# # if you use extern library, you can specify some compile and link options
# GCC_OPTIONS += -std=c++11
# INCLUDE_OPTIONS += -Ipath
# LD_OPTIONS += -Lpath -lmy_lib

# Samples for some of boost libraries 
# LD_OPTIONS += -L$(COTS_PLATEFORM)/boost/lib
# LD_OPTIONS += -lboost_chrono
# LD_OPTIONS += -lboost_filesystem
# LD_OPTIONS += -lboost_random
# LD_OPTIONS += -lboost_regex
# LD_OPTIONS += -lboost_signals
# LD_OPTIONS += -lboost_system
# LD_OPTIONS += -lboost_thread
# LD_OPTIONS += -lboost_timer
# ...

# # GCC_OPTIONS_ADDONS will ONLY be apply to build addons
# GCC_OPTIONS_ADDONS += -std=c++11

# # GCC_OPTIONS for a specific file %fileName%
# GCC_OPTIONS_$(COMPONENT_NAME)_%fileName% += -std=c++11

# End of user code
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

ifndef COMPILE_CHAIN_K2
$(error Variable COMPILE_CHAIN_K2 is not defined)
endif
include $(COMPILE_CHAIN_K2)/rules_model.mk

# V V V V V V V V V V V V V V V V V V V V V V V V V
# Start of user code : User additional rules
#

#postcompile_K2_SMU_TME2 :
#	ln -s lib_tools_k2.so $(SO_LIB_DIR)/lib_tools_K2.so

#precompile_K2_SMU_TME2 :
#	...something...

# End of user code
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^

