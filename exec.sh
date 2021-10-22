myloc=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
source $myloc/env/bin/activate
python3 $myloc/status.py -n QN -f /home/omia/Documents/logs/faust.log -d /home/omia/Documents/logs/flujo_quicentro_norte.log
