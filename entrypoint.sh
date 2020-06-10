#!/bin/bash
source activate kddcup
exec python local_test.py $@
