SET PythonPath=C:\ZPW\Stage\Python\RunTime\python-3.12
SET PATH=%PATH%;%PythonPath%;%PythonPath%\Scripts;%PythonPath%\Lib
ECHO OFF
CD %PythonPath%
ECHO Upgrading Pip:  
python -m pip install -U pip
ECHO Installing xlsxwriter
python -m pip install xlsxwriter==3.1.9
ECHO Installing numpy
python -m pip install numpy==1.26.4
ECHO upgrade pyarrow
python -m pip install pyarrow==15.0.0
ECHO Installing pandas
python -m pip install pandas==2.2.0
ECHO Installing python-dateutil
python -m pip install python-dateutil==2.8.2
ECHO Installing xlrd
python -m pip install xlrd==2.0.1
ECHO Installing tqdm
python -m pip install tqdm==4.66.1
ECHO upgrade openpyxl
python -m pip install openpyxl==1.1.0
