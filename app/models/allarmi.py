from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import IntegerField
from peewee import Model


class _BaseAllarmiModel(Model):
    ID = IntegerField(primary_key=True)
    Data = DateTimeField()
    Messaggio = CharField()


class PolycommAllarmiModel(_BaseAllarmiModel):
    New = BooleanField()
    Total_Suitcase = IntegerField()

    class Meta:
        db_table = 'Allarmi'


class PackflyAllarmiModel(_BaseAllarmiModel):
    class Meta:
        db_table = 'Allarmi'
