# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 02:43:17 2020

@author: Steven Hiram

Calculo del lead time en base a diferencia de tiempo entre: 
    - 3 estaciones que detectan onda P
    - 1 estacion en la capital que detecta onda S 
"""

def Estacion_Capital(Estat):
    # ----------
    # Entradas:
    # Estat     = Nombre de la estación
    # ----------
    # Salidas:
    # val       = Booleano para indicar si esta o no en la capital 
    # -------
    
    #Declaración e inialización de variable
    val = False
    #Estaciones consideradas en la capital
    CIUDAD = ['CIRS','VILL','SJPIN','CMONM','CINGE','CSTER','CASUN','KINAL',
              'ITC','JUAMA','EXCEL','CCONS','IPRES','TADEO','CBIL','CAUST',
              'LSECB','ICREY','ACRIS','SEUNI','ASEGG','CSAGC','AMGGT','LGUAT',
              'CDBOS','RGIL','JUNKA','CEPRO','NRNJO','SMP','SPAYM','BVH','ALUX',
              'TUC','VILLC','MERCK','RCACE']
    #Busqueda de estación 
    if(Estat in CIUDAD):   val = True
    return val

def Lead_time(folder,homeDir,PRINT = False,READ = True):
    # ----------
    # Entradas:
    # folder    = Nombre del evento
    # homeDir   = Directorio con eventos
    # PRINT     = Bandera para prints
    # READ      = Bandera para leer csv o usar el archivo proporcionado como parametro
    # ----------
    # Salidas:
    # list       = Lista con estaciones y tiempos de arrivo 
    # -------
    
    #Librerias
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    if(READ):   
        est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
        est.sort_values(by = ['DeltaT (segundos)'], inplace=True)
    #LLamada con folder ya filtrado
    else:       est = folder
    
    
    #Filtramos para buscar primer arrivo P
    estP = est[est['Onda'].isin(['P'])] 
    #Declaración e inialización de variables
    timeP ,est_P = 0.0,'NONE'
    
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo P que no esté en la capital
    for a,b in zip(estP['Est'],estP['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeP == 0.0 and Estacion_Capital(a) == False):   timeP ,est_P = b, a


    #Filtramos para buscar primer arrivo S
    estS = est[est['Onda'].isin(['S'])]
    #Declaración e inialización de variables
    timeS, est_S = 0.0, 'NONE'
   
    #Recorrido de estaciones y tiempo de arrivo
    #Se revisa que sea un arrivo S esté en la capital
    for a,b in zip(estS['Est'],estS['DeltaT (segundos)']):
        #Sustitucion en primer caso 
        if(timeS == 0.0 and Estacion_Capital(a)):   timeS ,est_S = b, a
    
    if(PRINT):
        if(timeP != 0.0 and timeS != 0.0):  
            #Evento en la Capital
            if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
            #Evento buscado
            else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        
        #En caso que no se encuentre una P fuera de la capital o una S en la capital    
        else:   print('No es posible calcular')
    
    return (est_P, timeP, est_S, timeS)


# Funcion que retorna el tiempo de arrivo
def myFunc(e):
  return e['DeltaT (segundos)']

#Lead Time para 3 estaciones P
def Lead_time2(folder, homeDir,PRINT = False,READ = True):
    # ----------
    # Entradas:
    # folder    = Nombre del evento
    # homeDir   = Directorio con eventos
    # PRINT     = Bandera para prints
    # READ      = Bandera para leer csv o usar el archivo proporcionado como parametro
    # ----------
    # Salidas:
    # list       = Lista con estaciones y tiempos de arrivo 
    # -------
    
    #Librerias
    import pandas as pd 
    
    #Leemos el archivo con las estaciones del evento
    if(READ):   est = pd.read_csv(homeDir+str(folder)+'_estaciones.csv')
    #LLamada con folder ya filtrado
    else:       est = folder
    
    #Data adicional
    #Profundidad y magnitud del evento
    prof = est['Prof']
    profR = 0
    for a in prof:  profR = a;  break
    mag = est['mag'] 
    magR = 0
    for a in mag:  magR = a;  break
    Lat = est['Lat']
    LatR = 0
    for a in Lat:  LatR = a;  break
    Lon = est['Lon']
    LonR = 0
    for a in Lon:  LonR = a;  break
    
    #Filtramos para buscar primer arrivo P
    estP = est[est['Onda'].isin(['P'])] 
    #Declaración e inialización de variables
    timeP ,est_P = 0.0,'NONE'
    timeS, est_S, dist_s = 0.0, 'NONE', 0.0
    
    #Reporte de error si el evento no tiene ondas P
    if(estP.empty): 
        nombreError = est['Folder']
        print(f"Este evento no tiene ondas P {nombreError[min(nombreError.index)]}")
    else:
        #Ordeno las listas en base al tiempo de arrivo
        listT, listN = (list(t) for t in zip(*sorted(zip(estP['DeltaT (segundos)'].tolist(), estP['Est'].tolist()))))
    
        #Recorrido de estaciones y tiempo de arrivo
        #Se revisa que sea un arrivo P que no esté en la capital
        #Se rompre al encontrar el tercer caso*
        #Se usa el tercer caso ya que es la cantidad mínima de estaciones para declarar evento
        counter = 0
        for a,b in zip(listN,listT):
            if(timeP == 0.0 and Estacion_Capital(a) == False): 
                counter = counter + 1
                #Tercera estacion P
                if(counter == 3):
                    timeP ,est_P = b, a 
                    #print("P*")
                    break
    
        #Filtramos para buscar primer arrivo P
        estS = est[est['Onda'].isin(['S'])]
        #Reporte de error si el evento no tiene ondas S
        if(estS.empty): 
            nombreError = est['Folder']
            print(f"Este evento no tiene ondas S {nombreError[min(nombreError.index)]}")
        else:
            #Dist (km) 
            #Ordeno las listas en base al tiempo de arrivo
            listT, listN, Dist = (list(t) for t in zip(*sorted(zip(estS['DeltaT (segundos)'].tolist(), estS['Est'].tolist(),estS['Dist'].tolist()))))
            
            #Recorrido de estaciones y tiempo de arrivo
            #Se revisa que sea un arrivo S que este en la capital
            #Se rompre al encontrar el primer caso que tenga un lead-time positivo
            for a,b,c in zip(listN,listT,Dist):
               if(timeS == 0.0 and Estacion_Capital(a) == True and b>timeP):   
                timeS ,est_S, dist_s = b, a ,c
                break
    
    #print(est_S,timeS)
    if(PRINT):
        if(timeP != 0.0 or timeS != 0.0):  
            #Evento en la Capital
            if(timeS-timeP < 0.0):  print('Evento en la Capital.','Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
            #Evento buscado
            else:                   print('Lead time: '+str(timeS-timeP)+', entre '+est_P+' ,'+est_S)
        
        #En caso que no se encuentre una P fuera de la capital o una S en la capital    
        else:   print('No es posible calcular')
    
    return (est_P, timeP, est_S, timeS, profR, magR, dist_s, LatR, LonR)



def Multiple_Lead_time(name, homeDir,METHOD = False):
    # ----------
    # Entradas:
    # name      = Nombre del archivo a leer
    # homeDir   = Directorio con eventos
    # METHOD    = Bandera para cambiar entre 2 metodos
    # ----------
    # Salidas:
    # Archivo .csv
    # -------
    
    #Librerias
    import pandas as pd 
    import numpy as np
    
    #Leemos el archivo con las estaciones del evento
    ests = pd.read_csv(homeDir+str(name)+'_estaciones.csv')
    #Obtenemos el nombre de todos los folders
    events_names = np.unique(ests['Folder'])
    
    dataLT = []
    for element in events_names:
        #Filtramos el evento a analizar
        eventN = ests[ests['Folder'].isin([str(element)])]
        #Metodos alternativos para calcular el LeadTime
        if(METHOD): eventD = Lead_time(eventN,homeDir,False,False)
        else:       eventD = Lead_time2(eventN,homeDir,False,False)
        dataLT.append((element,eventD[7],eventD[8],eventD[5],eventD[4],eventD[3]-eventD[1],eventD[0],eventD[1],eventD[2],eventD[3],eventD[6]))
    
    #Conversion a DataFrame
    dataO = pd.DataFrame(dataLT,columns=['Folder','Lat','Lon','Mag','Prof','LeadTime','3eraEstacionP','TiempoP','EstacionS','TiempoS','Dist_s'])
    dataO.to_csv(homeDir+'/'+str(name)+'_LeadTime2_new.csv',index=True)
    
    
homeDir = "C:/Users/HRV/Desktop/Post-U/Trabajo/Prueba/Paper/"
name = "PaperTodos"