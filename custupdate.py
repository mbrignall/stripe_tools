import stripe
from decouple import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Google creds for Sheets access (add the json filename below!!)
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "Enter your json file name here",
    scope
)

client = gspread.authorize(creds)

# Stripe creds for Stripe access (.ent file needed with key=)
stripe.api_key = config('KEY')

# Just simply replace the below values for your sheet information,
# I'm using named ranges on the sheet in order to block out the
# data I want to read.
#
# For example: "Customer Spreadsheet" should be the Google Spreadsheet
# name, worksheet the tab on the sheet and so on.
custList = client.open(
    "Customer Spreadsheet").worksheet(
    "Worksheet in Spreadsheet"
)

custRange = custList.get_values('custRange')
typeRange = custList.get_values('custType')
count = 0

# This bit tells Stripe which customer from custRange
# to update with the type in typeRange
for custCell, typeCell in zip(custRange, typeRange):

    stripe.Customer.modify(
        custCell[0],
        description=typeCell[0]
)

    print(
        f'Successfully updated {custCell[0]}'
        f'with description: {typeCell[0]}'
)

    custCell = custRange[1]
    typeCell = typeRange[1]
    count += 1

print(
    f'script complete {count}'
    f'records updated.'
)
