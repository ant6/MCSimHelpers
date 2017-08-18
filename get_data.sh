#!/bin/bash

for f in *mm
do
  echo "Processing $f"
  cd $f/output
  cp cydos1.dat ../../$f.dat
  cp cydos1.png ../../$f.png
  cd ../..
done
