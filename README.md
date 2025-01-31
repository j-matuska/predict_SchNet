Script to predict docking score(DS) using neural network trained in SchNetPack 2.0

# Instalation

## Preparations
Create new python environment
```
python -m venv ~/.predict_SchNetPack
```
Folder`~/.predict_SchNetPack` can be changed to any path. Write access to parent folder have to be granted.

Install [SchNetPack](https://schnetpack.readthedocs.io/en/latest/index.html). For example:
```
git clone https://github.com/atomistic-machine-learning/schnetpack.git <dest_dir>
cd <dest_dir>
pip install .
```
## Core program

Download program
```
git clone https://github.com/j-matuska/predict_SchNet.git <dest_dir>
cd <dest_dir>
```
Install program
```
pip install .
```
# Usage

Activate python environment:
```
source ~/.predict_SchNetPack/bin/activate
```

Call predict.py
``` 
predict.py [-h] [--model MODEL] [--target TARGET] [--splits  '01 ...',] [--mode MODE] [--output FORMAT] XYZ file

Process comand-line inputs for predict.py.

positional arguments:
  XYZ file              Full name of xyz file in extended xyz file format containing structure of the molecules.

options:
  -h, --help            show this help message and exit
  --model MODEL         Optional choise of the pretrained NN model. Default: 'Schnet20_6_10Ang_train80'
  --target TARGET       Choise of variable name to predict (target name). Necessary in case of hte 'custom' model. Name have to be identical to name in XYZ file and custom model. Default: 'DS'
  --splits  '01 ...',   Optional choise of cross-validation instance from the pretrained NN model. Separated by space. Default: '01 02 03 04 05'
  --mode MODE           Optional choise of the computer resources. Mode 'serial' allocate 4 cpu and one graphic card. Mode 'parallel' aim to take all possible graphic cards (not fully functional).
                        Default: 'serial'
  --output FORMAT       Optional choise of the output format. Default: 'predicted'
```
This can be showed by `python3 /path/to/predict.py -h`

# Instalation verification

Extract file `in_vitro.xyz.tar.xz` in folder `./test`:
```
tar -xvxf in_vitro.xyz.tar.xz
```
Then run command 
```
bash ./test.sh  ~/.predict_SchNetPack/bin/activate
```
and follow the instructions.

# References

Please cite the folling references when using a given model:
* Schnet20_6_5Ang_train80 : J. Matúška, L. Bucinsky, M. Gall, M. Pitoňák, M. Štekláč.
J. Phys. Chem. 2024, B128(20) , 4943-4951.[https://doi.org/10.1021/acs.jpcb.4c00296](https://doi.org/10.1021/acs.jpcb.4c00296)
* Schnet20_6_10Ang_train80, Schnet03_6_10Ang_train80 : L. Bucinsky, M. Gall, J. Matúška, M. Pitoňák, M. Štekláč. 
Advances and critical assessment of machine learning techniques for prediction of docking scores. 
Int. J. Quantum Chem. 2023, 123(24), e27110. [https://doi.org/10.1002/qua.27110](https://doi.org/10.1002/qua.27110)
