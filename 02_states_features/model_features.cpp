
#include <LoggerServices.hpp>

#include "model_features.hpp"

namespace model_features {

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

  void update_features__algo( K2::Kernel::IKernelServices * kernelServices,
                              Model_Record                * mod,
                              void                        * parameter,
                              void                        * result)
  {
      // update internal 'time' value and log it
      mod->internal->time_2x = mod->feature->uptime * 2;
      K2::Services::LogInformationF("internal[time_2x] = %d", mod->internal->time_2x);

      // log the feature 'uptime' value and update it
      K2::Services::LogInformationF("feature[uptime] = %d", mod->feature->uptime);
      mod->feature->uptime += 1;
  }
}
