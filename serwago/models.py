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
    phonenumber=db.Column(db.Integer)

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

class Koszyk (db.Model):
    _tablename_="koszyk"
    id = db.Column(db.Integer, nullable=False, primary_key= True)
    id_towar = db.Column(db.Integer, db.ForeignKey("towar.id"))
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

class Towar(db.Model):
    _tablename_="towar"
    id = db.Column(db.Integer, primary_key= True)
    nazwa=db.Column(db.String(50), nullable = False, unique = True)
    id_rodzaj=db.Column(db.Integer, db.ForeignKey("rodzaj.id"), nullable=False)
    ilosc=db.Column(db.Integer)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"), nullable=False)
    
    
class Rodzaj(db.Model):
    _tablename_="rodzaj"
    id = db.Column(db.Integer, primary_key= True)
    nazwa = db.Column(db.String(50), nullable = False, unique = True)


class CPU (db.Model):
    _tablename_="cpu"
    id= db.Column(db.Integer, primary_key= True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    model= db.Column(db.String(50), nullable = False, unique = True)
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
    _tablename_='producent'
    id=db.Column(db.Integer, primary_key=True)
    producent=db.Column(db.String(20), nullable = False, unique = True)

class Architektura (db.Model):
    _tablename_='architektura'
    id=db.Column(db.Integer, primary_key=True)
    architektura=db.Column(db.String(30), nullable = False, unique = True)

class Socket (db.Model):
    _tablename_='socket'
    id=db.Column(db.Integer, primary_key=True)
    socket=db.Column(db.String(10), nullable = False, unique = True)
    




class GPU(db.Model):
    _tablename_="gpu"
    id= db.Column(db.Integer, primary_key= True)
    model= db.Column(db.String(60), nullable = False, unique = True)
    id_producent=db.Column(db.Integer, db.ForeignKey("producent.id"))
    pamiecilosc=db.Column(db.Integer)
    pamiectyp=db.Column(db.String(8))
    rdzenietakt=db.Column(db.Integer)
    rdzenietaktturbo=db.Column(db.Integer)
    pamiecietakt=db.Column(db.Integer)
    cuda=db.Column(db.Integer)
    rdzeniert=db.Column(db.Integer)
    rdzenietensor=db.Column(db.Integer)
    dlugosckarty=db.Column(db.Integer)
    pcie=db.Column(db.String(15))
    zlaczaVGA=db.Column(db.Integer)
    zlaczaDVI=db.Column(db.Integer)
    zlaczaHDMI=db.Column(db.Integer)
    zlaczaDP=db.Column(db.Integer)
    tdp=db.Column(db.Integer)
    laczeniekart=db.Column(db.Boolean)




