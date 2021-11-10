#!/usr/bin/env python3
import datetime
import requests

DATE, COLUMN_NAME, TIME_STAMP, AMOUNT, CZK_PRICE = range(5)


def Get_Value(obj):
    try:
        obj = int(obj)
    except ValueError:
        pass
    if isinstance(obj, str):
        if obj.lower() == obj:
            return 1/ord(obj)
        return 1/(ord(obj.lower())-0.5)
    return obj
#print(Get_Value("4"))


def IsBigger(str_1, str_2): # porovná 2 řetězce a podle abecedy rozhodne který je "větší"
    i = 0
    while i < len(str_1):
        try:
            #print(Get_Value(str_1[i]),Get_Value(str_2[i]))
            if Get_Value(str_1[i]) > Get_Value(str_2[i]):
                return True
            if Get_Value(str_1[i]) < Get_Value(str_2[i]):
                return False
        except IndexError: # pokud str_2 je podřetězcem str_1 -> str_1 je větší
            return True
        i += 1
    return False # v případě, že jsou řetězce stejné
#print(IsBigger('ASOB','TREZOR'))


def SortMinToMax(Data):
    #list_of_date = []
    #list_of_column = []
    i = 0
    while i < len(Data):
        min = i
        j = i + 1    
        while j < len(Data): 
            if IsBigger(Data[min][DATE], Data[j][DATE]):
                min = j
            if Data[min][DATE] == Data[j][DATE] and IsBigger(Data[j][COLUMN_NAME], Data[min][COLUMN_NAME]):
                min = j
            if Data[min][DATE] == Data[j][DATE] and Data[j][COLUMN_NAME] == Data[min][COLUMN_NAME] and IsBigger(Data[j][TIME_STAMP], Data[min][TIME_STAMP]):
                min = j
            j += 1
        L_min = Data[min]
        Data[min] = Data[i]
        Data[i] = L_min
        i += 1
    #print(Data)
    #print(list_of_column,list_of_date)
    return Data

def GenerateTab(SortedData):
    list_of_date = []
    list_of_column = []
    for h in range(len(SortedData)):
        if list_of_date.count(SortedData[h][DATE]) == 0: list_of_date.append(SortedData[h][DATE])
        if list_of_column.count(SortedData[h][COLUMN_NAME]) == 0: list_of_column.append(SortedData[h][COLUMN_NAME])
    list_of_column = sorted(list_of_column)
    list_of_date = sorted(list_of_date)


    tab = ["date"]
    for column in list_of_column:
        tab.append(column)
    tab.append("Total[CZK]")
    Tab = [tab]
    for date in list_of_date:
        line = [date]
        total = 0
        for column in list_of_column:
            amount, in_czk  = Find_in_line(SortedData, date, column)
            line.append(amount)
            total += float(in_czk)
        line.append(total)
        Tab.append(line)


    #print(Tab)
    return Tab


def Find_in_line(SortedData, line_name, column_name):
    for line in SortedData:
        if column_name in line and line_name in line:
            return line[3], line[4]
    return "-", 0



    
def PrintTab(Tab):
    width = 20
    for r in Tab:
        for x in r:
            print("{0:<{w}}".format(x,w=width),end="")
        print("")
        if r[0] == "date":
            for x in r:
                print("{0:-<{w}}".format("",w=width),end="")
            print("")
        


           
def GetData(Tab):

    last_line = Tab[len(Tab)-1]
    t = str(datetime.datetime.now())[:str(datetime.datetime.now()).find(" ")]
    date = input("Zadejte datum [{0}]:".format(t))
    if not date:
        date = t

    for i in range(len(Tab[0])):
        if Tab[0][i] != "date" and Tab[0][i] != "Total[CZK]":
            amount = input("Zadejte sumu pro {0}:".format(Tab[0][i]))
            n = Tab[0][i]
            if amount:
                try:
                    sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
                except:
                    sat, czk = 0, 0
            if not amount:
                try:
                    amount = last_line[i]
                    sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
                except:
                    amount = "-"
                    czk = 0#"""
        


            time_stamp = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
            f = open(filename, "a", encoding="utf8")
            f.write("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))            
            f.close()


    while True:
        n = input("Zadejte novou položku (př.: Coinbase[BTC]):")
        if not n:
            break
        amount = input("Zaadejte sumu pro {0}:".format(n))
        if amount:
            try:
                sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
            except:
                sat, czk = 0, 0
        if not amount:
            try:
                amount = last_line[i]
                sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
            except:
                amount = "-"
                czk = 0#"""
        time_stamp = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
        f = open(filename, "a", encoding="utf8")
        f.write("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))            
        f.close()



def to_sats(a, m,url='https://blockchain.info/ticker'):
    eur = requests.get(url).json()['EUR']['15m']
    czk = requests.get(url).json()['CZK']['15m']
    if m == "CZK":
        return a/czk*100000000, a
    if m == "EUR":
        return a/eur*100000000, a/eur*czk

    if m == "BTC":
        return a*100000000, a*czk
    




        
        
    

    
            
        



 
#SortMinToMax(Data)


while True:

    filename='portfolio_data.txt'
    Data = list()
    for line in open(filename, encoding="utf8"):    # otevření souboru a načtení řádky po řádku
        line = line.rstrip()                        # rstrip() - odstraní bílá místa na pravo
        field = line.split(":") # type of fields = list
        Data.append(field)

    SortedData = SortMinToMax(Data)
    MyTab = GenerateTab(SortedData)
    PrintTab(MyTab)
    GetData(MyTab)

#print(MyTab[len(MyTab)-1])
#"""





