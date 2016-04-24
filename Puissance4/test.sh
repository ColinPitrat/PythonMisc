#!/bin/sh

(
for i in `seq 1 6`
do
    echo -n "hori$i: "
    python2 Puissance4.py hori$i fast
done

for i in `seq 1 6`
do
    echo -n "vert$i: "
    python2 Puissance4.py vert$i fast
done

for i in `seq 1 6`
do
    echo -n "mont$i: "
    python2 Puissance4.py mont$i fast
done

for i in `seq 1 6`
do
    echo -n "desc$i: "
    python2 Puissance4.py desc$i fast
done

for i in `seq 1 4`
do
    echo -n "mixv$i: "
    python2 Puissance4.py mixv$i fast
done

for i in `seq 1 8`
do
    echo -n "mixh$i: "
    python2 Puissance4.py mixh$i fast
done

for i in `seq 1 8`
do
    echo -n "mixm$i: "
    python2 Puissance4.py mixm$i fast
done

for i in `seq 1 6`
do
    echo -n "mixd$i: "
    python2 Puissance4.py mixd$i fast
done
) | tee /tmp/result.log

diff /tmp/result.log result.txt
if [ $? -eq 0 ] 
then
    echo " == Tests OK =="
fi
