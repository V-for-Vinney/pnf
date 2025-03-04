from peewee import CharField
from peewee import IntegerField
from peewee import Model


class _BaseSettingsModel(Model):
    ID = IntegerField(primary_key=True)
    ID_Macchina = IntegerField()


class PolycommSettingsModel(_BaseSettingsModel):
    Frame_Video = IntegerField()
    Tempo_Primo_Tensionamento = IntegerField()
    Tempo_Ultimo_Tensionamento = IntegerField()
    Tempo_Altezza_Salita_ini = IntegerField()
    Tempo_Sormonto = IntegerField()
    Software_Pagamenti = CharField()
    Titolo_Software_Pagamenti = CharField()
    Vel_Pulsante_1 = IntegerField()
    Vel_Pulsante_2 = IntegerField()
    Vel_Pulsante_3 = IntegerField()
    Vel_Pulsante_4 = IntegerField()
    Vel_Pulsante_5 = IntegerField()
    Remote_Address = CharField()
    Remote_Port = IntegerField()
    TimeOut = CharField()
    DownloadServer = CharField()
    DownloadHour = IntegerField()

    class Meta:
        db_table = 'Settings'


class PackflySettingsModel(_BaseSettingsModel):
    POS_Link = CharField()
    POS_Name = CharField()

    class Meta:
        db_table = 'Settings'