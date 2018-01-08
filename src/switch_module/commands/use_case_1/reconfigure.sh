THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
BMV2_PATH=$THIS_DIR/../../../../../bmv2

CLI_PATH=$BMV2_PATH/targets/simple_switch/sswitch_CLI

$CLI_PATH --thrift-port 9090 < $THIS_DIR/s1-new.txt
$CLI_PATH --thrift-port 9091 < $THIS_DIR/s2-new.txt
$CLI_PATH --thrift-port 9092 < $THIS_DIR/s3-new.txt
