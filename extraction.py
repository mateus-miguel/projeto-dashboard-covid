from typing import Iterator
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

def date_range(start_date: datetime, end_date: datetime) -> Iterator[datetime]:
  # Retorna um iterador de datas no formato datetime dentro de um intervalo
  date_range_days: int = (end_date - start_date).days
  for lag in range(date_range_days):
      yield start_date + timedelta(lag)

start_date = datetime(2021, 1, 1)
end_date = datetime(2021, 12, 31)

cases = None
cases_is_empty = True

for date in date_range(start_date=start_date, end_date=end_date):
    date_str = date.strftime('%m-%d-%Y') # formato do GitHub do JHU
    data_source_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{date_str}.csv'

    caso = pd.read_csv(data_source_url, sep=',')
    caso = caso.drop(['FIPS', 'Admin2', 'Last_Update', 'Lat', 'Long_', 'Recovered', 'Active', 'Combined_Key', 'Case_Fatality_Ratio'], axis=1)
    caso = caso.query('Country_Region == "Brazil"').reset_index(drop=True)
    caso['Date'] = pd.to_datetime(date.strftime('%Y-%m-%d'))

    if cases_is_empty:
        cases = caso
        cases_is_empty = False
    else:
        cases = pd.concat([cases, caso], ignore_index=True)

print('Finalizado!')
