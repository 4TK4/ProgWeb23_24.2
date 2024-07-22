#ATTENZIONE!!!
#in realtà django chiama 'view' ciò che per noi è il controller!!!

from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import ContrattoTelefonico, SIM, Telefonata


"""
esempio slides
def paramsToJson(request):
    if request.method== "GET":
        params= request.GET
    else:
        params= request.POST
    o = {}
    for n in params.dict().keys():
        o[n] = params.get(n)
        res = HttpResponse(content_type="application/json")
        res.write(json.dumps(o))
        return res
"""
   
"""
utilizzo sessioni (potrebbero servirci in futuro) 
def StartSession(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter== None:
        request.session["counter"] = 1
        res.write("Session Started")
    else:
        res.write("Session alreadystarted")
    return res

def CloseSession(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter!= None:
        del request.session["counter"]
        res.write("Session stopped")
    else:
        res.write("Session notstarted")
    return res

def SessionCount(request):
    res = HttpResponse(content_type="text/html")
    counter= request.session.get("counter")
    if counter== None:
        res.write("No session activated")
    else:
        counter+=1;
        res.write("Counteris{}".format(counter))
        request.session["counter"]=counter;
    return res
"""
#view home
def home(request):
    return render(request, '../templates/index.html')  

#view ContrattoTelefonico
def contrattoTelefonico(request):
    numero = request.POST.get("Numero", "") 
    data_attivazione = request.POST.get("DataAttivazione", "")
    tipo = request.POST.get("Tipo", "")
    
    query, params = get_contratto(numero, data_attivazione, tipo)
    results = []
    error = ""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        error = str(e)


    #for result in results:
       # result['DataAttivazione'] = result['DataAttivazione'].strftime('%d-%m-%y')

    context = {
        'results':results
    }
    
    print(results)
    return render(request, '../templates/contrattoTelefonico.html', context)

#funzione che crea la query per cercare i contratti in base ai filtri di ricerca,
#comprese le informazioni riguardo al numero di telefonate effettuate, la SIM attiva attualmente associata
#e il numero di SIM disattive un tempo associate al contratto
def get_contratto(numero, data_attivazione, tipo):
    query = """
        SELECT 
            c.*,
            (SELECT COUNT(*) FROM telefonata t WHERE t.EffettuataDa = c.Numero) AS Telefonate,
            (SELECT s.Codice FROM simattiva s WHERE s.AssociataA = c.Numero) AS SIMAttiva,
            (SELECT COUNT(*) FROM simdisattiva sd WHERE sd.EraAssociataA = c.Numero) AS SIMDisattive
        FROM 
            contrattotelefonico c
        WHERE 
            1=1
    """
    params = []

    if numero:
        query += " AND c.Numero = %s"
        params.append(numero)
    if data_attivazione:
        query += " AND c.DataAttivazione = %s"
        params.append(data_attivazione)
    if tipo:
        query += " AND c.Tipo = %s"
        params.append(tipo)

    return query, params

def modifica_contratto(request, numero):
    if request.method == 'GET':
        numero = request.GET.get('Numero')
        tipo = request.GET.get('Tipo')
        minuti_residui = request.GET.get('MinutiResidui')
        credito_residuo = request.GET.get('CreditoResiduo')

        contratto = get_object_or_404(ContrattoTelefonico, numero=numero)
        
        if tipo == 'a consumo':
            contratto.tipo = tipo
            contratto.minuti_residui = minuti_residui
            contratto.credito_residuo = None
        elif tipo == 'a ricarica':
            contratto.tipo = tipo
            contratto.minuti_residui = None
            contratto.credito_residuo = credito_residuo
        
        contratto.save()
        return redirect('contrattoTelefonico')  
    return render(request, 'contratti/modifica_contratto.html')

def elimina_contratto(request, numero):
    query = "DELETE FROM contrattotelefonico WHERE Numero = %s" 
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [numero])
    except Exception as e:
        error = str(e)
        return redirect('numero', {'error': error})

    return redirect('contrattoTelefonico')



#view SIM
def sim(request):
    codice = request.POST.get("Codice", "") 
    associata_a = request.POST.get("AssociataA", "")
    tipo = request.POST.get("Tipo", "")
    stato = request.POST.get("Stato", "")
    
    query, params = get_SIM(codice, associata_a, tipo, stato)
    results = []
    error = ""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        error = str(e)

    context = {
        'results':results
    }
    
    return render(request, '../templates/sim.html', context)

#funzione che crea la query per cercare le SIM in base ai filtri di ricerca
def get_SIM(codice, associata_a, tipo, stato):
    query =""
    params = []
    if not stato or stato == "":
        query += """ SELECT * FROM simattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)    
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)
            
        query += """UNION SELECT * FROM simdisattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)    
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)
            
        query += """UNION SELECT * FROM simnonattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)   
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)
    
    elif stato and stato == "Attiva":
        query = """ SELECT * FROM simattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)    
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)
        
    elif stato and stato == "Disattiva":
        query = """ SELECT * FROM simdisattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)    
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)
            
    elif stato and stato == "Non attivata":
        query = """ SELECT * FROM simnonattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)    
        if associata_a:
            query += " AND AssociataA = %s"
            params.append(associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    return query, params

#view Telefonata
def telefonata(request): 
    effettuata_da = request.POST.get("EffettuataDa", "")
    data = request.POST.get("Data", "")
    
    query, params = get_telefonata(effettuata_da, data)
    results = []
    error = ""

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        error = str(e)

    context = {
        'results':results
    }
    
    return render(request, '../templates/telefonata.html', context)

#funzione che crea la query per cercare le SIM in base ai filtri di ricerca
def get_telefonata(effettuata_da, data):
    params = []
    query = """
    SELECT * FROM telefonata WHERE 1=1
    """
    params = []
    if effettuata_da:
        query += " AND EffettuataDa = %s"
        params.append(effettuata_da)
    if data:
        query += " AND Data LIKE %s"
        params.append(f'%{data}%')

    query += " ORDER BY EffettuataDa"
    return query, params



