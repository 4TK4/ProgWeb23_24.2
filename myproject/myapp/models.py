from django.db import models


#model per la tabella ContrattoTelefonico
class ContrattoTelefonico(models.Model):
    numero = models.IntegerField(primary_key=True)
    data_attivazione = models.DateField()
    tipo = models.CharField(max_length=20)
    minuti_residui = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    credito_residuo = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Contratto {self.numero} - {self.tipo}"


#model per la tabella SIMAttiva
class SIMAttiva(models.Model):
    codice = models.CharField(max_length=20, primary_key=True)
    tipo = models.CharField(max_length=20)
    associata_a = models.IntegerField(null=True, blank=True)
    era_associata_a = models.IntegerField(null=True, blank=True)
    data_attivazione = models.DateField(null=True, blank=True)
    data_disattivazione = models.DateField(null=True, blank=True)
  
    def __str__(self):
        return f"SIM {self.codice} - Tipo: {self.tipo}"
 
    
#model per la tabella SIMDisattiva
class SIMDisattiva(models.Model):
    codice = models.CharField(max_length=20, primary_key=True)
    tipo = models.CharField(max_length=20)
    associata_a = models.IntegerField(null=True, blank=True)
    era_associata_a = models.IntegerField(null=True, blank=True)
    data_attivazione = models.DateField(null=True, blank=True)
    data_disattivazione = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"SIM {self.codice} - Tipo: {self.tipo}"


#model per la tabella SIMNonAttiva
class SIMNonAttiva(models.Model):
    codice = models.CharField(max_length=20, primary_key=True)
    tipo = models.CharField(max_length=20)
    associata_a = models.IntegerField(null=True, blank=True)
    era_associata_a = models.IntegerField(null=True, blank=True)
    data_attivazione = models.DateField(null=True, blank=True)
    data_disattivazione = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"SIM {self.codice} - Tipo: {self.tipo}"


#model per la tabella Telefonata
class Telefonata(models.Model):
    counter = models.IntegerField()
    effettuata_da = models.IntegerField()
    data = models.DateField()
    ora = models.CharField(max_length=5)
    durata = models.IntegerField()
    costo = models.DecimalField(max_digits=20, decimal_places=2)

    #la chiave è composta da counter ed effettuata_da
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['counter', 'effettuata_da'], name='unique_telefonata')
        ]
    
    def __str__(self):
        return f"Telefonata ID: {self.counter}, EffettuataDa: {self.effettuata_da} - Data: {self.data}, Ora: {self.ora}"
