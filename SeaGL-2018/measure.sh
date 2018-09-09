#! /bin/bash
#
# This bashscript makes measurements of how long it takes to
# down load files for different combinations of packet loss
# rate and file size

iptable() {
  command=$1
  P=$2
  if [ "X${command}" = "X-L"; then
    sudo iptables ${command} INPUT -m statistic --mode random --probability ${P}
  else
    sudo iptables ${command} INPUT -m statistic --mode random --probability ${P} -j DROP
  fi
}


REMOTE="commercialventvac.com"
REMOTE_4=`host -t A $REMOTE`
REMOTE_4S=($REMOTE_4)
REMOTE_4_ADDR=${REMOTE_4S[3]}
REMOTE_6=`host -t AAAA $REMOTE`
REMOTE_6S=($REMOTE_6)
REMOTE_6_ADDR=${REMOTE_6S[4]}
echo "Remote $REMOTE has IPv4 address $REMOTE_4_ADDR and IPv6 address $REMOTE_6_ADDR"
date
for P in 0.0 0.01 1.00; do
  # For more documentation on -m statistic extension, see man iptables-extensions
  # statistic is a module  There two modes, random and nth.  --probability only works
  # with --mode random, and its argument must be between 0.0 and 1.0
  # --every n matches one packet every nth packet.  It only works with --mode nth.
  iptable -L $P
  iptable -A $P 
  for filename in 1000.txt 10000000.txt; do
    for family in "-4" "-6"; do
      if [ "X${family}" = "X-4" ]; then
         REMOTE_ADDR=${REMOTE_4_ADDR}
      else
         REMOTE_ADDR=${REMOTE_6_ADDR}
      fi
      echo "Family $family Remote address $REMOTE_ADDR"
      for protocol in http https ftp; do
        # FLUSH the counters
        sudo ip $family -oneline -s tcp_metrics flush address $REMOTE_ADDR
        echo "probability $P filename $filename family $family protocol $protocol remote address ${REMOTE_ADDR} "
        time wget $family --no-check-certificate ${protocol}://${REMOTE}/$filename
        # Get statistics on the tcp_metrics 
        # See man ip-tcp_metrics
        # SHOW the counters
        ip $family -oneline -stats -details tcp_metrics show address $REMOTE_ADDR
      done
    done
  done
  # Delete the optable entry
  iptable -D $P
done
    
