#!/bin/sh

nb_tests=`ls tests/test*.txt | wc -l`

# Check consistency of all network files with their tests files
for i in `seq 1 $nb_tests`
do
  test_file="tests/test${i}.txt"
  network_file=`head -n 1 "$test_file"`
  expected="tests/network${i}.txt"
  if [ "$network_file" -ne "$expected" ]
  then
    echo "ERROR: Expected '$expected' network file in '$test_file', got '$network_file'"
    exit 1
  fi
done

for i in `seq 1 $nb_tests`
do
  test_file="tests/test${i}.txt"
  result_file="tests/result${i}.txt"
  echo " ====== Running test $i ====="
  if [ -f "$result_file" ]
  then
    echo " * Skipping - already ran * "
  else
    unbuffer python main.py train "$test_file" | tee "$result_file"
  fi
done

