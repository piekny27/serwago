from xml.etree.ElementTree import ProcessingInstruction
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
        self.genGPU()
        self.genMyszki()
        self.genKlawiatury()
        self.genSluchawki()
        self.genProducent()
        self.genArchitektura()
        self.genSocket()
        self.genInterfejs()
        self.genLaczeniekart()
        self.genPamiectyp()
        self.genPcie()
        self.genTypMyszki()
        self.genTypSensora()
        self.genTypKlawiatury()
        self.genTypSluchawek()
        


    def genUserRoles(self):
        self.db.session.add(UserRole(id=1, name=UserRole.BASIC))
        self.db.session.add(UserRole(id=2, name=UserRole.ADMIN))
        self.db.flush()


    def genUsers(self):
        usernames = ["Bartek", "Ola", "Karolina", "Kasia", "Natalia", "Krzysztof", "Jan", "Aleksander", "Mateusz", "Piotr"]
        admin = User(username="Kacper", email="Kacper@gmail.com", password_hash=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)), role_id = 2, profile_id=random.randint(1,10))
        self.db.addUser(admin)
        admin = User(username="Aleksander Trzeciak", email="olexix@gmail.com", password='12345678', role_id = 2, profile_id=random.randint(1,10))
        self.db.addUser(admin)
        admin = User(username="Piotr Orwiński", email="difortis3@gmail.com", password='12345678', role_id = 2, profile_id=random.randint(1,10))
        self.db.addUser(admin)
        admin = User(username="Mateusz Piękny", email="m.piekny97@gmail.com", password='12345678', role_id = 2, profile_id=random.randint(1,10))
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
            cenar=random.uniform(1.0, 10000.0)
            new_Towar=Towar(nazwa=towar, id_rodzaj=random.randint(3,5), ilosc=random.randint(0, 1000), cena=round(cenar, 2) , id_producent=random.randint(1,8))
            self.db.session.add(new_Towar)
            self.db.session.commit()
            self.towary.append(new_Towar)
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

    def genProducent(self):
        inc = 0
        producent = ["Intel", "NVIDIA", "AMD", "Steelseries", "Razer", "Zalman"]
        for producent in producent:
                self.db.session.add(Producent(producent=producent))
                self.db.session.commit()
                inc+=1

   
    def genCPU(self):
            for towar in self.towary:
                if towar.id_rodzaj==4:
                        self.db.session.add(CPU(id_producent=1, model=towar.id, rdzenie=8, watki=8, id_architektura=6, zegarbase=2.9, zegarmax=4.3, iGPU=0, tdp=65, cache="12 MB", id_socket=4))
                        self.db.session.commit()  


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

    def genGPU(self):
            for towar in self.towary:
                if towar.id_rodzaj==3:
                        self.db.session.add(GPU(id_producent=3, model=towar.id, pamiecilosc=24, id_pamiectyp=6, rdzenietakt=1560, rdzenietaktturbo=1950, cuda=10752, rdzeniert=84, rdzenietensor=336, dlugosckarty=326, id_pcie=1, zlaczaVGA=0, zlaczaDVI=0, zlaczaHDMI=1, zlaczaDP=3, tdp=450, id_laczeniekart=1))
                        self.db.session.commit()  


    def genPamiectyp(self):
        inc = 0
        pamiectyp = ["DDR3", "DDR5", "GDDR5", "GDDR5X", "GDDR6", "GDDR6X", "HBM2"]
        for pamiectyp in pamiectyp:
            self.db.session.add(Pamiectyp(pamiectyp=pamiectyp))
            self.db.session.commit()
            inc+=1
        
    def genLaczeniekart(self):
        self.db.session.add(Laczeniekart(laczeniekart="SLI", maxilosckart=4))
        self.db.session.add(Laczeniekart(laczeniekart="CrossFireX", maxilosckart=4))
        self.db.session.add(Laczeniekart(laczeniekart="Brak", maxilosckart=0))
        self.db.session.commit()


    def genPcie(self):
        inc = 0
        pcie = ["PCI-Express 4.0 x16", "PCI-Express 4.0 x8", "PCI-Express 4.0 x4", "PCI-Express 3.0 x16", "PCI-Express 3.0 x8", "PCI-Express 3.0 x4", "PCI-Express 2.0 x16", "PCI-Express 2.0 x8", "PCI-Express 2.0 x4"]
        for pcie in pcie:
            self.db.session.add(Pcie(pcie=pcie))
            self.db.session.commit()
            inc+=1

    def genMyszki(self):
            for towar in self.towary:
                if towar.id_rodzaj==7:
                        self.db.session.add(Myszki(id_producent=4, model=towar.id))
                        self.db.session.commit()


    def genTypMyszki(self):
        inc = 0
        typmyszki=["Bezprzewodowa", "Przewodowa"]
        for typmyszki in typmyszki:
            self.db.session.add(TypMyszki(typmyszki=typmyszki))
            self.db.session.commit()
            inc+=1

    def genTypSensora(self):
        inc = 0
        typsensora=["Laserowy", "Optyczny"]
        for typsensora in typsensora:
            self.db.session.add(TypSensora(typsensora=typsensora))
            self.db.session.commit()
            inc+=1


    def genKlawiatury(self):
            for towar in self.towary:
                if towar.id_rodzaj==5:
                        self.db.session.add(Klawiatury(id_producent=4, model=towar.id, id_typklawiatury=random.randint(1,2), dlugosckabla=random.uniform(0.0, 3.0), id_interfejs=random.randint(1,2)))
                        self.db.session.commit()

    def genTypKlawiatury(self):
        inc = 0
        typklawiatury=["Bezprzewodowa", "Przewodowa"]
        for typklawiatury in typklawiatury:
            self.db.session.add(TypKlawiatury(typklawiatury=typklawiatury))
            self.db.session.commit()
            inc+=1

    def genSluchawki(self):
            for towar in self.towary:
                if towar.id_rodzaj==2:
                        self.db.session.add(Sluchawki(id_producent=4, model=towar.id, id_typsluchawek=random.randint(1,2), dlugosckabla=random.uniform(0.0, 3.0)))
                        self.db.session.commit()




    def genTypSluchawek(self):
        inc = 0
        typsluchawek=["Bezprzewodowe", "Przewodowe"]
        for typsluchawek in typsluchawek:
            self.db.session.add(TypSluchawek(typsluchawek=typsluchawek))
            self.db.session.commit()
            inc+=1
    
    def genInterfejs(self):
        inc = 0
        interfejs=["USB", "Bluetooth"]
        for interfejs in interfejs:
            self.db.session.add(Interfejs(interfejs=interfejs))
            self.db.session.commit()
            inc+=1



if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.genDB()