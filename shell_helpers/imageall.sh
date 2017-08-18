#!/bin/bash

for f in run*
do
  echo "Processing $f"
  cd $f/output
  convertmc image --many "*.bdo"
  convertmc plotdata --many "*.bdo"
  cd ../..
done
