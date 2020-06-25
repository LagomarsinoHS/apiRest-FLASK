from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Contact (db.Model):
    __tablename__ = "contactos"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    direccion = db.Column(db.String(200), nullable=True)

    def serialize(self):
        return{
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "telefono": self.telefono,
            "direccion": self.direccion
        }
