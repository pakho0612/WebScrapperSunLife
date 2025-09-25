from const import URL
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from fcn import properFloat

from src.dataClass import ClaimEntry, Deposits, AllDeposits

def rowToClaimEntry(row):
    ## simply turns a row into a claim obj
    # [0] Date
    # [1] Member ID
    # [2] First Name
    # [3] Claim Number
    # [4] Claimed Amount
    # [5] Paid Amount
    # [6] PDF Link
    '''('21 Aug 2025', None), ('233017671', None)
    array([('', None), ('', None), ('150731', None), ('BR002569', None),
       ('Le chan', None),
       ('210825-AXJ79-00', '/GB_PRSS/wca/claimDetail?claimKey=150731|BR002569|Le Chan|210825-AXJ79-|00|000167385'),
       ('$591.00', None), ('$429.60', None)], dtype=object)
    '''
    return ClaimEntry(
            contractNumber=int(row[2][0]),
            memberID=row[3][0],
            firstName=row[4][0],
            claimNumber=row[5][0],
            claimedAmount=properFloat(row[6][0]),
            paidAmount=properFloat(row[7][0]),
            pdfLink=row[5][1]
        )
    
def readAllDeposits(rows):
    allDeposits = AllDeposits()
    curDate = None
    curDepositID = 0
    for row in rows:
        
        if not(all(np.equal(row[0], ('', None)))) : ##have a valid datetime 
            ## must be a new deposit if it has a date value
            curDate = int(datetime.strptime(row[0][0], '%d %b %Y').strftime("%Y%m%d"))
            allDeposits.addDate(curDate)
            curDepositID = 0

            if not(all(np.equal(row[1], ('', None)))): ##have a valid deposit ID
                curDepositID = int(row[1][0])
            else:
                curDepositID = 0
            ## create new deposits obj
            curDeposit = Deposits(curDate, curDepositID)
            allDeposits.addDeposit(curDeposit)
        elif not(all(np.equal(row[1], ('', None)))): ##have a valid deposit ID
            curDepositID = int(row[1][0])
            curDeposit = Deposits(curDate, curDepositID)
            allDeposits.addDeposit(curDeposit)

        if not(all(np.equal(row[2], ('', None)))): ## have a valid contract number
            claim = rowToClaimEntry(row)
            allDeposits.addClaim(claim, curDate, curDepositID)
        else: ## no contractact number is the row that contains only the total amount
            (allDeposits.getDeposit(curDate, curDepositID)).setPaidTotal(properFloat(row[7][0]))
    return allDeposits



def main():
    tables = pd.DataFrame(pd.read_html(URL, extract_links="all")[7]) ## 7 stores the target insurance data
    ##print(tables)
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
    allDeposits = readAllDeposits(tables.values)

    startDate = 20250801
    endDate = 20250901
    total = 1416.72
    result = allDeposits.searchTotal(startDate, endDate, total)
    print(result)



if __name__ == "__main__":
    main();