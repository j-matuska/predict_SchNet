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
Install requirements (obsolete)
```
pip install -r requirements.txt
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
python3 /path/to/predict.py [-h] [--model MODEL] [--splits  '01 ...',] [--device DEVICE] [--output FORMAT] XYZ file

positional arguments:
  XYZ file              Full name of xyz file in extended xyz file format containing structure of the molecules.

options:
  -h, --help            show this help message and exit
  --model MODEL         Optional choise of the pretrained NN model. Default: 'Schnet03_6_10Ang_train80'
  --splits  '01 ...',   Optional choise of cross-validation instance from the pretrained NN model. Separated by space. Default: '01 02 03 04 05'
  --device DEVICE       Optional choise of the computer resource. Default: 'cpu'
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
