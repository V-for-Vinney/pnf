from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model


class _BaseAllarmiModel(Model):
    id = IntegerField(column_name='ID')
    data = DateTimeField(column_name='Data')
    messagio = CharField(column_name='Messaggio')


class PolycommAllarmiModel(_BaseAllarmiModel):
    new = BooleanField(column_name='New')
    total_suitcase = IntegerField(column_name='Total_Suitcase')

    class Meta:
        db_table = 'Allarmi'


class PackflyAllarmiModel(_BaseAllarmiModel):

    class Meta:
        db_table = 'Allarmi'

