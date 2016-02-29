
#include <LoggerServices.hpp>

#include "model_states.hpp"

namespace model_states {

  void _initialize_internal__algo( K2::Kernel::IKernelServices * kernelServices,
                                   Model_Record                * mod,
                                   void                        * parameter,
                                   void                        * result) {
  }

  void _save_context__algo( K2::Kernel::IKernelServices * kernelServices,
                            Model_Record                * mod,
                            void                        * parameter,
                            void                        * result) {
  }

  void _restore_context__algo( K2::Kernel::IKernelServices * kernelServices,
                               Model_Record                * mod,
                               void                        * parameter,
                               void                        * result) {
  }

  void _step_zero__algo( K2::Kernel::IKernelServices * kernelServices,
                         Model_Record                * mod,
                         void                        * parameter,
                         void                        * result) {
  }

  void update_states__algo( K2::Kernel::IKernelServices * kernelServices,
                            Model_Record                * mod,
                            void                        * parameter,
                            void                        * result)
  {
      // update internal 'steps' value
      mod->internal->steps_10x = mod->state->steps * 10;
      K2::Services::LogInformationF("internal[steps_10x] = %d", mod->internal->steps_10x);

	  // log the 'steps' state value and update it
      K2::Services::LogInformationF("state[steps] = %d", mod->state->steps);
      mod->state->steps += 1;
  }
}
