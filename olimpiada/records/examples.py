from records.models import Record

datas = [
    {'holder': 'Pantelis', 'gender': Record.RecordGenderOptions.MEN, 'event': Record.RecordEventOptions.MIDDLEDISTANCE1500, 'place':'SEF', 'stadium':Record.RecordStadiumOptions.INDOORS, 'performance': 4.18, 'record_date':None, 'timestamp':None, 'updated':None},
    {'holder': 'Anastasis', 'gender': Record.RecordGenderOptions.MEN, 'event': Record.RecordEventOptions.SPRINT400, 'place': 'Agios Kosmas', 'stadium':Record.RecordStadiumOptions.OUTDOORS, 'performance': 52.34, 'record_date':None, 'timestamp':None, 'updated':None},
    {'holder': 'Giannis', 'gender': Record.RecordGenderOptions.MEN, 'event': Record.RecordEventOptions.SPRINT200, 'place': 'Palini', 'stadium':Record.RecordStadiumOptions.OUTDOORS, 'performance':24.56, 'record_date':None, 'timestamp':None, 'updated':None},
    {'holder': 'Ioanna', 'gender': Record.RecordGenderOptions.WOMEN, 'event': Record.RecordEventOptions.HURDLES400, 'place': 'SEF', 'stadium':Record.RecordStadiumOptions.INDOORS, 'performance': 63.45, 'record_date':None, 'timestamp':None, 'updated':None},
    {'holder': 'Aggeliki', 'gender': Record.RecordGenderOptions.WOMEN, 'event': Record.RecordEventOptions.SPRINT400, 'place': 'Loutraki', 'stadium':Record.RecordStadiumOptions.OUTDOORS, 'performance': 59.80, 'record_date':None, 'timestamp':None, 'updated':None},
]

my_new_objs = []
for data in datas:
    my_new_objs.append(Record(**data))

Record.objects.bulk_create(my_new_objs, ignore_conflicts=True)