import requests
from airtable import Airtable

from utils.keys import AIRTABLE_BASE_KEY, AIRTABLE_API_KEY


def get_table(table):

    air_table = Airtable(AIRTABLE_BASE_KEY, table, api_key=AIRTABLE_API_KEY)
    res = air_table.get_all()
    return res


def test():
    params = {
        'fields': {
            'Slack User': 'Allen2',
            'Email': 'email@email.com',
            'Service': ['recBxmDasLXwmVB78'],
            'Skillsets': ["Web (Frontend Development)"],
            'Additional Details': 'Details'}
    }

    headers = {
        'authorization': "Bearer " + AIRTABLE_API_KEY
    }
    res = requests.post("https://api.airtable.com/v0/app2p4KgQKx35WoCm/Mentor%20Request",
                        json=params,
                        headers=headers)
    # print(res.content)


if __name__ == '__main__':
    # test()
    get_table('Services')

services_records = {
    'General Guidance - Slack Chat': 'recBxmDasLXwmVB78',
    'General Guidance - Voice Chat': 'recDyu4PMbPl7Ti58',
    'Pair Programming': 'recHCFAO9uNSy1WDs',
    'Code Review': 'recUK55xJXOfAaYNb',
    'Resume Review': 'recXZzUduWfaxWvSF',
    'Mock Interview': 'recdY4XLeN1CPz1l8'
}
