import stripe
from decouple import config
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Google creds for Sheets access (please add your json file)
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "Enter your json file name here",
    scope
)

client = gspread.authorize(creds)

# Stripe creds for Stripe access (use .env file with API key in)

stripe.api_key = config("KEY")

# Just simply replace the below values for your
# sheet information, I'm using named ranges on the sheet in order to
# block out the data I want to read. For example: "Customer Spreadsheet"
# should be the Google Spreadsheet name,
# worksheet the tab on the sheet and so on.

custList = client.open(
    "Customer Spreadsheet"
    ).worksheet(
    "Enter Worksheet here"
    )
custId = custList.get_values("InvoiceCust")
priceId = custList.get_values("InvoicePrice")
count = 0

# In order to one-off invoice we need to create a Item to add to a one-off
# invoice then we add the item to the created invoice.
# After doing so this will finalise and then send the one-off invoice.

for custCell, priceCell in zip(custId, priceId):

    stripe.InvoiceItem.create(
        customer=custCell[0],
        price=priceCell[0]
    )

    invoice = stripe.Invoice.create(
        customer=custCell[0],
        pending_invoice_items_behavior="include",
        collection_method="send_invoice",
        days_until_due="7",
        description="Invoice for X. Thanks.",
    )

    stripe.Invoice.finalize_invoice(invoice.id)

    stripe.Invoice.send_invoice(invoice.id)

    print(
        f'successfully invoiced'
        f'{custCell[0]}'
        f'with {invoice.id}'
    )

    custCell = custId[1]
    priceCell = priceId[1]
    count += 1

print(f"script complete {count} records updated.")
