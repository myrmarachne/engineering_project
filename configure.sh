#!/bin/bash                                                                                                         
# Copy the Simple Swithc architecture file and the p4c

THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

BMV2_PATH=$THIS_DIR/../bmv2/targets/simple_switch
P4C=$THIS_DIR/../p4c/p4include/

BMV2_NEW=$THIS_DIR/src/p4_changed_files/simple_switch
P4C_NEW=$THIS_DIR/src/p4_changed_files/p4c

cp $BMV2_NEW/simple_switch.cpp $BMV2_PATH/simple_switch.cpp
cp $BMV2_NEW/simple_switch.h $BMV2_PATH/simple_switch.h
cp $P4C_NEW/v1model.p4 $P4C/v1model.p4
