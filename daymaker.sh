#!/bin/bash
DAYNUM=$1
cp -R dayNUMBER day${DAYNUM}
mv day${DAYNUM}/dayNUMBER_solver.py day${DAYNUM}/day${DAYNUM}_solver.py
mv day${DAYNUM}/test_dayNUMBER_solver.py day${DAYNUM}/test_day${DAYNUM}_solver.py
sed -i '' "s/dayNUMBER/day${DAYNUM}/" "day${DAYNUM}/test_day${DAYNUM}_solver.py"