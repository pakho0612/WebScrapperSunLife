
class transactionEntry:
    ## Contract Number: X
    ## Member ID: X
    ## First Name: v
    ## Claim Number: X
    ## Claimed Amount: X
    ## Paid Amount: v
    ## PDF Link: v:
    def __init__(self):
        self.contractNumber = 0
        self.memberID = 0
        self.firstName = ""
        self.claimNumber = 0
        self.claimedAmount = 0
        self.paidAmount = 0
        self.pdfLink = ""

    def transactionEntry(self, contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink):
        self.contractNumber = contractNumber
        self.memberID = memberID
        self.firstName = firstName
        self.claimNumber = claimNumber
        self.claimedAmount = claimedAmount
        self.paidAmount = paidAmount
        self.pdfLink = pdfLink

class dataEntry:
    def __init__(self):
        self.date = None
        self.deposits = {} ## {date: [depositEntry]}

    def addDeposit(self, deposit):
        if (type(deposit) == depositEntry):
            self.deposits.append(deposit)
        else:
            return Exception("Cannot add deposit: Invalid deposit entry")

    def addTransaction(self, date, depositID, contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink=""):
        if date not in self.deposits:
            self.deposits[date] = {}
        if depositID not in self.deposits[date]:
            self.deposits[date][depositID] = depositEntry(depositID=depositID)
        transaction = transactionEntry(contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink)
        self.deposits[date][depositID].addTransaction(transaction)

    def setDate(self, date):
        self.date = date