SET PythonRoot=C:\ZPW\Stage\Python\RunTime\python-3.12
SET PYTHONPATH=C:\ZPW\Stage\Modules
SET PythonInstallDir=C:\ZPW\Stage
SET PythonVersion=python-3.12
SET PATH=%PATH%;%PythonRoot%;%PythonRoot%\Scripts;%PythonRoot%\Lib
cd C:\ZPW\Stage
%PythonRoot%\python.exe %PythonInstallDir%\Modules\Lezen_Stage_3.00-Full.py
%PythonRoot%\python.exe %PythonInstallDir%\Modules\GetAndProcessReportData.py