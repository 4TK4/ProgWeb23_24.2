from datetime import datetime

#metodo per formattare la data da yyyy/mm/dd a dd/mm/yy
def formatta_data(data):
    try:
        # Convertire dal formato yyyy-mm-dd al formato dd/mm/yy
        risultato = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%y")
    except ValueError:
        # Se la conversione fallisce, imposta risultato a None
        risultato = None
    return risultato
