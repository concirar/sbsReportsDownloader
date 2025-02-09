import pandas as pd
import numpy as np



# URLS : Main SBS URL and URL for SBS Statistics
pUrlSbsStats='https://intranet2.sbs.gob.pe/estadistica/financiera/'

######################################################################################################################################
# DataFrames
######################################################################################################################################

# Calendar
listCalendar=[
    ["01","Enero","en"],
    ["02","Febrero","fe"],
    ["03","Marzo","ma"],
    ["04","Abril","ab"],
    ["05","Mayo","my"],
    ["06","Junio","jn"],
    ["07","Julio","jl"],
    ["08","Agosto","ag"],
    ["09","Setiembre","se"],
    ["10","Octubre","oc"],
    ["11","Noviembre","no"],
    ["12","Diciembre","di"]]
dfCalendar=pd.DataFrame(listCalendar, columns = ['numMonth','nameMonth','nameMonthShort'])

print('Loading dfCalendar...')


# Type of Entities - Reports
# BM: Banca Múltiple - EF: Empresas Financieras
# TCS: Tipo de Crédito y Situación - EGP: Estado de Ganancias y Pérdidas
# CCXTC: Créditos Castigados por Tipo Crédito - CDTCS: Créditos Directos según Tipo de Crédito y Situación

listReportsByTypeEnts=[
    ["BM","BancaMultiple","Tipo de Credito y Situacion","TCS","B-2334"],
    ["BM","BancaMultiple","Balance General y Estado de Ganancias y Pérdidas","BG_GYP","B-2201"],
    ["BM","BancaMultiple","Creditos Castigados por Tipo Credito","CCXTC","B-2369"],
    ["BM","BancaMultiple","Créditos Directos según Tipo de Crédito y Situación","CDTCS","B-2334"],
    ["EF","EmpresasFinancieras","Tipo de Credito y Situacion","TCS","B-3219"],
    ["EF","EmpresasFinancieras","Balance General y Estado de Ganancias y Pérdidas","BG_GYP","B-3101"],
    ["EF","EmpresasFinancieras","Creditos Castigados por Tipo Credito","CCXTC","B-3234"],
    ["EF","EmpresasFinancieras","Créditos Directos según Tipo de Crédito y Situación","CDTCS","B-3220"]        
] 
dfReportsByTypeEnts=pd.DataFrame(listReportsByTypeEnts, \
                                 columns = ['typeEntCode','typeEnt','reportName','reportCode','reportsByTypeEntCode'])

print('Loading dfReportsByTypeEnts...')

######################################################################################################################################
# Functions
######################################################################################################################################
