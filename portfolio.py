import datetime
import requests

class SortedList:

    def __init__(self, sequence = None):           
        self.__key = str.lower
        if sequence is None: 
            self.__list = []
        else:
            self.__list = sorted(sequence, key = self.__key)

    def __str__(self):
        """Vrátí řetězcovou verzi seznamu čitelnou pro člověka."""
        return str(self.__list)

    def add_new(self, value):
        """přidá prvek do seznamu, který tam ještě není"""
        if self.__list.count(value) == 0:
            self.__list.append(value)
            self.__list = sorted(self.__list, key = self.__key)

    def __getitem__(self, index):
        """Vrátí hodnotu na zadané indexové pozici
        >>> L[15]
        """
        return self.__list[index]

    def __len__(self):
        return len(self.__list)

    
class Tab:

    def __init__(self):
        self.X = SortedList()
        self.Y = SortedList()
        self.Z = SortedList()
        self.dict = {}

    def __str__(self):
        space = 20
        r = "{0:<{s}}".format("date",s=space)
        for y in self.Y:
            r += "{0:<{s}}".format(y,s=space)
        r += "{0:<{s}}".format("Total[CZK]",s=space)
        r += "\n"
        for x in self.X:
            r += "{0:<{s}}".format(str(x),s=space)
            tot = 0
            for y in self.Y:
                try:
                    v = SortedList( self.dict[x][y].keys() )
                    z = v[len(v)-1]
                    #print(z)
                    val = (self.dict[x][y][z][0])
                    r += "{0:<{s}}".format(val,s=space)
                    tot += float(self.dict[x][y][z][1])    
                except:
                    r += "{0:<{s}}".format("",s=space)
            r += "{0:<{s}}\n".format(str(tot),s=space)
        return r

    def get_x(self):
        return str(self.X)

    def get_y(self):
        return self.Y

    def get_last(self, y):
        x = self.X[len(self.X)-1]
        v = SortedList( self.dict[x][y].keys() )
        z = v[len(v)-1]
        val = (self.dict[x][y][z][0])
        return val
        

    def update(self, L):
        x = L[0]
        y = L[1]
        z = L[2]
        value = L[3]
        czk = L[4]
        self.X.add_new(x)
        self.Y.add_new(y)
        self.Z.add_new(z)
        try:
            try:
                self.dict[x][y].update({z:[value,czk]})
            except:
                self.dict[x].update({y:{z:[value,czk]}})
        except:
            self.dict.update({x:{y:{z:[value,czk]}}})

   
    






def to_sats(a, m,url='https://blockchain.info/ticker'):
    try:
        eur = requests.get(url).json()['EUR']['15m']
        czk = requests.get(url).json()['CZK']['15m']
    except:
        return None
    if m == "CZK":
        return a/czk*100000000, a
    if m == "EUR":
        return a/eur*100000000, a/eur*czk
    if m == "BTC":
        return a*100000000, a*czk


def Get_data(T):
    t = str(datetime.datetime.now())[:str(datetime.datetime.now()).find(" ")]
    date = input("Zadejte datum [{0}]:".format(t))
    if not date:
        date = t
    for n in T.get_y():
        sat, czk = 0, 0

        amount = input( "Zadejte sumu pro {0}:".format(n) )
        if amount:
            try:
                sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
            except:
                pass
        if not amount:
            try:
                amount = T.get_last(n)
                sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
            except:
                amount = "-"
                czk = 0#"""



        time_stamp = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
        #print("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))
        f = open(filename, "a", encoding="utf8")
        f.write("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))            
        f.close()

    while True:
        sat, czk = 0, 0
        n = input("Zadejte novou položku (př.: Coinbase[BTC]):")
        if not n:
            break
        amount = input("Zaadejte sumu pro {0}:".format(n))
        if amount:
            try:
                sat, czk = to_sats(float(amount),n[n.find("[")+1:n.find("]")])
            except:
                pass
    
        time_stamp = str(datetime.datetime.now()).replace(":","-").replace(" ","_")
        #print("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))
        f = open(filename, "a", encoding="utf8")
        f.write("{0}:{1}:{2}:{3}:{4}\n".format(date,n,time_stamp,amount,czk))            
        f.close()








while True:
    T = Tab()
    
    #T.update(["2021-11-02","BTC","2021-11-09_14-53-25.753076","A.32158","400000"])
    #print(T)
    filename='portfolio_data.txt'
    for line in open(filename, encoding="utf8"):    # otevření souboru a načtení řádky po řádku
        line = line.rstrip()                        # rstrip() - odstraní bílá místa na pravo
        field = line.split(":") # type of fields = list
        T.update(field)
    print(T)
    
    Get_data(T)























