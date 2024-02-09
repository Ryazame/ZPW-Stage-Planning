<h2>Compiling</h2>


This program is written to assist the ZPW Planning department in handling the reauests for interns.
How to/

First download Python Embedded 3.12 from https://www.python.org/downloads/windows/
Extract the contents of this zipfile into
C:\Git\ZPW-Stage-Planning\Python\RunTime\python-3.12
Alter the python312._pth file and uncomment the import line

it should look like this:

<code>python312.zip
.
import site
</code>

Now you can dowload the content of this repo and extract it into: C:\Git\
Using NSIS Edit you can now compile the installer.
You can download NSIS edit here: https://portableapps.com/apps/development/hm_nis_edit_portable

<h2>Installing</h2>
After compilation you should now have the file C:\Git\ZPW-Stage-Planning\Python\Setup\Setup ZPW Stageplanning.exe
