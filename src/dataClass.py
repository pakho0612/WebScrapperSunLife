
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

    def add(self, claim):
        if (type(claim) == ClaimEntry):
            self.deposits.append(claim)
            self.paidTotal += claim.paidAmount
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