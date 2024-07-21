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

def home(request):
    return render(request, '../templates/index.html')   #mando richiesta (contesto) del template che voglio chiamare

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

def get_contratto(numero, data_attivazione, tipo):
    query = """
        SELECT 
            c.*,
            (SELECT COUNT(*) FROM telefonata t WHERE t.EffettuataDa = c.Numero) AS Telefonate
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

def sim(request):
    return render(request, '../templates/sim.html')

def telefonata(request):
    return render(request, '../templates/telefonata.html')
