from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model


class _BaseSuitcaseModel(Model):
    id = IntegerField(column_name='ID')
    id_totale = IntegerField(column_name='ID_Totale')
    id_parziale = IntegerField(column_name='ID_Parziale')
    data_ini = DateTimeField(column_name='Data_ini')
    esito = BooleanField(column_name='Esito')
    barcode = CharField(column_name='Barcode')
    id_user_name = IntegerField(column_name='ID_UserName')
    data_fine = DateTimeField(column_name='Data_Fine')


class PolycommSuitcaseModel(_BaseSuitcaseModel):
    barcode = IntegerField(column_name='Barcode')
    id_user_name = IntegerField(column_name='ID_Utente')
    data_fine = DateTimeField(column_name='Data')
    ko_peso = BooleanField(column_name='KO_Peso')
    ko_stop = BooleanField(column_name='KO_STOP')
    allarme_on = BooleanField(column_name='Allarme_ON')
    id_macchina = IntegerField(column_name='ID_Macchina')

    class Meta:
        db_table = 'Suitcase'


class PackflySuitcaseModel(_BaseSuitcaseModel):
    ricetta = IntegerField(column_name='Ricetta')
    allarme = IntegerField(column_name='Allarme')

    class Meta:
        db_table = 'Suitcase'
