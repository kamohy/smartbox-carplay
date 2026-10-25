#!/bin/sh
#LY_BOOT_MODE=$1
#LY_DEBUG_MODE=$2

echo "WORKDIR=$WORKDIR"

if [ $LY_BOOT_MODE == 'update' ];then
	rm -fr /mnt/UDISK/ly_linktype_aa
fi
mkdir -p /tmp/app

lypack d $WORKDIR/lylink /tmp/app
if [ -f /mnt/UDISK/ly_linktype_aa ];then
	date -s "2024-11-28 10:00:00"
	cp -H $WORKDIR/raaservice \
		$WORKDIR/mtpservice \
		$WORKDIR/libcrypto.so.1.1 \
		$WORKDIR/libssl.so.1.1 \
		$WORKDIR/liblylinkmw.so.1 \
		$WORKDIR/libprotobuf-c.so.1 \
		$WORKDIR/my.ttf /tmp/app/

	rm /tmp/app/libr*.so /tmp/app/rc*
	ln -s $WORKDIR/logo /tmp/raaui
	ln -s $WORKDIR/raa.crt /tmp/app/
	$WORKDIR/lyUpdate.sh $WORKDIR &
	cp $WORKDIR/lyLoadModule.sh /tmp/
	/tmp/lyLoadModule.sh $LY_BOOT_MODE &
	raaservice -B -w -d
else
	echo "run carplay mode"
	chmod 755 /tmp/app/rcpservice


	echo " run mdnsd"
	logwrapper mdnsd &
	
	cp -Hr $WORKDIR/libdns_sd.so \
		$WORKDIR/my.ttf \
		$WORKDIR/logo /tmp/app/

	

	echo " run ly_testcp"
	logwrapper ly_testcp -f=2 &

	echo " run rcpservice"
	if [ -f /tmp/app/rcpservice ];then
	nice -n -9 /tmp/app/rcpservice > /dev/null 2>&1 &
	else
	nice -n -9 $WORKDIR/rcpservice > /dev/null 2>&1 &
	fi

	$WORKDIR/lyUpdate.sh $WORKDIR &

	cp $WORKDIR/lyLoadModule.sh /tmp/
	/tmp/lyLoadModule.sh $LY_BOOT_MODE &

	trial=0
	myFile="/tmp/lyrcpok"
	while [ ! -f "$myFile" ] && [ $trial -le 50 ]
	do 
	    sleep 0.1
	    trial=$(($trial + 1 ))
	done

	echo " run lylinkapp"
	nice -n -15 $WORKDIR/lylinkapp -w &
fi


echo 3 > /proc/sys/vm/drop_caches

# Bad-Hippo 0.9.1: run recorder from RAM, with no working directory on customer.
if [ "$LY_BOOT_MODE" != update ] && [ -x "$WORKDIR/bh-log-recorder.sh" ]; then
    if cp "$WORKDIR/bh-log-recorder.sh" /tmp/bh-recorder.sh && chmod 755 /tmp/bh-recorder.sh; then
        (cd / && exec /tmp/bh-recorder.sh run) >/dev/null 2>&1 &
    fi
fi


