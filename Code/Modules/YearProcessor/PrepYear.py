import configparser
def GetParamsFromConfig(Year):
    FilePath="""C:\\ZPW\\Stage\\Code\\Modules\\config\\{}.ini""".format(Year)
    config = configparser.ConfigParser()
    config.read(FilePath)
    year=config["GENERAL"]["year"]
    RootDrive = config["STORAGEPARAMETERS"]["RootDrive"]
    FormFileNaam = config["STORAGEPARAMETERS"]["FormFileRootNaam"]
    BackupPath=config["STORAGEPARAMETERS"]["BackupPath"]
    ProcessDelta=config["PROCESSPARAMS"]["ProcessDelta"]
    return year,RootDrive,FormFileNaam,BackupPath,ProcessDelta
