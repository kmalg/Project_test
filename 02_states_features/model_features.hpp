
#ifndef MODEL_FEATURES__HPP
#define MODEL_FEATURES__HPP

#include "IKernelServices.hpp"
#include "model_features_internal.hpp"

namespace model_features {

  using namespace K2::Services;

  struct String_Record {
  };

  //
  // Define here the features of the model.
  //
  struct Feature_Record {
      K2::UInt64 uptime; // define the 'uptime' feature of the model
  };

  struct State_Record {
  };

  struct Input_Record {
  };

  struct Output_Record {
  };

  struct CallPoint_Record {
  };

  struct Routine_Record {
  };

  struct Algo_Record {
    K2::Kernel::IAlgo * _initialize_internal;
    K2::Kernel::IAlgo * _save_context;
    K2::Kernel::IAlgo * _restore_context;
    K2::Kernel::IAlgo * _step_zero;
    K2::Kernel::IAlgo * update_features;
  };

  struct Extension_Record
  {
  };

  struct Shared_Feature_Record
  {
  };

  struct Model_Record {
    K2::Kernel::IModel * model;
    String_Record      * string;
    Feature_Record     * feature;
    Input_Record       * input;
    State_Record       * state;
    Output_Record      * output;
    Internal_Record    * internal;
    CallPoint_Record   * callpoint;
    Routine_Record     * routine;
    Algo_Record        * algo;
    Extension_Record   * extension;
    Shared_Feature_Record * shared_feature;
  };

  void _initialize_internal__algo( K2::Kernel::IKernelServices * kernelServices,
                                   Model_Record                * mod,
                                   void                        * parameter,
                                   void                        * result);

  void _save_context__algo( K2::Kernel::IKernelServices * kernelServices,
                            Model_Record                * mod,
                            void                        * parameter,
                            void                        * result);

  void _restore_context__algo( K2::Kernel::IKernelServices * kernelServices,
                               Model_Record                * mod,
                               void                        * parameter,
                               void                        * result);

  void _step_zero__algo( K2::Kernel::IKernelServices * kernelServices,
                         Model_Record                * mod,
                         void                        * parameter,
                         void                        * result);

  // this algo is used to update the feature 'uptime' value
  void update_features__algo( K2::Kernel::IKernelServices * kernelServices,
                              Model_Record                * mod,
                              void                        * parameter,
                              void                        * result);
}

#endif
