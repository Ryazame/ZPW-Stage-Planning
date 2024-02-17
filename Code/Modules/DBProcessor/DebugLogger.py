import logging,os

def CreateLog():
    log=logging.getLogger('StageLogger')
    if log.hasHandlers():
        log.handlers=[]

    log.setLevel(logging.WARNING)
    #formatter=logging.Formatter('%(asctime)s :: %(levelnames)s :: %(funcName)s :: %(lineno)d :: %(message)s')
    #formatter=logging.Formatter(fmt=' %(name)s :: %(levelname)s :: %(message)s')
    formatter=logging.Formatter(fmt=' %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log

