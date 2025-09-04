from const import URL
import pandas as pd
from src.dataClass import transactionEntry, depositEntry

def main():
    tables = pd.DataFrame(pd.read_html(URL, extract_links="all")[7]) ## 7 stores the target insurance data
    print(tables)
    colHeader = []
    for col in tables.columns: ## creating column header list
        colHeader.append(col[0]) ## ('Date of statement', None) extract only the string
    print(colHeader)
    ## need to group entries by date first then deposit ID(aka under same transaction) with total amount deposited
    ## Date: Array[]
    ##      Amount: 
    ##      Deposit ID: 
    ##                  Array[]
    ##                  Contract Number: X
    ##                  Member ID: X
    ##                  First Name: v
    ##                  Claim Number: X
    ##                  Claimed Amount: X
    ##                  Paid Amount: v
    ##                  PDF Link: v:
    data = ETLData()
    for row in tables.values:



if __name__ == "__main__":
    main();