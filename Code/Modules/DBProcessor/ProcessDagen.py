import pandas as pd
import time, datetime
import logging
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from DBProcessor import DebugLogger as l
log=l.CreateLog()
#log.setLevel(logging.DEBUG)
from tqdm import tqdm
from DBProcessor import WriteDFToDB
def GetDFDagen(df):
    df_Dagen=df[['ID',
'1 ste Stagedag','2 de Stagedag','3 de Stagedag','4 de Stagedag','5 de Stagedag',
'6 de Stagedag','7 de Stagedag','8 ste Stagedag','9 de Stagedag','10 de Stagedag',
'11 de Stagedag','12 de Stagedag','13 de Stagedag','14 de Stagedag','15 de Stagedag',
'16 de Stagedag','17 de Stagedag','18 de Stagedag','19 de Stagedag','20 ste Stagedag',
'21 ste Stagedag','22 ste Stagedag','23 ste Stagedag','24 ste Stagedag','25 ste Stagedag',
'26 ste Stagedag','27 ste Stagedag','28 ste Stagedag','29 ste Stagedag','30 ste Stagedag',
'31 ste Stagedag','32 ste Stagedag','33 ste Stagedag','34 ste Stagedag','35 ste Stagedag',
'36 ste Stagedag','37 ste Stagedag','38 ste Stagedag','39 ste Stagedag','40 ste Stagedag',
'41 ste Stagedag','42 ste Stagedag','43 ste Stagedag','44 ste Stagedag','45 ste Stagedag',
'46 ste Stagedag','47 ste Stagedag','48 ste Stagedag','49 ste Stagedag','50 ste Stagedag']]
    return df_Dagen
def ProcessHeaders(df_Dagen): 
    EmptyFrame = False
    log.debug('|--> create a list of all the columns')
    columns = list(df_Dagen)
    log.debug('|--> create lists to hold headers & months')
    headers = []
    days = []
    log.debug('|--> split columns list into headers and months')
    for col in columns:
        if col.endswith('Stagedag'):
            days.append(col)
        else:
            headers.append(col)
    return days,headers

def ProcesDag(df_Dagen,headers,days):
    log.debug('|--> Creating Date columns')
    D_Dag=pd.melt(df_Dagen,id_vars=headers,value_vars=days,var_name='Comment',value_name='Date')
    D_Dag = D_Dag[D_Dag.Date != 0]
    D_Dag = D_Dag.drop(['Comment'], axis=1)
    D_Dag['Dagen']=D_Dag['Date'].astype('datetime64[ns]')
    del D_Dag['Date']
    D_Dag['Dag']=D_Dag['Dagen'].dt.day
    D_Dag['Maand']=D_Dag['Dagen'].dt.month
    D_Dag['Jaar']=D_Dag['Dagen'].dt.year
    D_Dag['IngeSchreven']=1
    return D_Dag

def CreateMonthFrame(Inputdf,MaandNr,Jaar):
    Query = 'Maand=='+str(MaandNr)+' and Jaar=='+str(Jaar)
    df = Inputdf.query(Query)
    return df

def CreateMonthResult(Year,D_Dag):
    columns = ['ID',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
    todays_date = datetime.datetime.now().date()
    index = pd.date_range(todays_date-datetime.timedelta(10), periods=10, freq='D')
    MaandResultaat = pd.DataFrame(index=index, columns=columns)
    for Maand in tqdm(range(1,13), colour="green", desc="Loading maanden..."):
        time.sleep(0.5)
        if Maand < 7:
            Jaar = str(int(Year)+1)
        else:
            Jaar = str(Year)
        log.debug('|--> Verwerken van de maandgegevens voor maand nr.: '+str(Maand)+'...')
        MonthFrame = CreateMonthFrame(D_Dag,Maand,Jaar)
        if not MonthFrame.empty:
            DatumResultaat = pd.DataFrame([]).fillna(0)
            DatumResultaat = MonthFrame.pivot(index='ID', columns='Dag', values='IngeSchreven')
            DatumResultaat['Maand']=Maand
            DatumResultaat['Jaar']=Jaar
            DatumResultaat['ID']=DatumResultaat.index
            #MaandResultaat = pd.concat([MaandResultaat,DatumResultaat]).fillna(0)
            if not MaandResultaat.empty and not DatumResultaat.empty:
                MaandResultaat = pd.concat([MaandResultaat, DatumResultaat], axis=0)
            else:
                MaandResultaat = pd.DataFrame()
            # Fill any remaining NaN values with 0
            MaandResultaat.fillna(0, inplace=True)
            #MaandResultaat=MaandResultaat.infer_objects(copy=False).fillna(0, inplace=True)
    MaandResultaat=MaandResultaat.apply(pd.to_numeric)
    log.debug('|--> Dataframe genormaliseerd')
    return MaandResultaat
    
def WriteMaandToDB(ProcessDelta,Year,db,df_Data,cf,D_Dag):
    MaandResultaat=CreateMonthResult(Year,D_Dag)
    DataSet = pd.merge(df_Data, MaandResultaat,how='left', on=['ID'])
    DataSet = pd.merge(cf,DataSet,how='inner', on=['ID'])
    SchemaDataSet = 'Schema_Dataset_'+str(int(Year)+1)
    if ProcessDelta:
        WriteDFToDB.DFToDB(df=DataSet,db=db,Schema=SchemaDataSet,if_exists='append')
        log.debug('|--> Delta Dataframe opgeslagen in de database')
    else:
        WriteDFToDB.DFToDB(df=DataSet,db=db,Schema=SchemaDataSet,if_exists='replace')
        log.info('|--> Dataset met maandresultaten opgeslagen in de database')
    return SchemaDataSet