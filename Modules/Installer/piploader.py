import pip._internal as pip

def LoadModules(package):
    pip.main(['install', package])


LoadModules("xlsxwriter")
LoadModules("numpy")
LoadModules("pandas")
LoadModules("python-dateutil")
LoadModules("xlrd")
LoadModules("tqdm")
