from flask import Flask, render_template, request, jsonify
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Contact

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True 
app.config['ENV'] = 'development' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@host:port/database' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/contact' 
db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)
CORS(app)


#Pagina que mostrara al levantar la aplicacion
@app.route("/")
def main():
    return render_template("index.html")



@app.route("/contactos", methods=["GET"])
def getContactos():
    contactos = Contact.query.all()
    if contactos:
        contactos = list(map(lambda contacto: contacto.serialize(), contactos))
        return jsonify(contactos),200
    else:
        return jsonify({"msg": "No hay contactos"})

@app.route("/contactos/<user>", methods=["GET"])
def getContacto(user):
    #contactos = Contact.query.filter_by(nombre = user).all()#Traigo todos los que su nombre sean iguales
    contactos = Contact.query.filter(Contact.nombre.ilike(f"%{user}%"))#OJO CON EL FILTER, ES DISTINTO AL OTRO Y TRAEN DISTINTAS COSAS
    if contactos:
        contactos=list(map(lambda contacto: contacto.serialize(), contactos))
        return jsonify(contactos), 200
    else:
        return jsonify({"msg": "No existe ese contacto"})

@app.route("/contactos/", methods=["POST"])
def postContacto():
    valor_nombre = request.json.get("nombre", None)
    valor_email =  request.json.get("email", None)
    valor_telefono = request.json.get("telefono", None)
    valor_direccion = request.json.get("direccion", "")

    if  not valor_nombre or valor_nombre == "":
        return jsonify({"msg": "Error, falta Nombre"}),400
    if not valor_email or valor_email == "":
        return jsonify({"msg": "Error, falta email"}),400
    if not valor_telefono or valor_email == "":
        return jsonify({"msg": "Error, falta teléfono"}),400

    if valor_email:
        #contactoEmail = Contact.query.filter_by(email = valor_email).first() PREGUNTAR
        contactoEmail = Contact.query.filter_by(email = valor_email).first() #preguntar por email específico
        if contactoEmail:
            return jsonify({"msg": "El correo se encuentra ocupado, favor usar otro"})

    objContacto = Contact()
    objContacto.nombre = valor_nombre
    objContacto.email = valor_email
    objContacto.telefono = valor_telefono
    objContacto.direccion = valor_direccion

    db.session.add(objContacto)
    db.session.commit()
  
    return jsonify({"msg": f"usuario {objContacto.nombre} fue creado Exitosamente"}),200


@app.route("/contactos/<int:id>", methods=["PUT"])
def editContacto(id):
    valor_nombre = request.json.get("nombre", None)
    valor_email =  request.json.get("email", None)
    valor_telefono = request.json.get("telefono", None)
    valor_direccion = request.json.get("direccion", "")

    if  not valor_nombre or valor_nombre == "":
        return jsonify({"msg": "Error, falta Nombre"}),400
    if not valor_email or valor_email == "":
        return jsonify({"msg": "Error, falta email"}),400
    if not valor_telefono or valor_email == "":
        return jsonify({"msg": "Error, falta teléfono"}),400

    if valor_email:
        #contactoEmail = Contact.query.filter_by(email = valor_email).first() PREGUNTAR
        contactoEmail = Contact.query.filter_by(email = valor_email).first() #preguntar por email específico
        if contactoEmail:
            return jsonify({"msg": "El correo se encuentra ocupado, favor usar otro"})

    contactId = Contact.query.get(id)

    if not contactId:
        return jsonify({"msg": "Usuario no encontrado, favor probar nuevamente"})
    
    if valor_nombre:
        contactId.nombre = valor_nombre
    if valor_email:
        contactId.email = valor_email
    if valor_telefono:
        contactId.telefono = valor_telefono

    #Direccion no se valida porque no es obligatorio el campo        
    contactId.direccion = valor_direccion

    db.session.commit()
    return jsonify(contactId.serialize()), 200

    

@app.route("/contactos/<int:id>", methods=["DELETE"])
def deleteContacto(id):
    contacto = Contact.query.get(id)
    if contacto:
        db.session.delete(contacto)
        db.session.commit()

        data={
            "msg": f"Usuario {contacto.nombre} fue eliminado exitosamente"
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "Usuario no encontrado, imposible eliminar"})








if __name__ == "__main__":
    manager.run()