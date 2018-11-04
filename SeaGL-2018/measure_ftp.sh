# /bin/bash
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


# Get rid of any cruft from previous runs
rm *.data.*

REMOTE="jeffs-desktop"

if [ "X${REMOTE}" = "XSMALL_DELL" ]; then
	# Small Dell IPv4 RFC 1918 private IPv4 address
	REMOTE_4_ADDR="192.168.0.3"
	# Small Dell IPv6 IPv6 address
	REMOTE_6_ADDR="2602:47:d433:bb00:99d1:b78c:dd68:1477"
elif [ "X${REMOTE}" = "Xjeffs-desktop" ]; then
	REMOTE_4_ADDR="192.168.0.21"
	REMOTE_6_ADDR="2602:4b:ac68:b00:9e80:c519:f006:59c"
else
	REMOTE_4=`host -t A $REMOTE`
	REMOTE_4S=($REMOTE_4)			# Only needed to extract IPv4 address from host command
	REMOTE_4_ADDR=${REMOTE_4S[3]}
	REMOTE_6=`host -t AAAA $REMOTE`
	REMOTE_6S=($REMOTE_6)
	REMOTE_6_ADDR=${REMOTE_6S[4]}
fi
if [ "X${HOSTNAME}" = "Xjeffs-desktop" ] ; then
	# Get rid of a local idiosyncrasy of mine that happens to really break the results file
	unalias egrep
	INTERFACE="eno1"
elif  [ "X${HOSTNAME}" = "Xsmalldell" ] ; then
	INTERFACE="enp0s25"
else
	echo "HOSTNAME is $HOSTNAME which is a bad name"
	exit 1
fi
TIMESTAMP=$(date +%Y%m%d-%H%M)
LOG_FILE="ftp_performance_$TIMESTAMP.log"
RESULTS_FILE="ftp_performance_$TIMESTAMP.results"
TIME_FILE="ftp_performance_$TIMESTAMP.time"
if [ -f $RESULTS_FILE ]; then
  rm $RESULTS_FILE
fi
if [ -f $LOG_FILE ]; then
  rm $LOG_FILE
fi
if [ -f $TIME_FILE ]; then
  rm $TIME_FILE
fi
# Have to first add a classless qdisc
sudo tc qdisc add dev $INTERFACE root netem
echo "Remote $REMOTE has IPv4 address $REMOTE_4_ADDR and IPv6 address $REMOTE_6_ADDR" | tee -a $LOG_FILE
# When adding indices, always make sure that the ordering is such that the most rapidly changing
# index in the echo commands below is last on the line.
# for size in 1024.data 2048.data 4096.data; do
for size in 1024.data 2048.data 4096.data; do
	# There is a bug in tc: it won't handle 0 as a valid delay time.
#	for loss in  0 10 20 50 75 100; do
	for loss in  0 10 20 50; do
#		for delay in  0 10.0 20.0 50.0 100.0; do
		for delay in  0 10.0 20.0; do
			# See also https://www.cs.unm.edu/~crandall/netsfall13/TCtutorial.pdf
			# There is a bug in the tc: it won't accept 0 as a value for loss (see end of this file for details)
# [jeffs@smalldell ~]$ 


			if [ delay = "0" ]; then delay1="0.00000000001"; else delay1="$delay"; fi
			sudo tc qdisc replace dev $INTERFACE root netem delay ${delay1}ms loss ${loss}% 
			sudo tc qdisc show dev $INTERFACE | tee -a $LOG_FILE
# Uncomment the next line for debugging the tc command
#			sudo tc qdisc show dev $INTERFACE >> $TIME_FILE
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv4 " >> $LOG_FILE
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv4 " >> $TIME_FILE
			echo " "
			if ! /usr/bin/time -a -o $TIME_FILE -f "%e (sec) elapsed" wget -4 -a $LOG_FILE ftp://${REMOTE_4_ADDR}/${size}; then
				echo "wget -4 ftp://${REMOTE_ADDR}/${size} FAILED" | tee -a $LOG_FILE
				echo "`date +"%Y-%M-%d %H:%M:%S"`(0.0 KB/s) - ‘${size}’ saved [0] wget FAILS" | tee -a $LOG_FILE

			fi
			egrep "LOSS=| saved " $LOG_FILE | tail -2 
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv6  " >> $LOG_FILE
			echo -n "parameters SIZE=${size} LOSS=${loss} DELAY=${delay} PROTOCOL=IPv6  " >> $TIME_FILE
			if ! /usr/bin/time -a -o $TIME_FILE -f "%e (sec) elapsed" wget -6 -a $LOG_FILE ftp://[${REMOTE_6_ADDR}]/${size}; then
				echo "wget -6 ftp://${REMOTE_ADDR}/${size} FAILED" | tee -a $LOG_FILE
				echo "`date +"%Y-%M-%d %H:%M:%S"`(0.0 KB/s) - ‘${size}’ saved [0] wget FAILS" | tee -a $LOG_FILE
			fi
			echo " "
			date; egrep "LOSS=| saved " $LOG_FILE | tail -4
		done
	done
done
rm *.data
# Clean up - remove the classless qdisc
sudo tc qdisc delete dev $INTERFACE root netem
echo "Raw results in file $LOG_FILE .  Scrubbed results in $RESULTS_FILE"
egrep "saved|parameters" $LOG_FILE > $RESULTS_FILE
echo "RUnning results2MultiIndex.py"
python3 results2MultiIndex.py $RESULTS_FILE

exit 0
# Change TCP window size
# From https://netbeez.net/blog/how-to-adjust-the-tcp-window-size-limit-on-linux/
#echo 'net.core.wmem_max=4194304' &gt;&gt; /etc/sysctl.conf
#echo 'net.core.rmem_max=12582912' &gt;&gt; /etc/sysctl.conf
#echo 'net.ipv4.tcp_rmem = 4096 87380 4194304' &gt;&gt; /etc/sysctl.conf
#echo 'net.ipv4.tcp_wmem = 4096 87380 4194304' &gt;&gt; /etc/sysctl.conf
sysctl -p
# Here are the details on the tc bug:
# [jeffs@smalldell ~]$ INTERFACE="enp0s25"
# [jeffs@smalldell ~]$ loss=0
# [jeffs@smalldell ~]$ delay=0.0
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss ${loss}%
# Illegal "loss percent" <=========
# [jeffs@smalldell ~]$ loss=0.000000001
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss ${loss}%
# [jeffs@smalldell ~]$ sudo tc qdisc show dev $INTERFACE
# qdisc netem 800d: root refcnt 2 limit 1000
# [jeffs@smalldell ~]$ loss=1
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss ${loss}%
# [jeffs@smalldell ~]$ sudo tc qdisc show dev $INTERFACE
# qdisc netem 800d: root refcnt 2 limit 1000 loss 1%
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0%
# Illegal "loss percent"
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.0%
# Illegal "loss percent"
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.01%
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 1.00%
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.00%
# Illegal "loss percent"
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss .00%
# Unknown loss parameter: .00%
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0%
# Illegal "loss percent"
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.0 %
# Illegal "loss percent"
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.01 %
# What is "%"?
# Usage: ... netem [ limit PACKETS ]
# [jeffs@smalldell ~]$ sudo tc qdisc replace dev $INTERFACE root netem delay $delay loss 0.01%
# [jeffs@smalldell ~]$ 

