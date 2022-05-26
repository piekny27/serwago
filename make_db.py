from serwago.models import *
import random
import datetime
import time
import string

class DBGenerator():
    def __init__(self):
        self.db = DBConnection()
        self.towary = []
        self.users = []

    def cleanDB(self):
        self.db._engine.drop_all()
        self.db._engine.create_all()

    def genDB(self):
        self.genUserProfiles()
        self.genUserRoles()
        self.genUsers()
        self.genRodzaje()
        self.genTowary()
        self.genKoszyk()
        self.genCPU()
        self.genProducent()
        self.genArchitektura()
        self.genSocket()
        self.genLaczeniekart()
        

    def genUserRoles(self):
        self.db.session.add(UserRole(id=1, name=UserRole.BASIC))
        self.db.session.add(UserRole(id=2, name=UserRole.ADMIN))
        self.db.flush()


    def genUsers(self):
        usernames = ["Bartek", "Ola", "Karolina", "Kasia", "Natalia", "Krzysztof", "Jan", "Aleksander", "Mateusz", "Piotr"]
        admin = User(username="Kacper", email="Kacper@gmail.com", password_hash=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)), role_id = 2, profile_id=random.randint(1,10))
        self.db.addUser(admin)
        self.users.append(admin)
        inc=0
        for user in usernames:
            user = User(username=user, email=user+"@gmail.com", password_hash=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)), role_id = 1, profile_id=random.randint(1,10))
            self.users.append(user)
            self.db.addUser(user)
            inc+=1
        self.db.flush()

    def genUserProfiles(self):
        for x in range(10):
            self.db.session.add(UserProfile(first_name="Mateusz", last_name="Kowalski", gender="Male"))
            self.db.session.commit()
    

    def genRodzaje(self):
        rodzaje = ["Układy scalone", "Słuchawki", "Karty graficzne", "Procesory", "Klawiatury", "Obudowy", "Myszki"]
        for rodzaj in rodzaje:
            self.db.session.add(Rodzaj(nazwa=rodzaj))
            self.db.session.commit()

    def genTowary(self):
        inc = 0
        towary = ["Arduino Nano", "Steelseries Arctis 5", "RTX 3090 Ti", "Core i5-10400", "Steelseries Apex 7", "Zalman Z-Machine 500 ARGB", "Razer Mamba Elite", "Ryzen 1700"]
        for towar in towary:
            self.db.session.add(Towar(nazwa=towar, id_rodzaj = inc, ilosc=random.randint(0, 1000), id_producent=random.randint(1,6)))
            self.db.session.commit()
            inc+=1

    def genKoszyk(self):
        num = random.randint(0, 10)
        for koszyk in range(num):
            num2 = random.randint(0, 10)
            for towar in range(num2):
                num3 = random.randint(1, 8)
                num4 = random.randint(1, 8)
                self.db.session.add(Koszyk(id_towar=num3, id_user = num4 ))
                self.db.session.commit()

    def genLaczeniekart(self):
        inc = 0
        laczeniekart=["SLI", "CrossFireX", "Brak"]
       
        
        for laczeniekart in laczeniekart:
            self.db.session.add(Laczeniekart(laczeniekart=laczeniekart, maxilosckart=random.randint(0,4)))
            self.db.session.commit()
            inc+=1


    def genProducent(self):
        inc = 0
        producent = ["Intel", "NVIDIA", "AMD", "Steelseries", "Razer", "Zalman"]
        for producent in producent:
                self.db.session.add(Producent(producent=producent))
                self.db.session.commit()
                inc+=1


    def genArchitektura(self):
        inc = 0
        architektura = ["Skylake", "Cannon Lake","Tiger Lake","Alder Lake","Coffee Lake", "Comet Lake", "Laby Lake", "Zen 1", "Zen 1+", "Zen 2", "Zen 3"]
        for architektura in architektura:
                self.db.session.add(Architektura(architektura=architektura))
                self.db.session.commit()
                inc+=1


    def genSocket(self):
        inc = 0
        socket = ["LGA 1151 (Skylake)", "LGA 1151 (Kaby Lake)", "LGA 1151 (Coffee Lake)", "LGA 1200 (Comet Lake)", "LGA 1200 (Rocket Lake)", "AM4"]
        for socket in socket:
                self.db.session.add(Socket(socket=socket))
                self.db.session.commit()
                inc+=1



   
    def genCPU(self):
     self.db.session.add(CPU(id_producent=1, model=4, rdzenie=8, watki=8, id_architektura=6, zegarbase=2.9, zegarmax=4.3, iGPU=0, tdp=65, cache="12 MB", id_socket=4))
     self.db.session.add(CPU(id_producent=3, model=8, rdzenie=8, watki=16, id_architektura=8, zegarbase=3.0, zegarmax=3.7, iGPU=0, tdp=65, cache="16 MB", id_socket=6))   
     self.db.session.commit()  

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.genDB()