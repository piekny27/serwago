from serwago import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConnection(metaclass=Singleton):
    def __init__(self):
        self._engine = db
        Session = self._engine.session
        self.session = Session
    
    def flush(self):
        self.session.commit()

    def fetchUsers(self):
        return self.session.query(User).all()
    
    def getUser(self, name):
        return self.session.query(User).filter(User.username == name).first()

    def getRoleName(self, id):
        return self.session.query(UserRole).filter(UserRole.id == id).first().name
    
    def addUser(self, user):
        self._engine.session.add(user)
    
class UserRole(db.Model):
    BASIC = "BASIC"
    ADMIN = "ADMIN"
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    user = db.relationship('User', backref=db.backref('users'))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    password_hash = db.Column(db.String(60), nullable = False)
    active = db.Column(db.Boolean(), nullable = False, default = True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    profile_id=db.Column(db.Integer, db.ForeignKey("profiles.id", ondelete="CASCADE"),nullable=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def role(self):
        return DBConnection().getRoleName(self.role_id)

class UserProfile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    gender = db.Column(db.String(6))
    nationality = db.Column(db.String(30))
    avatarName = db.Column(db.String(30))
    user=db.relationship('User', backref=db.backref("profiles"))
    

    
class Koszyk (db.Model):
    __tablename__="koszyk"
    id = db.Column(db.Integer, nullable=False, primary_key= True)
    id_towar = db.Column(db.Integer, db.ForeignKey("towar.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

class Towar(db.Model):
    __tablename__="towar"
    id = db.Column(db.Integer, primary_key= True)
    nazwa=db.Column(db.String(50), nullable = False, unique = True)
    id_rodzaj=db.Column(db.Integer, db.ForeignKey("rodzaj.id"), nullable=False)
    ilosc=db.Column(db.Integer)
    cena=db.Column(db.Float)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"), nullable=False)
    
    
class Rodzaj(db.Model):
    __tablename__="rodzaj"
    id = db.Column(db.Integer, primary_key= True)
    nazwa = db.Column(db.String(50), nullable = False, unique = True)


class CPU (db.Model):
    __tablename__="cpu"
    id= db.Column(db.Integer, primary_key= True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.Integer, db.ForeignKey("towar.id"))
    rdzenie=db.Column(db.Integer)
    watki=db.Column(db.Integer)
    id_architektura=db.Column(db.Integer, db.ForeignKey("architektura.id"))
    zegarbase=db.Column(db.Integer)
    zegarmax=db.Column(db.Integer)
    iGPU=db.Column(db.Boolean())
    tdp=db.Column(db.Integer)
    cache=db.Column(db.String(8))
    id_socket=db.Column(db.Integer, db.ForeignKey("socket.id"))


class Producent (db.Model):
    __tablename__='producent'
    id=db.Column(db.Integer, primary_key=True)
    producent=db.Column(db.String(20), nullable = False, unique = True)

class Architektura (db.Model):
    __tablename__='architektura'
    id=db.Column(db.Integer, primary_key=True)
    architektura=db.Column(db.String(30), nullable = False, unique = True)

class Socket (db.Model):
    __tablename__='socket'
    id=db.Column(db.Integer, primary_key=True)
    socket=db.Column(db.String(10), nullable = False, unique = True)

class GPU(db.Model):
    __tablename__="gpu"
    id= db.Column(db.Integer, primary_key= True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.Integer, db.ForeignKey("towar.id"))
    pamiecilosc=db.Column(db.Integer)
    id_pamiectyp=db.Column(db.Integer, db.ForeignKey("pamiectyp.id"))
    rdzenietakt=db.Column(db.Integer)
    rdzenietaktturbo=db.Column(db.Integer)
    pamiecietakt=db.Column(db.Integer)
    cuda=db.Column(db.Integer)
    rdzeniert=db.Column(db.Integer)
    rdzenietensor=db.Column(db.Integer)
    dlugosckarty=db.Column(db.Integer)
    id_pcie=db.Column(db.String(25), db.ForeignKey("pcie.id"))
    zlaczaVGA=db.Column(db.Integer)
    zlaczaDVI=db.Column(db.Integer)
    zlaczaHDMI=db.Column(db.Integer)
    zlaczaDP=db.Column(db.Integer)
    tdp=db.Column(db.Integer)
    id_laczeniekart=db.Column(db.Integer, db.ForeignKey("laczeniekart.id"))


class Laczeniekart(db.Model):
    __tablename__='laczeniekart'
    id=db.Column(db.Integer, primary_key=True)
    laczeniekart=db.Column(db.String(12), nullable=False, unique=True)
    maxilosckart=db.Column(db.Integer)
    
class Pamiectyp(db.Model):
    __tablename__="pamiectyp"
    id=db.Column(db.Integer, primary_key=True)
    pamiectyp=db.Column(db.String(8), nullable = False, unique = True)


class Pcie(db.Model):
    __tablename__="pcie"
    id=db.Column(db.Integer, primary_key=True)
    pcie=db.Column(db.String(20), nullable = False, unique = True)



class Sluchawki(db.Model):
    __tablename__="sluchawki"
    id=db.Column(db.Integer, primary_key=True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.Integer, db.ForeignKey("towar.id"))
    id_typsluchawek=db.Column(db.Integer, db.ForeignKey("typsluchawek.id"))
    dlugosckabla=db.Column(db.Float)



class TypSluchawek(db.Model):
    __tablename__="typsluchawek"
    id=db.Column(db.Integer, primary_key=True)
    typsluchawek=db.Column(db.String(20), nullable = False, unique = True)

class Myszki(db.Model):
    __tablename__="myszki"
    id=db.Column(db.Integer, primary_key=True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.Integer, db.ForeignKey("towar.id"))
    id_typmyszki=db.Column(db.Integer, db.ForeignKey("typmyszki.id"))
    id_typsensora=db.Column(db.Integer, db.ForeignKey("typsensora.id"))
    dlugosckabla=db.Column(db.Integer)
    czulosc=db.Column(db.Integer)
    id_interfejs=db.Column(db.Integer, db.ForeignKey("interfejs.id"))

class TypMyszki(db.Model):
    __tablename__="typmyszki"
    id=db.Column(db.Integer, primary_key=True)
    typmyszki=db.Column(db.String(20), nullable = False, unique = True)

class TypSensora(db.Model):
    __tablename__="typsensora"
    id=db.Column(db.Integer, primary_key=True)
    typsensora=db.Column(db.String(20), nullable = False, unique = True)

class Klawiatury(db.Model):
    __tablename__="klawiatury"
    id=db.Column(db.Integer, primary_key=True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.Integer, db.ForeignKey("towar.id"))
    id_typklawiatury=db.Column(db.Integer, db.ForeignKey("typklawiatury.id"))
    dlugosckabla=db.Column(db.Integer)
    id_interfejs=db.Column(db.Integer, db.ForeignKey("interfejs.id"))



class TypKlawiatury(db.Model):
    __tablename__="typklawiatury"
    id=db.Column(db.Integer, primary_key=True)
    typklawiatury=db.Column(db.String(20), nullable = False, unique = True)





class Interfejs(db.Model):
    __tablename__="interfejs"
    id=db.Column(db.Integer, primary_key=True)
    interfejs=db.Column(db.String(25), nullable = False, unique = True)


