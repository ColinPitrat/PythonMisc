cat tests.txt | while read line 
do 
    temps=`(time echo $line | python2 AdditionMystereGeneriqueAcceleree.py ) 2>&1 | grep real | sed 's/real//'`
    echo "$temps - $line"
done 
