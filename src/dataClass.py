class depositEntry:
    def __init__(self):
        self.amount = 0
        self.depositID = 0
        self.transactions = [] ## [transactionEntry]

    def depositEntry(self, amount=0, depositID=0, transactions=[]):
        self.amount = amount
        self.depositID = depositID
        self.transactions = transactions
    
    def setAmount(self, amount):
        self.amount = amount

    def addTransaction(self, contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink=""):
        self.transactions.append(transactionEntry(contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink))

    def addTransaction(self, transaction):
        if(type(transaction)==transactionEntry):
            self.transactions.append(transaction)
        else:
            return Exception("Cannot add transaction:Invalid transaction entry")

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
        self.deposits = [] ## [depositEntry]
    
    def addDeposit(self, deposit):
        if (type(deposit) == depositEntry):
            self.deposits.append(deposit)
        else:
            return Exception("Cannot add deposit: Invalid deposit entry")

    def addDeposit(self, depositID, contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink=""):
        deposit = depositEntry(depositID=depositID)
        transaction = transactionEntry(contractNumber, memberID, firstName, claimNumber, claimedAmount, paidAmount, pdfLink)
        deposit.addTransaction(transaction)
        self.addDeposit(deposit)