#!/bin/bash

# This script is used to run the unit tests for the registration tracker app.
declare -a controllers=(
[0]=advisors_cont
[1]=students_cont
[2]=courses_cont
[3]=semesters_cont
[4]=prerequisites_cont
[5]=plans_cont
[6]=majors_cont
[7]=concentration_cont
)

for controller_idx in $(seq 0 $((${#controllers[@]}-1)));
do
    echo 'Running unit tests for controller: '${controllers[$controller_idx]}
    python test_${controllers[$controller_idx]}.py
    echo
done
