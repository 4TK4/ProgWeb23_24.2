#file contenente funzioni python richiamate dai controller definiti in views.py

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

#funzione per formattare la data da yyyy/mm/dd a dd/mm/yy
def formatta_data(data):
    try:
        # Convertire dal formato yyyy-mm-dd al formato dd/mm/yy
        risultato = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%y")
    except ValueError:
        # Se la conversione fallisce, imposta risultato a None
        risultato = None
    return risultato

#funzione che genera la query per il riempimento della tabella dei contratti in base ai filtri di ricerca inseriti
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


#funzione che genera la query per il riempimento della tabella delle SIM in base ai filtri di ricerca inseriti
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


#funzione che genera la query per il riempimento della tabella delle telefonate in base ai filtri di ricerca inseriti
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
    return query, params