#ATTENZIONE!!!
#in realtà django chiama 'view' ciò che per noi è il controller!!!

from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .utils import formatta_data
from .models import ContrattoTelefonico, SIMAttiva, SIMDisattiva, SIMNonAttiva, Telefonata


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
@csrf_exempt
def home(request):
    return render(request, '../templates/index.html')

#view ContrattoTelefonico
@csrf_exempt
def contrattoTelefonico(request):
    numero = request.POST.get("Numero", "")
    data_attivazione = request.POST.get("DataAttivazione", "")
    tipo = request.POST.get("Tipo", "")
    
    # Convertire data_attivazione nel formato dd/mm/yy
    if data_attivazione:
        data_attivazione = formatta_data(data_attivazione)
    
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

    context = {
        'results':results
    }

    print(results)
    return render(request, '../templates/contrattoTelefonico.html', context)

#funzione che crea la query per cercare i contratti in base ai filtri di ricerca,
#comprese le informazioni riguardo al numero di telefonate effettuate, la SIM attiva attualmente associata
#e il numero di SIM disattive un tempo associate al contratto
@csrf_exempt
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

@csrf_exempt
def aggiungi_contratto(request):
    error = None
    results = []

    if request.method == 'POST':
        numero = request.POST.get('Numero', '')
        data_attivazione = request.POST.get('DataAttivazione', '')
        tipo = request.POST.get('Tipo', '')
        credito_residuo = request.POST.get('CreditoResiduo', '')
        minuti_residui = request.POST.get('MinutiResidui', '')

        try:
            data_ap_dt = datetime.strptime(data_ap, '%Y-%m-%d') if data_ap else None
            data_ch_dt = datetime.strptime(data_ch, '%Y-%m-%d') if data_ch else None
        except ValueError:
            error = "Formato data non valido"
            print(error)
            data_ap_dt = None
            data_ch_dt = None

        is_valid = controllo(attiva, data_ch_dt, data_ap_dt,False)

        if is_valid:
            query = """
                INSERT INTO contrattotelefonico (Numero, DataAttivazione, Tipo, CreditoResiduo, MinutiResidui)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (numero, data_attivazione, tipo, credito_residuo, minuti_residui)
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
            except Exception as e:
                error = str(e)
                print("Errore! "+error)

            print("Contratto telefonico inserito correttamente, con questi valori",params)
            return redirect('contrattoTelefonico')
        else:
            error = "Errore nei dati inseriti"
            print(error)
    context = {
        'results': results,
        'error': error
    }
    return render(request, 'modifica_contratto.html', context)




@csrf_exempt
def modifica_contratto(request, numero):
    error = None
    context = {}
    results={}
    if request.method == 'POST':
        tipo = request.POST.get('Tipo')
        minuti_residui = request.POST.get('MinutiResidui')
        credito_residuo = request.POST.get('CreditoResiduo')
        query = """
                UPDATE contrattotelefonico SET Tipo = %s, MinutiResidui = %s, CreditoRedisuo = %s
                WHERE Numero = %s
            """
        params = (numero, tipo, minuti_residui, credito_residuo)
        try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
        except Exception as e:
                error = str(e)

        return redirect('contrattoTelefonico')
    return render(request, 'modifica_contratto.html', context)

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

@csrf_exempt
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
@csrf_exempt
def sim(request):
    codice = request.POST.get("Codice", "")
    associata_a = request.POST.get("AssociataA", "") if request.method == 'POST' else request.GET.get("AssociataA", "")
    era_associata_a = request.GET.get("EraAssociataA","")
    tipo = request.POST.get("Tipo", "")
    stato = request.POST.get("Stato", "")

    query, params = get_SIM(codice, associata_a, era_associata_a, tipo, stato)
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
def get_SIM(codice, associata_a, era_associata_a, tipo, stato):
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
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
        if era_associata_a:
            query += " AND EraAssociataA = %s"
            params.append(era_associata_a)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    return query, params

#view Telefonata
@csrf_exempt
def telefonata(request):
    effettuata_da = request.POST.get("EffettuataDa", "")
    data = request.POST.get("Data", "")
    
     # Convertire data nel formato dd/mm/yy
    if data:
        data = formatta_data(data)
    
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
@csrf_exempt
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
        query += " AND Data = %s"
        params.append(data)
    query += " ORDER BY EffettuataDa"
    return query, params
