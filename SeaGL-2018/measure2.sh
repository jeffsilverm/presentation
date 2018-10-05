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






REMOTE="commercialventvac.com"
# REMOTE="SMALL_DELL"
if [ "X${REMOTE}" = "XSMALL_DELL" ]; then
	# Small Dell IPv4 RFC 1918 private IPv4 address
	REMOTE_4_ADDR="192.168.0.25"
	# Small Dell IPv6 IPv6 address
	REMOTE_6_ADDR="2602:4b:ac60:9b00:bf35:14d2:bba0:ae44" 
	INTERFACE="enp3s0"
else
	REMOTE_4=`host -t A $REMOTE`
	REMOTE_4S=($REMOTE_4)
	REMOTE_4_ADDR=${REMOTE_4S[3]}
	REMOTE_6=`host -t AAAA $REMOTE`
	REMOTE_6S=($REMOTE_6)
	REMOTE_6_ADDR=${REMOTE_6S[4]}
fi
LOG_FILE="wget_performance.log"
RESULTS_FILE="wget_performance.results"
# Have to first add a classless qdisc
sudo tc qdisc add dev $INTERFACE root netem
echo "Remote $REMOTE has IPv4 address $REMOTE_4_ADDR and IPv6 address $REMOTE_6_ADDR" | tee -a $LOG_FILE
# When adding indices, always make sure that the ordering is such that the most rapidly changing
# index in the echo commands below is last on the line.
for size in 1000.txt 1000000.txt; do
	for loss in 1 5 10; do
		for delay in 0.1 0.2 0.5; do
			# See also https://www.cs.unm.edu/~crandall/netsfall13/TCtutorial.pdf
			sudo tc qdisc replace dev $INTERFACE root netem delay ${delay}ms loss ${loss}% 
			for protocol in 4 6; do
				if [ $protocol -eq 4 ] ; then
					REMOTE_ADDR=$REMOTE_4_ADDR
				else
					REMOTE_ADDR=$REMOTE_6_ADDR
				fi
				echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTCOL=IPv${protocol} " >> $LOG_FILE
				echo " "
				if ! wget -${protocol} -a $LOG_FILE ftp://${REMOTE_ADDR}/${size}; then
					echo "wget -${protocol} ftp://${REMOTE_ADDR}/${size} FAILED"; exit 1; fi
			done
		done
	done
done
rm 100*.txt
# Clean up - remove the classless qdisc
sudo tc qdisc delete dev $INTERFACE root netem
echo "Raw results in file $LOG_FILE .  Scrubbed results in $RESULTS_FILE"
egrep "saved|parameters" $LOG_FILE > $RESULTS_FILE


