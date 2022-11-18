# -*- coding: utf-8 -*-

# импорт библиотек
import pandas as pd
from datetime import datetime 
import time
import os
import glob


path = input('Path:') # ввод пути к файлам
csv_files = glob.glob(os.path.join(path, "*.csv")) # составляем список файлов

# цикл с расчетами по файлам
for file in csv_files:
    
    file_name = os.path.basename(file)

    # загрузка и ввод данных
    promery = pd.read_csv(file, sep=',') # чтение файла
    datetime_str = input('Date of {} (01.01.2022 01:01:01):'.format(file_name)) # ввод даты
    time_creation = time.mktime(datetime.strptime(datetime_str, 
                                '%d.%m.%Y %H:%M:%S').timetuple()) # перевод строки в формат даты unix

    # обработка
    promery = promery[promery['Depth[ft]'] > 0] # убираем нулевые значения
    promery['Depth[m]'] = promery['Depth[ft]'] * 0.3048 + 0.2 # переводим глбину в метры
    duration = promery.iloc[len(promery)-1, 13] / 1000 # подсчитываем длительность промеров
    promery['TimeOffset[s]'] = promery['TimeOffset[ms]'] / 1000 # создаем столбец с секундами
    time_start = time_creation - duration # подсчитываем время старта промеров
    promery['datetime'] = promery['TimeOffset[s]'] + time_start # создаем столбец с абсолютным временем записи

    # сохранение файла
    promery.to_csv(path+"\\_corr_"+file_name, sep=',', index=False)