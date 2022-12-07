import requests
import json
import prettytable
import numpy as np
import pandas as pd


def get_data(state_id, data_type):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": [f'SMU{state_id}0000005000000{data_type}'], "startyear": "2021", "endyear": "2021"})
    p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)

    periods = []
    values = []

    for series in json_data['Results']['series']:
        x = prettytable.PrettyTable(["series id", "year", "period", "value", "footnotes"])
        seriesId = series['seriesID']
        for item in series['data']:
            # year = item['year']
            period = item['period']
            value = item['value']
            # footnotes=""
            for footnote in item['footnotes']:
                if footnote:
                    footnotes = footnotes + footnote['text'] + ','

            if 'M01' <= period <= 'M12':
                periods.append(f"2021 {period}")
                values.append(value)
        return {'periods': periods, 'values': values}

        # output = open(seriesId + '.txt','w')
        # output.write (x.get_string())
        # output.close()


df = pd.DataFrame(get_data('02','01'))
print(df)