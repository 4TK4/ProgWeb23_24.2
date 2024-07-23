from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .utils import formatta_data
from .models import ContrattoTelefonico, SIMAttiva, SIMDisattiva, SIMNonAttiva, Telefonata


# view home
@csrf_exempt
def home(request):
    return render(request, 'index.html')

@csrf_exempt
def contrattoTelefonico(request):
    numero = request.POST.get("Numero", "") if request.method == 'POST' else request.GET.get("Numero", "") 
    data_attivazione = request.POST.get("DataAttivazione", "")
    tipo = request.POST.get("Tipo", "")
    
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
        'results': results,
        'error': error
    }

    return render(request, 'contrattoTelefonico.html', context)

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
def inserisci_contratto(request):
    if request.method == "POST":
        numero = request.POST.get('Numero')
        data_attivazione = request.POST.get('DataAttivazione')
        tipo = request.POST.get('Tipo')
        minuti_residui = request.POST.get('MinutiResidui')
        credito_residuo = request.POST.get('CreditoResiduo')
        
        data_attivazione = formatta_data(data_attivazione)
        # Validazione e gestione dei valori vuoti
        minuti_residui = minuti_residui if minuti_residui else None
        credito_residuo = credito_residuo if credito_residuo else None
        query = """
            INSERT INTO contrattotelefonico (Numero, DataAttivazione, Tipo, MinutiResidui, CreditoResiduo)
            VALUES (%s, %s, %s, %s, %s)
        """
        error = ""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (numero, data_attivazione, tipo, minuti_residui, credito_residuo))
            connection.commit()  # Assicurati di avere le parentesi per eseguire il commit
        except Exception as e:
            error = str(e)
            # Gestisci l'errore (ad esempio, loggalo o passalo al contesto per la visualizzazione)
            print(error)

        return redirect(reverse('inserimento_successo'))

def inserimento_successo(request):
    return render(request, 'inserimento_successo.html')

@csrf_exempt 
def modifica_contratto(request):
    if request.method == "POST":
        numero = request.POST.get('Numero')
        data_attivazione = request.POST.get('DataAttivazione')
        tipo = request.POST.get('Tipo')
        minuti_residui = request.POST.get('MinutiResidui')
        credito_residuo = request.POST.get('CreditoResiduo')

        # Validazione e gestione dei valori vuoti
        minuti_residui = minuti_residui if minuti_residui else None
        credito_residuo = credito_residuo if credito_residuo else None

        query = """
            UPDATE contrattotelefonico
            SET Tipo = %s, MinutiResidui = %s, CreditoResiduo = %s
            WHERE Numero = %s AND DataAttivazione = %s;
        """

        error = ""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (tipo, minuti_residui, credito_residuo, numero, data_attivazione))
            connection.commit()
        except Exception as e:
            error = str(e)
            print(error)
        return redirect(reverse('modifica_successo'))

def modifica_successo(request):
    return render(request, 'modifica_successo.html')

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

# view SIM
@csrf_exempt
def sim(request):
    codice = request.POST.get("Codice", "")
    numero = request.POST.get("Numero", "") if request.method == 'POST' else request.GET.get("Numero", "")
    tipo = request.POST.get("Tipo", "")
    stato = request.POST.get("Stato", "") if request.method == 'POST' else request.GET.get("Stato", "")

    query, params = get_SIM(codice, numero, tipo, stato)
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

# funzione che crea la query per cercare le SIM in base ai filtri di ricerca
def get_SIM(codice, numero, tipo, stato):
    query =""
    params = []
    if not stato or stato == "":
        query += """ SELECT * FROM simattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

        query += """UNION SELECT * FROM simdisattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

        query += """UNION SELECT * FROM simnonattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    elif stato and stato == "Attiva":
        query = """ SELECT * FROM simattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    elif stato and stato == "Disattiva":
        query = """ SELECT * FROM simdisattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    elif stato and stato == "Non attivata":
        query = """ SELECT * FROM simnonattiva WHERE 1=1 """
        if codice:
            query += " AND Codice = %s"
            params.append(codice)
        if numero:
            query += " AND (AssociataA = %s OR EraAssociataA = %s)"
            params.append(numero)
            params.append(numero)
        if tipo:
            query += " AND TipoSIM = %s"
            params.append(tipo)

    return query, params

# view Telefonata
@csrf_exempt
def telefonata(request):
    effettuata_da = request.POST.get("EffettuataDa", "") if request.method == 'POST' else request.GET.get("EffettuataDa", "")
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
        'results': results,
        'error': error,
    }

    return render(request, '../templates/telefonata.html', context)

# funzione che crea la query per cercare le SIM in base ai filtri di ricerca
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
    # query += " ORDER BY EffettuataDa"
    return query, params
