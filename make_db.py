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
        self.genUserRoles()
        self.genUsers()
        self.genRodzaje()
        self.genTowary()
        self.genKoszyk()

    def genUserRoles(self):
        self.db.session.add(UserRole(id=1, name=UserRole.BASIC))
        self.db.session.add(UserRole(id=2, name=UserRole.ADMIN))
        self.db.flush()


    def genUsers(self):
        usernames = ["Bartek", "Ola", "Karolina", "Kasia", "Natalia", "Krzysztof", "Jan"]
        admin = User(username="Kacper", email="Kacper@gmail.com", password_hash=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)), role_id = 2)
        self.db.addUser(admin)
        self.users.append(admin)
        for user in usernames:
            user = User(username=user, email=user+"@gmail.com", password_hash=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)), role_id = 1)
            self.users.append(user)
            self.db.addUser(user)
        self.db.flush()

    def genRodzaje(self):
        rodzaje = ["Układy scalone", "Słuchawki", "Karty graficzne", "Procesory", "Klawiatury", "Obudowy", "Myszki"]
        for rodzaj in rodzaje:
            self.db.session.add(Rodzaj(nazwa=rodzaj))
            self.db.session.commit()

    def genTowary(self):
        inc = 0
        towary = ["Arduino Nano", "Steelseries Arctis 5", "RTX 3090 Ti", "Intel Core i7-12900K", "Steelseries Apex 7", "Zalman Z-Machine 500 ARGB", "Razer Mamba Elite"]
        for towar in towary:
            self.db.session.add(Towar(nazwa=towar, id_rodzaj = inc))
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

if __name__ == "__main__":
    generator = DBGenerator()
    generator.cleanDB()
    generator.genDB()