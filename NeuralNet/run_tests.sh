#!/bin/sh
nb_tests=`ls tests/test*.txt | wc -l`
for i in `seq 1 $nb_tests`
do
  echo " ====== Running test $i ====="
  if [ -f tests/result${i}.txt ]
  then
    echo " * Skipping - already ran * "
  else
    unbuffer python main.py train tests/test${i}.txt | tee tests/result${i}.txt
  fi
done

