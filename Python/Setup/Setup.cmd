SET PythonPath=C:\Python\Python310
SET PATH=%PATH%;%PythonPath%;%PythonPath%\Scripts;%PythonPath%\Lib
ECHO OFF
CD %PythonPath%
ECHO Installing pip
REM %PythonPath%\python get-pip.py
ECHO Upgrading Pip:  
%PythonPath%\python -m pip install -U pip
ECHO Installing xlsxwriter
%PythonPath%\python -m pip install xlsxwriter
ECHO Installing numpy
%PythonPath%\python -m pip install numpy
ECHO Installing pandas
%PythonPath%\python -m pip install pandas
ECHO Installing python-dateutil
%PythonPath%\python -m pip install python-dateutil
ECHO Installing xlrd
%PythonPath%\python -m pip install xlrd
ECHO Installing tqdm
%PythonPath%\python -m pip install tqdm
ECHO Updating
%PythonPath%\python -m pip install xlsxwriter -U
ECHO upgrade numpy
%PythonPath%\python -m pip install numpy -U
ECHO upgrade pandas
%PythonPath%\python -m pip install pandas -U
ECHO upgrade python-dateutil
%PythonPath%\python -m pip install python-dateutil -U
ECHO upgrade xlrd
%PythonPath%\python -m pip install xlrd -U
ECHO upgrade tqdm
%PythonPath%\python -m pip install tqdm -U