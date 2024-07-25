#ATTENZIONE!!!
#è il file con i controller: django chiama 'view' ciò che in realtà è un controller

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .utils import formatta_data, get_contratto, get_SIM, get_telefonata
from .models import ContrattoTelefonico, SIMAttiva, SIMDisattiva, SIMNonAttiva, Telefonata



#__________________________________HOME_____________________________________#
#controller che chiama la pagina index.html
@csrf_exempt
def home(request):
    return render(request, 'index.html')



#__________________________________CONTRATTO TELEFONICO_____________________________________#
#controller che costruisce il contesto da passare al template contrattoTelefonico.html
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



#__________________________________INSERIMENTO NUOVO CONTRATTO_____________________________________#
#controller per l'inserimento di un nuovo contratto, invocato quando si preme il pulsante 
#'Inserisci' del modal per l'aggiunta di un nuovo contratto.
#Se esiste già un contratto con il numero di telefono specificato, allora la richiesta viene re-indirizzata 
#al controller inserimento_fallito; se invece l'inserimento va a buon fine, allora la richiesta
#viene re-indirizzata al controller inserimento_successo
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
        
        #query per verificare se è già presente un contratto con il numero di telefono specificato. 
        controllo_query = """SELECT COUNT(*) FROM contrattotelefonico WHERE Numero = %s"""
        try:
            with connection.cursor() as cursor:
                cursor.execute(controllo_query, [numero])
                count = cursor.fetchone()[0]  # Ottieni il conteggio dalla query
                
                if count > 0:
                    return redirect(reverse('inserimento_fallito'))    
            
            #query per l'inserimento della tupla nella tabella dei contratti
            query = """
                INSERT INTO contrattotelefonico (Numero, DataAttivazione, Tipo, MinutiResidui, CreditoResiduo)
                VALUES (%s, %s, %s, %s, %s)
            """
            error = ""
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, (numero, data_attivazione, tipo, minuti_residui, credito_residuo))
                connection.commit() 
            except Exception as e:
                error = str(e)
                print(error)


            return redirect(reverse('inserimento_successo'))
        except Exception as e:
            error = str(e)
            print(error)
    
            
#controller che chiama la pagina di notifica di avvenuto inserimento di un contratto
def inserimento_successo(request):
    return render(request, 'inserimento_successo.html')


#controller che chiama la pagina di notifica di fallito inserimento di un contratto
def inserimento_fallito(request):
    return render(request, 'inserimento_fallito.html')



#__________________________________MODIFICA DI UN CONTRATTO_____________________________________#
#controller per la modifica di un contratto
@csrf_exempt 
def modifica_contratto(request):
    if request.method == "POST":
        numero = request.POST.get('Numero')
        tipo = request.POST.get('Tipo')
        minuti_residui = request.POST.get('MinutiResidui')
        credito_residuo = request.POST.get('CreditoResiduo')

        # Validazione e gestione dei valori vuoti
        minuti_residui = minuti_residui if minuti_residui else None
        credito_residuo = credito_residuo if credito_residuo else None

        query = """
            UPDATE contrattotelefonico
            SET Tipo = %s, MinutiResidui = %s, CreditoResiduo = %s
            WHERE Numero = %s;
        """
        error = ""
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (tipo, minuti_residui, credito_residuo, numero))
            connection.commit()
        except Exception as e:
            error = str(e)
            print(error)
        return redirect(reverse('modifica_successo'))


#controller che chiama la pagina di notifica di avvenuta modifica di un contratto
def modifica_successo(request):
    return render(request, 'modifica_successo.html')



#__________________________________ELIMINAZIONE DI UN CONTRATTO_____________________________________#
#controller per l'eliminazione di un contratto, che re-indirizza la richiesta sul controller elimina_successo
@csrf_exempt
def elimina_contratto(request, numero):
    #se elimino un contratto, elimino anche le sim e le telefonate ad esso associate
    queries = [
        "DELETE FROM telefonata WHERE EffettuataDa = %s",
        "DELETE FROM simattiva WHERE AssociataA = %s",
        "DELETE FROM simdisattiva WHERE EraAssociataA = %s",
        "DELETE FROM contrattotelefonico WHERE Numero = %s"
    ]
    try:
        with connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query, [numero])
    except Exception as e:
        error = str(e)
        return redirect('numero', {'error': error})
    return redirect(reverse('elimina_successo'))

#controller che chiama la pagina elimina_successo.html, in cui semplicemente si visualizza un messaggio di avvenuta eliminazione
def elimina_successo(request):
    return render(request, 'elimina_successo.html')



#__________________________________SIM_____________________________________#
#controller che costruisce il contesto da passare al template sim.html
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



#__________________________________TELEFONATA_____________________________________#
#controller che costruisce il contesto da passare al template telefonata.html
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


