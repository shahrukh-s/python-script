import csv
import json


def export_json(data):
    fieldname = ['Name', 'Value']
    a = {'Name': '', 'Value': ''}
    with open('file.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldname)
        writer.writeheader()
        for d in data['Variables']:
            try:
            #    for environment in d.get('Scope')['Environment']:
            #        if environment == 'Environments-1671':
                        a['Name'] = d.get('Name')
                        a['Value'] = d.get('Value')
                        writer.writerow(a)
            except KeyError:
                continue


if __name__ == '__main__':
    with open("MYFILENAME.json") as json_file:
        data = json.load(json_file)
    export_json(data)
