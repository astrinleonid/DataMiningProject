import requests
import json
import prettytable
import numpy as np
import pandas as pd

DATA_TYPES = {"01":	"all_employees",
"02":	"avg_weekly_hours",
"03":	"avg_hour_earnings",
"11":	"avg_week_earnings",
}
MONTH_NAMES ={
"M01" : "January",
    "M02" : "February",
    "M03" : "March",
    "M04" : "April",
    "M05" : "May",
    "M06" : "June",
    "M07" : "July",
    "M08" : "August",
    "M09" : "September",
    "M10" : "October",
    "M11" : "November",
    "M12" : "December"
}

def get_data(state_id):

    headers = {'Content-type': 'application/json'}
    result = {}
    for data_type in DATA_TYPES:
        print(f"Data type : {data_type}, name : {DATA_TYPES[data_type]}")
        data = json.dumps({"seriesid": [f'SMU{state_id}0000005000000{data_type}'], "startyear": "2021", "endyear": "2021"})
        p = requests.post('https://api.bls.gov/publicAPI/v1/timeseries/data/', data=data, headers=headers)
        json_data = json.loads(p.text)
        print(json_data)

        for series in json_data['Results']['series']:
            x = prettytable.PrettyTable(["series id", "year", "period", "value", "footnotes"])
            seriesId = series['seriesID']
            for item in series['data']:
                year = item['year']
                period = item['period']
                value = item['value']
                print(f"Period : {period}, value : {value}")
                if 'M01' <= period <= 'M12':
                    period_and_year = f"{year}, {MONTH_NAMES[period]}"
                    if period_and_year not in result:
                        result[period_and_year] = {DATA_TYPES[data_type] : value}
                    else:
                        result[period_and_year].update({DATA_TYPES[data_type]: value})

    for period, values in result.items():
        avg_yearly_salary = float(values['avg_week_earnings']) * 50
        result[period].update({'avg_yearly_salary' : avg_yearly_salary})
    return result

        # output = open(seriesId + '.txt','w')
        # output.write (x.get_string())
        # output.close()


print(get_data('02'))
