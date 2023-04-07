from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
db = SQLAlchemy(app)

# Creamos el modelo de la base de datos

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    # Creamos un metodo para mostrar los datos

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }     

# Creamos las tablas para la base de datos
 
with app.app_context():
    db.create_all()    


# Rutas

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()    
    return jsonify({'contacts': [contact.serialize() for contact in contacts]})

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(contact)
    db.session.commit()

    return jsonify({'message': 'contacto creado con exito', 'contact': contact.serialize()}), 201 

# VERIFUCAS SI UN CONTACTO EXISTE

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)   
    if not contact:
        return jsonify({'message': 'contacto no encontrado'}), 404
    return jsonify({'contact': contact.serialize()}) 


# ACTUALIZAR UN CONTACTO

@app.route('/contacts/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)   
    data = request.get_json()
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone'] 

    # Guardamos los cambios en l;a base de datos
        db.session.commit()       
    
    return jsonify({'message': 'contacto actualizado con exito', 'contact': contact.serialize()})


# Eliminar un contacto

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({'message': 'contacto no encontrado'}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'contacto eliminado con exito'})