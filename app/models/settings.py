from peewee import CharField
from peewee import IntegerField
from peewee import Model


class _BaseSettingsModel(Model):
    id = IntegerField(column_name='ID')  # Auto-incrementing primary key
    id_macchina = IntegerField(column_name='ID_Macchina')


class PolycommSettingsModel(_BaseSettingsModel):
    frame_video = IntegerField(column_name='Frame_Video')
    tempo_primo_tensionamento = IntegerField(column_name='Tempo_Primo_Tensionamento')
    tempo_ultimo_tensionamento = IntegerField(column_name='Tempo_Ultimo_Tensionamento')
    tempo_altezza_salita_ini = IntegerField(column_name='Tempo_Altezza_Salita_ini')
    tempo_sormonto = IntegerField(column_name='Tempo_Sormonto')
    software_pagamenti = CharField(column_name='Software_Pagamenti')
    titolo_software_pagamenti = CharField(column_name='Titolo_Software_Pagamenti')
    vel_pulsante_1 = IntegerField(column_name='Vel_Pulsante_1')
    vel_pulsante_2 = IntegerField(column_name='Vel_Pulsante_2')
    vel_pulsante_3 = IntegerField(column_name='Vel_Pulsante_3')
    vel_pulsante_4 = IntegerField(column_name='Vel_Pulsante_4')
    vel_pulsante_5 = IntegerField(column_name='Vel_Pulsante_5')
    remote_address = CharField(column_name='Remote_Address')
    remote_port = IntegerField(column_name='Remote_Port')
    timeout = CharField(column_name='TimeOut')
    download_server = CharField(column_name='DownloadServer')
    download_hour = IntegerField(column_name='DownloadHour')

    class Meta:
        db_table = 'Settings'


class PackflySettingsModel(_BaseSettingsModel):
    pos_link = CharField(column_name='POS_Link')
    pos_name = CharField(column_name='POS_Name')

    class Meta:
        db_table = 'Settings'
