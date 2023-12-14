import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app, db
from app.models import Data

class TestDataRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.db = db

        with self.app.app_context():
            self.db.create_all()

    def tearDown(self):
        with self.app.app_context():
            self.db.drop_all()

    def test_insert_data(self):
        response = self.client.post("/data", json={"name": "Test de datos"})
        self.assertEqual(response.status_code, 200)

        # Verificar que los datos están en la base de datos
        with self.app.app_context():
            data = db.session.query(Data).filter_by(name="Test de datos").first()
            self.assertIsNotNone(data)

    def test_get_all_data(self):
        # Insertar datos de prueba
        with self.app.app_context():
            db.session.add(Data(name="Dato 1"))
            db.session.add(Data(name="Dato 2"))
            db.session.commit()

        response = self.client.get("/data")
        self.assertEqual(response.status_code, 200)

        data_list = response.json
        self.assertEqual(len(data_list), 2)
        self.assertEqual(data_list[0]["name"], "Dato 1")
        self.assertEqual(data_list[1]["name"], "Dato 2")

    def test_delete_data(self):
        # Insertar datos de prueba
        with self.app.app_context():
            db.session.add(Data(name="Borrar datos"))
            db.session.commit()

        # Obtener el ID del dato recién insertado
        with self.app.app_context():
            data_id = db.session.query(Data).filter_by(name="Borrar datos").first().id

        # Enviar solicitud de eliminación
        response = self.client.delete(f"/data/{data_id}")
        self.assertEqual(response.status_code, 200)

        # Verificar que el dato se haya eliminado de la base de datos
        with self.app.app_context():
            data = db.session.query(Data).filter_by(name="Borrar datos").first()
            self.assertIsNone(data)

if __name__ == "__main__":
    unittest.main()
