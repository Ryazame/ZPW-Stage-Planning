import pandas as pd
import re
import os
from tqdm import tqdm
from XLSX import WriteXLSX
from DBProcessor import DebugLogger as l
log=l.CreateLog()

def GetWZCs(DataSet): 
    df1 = DataSet
    df1.columns = [c.replace(' ', '_') for c in df1.columns]
    df1.columns = [c.replace('-', '_') for c in df1.columns]
    WZCs = df1.WCZ.unique().tolist()
    #df.values.tolist()
    log.debug('|--> WCZ data beschikbaar om mee te werken...')
    return WZCs

def GetMaandenSet(Year):
    MaandenSet = pd.DataFrame({'ProcessID':[1,2,3,4,5,6,7,8,9,10,11,12],
                            'MaandID':[7,8,9,10,11,12,1,2,3,4,5,6],
                            'Maand_Jaar':['juli '+str(Year),'augustus '+str(Year),'september '+str(Year),'oktober '+str(Year),'november '+str(Year),'december '+str(Year),
                                            'januari '+str(int(Year)+1),'februari '+str(int(Year)+1),'maart '+str(int(Year)+1),'april '+str(int(Year)+1),
                                            'mei '+str(int(Year)+1),'juni '+str(int(Year)+1)]})
    #MaandenSet = MaandenSet.apply(pd.to_numeric, downcast='integer', errors='ignore')
    return MaandenSet

def GetMaanden(DataSet,MaandenSet):
    Maanden = pd.to_numeric(DataSet['Maand'], downcast='integer',errors='ignore').unique()
    Maanden = pd.DataFrame({'MaandID': Maanden[:,]})
    Maanden = pd.merge(Maanden, MaandenSet,how='left', on='MaandID')
    Maanden.set_index('ProcessID', inplace=True)
    Maanden.sort_index(inplace=True)
    log.debug('|--> Maand/Jaar data beschikbaar om mee te werken...')
    return Maanden

def CleanupScholen(DataSet,ReplaceDict,CorrectDict):
    DataSet = DataSet.replace({"School": ReplaceDict}, regex=True).replace({"School": CorrectDict}, regex=True)
    DataSet['School']=DataSet['School'].str.lower()
    return DataSet

def FormatDataSetforXLSX(DataSet):
    ######################################
    # Reorder the dataset to allign conform the XLS Sheet

    DataSet = DataSet[['ID','Status','Naam_student','School','Studierichting_stage','Studiejaar_Module','Specialisatie','stage_uren',\
                        '1','2','3','4','5','6','7','8','9','10',\
                        '11','12','13','14','15','16','17','18','19','20',\
                        '21','22','23','24','25','26','27','28','29','30','31',\
                        'Maand','WCZ','Naam_aanvrager','Email_aanvrager','Tel_aanvrager',\
                        'Voorkeursafdeling','stage_dagen','uren_per_dag','Jaar']]
    log.debug('|--> Data geconfigureerd zoals in de Excel gewenst is...')
    return DataSet

def ProcessWCZ(WZCs,Year,xls_path,DataSet,Maanden):
    log.info('|--> Start processing WZCs...')
    #for WZC in tqdm(range(WZCs), colour="BLUE", desc="Loading WZCs..."):
    WZCList=WZCs
    for WZC in tqdm(WZCList, colour="BLUE", desc="Loading WZCs...   "):
        log.debug('|--->   We werken nu voor : '+WZC)
        FileName  = xls_path+str(Year)+'-'+str(int(Year)+1)+'_'+WZC+'.xlsx'
        Sheet = DataSet
        ######################################
        # Creating the file
        
        writer = pd.ExcelWriter(FileName, engine='xlsxwriter')

        for index, row in Maanden.iterrows():
            SheetName = str(row['Maand_Jaar']).replace(' ', '_')
            Maand_Jaar = row['Maand_Jaar']
            
            Maand_Jaar = str(Maand_Jaar)
            if Maand_Jaar == 'nan':
                log.debug('|----->   Found Nan')
            else:
                MaandID = row['MaandID']
                log.debug('|----->   We verwerken nu data voor: '+Maand_Jaar)
                
                ######################################
                # Filter the data before writing to the Excell sheet
                output = DataSet.loc[DataSet['Maand'] == MaandID]
                output = output.loc[output['WCZ'] == WZC]
                output = output.sort_values(by=['Studierichting_stage','ID'])
                output = output.drop(['WCZ','Maand','Jaar'], axis=1)
                ######################################
                # Write the data to the Excell sheet
                WriteXLSX.ExcelMarkup(output,Maand_Jaar,writer,SheetName)
            
        ######################################
        # Closing the file
        writer.close()
        log.debug('|---> File: '+FileName+' aangemaakt')

def ProcessScholen(ScholenList,DataSet,xls_scholen_Path,Maanden):
    log.info('|--> Start processing Scholen...')
    for school in tqdm(ScholenList, colour="YELLOW", desc="Loading scholen..."):
        #SchoolIndex = school['School']
        SchoolData = DataSet.loc[DataSet['School'] == school]
        SchoolData = SchoolData.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        School = school.strip()
        School = School.replace('-','_').replace(' ','_').replace('_bachelor','').replace('_brugopleiding','').replace('Hogeschool_Gent','HOGent').replace('HO_Gent','HOGent').replace('(in_het_kader_van_TWE)','').replace('Artevelde_HOGent','Artevelde').replace('__','_') 
            
        ############################################
        # Creëer de Contact DataSet
        Email_aanvrager = SchoolData.Email_aanvrager.map(lambda x:x.strip()).unique()
        Email_aanvrager = pd.DataFrame(Email_aanvrager)
        if not Email_aanvrager.empty:
            log.debug('|-->   We rapporteren nu voor : '+School)
            School_Path = xls_scholen_Path+'\\'+School
            Email_aanvrager.columns = ['Email_aanvrager']
            Email_aanvrager = Email_aanvrager[Email_aanvrager.Email_aanvrager.str.len().fillna(0)>1]
            Email_aanvrager = Email_aanvrager.Email_aanvrager.map(lambda x:x.strip()).unique()
        
            log.debug('|--->   Er is contact data beschikbaar om mee te werken...')
            #for contact in tqdm(Email_aanvrager, colour="CYAN", desc="Loading contacten..."):
            for contact in Email_aanvrager:
                log.debug('|---->   We creëren een rapport voor : "'+contact+'"')
                contactnaam = contact.strip().replace(' ', '_').replace('.', '_').replace('@', '_at_').replace('-', '_')
                contactnaam = re.sub('[^\w\-_\. ]', '_', contactnaam).replace('_at_', '@').strip()
                if not os.path.exists(School_Path):
                    os.makedirs(School_Path)
                    log.debug('|---> Created Folder: '+School_Path)
                School_File_Path = School_Path+'\\'+School.strip()+'_'
                FileName = School_File_Path+'_'+contactnaam+'.xlsx'
                log.debug('|---->   We creëren de file : "'+FileName+'"')
                writer = pd.ExcelWriter(FileName, engine='xlsxwriter')

                for index, row in Maanden.iterrows():
                    SheetName = str(row['Maand_Jaar']).replace(' ', '_')
                    Maand_Jaar = row['Maand_Jaar']
                    Maand_Jaar = str(Maand_Jaar)
                    if Maand_Jaar == 'nan':
                        print('|----->   Found Nan')
                    else:
                        MaandID = row['MaandID']
                        ######################################
                        # Write the data
                        output = SchoolData.loc[SchoolData['Email_aanvrager'] == contact]
                        output = output.loc[output['Maand'] == MaandID]
                        #output = output.drop(['Email_aanvrager'], axis=1)
                        output = output.drop(['Tel_aanvrager','Jaar'], axis=1)
                        
                        ######################################
                        # Write the data to the Excell sheet
                        #WriteXLSX.ExcelMarkup(output,MaandID,WZC)
                        WriteXLSX.ExcelMarkup(output,Maand_Jaar,writer,SheetName)
                ######################################
                # Closing the file
                writer.close()
                log.debug('|---->   File : '+FileName+' aangemaakt')
    log.info('________________________________________________________________________________________________')