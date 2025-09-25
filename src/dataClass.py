from datetime import datetime, timedelta


class ClaimEntry:
    ## Contract Number: X
    ## Member ID: X
    ## First Name: v
    ## Claim Number: X
    ## Claimed Amount: X
    ## Paid Amount: v
    ## PDF Link: v:
    def __init__(self, contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink):
        self.contractNumber = contractNumber
        self.memberID = memberID
        self.firstName = firstName
        self.claimNumber = claimNumber
        self.claimedAmount = claimedAmount
        self.paidAmount = paidAmount
        self.pdfLink = pdfLink

class Deposits:
    ## [Date][Deposits]
    def __init__(self, date, depositID):
        self.date = date
        self.depositID = depositID
        self.paidTotal = 0
        self.deposits = [] ## [depositEntry]
        self.num = 0

    def add(self, claim):
        if (type(claim) == ClaimEntry):
            self.deposits.append(claim)
            self.paidTotal += claim.paidAmount
            self.num+=1
        else:
            return Exception("Cannot add claim: Invalid claim entry")

    def setPaidTotal(self, paidTotal):
        if (self.paidTotal == paidTotal):## sanity check
            self.paidTotal = paidTotal
            return True
        else:
            return Exception("Cannot set paid total: Invalid amount")
        
    def setDate(self, date):
        self.date = date

class AllDeposits:
    def __init__(self):
        self.deposits = {}

    def addDate(self, date):
        try:
            if(type(date)!=int):
                int(datetime.strptime(date, '%d %b %Y').strftime("%Y%m%d"))
            self.deposits[date] = {}
        except:
            return Exception("Cannot add date: Invalid date")

    def addDeposit(self, deposit):
        if(type(deposit)==Deposits):
            self.deposits[deposit.date][deposit.depositID] = deposit
        else:
            return Exception("Cannot add deposit: Invalid deposit")
        
    def addClaim(self, claim, date, depositID):
        if(type(claim)==ClaimEntry):
            self.deposits[date][depositID].add(claim)
        else:
            return Exception("Cannot add claim: Invalid claim")
        
    def getDeposit(self, date, depositID):
        return self.deposits[date][depositID]
        
    def searchTotal(self, startDate, endDate, total):
        ## startDate: 20250823
        ## endDate: 20250901
        start = datetime.strptime(str(startDate), '%Y%m%d')
        end = datetime.strptime(str(endDate), '%Y%m%d')
        curDate = startDate
        out = []
        while curDate <= endDate:
            if curDate in self.deposits:## if we have depoist on the date
                for deposit in self.deposits[curDate].values():
                    if round(deposit.paidTotal,2) == round(total,2):
                        out.append(deposit)
            curDate = int((datetime.strptime(str(curDate), "%Y%m%d") + timedelta(days=1)).strftime("%Y%m%d")) ## advance cur date
        return out