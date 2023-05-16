import urllib.request
import datetime
import os
import pandas as pd

province_ids = range(1, 28)  

base_url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2023&type=Mean'

if not os.path.exists('csv_data'):
    os.makedirs('csv_data')

for province_id in province_ids:
    url = base_url.format(province_id)
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = 'VHI{}_{}.csv'.format(province_id, current_datetime)
    filepath = os.path.join('csv_data', filename)

    try:
        urllib.request.urlretrieve(url, filepath)
        print('Файл {} успішно скачано.'.format(filename))
    except Exception as e:
        print('Помилка при скачуванні файлу для provinceID {}: {}'.format(province_id, str(e)))