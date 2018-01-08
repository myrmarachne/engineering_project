THIS_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

python3.5 $THIS_DIR/frontend/run_ui.py
$THIS_DIR/backend/sniff
