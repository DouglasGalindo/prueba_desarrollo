from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from importlib.metadata import distribution,metadata,version
from datetime import datetime

app = Flask(__name__)



# Configuración de conexión a SQL Server
#app.config['SQLALCHEMY_DATABASE_URI'] = ("mssql+pyodbc://sa:123@192.168.1.68:1433/empresa?driver=ODBC+Driver+18+for+SQL+Server;Encrypt=no")
#app.config['SQLALCHEMY_DATABASE_URI'] = ("mssql+pyodbc://sa:123@192.168.1.68:1433/empresa;Encrypt=no?driver=ODBC+Driver+18+for+SQL+Server")
#app.config['SQLALCHEMY_DATABASE_URI'] = ("mssql+pyodbc://sa:123@192.168.1.68/empresa?driver=ODBC+Driver+17+for+SQL+Server;Encrypt=no")
#app.config['SQLALCHEMY_DATABASE_URI'] = ("mssql+pyodbc://sa:123@192.168.1.68:1433/empresa?driver=ODBC+Driver+18+for+SQL+Server")

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};' \
                   'SERVER=192.168.1.68;' \
                   'DATABASE=empresa;' \
                    "Encrypt=no;"\
                   'UID=sa;' \
                   'PWD=123'
    
  #      conn = pyodbc.connect(conn_str)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc:///?odbc_connect={}'.format(conn_str)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo de empleado
class Empleado(db.Model):
    __tablename__ = 'empleados'  # Asegúrate de que esta tabla exista en tu base de datos
    codigo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    id_departamento = db.Column(db.Integer, nullable=False)
    nombre_cargo = db.Column(db.String(50), nullable=False)
    fecha_contratacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Modelo de Departamentos
class Departamentos(db.Model):
    __tablename__ = 'departamentos'  # Asegúrate de que esta tabla exista en tu base de datos
    id_departamento = db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(100), nullable=False)


# API
api = Api(app)

empleado_model = api.model('Empleados', {
    'codigo': fields.Integer(required=True, description='ID del empleado'),
    'nombre': fields.String(required=True, description='Nombre del empleado'),
    'apellido': fields.String(required=True, description='Apellido del empleado'),
    'id_departamento': fields.Integer(required=True, description='Departamento del empleado'),
    'nombre_cargo': fields.String(required=True, description='Cargo del empleado'),
    'fecha_contratacion': fields.String(required=True, description='Fecha de contratación')
})

departamentos_model = api.model('departamentos', {
    'id_departamento': fields.Integer(required=True, description='ID del departamento'),
    'departamento': fields.String(required=True, description='Nombre del departamento')
})

@api.route('/api/empleados')
class EmpleadoList(Resource):
    def get(self):
        """Listar empleados"""
        empleados = Empleado.query.all()
        return [{'codigo': emp.codigo, 'nombre': emp.nombre, 'apellido': emp.apellido,
                 'id_departamento': emp.id_departamento, 'nombre_cargo': emp.nombre_cargo,
                 'fecha_contratacion': emp.fecha_contratacion.isoformat() } for emp in empleados], 200

    @api.expect(empleado_model)
    def post(self):
        """Agregar un nuevo empleado"""
        nuevo_empleado = Empleado(
            nombre=request.json['nombre'],
            apellido=request.json['apellido'],
            id_departamento=request.json['id_departamento'],
            nombre_cargo=request.json['nombre_cargo'],
            fecha_contratacion=datetime.strptime(request.json['fecha_contratacion'], '%Y-%m-%d')
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        return {'codigo': nuevo_empleado.codigo}, 201

@api.route('/api/empleados/<int:id>')
class EmpleadoResource(Resource):
    def get(self, id):
        """Obtener un empleado por ID"""
        empleado = Empleado.query.get(id)
        if empleado:
            return {'codigo': empleado.codigo, 'nombre': empleado.nombre, 'apellido': empleado.apellido,
                    'id_departamento': empleado.id_departamento, 'nombre_cargo': empleado.nombre_cargo,
                    'fecha_contratacion': empleado.fecha_contratacion.isoformat()}, 200
        return {'message': 'Empleado no encontrado'}, 404

    @api.expect(empleado_model)
    def put(self, id):
        """Actualizar un empleado existente"""
        empleado = Empleado.query.get(id)
        if empleado:
            empleado.nombre = request.json['nombre']
            empleado.apellido = request.json['apellido']
            empleado.id_departamento = request.json['id_departamento']
            empleado.nombre_cargo = request.json['nombre_cargo']
            empleado.fecha_contratacion = datetime.strptime(request.json['fecha_contratacion'], '%Y-%m-%d')
            db.session.commit()
            return {'message': 'Empleado actualizado'}, 200
        return {'message': 'Empleado no encontrado'}, 404

    def delete(self, id):
        """Eliminar un empleado por ID"""
        empleado = Empleado.query.get(id)
        if empleado:
            db.session.delete(empleado)
            db.session.commit()
            return {'message': 'Empleado eliminado'}, 204
        return {'message': 'Empleado no encontrado'}, 404

@api.route('/api/departamentos')
class DepartamentosList(Resource):
    def get(self):
        """Listar departamentos"""
        departamentos = Departamentos.query.all()
        return [{'id_departamento': dep.id_departamento, 'nombre': dep.departamento} for dep in departamentos], 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)


