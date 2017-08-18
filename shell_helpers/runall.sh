#!/bin/bash

for f in run*
do
  echo "Processing $f"
  bash $f/submit.sh
done
