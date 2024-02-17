SET PythonRoot=C:\ZPW\Stage\Code\Python\RunTime\python-3.12
SET PYTHONCODEPATH=C:\ZPW\Stage\Code\Modules
SET PythonInstallDir=C:\ZPW\Stage
SET PythonVersion=python-3.12
SET PATH=%PATH%;%PythonRoot%;%PythonRoot%\Scripts;%PythonRoot%\Lib
cd C:\ZPW\Stage
%PythonRoot%\python.exe %PYTHONCODEPATH%\Lezen_Stage_3.00-Full.py
%PythonRoot%\python.exe %PYTHONCODEPATH%\GetAndProcessReportData.py