#! /bin/bash

# First argument have to be properly set up python environment e.g. ~/.venv/bin/activate


# predict by predict.py
if [[ -r $1 ]] ; then
   source $1;
   else echo "None environment to set up"
fi;

if [[ -e ../predict.py ]] ; then 
    predict.py --model Schnet20_6_5Ang_train80 --splits '01 02 03 04 05' --mode serial --output expected_predicted in_vitro.xyz;
    else
       echo "Missing predict.py" ;
fi;
# evaluate by evaluate.py

if [[ -e evaluation.py ]] ; then
    python3 evaluation.py;
    else
        echo "Missing evaluation.py";
fi;
