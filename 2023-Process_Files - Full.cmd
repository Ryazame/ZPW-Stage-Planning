SET PythonPath=C:\ZPW\Stage\Python\RunTime\python-3.12
SET PythonInstallDir=C:\ZPW\Stage
SET PythonVersion=python-3.12
SET PATH=%PATH%;%PythonPath%;%PythonPath%\Scripts;%PythonPath%\Lib
cd C:\ZPW\Stage
%PythonPath%\python.exe %PythonInstallDir%\Modules\Lezen_Stage_3.00-Full.py
%PythonPath%\python.exe %PythonInstallDir%\Modules\GetAndProcessReportData.py