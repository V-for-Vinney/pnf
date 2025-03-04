from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model


class _BaseSuitcaseModel(Model):
    ID = IntegerField(primary_key=True)
    ID_Totale = IntegerField()
    ID_Parziale = IntegerField()
    Data_ini = DateTimeField()
    Esito = BooleanField()
    Barcode = CharField()


class PolycommSuitcaseModel(_BaseSuitcaseModel):
    Barcode = IntegerField()
    ID_Utente = IntegerField()
    Data = DateTimeField()
    KO_Peso = BooleanField()
    KO_STOP = BooleanField()
    Allarme_ON = BooleanField()
    ID_Macchina = IntegerField()

    class Meta:
        db_table = 'Suitcase'


class PackflySuitcaseModel(_BaseSuitcaseModel):
    ID_UserName = IntegerField()
    Data_Fine = DateTimeField()
    Ricetta = IntegerField()
    Allarme = IntegerField()

    class Meta:
        db_table = 'Suitcase'
