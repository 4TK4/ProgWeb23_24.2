
from django.db import connection


def insert_contratto(numero, data_attivazione, tipo, minuti_residui, credito_residuo):
    query_insert = "INSERT INTO contrattotelefonico (Numero, DataAttivazione, Tipo, MinutiResidui, CreditoResiduo) VALUES (%s, %s, %s, %s, %s)"
    connection.cursor.execute(query_insert, [numero, data_attivazione, tipo, minuti_residui, credito_residuo])