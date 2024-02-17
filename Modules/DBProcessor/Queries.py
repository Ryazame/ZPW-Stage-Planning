import pandas as pd
from DBProcessor import WriteDFToDB
from DBProcessor import DebugLogger as l
log=l.CreateLog()

def VerwijderDagDubbels(db):
    DB_Correctie_query = """
    select 
        ID*1000000+Jaar*100+Maand as Key,
        ID,
        dag,
        Maand,
        Jaar,
        MAX(Ingeschreven) as IngeSchreven
    from Schema_D_Dag
    group by
        ID,
        dag,
        Maand,
        Jaar"""
    D_Dag = pd.read_sql_query(DB_Correctie_query,db)
    log.debug('|-> Eventuele dubbels verwijderd uit de DB')
    return D_Dag

def GetResultsFromDB(SchemaDataSet,Year,EmptyFrame,db):
    ###################################
    # Query om zowel de totalen als de detail 
    # Uit de dataset te halen
    DB_Correctie_query = """;with StageSet as
    (SELECT
        D."ID",
        D."Status",
        trim(COALESCE(C."Correctie WZC",D."Aanduiden keuze voor WZC")) as WCZ,
        trim(COALESCE(C.[Correctie Naam en Voornaam],D."Naam student")) as "Naam student",
        (trim(D."Naam van de school of onderwijsinstelling")) as School,
        D."Naam aanvrager" as Naam_aanvrager,
        trim(COALESCE(C.CorrectieEMail, D."E-mail adres aanvrager")) as "Email_aanvrager",
        D."Telefoonnummer aanvrager" as Tel_aanvrager,
        trim(COALESCE(C.CorrectieStage,D."Studierichting/stage")) as Studierichting_stage,
        D."Studiejaar / Module" as Studiejaar_Module,
        D."Specialisatie",
        D."Voorkeursafdeling",
        D."Totaal aantal stage uren" as stage_uren,
        D."Totaal aantal stage dagen" as stage_dagen,
        D."Aantal te presteren uren per stage dag" as uren_per_dag,
        D."Jaar",
        D."Maand",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."1" END "1",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."2" END "2",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."3" END "3",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."4" END "4",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."5" END "5",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."6" END "6",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."7" END "7",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."8" END "8",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."9" END "9",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."10" END "10",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."11" END "11",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."12" END "12",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."13" END "13",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."14" END "14",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."15" END "15",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."16" END "16",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."17" END "17",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."18" END "18",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."19" END "19",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."20" END "20",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."21" END "21",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."22" END "22",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."23" END "23",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."24" END "24",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."25" END "25",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."26" END "26",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."27" END "27",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."28" END "28",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."29" END "29",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."30" END "30",
        CASE WHEN C.Status in ('Niet OK','Fout') THEN 0 ELSE D."31" END "31"
    From "Schema_CorrectieFile" C
    INNER JOIN {2} D on C.ID=D.ID
    WHERE C.Status not in ('Niet OK','Fout')
    AND C.ID > 0
    AND NOT Jaar is null
    AND Jaar between {0} and {1}
    )
    , Totalen as (
    select * FROM StageSet
    UNION ALL
    select 
        999999 as ID,
        'Totalen' as "Status",
        WCZ,
        COUNT(DISTINCT("Naam student")) as "Aantal Stagairs",
        COUNT(DISTINCT("School")) as "Aantal Scholen",
        Null as Naam_aanvrager,
        Null as "Email_aanvrager",
        null as Tel_aanvrager,
        Studierichting_stage as Studierichting_stage,
        Null as Studiejaar_Module,
        Null as "Specialisaties",
        NULL as "Voorkeursafdeling",
        Null as stage_uren,
        Null as stage_dagen,
        Null as uren_per_dag,
        "Jaar",
        "Maand",
        SUM("1") as "1",
        SUM("2") as "2",
        SUM("3") as "3",
        SUM("4") as "4",
        SUM("5") as "5",
        SUM("6") as "6",
        SUM("7") as "7",
        SUM("8") as "8",
        SUM("9") as "9",
        SUM("10") as "10",
        SUM("11") as "11",
        SUM("12") as "12",
        SUM("13") as "13",
        SUM("14") as "14",
        SUM("15") as "15",
        SUM("16") as "16",
        SUM("17") as "17",
        SUM("18") as "18",
        SUM("19") as "19",
        SUM("20") as "20",
        SUM("21") as "21",
        SUM("22") as "22",
        SUM("23") as "23",
        SUM("24") as "24",
        SUM("25") as "25",
        SUM("26") as "26",
        SUM("27") as "27",
        SUM("28") as "28",
        SUM("29") as "29",
        SUM("30") as "30",
        SUM("31") as "31"
    from StageSet
    WHERE NOT Jaar is null
    AND Jaar between {0} and {1}
    GROUP by WCZ,Studierichting_stage,"Maand","Jaar"
    order by WCZ,Studierichting_stage,"Jaar","Maand" DESC)

    select * from Totalen
    """.format(Year,int(Year)+1,SchemaDataSet)

    if EmptyFrame == False:
        DataSet = pd.read_sql_query(DB_Correctie_query,db)
        #DataSet.to_sql('Results_Dataset', con=db, if_exists='replace')
        WriteDFToDB.DFToDB(df=DataSet,db=db,Schema='Results_Dataset',if_exists='replace')
        DataSet = DataSet.apply(pd.to_numeric, downcast='integer', errors='ignore')
        #DataSet = DataSet.apply(pd.to_numeric, downcast='integer', errors='coerce')
        #DataSet = DataSet.dropna()
        log.info('|--> Stagedata beschikbaar om mee te werken...')
        return DataSet
    else:
        log.warning('|--> Niets te doen...')
        return None
    

def GetScholen(db,SchemaDataSet,ReplaceDict,CorrectDict):
    DB_Correctie_query = """SELECT DISTINCT(trim("Naam van de school of onderwijsinstelling")
    ) as School FROM {0}""".format(SchemaDataSet)
    Scholen = pd.read_sql_query(DB_Correctie_query,db).replace(ReplaceDict, regex=True).replace(CorrectDict, regex=True)
    if Scholen.empty:
        log.warning('|--> GEEN Schooldata beschikbaar om mee te werken...')
        return None
    else:
        log.info('|--> Schooldata beschikbaar om mee te werken...')
        Scholen = Scholen.replace({"School": ReplaceDict}, regex=True).replace({"School": CorrectDict}, regex=True)
        Scholen = Scholen.drop_duplicates()
        Scholen['School']=Scholen['School'].str.lower()
        ScholenList=Scholen.School.unique().tolist()
        return ScholenList