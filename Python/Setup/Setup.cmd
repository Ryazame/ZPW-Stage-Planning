SET PythonPath=C:\ZPW\Stage\Python\RunTime\python-3.12
SET PATH=%PATH%;%PythonPath%;%PythonPath%\Scripts;%PythonPath%\Lib
ECHO OFF
CD %PythonPath%
ECHO Upgrading Pip:  
python -m pip install -U pip
ECHO Installing xlsxwriter
python -m pip install xlsxwriter
ECHO Installing numpy
python -m pip install numpy
ECHO Installing pandas
python -m pip install pandas
ECHO Installing python-dateutil
python -m pip install python-dateutil
ECHO Installing xlrd
python -m pip install xlrd
ECHO Installing tqdm
python -m pip install tqdm
ECHO Updating
python -m pip install xlsxwriter -U
ECHO upgrade numpy
python -m pip install numpy -U
ECHO upgrade pandas
python -m pip install pandas -U
ECHO upgrade python-dateutil
python -m pip install python-dateutil -U
ECHO upgrade xlrd
python -m pip install xlrd -U
ECHO upgrade tqdm
python -m pip install tqdm -U
ECHO upgrade openpyxl
python -m pip install openpyxl -U