import sys
sys.path.append(r'C:\ZPW\Stage\Code\Modules')
#Import Program Modules
from YearProcessor import PrepYear, Backup,ProcessData
#from StringFunctions import MultiReplacer
from XLSX import ReadXLSX#,WriteXLSX
from DBProcessor import WriteDFToDB,ReadInputData,ProcessDagen,Queries
from DBProcessor import DebugLogger as l

#Import Native Modules
import json
import warnings
import sqlite3
import datetime
import os

log=l.CreateLog()
Current_Year = datetime.date.today().year
Current_Month = datetime.date.today().month
log.info('________________________________________________________________________________________________')
log.info('| * Running in year: {}'.format(Current_Year))
log.info('| * Running in month: {}'.format(Current_Month))
if Current_Month > 0 and Current_Month < 7:
    Current_Year=int(Current_Year)-1
else:
    Current_Year=int(Current_Year)
log.info('| * Schooljaar : {0}'.format(str(int(Current_Year))+' - '+str(int(Current_Year)+1)))
Year,RootDrive,FormFileNaam,BackupPath,ProcessDelta=PrepYear.GetParamsFromConfig(Current_Year)

ExcellFile = '{0}Input\\{1}'.format(RootDrive,FormFileNaam)
xls_path = '{0}OutPut\\{1}\\Stage_Output_'.format(RootDrive,Year)
xls_scholen_Path = '{0}OutPut\\{1}\\School\\'.format(RootDrive,Year)
CorrectieFile = '{0}Goedkeuringen\\Stage-Goedkeuring-{1}.xlsx'.format(RootDrive,Year)
DBFilePath = "{0}Code\\Database\\Dataset_{1}.sqlite".format(RootDrive,Year)
dt_date = datetime.datetime.now()
BackupDate = dt_date.strftime('%Y-%m-%d')
log.info('|--- De gebruikte programma settings zijn:')
log.info('| * Inputfile:{0}'.format(ExcellFile))
log.info('| * Outputfiles : {0}*.xlsx'.format(xls_path))
log.info('| * Database : {0}'.format(DBFilePath))
log.info('| * School Files : {0}[School]\\[Contact]-ReportFile*.xlsx'.format(xls_scholen_Path))
log.info('| * Correctie File : {0}'.format(CorrectieFile))
log.info('|--- Start Programma')
log.info('________________________________________________________________________________________________')

log.debug('|> Opening JSON files')
try:
    with open("""C:\\ZPW\\Stage\\Code\\Modules\\JSON\\CorrectDict.JSON""") as json_file:
        CorrectDict = json.load(json_file)
except:
    CorrectDict = {
"-": "_",
" ": "_",
"__": "_",
"()": ""
}
try:
    with open("""C:\\ZPW\\Stage\\Code\\Modules\\JSON\\ReplaceDict.JSON""") as json_file:
        ReplaceDict = json.load(json_file)
except:
    ReplaceDict = {
    "bachelor": "",
    "brugopleiding": "",
    "Artevelde Hogeschool Gent": "Artevelde",
    "Hogeschool Gent": "HOGent",
    "HO_Gent": "HOGent",
    "(in het kader van TWE)": "",
    "gent": "Gent"
}

log.debug('|> Creating Outputdir')
OutPathDir=RootDrive+'OutPut\\{0}'.format(Year)
if not os.path.exists(OutPathDir):
    os.makedirs(OutPathDir)
    log.info('"{}" Directory made...'.format(OutPathDir))
if not os.path.exists(xls_scholen_Path):
    os.makedirs(xls_scholen_Path)

log.debug('|> Connect to DB')
db = sqlite3.connect(DBFilePath)
log.info('Connected to database: "{0}"'.format(DBFilePath))
MaxID = 0

log.debug('|> Setting Warnings filter...')
warnings.filterwarnings('ignore','.*',UserWarning)


log.debug('|> Reading XLSX File to df & DB')
df = ReadXLSX.ReadInputFile(ExcellFile)
df_Data=ReadInputData.ReadDfData(df)
WriteDFToDB.DFToDB(df=df_Data,db=db,Schema='Schema_InputFile',if_exists='replace')

log.debug('|> Get dagen from ExcellFile')
df_dagen=ProcessDagen.GetDFDagen(df)
days,headers=ProcessDagen.ProcessHeaders(df_dagen)

log.debug('|> Create D_Dag df without doubles')
D_Dag=ProcessDagen.ProcesDag(df_dagen,headers,days)
WriteDFToDB.DFToDB(df=D_Dag,db=db,Schema='Schema_D_Dag',if_exists='replace')
D_Dag=Queries.VerwijderDagDubbels(db=db)
log.debug('|-> Eventuele dubbels verwijderd uit de Dataset')

log.debug('|> Read Corrections from Correction Excel file & Backup this file')
cf = ReadXLSX.ReadCorrectieFile(CorrectieFile)
WriteDFToDB.DFToDB(df=cf,db=db,Schema='Schema_CorrectieFile',if_exists='replace')
BackupFUllPath='{0}{1}-CorrectieFile-{2}.xlsx'.format(BackupPath,BackupDate,Year)
Backup.MakeDfBackup(cf,BackupFUllPath)

log.debug('|> Process the the input data and push it to the DB')
SchemaDataSet=ProcessDagen.WriteMaandToDB(False,Year,db,df_Data,cf,D_Dag)
DataSet=Queries.GetResultsFromDB(SchemaDataSet,Year,False,db)
if not DataSet.empty:
    EmptyFrame=False
    log.info('|--> Data to work with... Processing')
else:
    EmptyFrame = True
    log.warning('|--> No data to work with... Stopping')

if not EmptyFrame:
    log.debug('|-> Cleanup the school names and get the unique schools and write back to DB')
    Scholen=Queries.GetScholen(db,SchemaDataSet,ReplaceDict,CorrectDict)
    DataSet=ProcessData.CleanupScholen(DataSet,ReplaceDict,CorrectDict)
    WriteDFToDB.DBCloseAndCommit(db)
    log.debug('|-> Get the unique WCZs from Dataset')
    WZCs=ProcessData.GetWZCs(DataSet)
    log.debug('|-> Get the unique Months from Dataset')
    MaandenSet=ProcessData.GetMaandenSet(Year)
    Maanden=ProcessData.GetMaanden(DataSet,MaandenSet)
    log.debug('|-> Reorder the dataset to allign conform the XLS Sheet')
    DataSet=ProcessData.FormatDataSetforXLSX(DataSet)
    log.debug('|-> Process all the data for the WCZs for all known months...')
    ProcessData.ProcessWCZ(WZCs,Year,xls_path,DataSet,Maanden)
    log.debug('|-> Process all the data for the Scholen for all known months...')
    ProcessData.ProcessScholen(Scholen,DataSet,xls_scholen_Path,Maanden)