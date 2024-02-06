SET PythonInstallDir=C:\ZPW\Stage
SET PythonVersion=python-3.12
SET PythonPath=""
ECHO OFF
%PythonPath%\python.exe %PythonInstallDir%\Modules\Lezen_Stage_3.00-Full.py
REM %PythonPath%\python.exe %PythonInstallDir%\GenereerSubsidieDossier.py
%PythonPath%\python.exe %PythonInstallDir%\Modules\GetAndProcessReportData.py