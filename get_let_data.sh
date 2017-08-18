#!/bin/bash

for f in *mm
do
  echo "Processing $f"
  cd $f/output
  cp tlet1.dat ../../$f-tlet.dat
  cp dletg1.dat ../../$f-dletg.dat
  
  cp tlet1.png ../../$f-tlet.png
  cp dletg1.png ../../$f-dletg.png
  cd ../..
done
