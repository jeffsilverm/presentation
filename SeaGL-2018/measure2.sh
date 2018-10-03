#! /bin/bash
#
# This bashscript makes measurements of how long it takes to
# down load files for different combinations of packet loss
# rate, network delay, and file size.

network_em() {
  command=$1	# add, change, remove
  P=$2
  L=$3
  REMOTE_ADDR=$4
  
  if [ "X${command}" = "Xadd" ] ; then
 # See http://man7.org/linux/man-pages/man8/tc-tbf.8.html
# tc [ OPTIONS ] qdisc [ add | change | replace | link | delete ] dev
       tc DEV [ parent qdisc-id | root ] [ handle qdisc-id ] [ ingress_block
       BLOCK_INDEX ] [ egress_block BLOCK_INDEX ] qdisc [ qdisc specific
       parameters ]
    sudo 
  elif [ "X${command}" = "Xchange" ]; then
    sudo 
  fi
}







REMOTE="SMALL_DELL"
# REMOTE_4=`host -t A $REMOTE`
# REMOTE_4S=($REMOTE_4)
# REMOTE_4_ADDR=${REMOTE_4S[3]}
# REMOTE_6=`host -t AAAA $REMOTE`
# REMOTE_6S=($REMOTE_6)
# REMOTE_6_ADDR=${REMOTE_6S[4]}
# Small Dell IPv4 RFC 1918 private IPv4 address
REMOTE_4_ADDR="192.168.0.25"
# Small Dell IPv6 IPv6 address
REMOTE_6_ADDR="2602:4b:ac60:9b00:bf35:14d2:bba0:ae44" 
INTERFACE="enp3s0"
LOG_FILE="wget_performance.log"
RESULTS_FILE="wget_performance.results"
# Have to first add a classless qdisc
sudo tc qdisc add dev $INTERFACE root netem
echo "Remote $REMOTE has IPv4 address $REMOTE_4_ADDR and IPv6 address $REMOTE_6_ADDR"
for loss in 1 5 10; do
  for delay in 0.1 0.2 0.5; do
# See also https://www.cs.unm.edu/~crandall/netsfall13/TCtutorial.pdf
    sudo tc qdisc replace dev $INTERFACE root netem delay ${delay}ms loss ${loss}% 
    echo -n "parameters `date` LOSS=${loss} DELAY=${delay} IPv4" >> $LOG_FILE
    echo    "parameters `date` LOSS=${loss} DELAY=${delay} IPv4"
    if ! wget -4 -a $LOG_FILE ftp://${REMOTE_4_ADDR}/8192.data; then echo "wget -4 FAILED"; exit 1; fi
    echo -n "parameters `date` LOSS=${loss} DELAY=${delay} IPv6!" >> $LOG_FILE
    echo    "parameters `date` LOSS=${loss} DELAY=${delay} IPv6!"
    if ! wget -6 -a $LOG_FILE ftp://[${REMOTE_6_ADDR}]/8192.data; then echo "wget -6 FAILED"; exit 1; fi
  done
done
rm 8192.data
# Clean up - remove the classless qdisc
sudo tc qdisc delete dev $INTERFACE root netem
echo "Raw results in file $LOG_FILE .  Scrubbed results in $RESULTS_FILE"
egrep "saved|parameters" $LOG_FILE > $RESULTS_FILE


