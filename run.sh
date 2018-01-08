THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

MAINP4=$"/src/switch_module/p4/main.p4"
SOURCE=$THIS_DIR$MAINP4

MAINP4JSON=$"/src/switch_module/p4/main.p4.json"
SOURCEJSON=$THIS_DIR$MAINP4JSON

TOPOLOGY="/mininet/topology_1.py"

p4c-bm2-ss --p4v 16 $SOURCE -o $SOURCEJSON
sudo python2 $THIS_DIR$TOPOLOGY --behavioral-exe "simple_switch" --json $SOURCEJSON
