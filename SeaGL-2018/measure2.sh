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






# REMOTE="commercialventvac.com"
REMOTE="SMALL_DELL"
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
if [ -f $RESULTS_FILE ]; then
  rm $RESULTS_FILE
fi
if [ -f $LOG_FILE ]; then
  rm $LOG_FILE
fi
# Have to first add a classless qdisc
sudo tc qdisc add dev $INTERFACE root netem
echo "Remote $REMOTE has IPv4 address $REMOTE_4_ADDR and IPv6 address $REMOTE_6_ADDR" | tee -a $LOG_FILE
# When adding indices, always make sure that the ordering is such that the most rapidly changing
# index in the echo commands below is last on the line.
for size in 1024.data 2048.data ; do
	for loss in 1 5 10; do
		for delay in 0.1 0.2 0.5; do
			# See also https://www.cs.unm.edu/~crandall/netsfall13/TCtutorial.pdf
			sudo tc qdisc replace dev $INTERFACE root netem delay ${delay}ms loss ${loss}% 
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv4 " | tee -a  $LOG_FILE
			echo " "
			if ! wget -4 -a $LOG_FILE ftp://${REMOTE_4_ADDR}/${size}; then
				echo "wget -6 ftp://${REMOTE_ADDR}/${size} FAILED"; exit 1; fi
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv6  " | tee -a $LOG_FILE
			if ! wget -6 -a $LOG_FILE ftp://[${REMOTE_6_ADDR}]/${size}; then
				echo "wget -6 ftp://${REMOTE_ADDR}/${size} FAILED"; exit 1; fi
			echo " "
		done
	done
done
rm *.data
# Clean up - remove the classless qdisc
sudo tc qdisc delete dev $INTERFACE root netem
echo "Raw results in file $LOG_FILE .  Scrubbed results in $RESULTS_FILE"
egrep "saved|parameters" $LOG_FILE > $RESULTS_FILE

exit 0
# Change TCP window size
# From https://netbeez.net/blog/how-to-adjust-the-tcp-window-size-limit-on-linux/
#echo 'net.core.wmem_max=4194304' &gt;&gt; /etc/sysctl.conf
#echo 'net.core.rmem_max=12582912' &gt;&gt; /etc/sysctl.conf
#echo 'net.ipv4.tcp_rmem = 4096 87380 4194304' &gt;&gt; /etc/sysctl.conf
#echo 'net.ipv4.tcp_wmem = 4096 87380 4194304' &gt;&gt; /etc/sysctl.conf
sysctl -p
