from datetime import datetime

#create a log file everytime the program runs
fp = open("AccountsLog.txt", mode = "w+")
fp.close()

#menu display
menu = """Welcome to the Bank Accounts Management App
1- Print All Accounts (tabular format)
2- Create an account (Enter code, client name, bank name, account type and balance)
3- Create/update the password for an account (Enter account code)
4- Withdraw an amount from an account (account code & amount)
5- Deposit an amount to an account (Enter account code & amount)
6- Transfer an amount between accounts (Enter from and to account codes and amount)
7- Get balance of a given account (Enter account code)
8- Display the log file
9- Exit
Enter your option: """

Accounts = {}   # Dictionary of Accounts 

#Creating BankAccount class from lab
class BankAccount:
    #defining variables
    #preset Balance and Password
    def __init__(self, Code, Name, Bank, Type, Balance = 0, Password =''):
        #verifies account type
        if Type in ['chequing', 'saving', 'invest', 'loan', 'TFSA', 'RRSP']:
            self.code = Code
            self.name = Name
            self.bank = Bank
            self.type = Type
            self.balance = Balance
            self.password = Password
            self.access = datetime.now()
        else:
            print("Error, invalid account type")
    
    #format printing
    def __repr__(self):
        x = "{:<8d}{:30s}{:10s}{:10s}{:<10.2f}{:}"
        print(x.format(self.code,self.name,self.bank,self.type,self.balance, self.access))

    #withdrawing from account
    def withdraw(self, amount):
        if amount > self.balance:
            print("Error, not enough funds!")
        else:
            self.balance = self.balance - amount
            print("Successful withdraw, here is your new balance:", self.balance)
        self.access = datetime.now()
    #depositing to account
    def deposit(self, amount):
        self.balance = self.balance + amount
        print("Your account now has a balance of", self.balance)
        self.access = datetime.now()
    #transfering to from account to account
    def transfer(self, other, amount):
        self.balance = self.balance - amount
        other.balance = other.balance + amount
        print("Successful Transfer")
        self.access = datetime.now()
        other.access = datetime.now()
    #get balance
    def get_balance(self):
        print(self.name + ", your balance is:", self.balance)
        self.access = datetime.now()
    #bank interest
    def Add_interest(self, rate):
        rate = float(rate)
        if rate > 0 and (rate <= 6.0):
            self.balance = self.balance * (1+rate)
        else:
            print("Error, invalid rate")
    #create account password
    def create_pwd(self):
        pw = input("Enter a password: ")
        length = len(pw)
        count = 0
        #count the number of lowercase letters
        for i in range(0, length-1):
            if pw[i].islower() == True:
                count += 1
        #verification for password
        if (pw[:length-2].isalnum() == False): 
            print('Error, password is not composed of letters and digits only')
            return False
        elif (pw[length-1] != "#"):
            print('Error, password does not end with "#"')
            return False
        elif length < 8 or length > 15:
            print('Error, password must contain minimum length 8 characters and maximum length 15 characters')
            return False
        elif pw[0].isupper() == False:
            print('Error, password must start with a capital letter')
            return False
        elif pw[length-5:length-1].isdigit() == False:
            print('Error, password must end with 4 digits.')
            return False
        elif count == 0:
            print('Error, password must contain atleast 1 small letter')
            return False
        else:
            print("Password accepted")
            self.password = pw
            return True
    #Returning balance of an account (for option 6)
    def balance(self):
        self.access = datetime.now() 
        return self.balance
    #Returning date accessed of an account (for log file)
    def date(self):
        return self.access
    #Returning Password of an account (for verification)
    def getpw(self):
        return self.password

#open accounts.txt and input all the data to Accounts
#file = open('accounts.txt',mode = 'r')
for line in file.readlines():
    line = line.strip('\n')
    data = line.split(',')
    data[0] = int(data[0])
    data[4] = float(data[4])
    Accounts[data[0]] = BankAccount(data[0],data[1],data[2],data[3],data[4])

#function for tubular printing
def PrintAllAccounts(A):
    print("{:8s}{:30s}{:10s}{:10s}{:10s}{:}".format('code', 'name', 'bank', 'type', 'balance','date accessed'))
    for key in A.keys():
        BankAccount.__repr__(A[key])

option = 0
while option != 9:
    option = int(input(menu))
    #option for printing all accounts
    if option == 1:
        PrintAllAccounts(Accounts)
    #creating account
    if option == 2:
        fp = open("AccountsLog.txt", mode = "a")
        account_info = input("enter account info:") 
        acc = account_info.split(",") 
        acc_code = int(acc[0]) 
        Accounts[acc_code]= BankAccount(acc_code,acc[1],acc[2],acc[3],float(acc[4]))
        fp.write(str(acc[0])+" creation: "+str(Accounts[acc_code].date())+"\n")
        fp.close()
        
    #creating password
    if option == 3:
        acc = int(input("Enter account code:"))
        if acc in Accounts.keys():
            #loop for verification and reopening user input if invalid password
            while Accounts[acc].create_pwd() == False:
                Accounts[acc].create_pwd()
                if Accounts[acc].create_pwd() == True:
                    break
        else:
            print("Error, account not found.")
    
    #option for withdrawing
    if option == 4:
        acc = int(input("Enter account code:"))
        fp = open("AccountsLog.txt", mode = "a")
        #verify if account exists
        if acc in Accounts.keys():
            #password verification
            password = input("Enter account password (empty if no password):")
            if password == Accounts[acc].getpw():
            #amount withdrawing
                amount = float(input("Enter withdraw amount:"))
                BankAccount.withdraw(Accounts[acc], amount)
                #log keeping
                fp.write(str(acc)+" withdraw "+ str(amount)+": "+str(Accounts[acc].date())+"\n")
            else:
                print("Wrong password")
        else:
            print("Error, account not found.")
        fp.close()
    
    #option for depositing
    if option == 5:
        acc = int(input("Enter account code:"))
        fp = open("AccountsLog.txt", mode = "a")
        #verify if account exists
        if acc in Accounts.keys():
            #password verification
            password = input("Enter account password (empty if no password):")
            if password == Accounts[acc].getpw():
            #amount withdrawing
                amount = float(input("Enter withdraw amount:"))
                BankAccount.deposit(Accounts[acc], amount)
                #log keeping
                fp.write(str(acc)+" password: "+str(Accounts[acc].date())+"\n")
            else:
                print("Wrong password")
        else:
            print("Error, account not found.")
        fp.close()
    
    if option == 6:
        acc_from = int(input("Enter original account:"))
        fp = open("AccountsLog.txt", mode = "a")
        #verification for account existance
        if acc_from in Accounts.keys():
            password = input("Enter account password (empty if no password):")
            #verification for password
            if password == Accounts[acc_from].getpw():
                acc_to = int(input("Enter the account that you are sending to:"))
                #verification for account existance
                if acc_to in Accounts.keys():
                    amount = float(input("Enter amount:"))
                    #verification for enough balance
                    if amount > BankAccount.balance(Accounts[acc_from]):
                        print("Error, amount exceeds original account's balance.")
                    else:
                        Accounts[acc_from].transfer(Accounts[acc_to],amount)
                        fp.write(str(acc_from)+" transfered to "+str(acc_to)+ str(amount)+": "+str(Accounts[acc_from].date())+"\n")
                else:
                    print("Error, account not found.")
            else:
                print("Invalid Password")
        else:
            print("Error, account not found.")
        fp.close()
    
    if option == 7:
        fp = open("AccountsLog.txt", mode = "a")
        acc = int(input("Enter account:"))
        #verification for account existance
        if acc in Accounts.keys():
            #verification for password
            password = input("Enter account password (empty if no password):")
            if password == Accounts[acc_from].getpw():
                #call get balance
                Accounts[acc].get_balance()
                fp.write(str(acc)+" was accessed at: "+str(Accounts[acc].date())+"\n")
            else:
                print("Invalid Password")
        else:
            print("Error, account not found.")
        fp.close()
    
    if option == 8:
        fp = open("AccountsLog.txt", mode = "r")
        #read log
        for line in fp.readlines():
            line.strip("/n")
            print(line)
        fp.close()
    
    # option 9 code  
    elif option == 9:
        print("Exiting...")

    
