import csv
import qrcode
import re
from rich import print
from urllib import parse

def clean(string):
	cleaned = re.sub('[\(\):]', '', string)
	return re.sub('[. ]', '-', cleaned)

with open('export.csv', newline='') as file:
    reader = csv.reader(file, delimiter='\t')
    uris = list(reader)

for issuer, label, secret in uris:
	print(f'[yellow]{issuer}[/yellow]: [blue]{label}[/blue]')

	uri = f'otpauth://totp/{parse.quote(label)}?secret={secret}&issuer={parse.quote(issuer)}'

	image = qrcode.make(uri)
	image.save('qr/' + clean(issuer) + '-' + clean(label) + '.png')
