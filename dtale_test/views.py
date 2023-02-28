import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from django.http import HttpResponse
from django.shortcuts import redirect

from dtale.views import startup


def index(request):
    return HttpResponse("""
        <h1>PropReturns Visualisation Tool</h1>
        <span>Click Here to view the data</span><a href="/create-df">link</a>
    """)

def create_df(request):
    # establish a connection to the PostgreSQL database
    conn = psycopg2.connect(
    host = 'data-scraping-mah.cnpkaa7lysya.ap-south-1.rds.amazonaws.com',
    port = 5432,
    user = 'postgres',
    password = 'data_scraping_mah',
    database='master_tables'
    )

    # create a cursor object
    cur = conn.cursor()
    print("Reading the data")
    # execute the SQL query
    cur.execute('SELECT * FROM "Cleaned_RM_Alpha_Leave_and_licence"')

    # fetch the results into a list of tuples
    rows = cur.fetchall()

    # close the cursor and connection
    cur.close()
    conn.close()
    print("The data will be displayed")
    # create a Pandas DataFrame from the results
    df = pd.DataFrame(rows, columns=['Village Name', 'Document Name', 'Rent/Month', 'Deposit',
       'Other Information', 'Area (in square feet)', 'Seller Name & Address',
       'Buyer Name & Address', 'Submission Date YYYY MM DD',
       'Transaction Date YYYY MM DD', 'Document Number', 'Stamp Duty',
       'Registration Fee', 'Asset Type', 'Building Name', 'Buyer Name',
       'Seller Name', 'Rental Terms', 'Has Extra Area Info', 'id'])
    
    kanakia_df = df[df['Building Name'].str.lower().str.startswith('kanakia', na=False)]

    # create a D-Tale instance with the data
    instance1 = startup(data=df, ignore_duplicate=True)

    # create a D-Tale instance with the second dataframe
    instance2 = startup(data=kanakia_df, ignore_duplicate=True)
    
    # redirect to the D-Tale web interface for the first dataframe instance
    resp1 = redirect(f"/flask/dtale/main/{instance1._data_id}")

    # redirect to the D-Tale web interface for the second dataframe instance
    resp2 = redirect(f"/flask/dtale/main/{instance2._data_id}")

    # return both responses
    return HttpResponse(f"""
        <h1>PropReturns Visualisation Tool</h1>
        <span>View Complete Data: </span><a href="{resp1.url}">link</a>
        <br>
        <span>View Kanakia only data: </span><a href="{resp2.url}">link</a>
    """)








# def create_df(request):
#     # read the data into a pandas DataFrame
#     df = pd.read_csv('/Users/kathanbhavsar/Desktop/PropReturns/kathan_test_rm_alpha.csv', low_memory = False)    
#     instance = startup(data=df, ignore_duplicate=True)
#     resp = redirect(f"/flask/dtale/main/{instance._data_id}")
#     return resp