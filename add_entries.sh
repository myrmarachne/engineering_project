THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BMV2_PATH=$THIS_DIR/../bmv2/targets/simple_switch
json=""
if [ $# -eq 1 ]; then
    echo "Using JSON input $1"
    json="--json $1"
fi

CLI=$BMV2_PATH/simple_switch_CLI
TOOLS_DIR=$BMV2_PATH/../../tools/

$CLI $json $port --thrift-port 9090 --thrift-ip 127.0.0.1 < $THIS_DIR/src/switch_module/tags/tags1.txt
$CLI $json $port --thrift-port 9091 --thrift-ip 127.0.0.1 < $THIS_DIR/src/switch_module/tags/tags2.txt
$CLI $json $port --thrift-port 9092 --thrift-ip 127.0.0.1 < $THIS_DIR/src/switch_module/tags/tags3.txt

