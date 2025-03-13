from pprint import pprint
from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def get_sheet_data():
    sheet = client.open("BTC Pacific Coast Seniors 2025").sheet1
    all_data = sheet.get_all_values()  # Fetch all values as a list of lists

    # Transpose the data so that columns become rows
    transposed_data = list(map(list, zip(*all_data)))  
    transposed_data = [row[:4] for row in transposed_data]

    final_data = transposed_data[6:10] + transposed_data[5:0:-1] + transposed_data[:1]
    pprint(final_data)
    return final_data

@app.route("/")
def index():
    data = get_sheet_data()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
