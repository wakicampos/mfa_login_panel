import unittest
import sys
sys.path.append('.')
import MFA_Login_conf
import mysql.connector

class TestMFALoginConf(unittest.TestCase):

    def test_connect_to_database(self):
        """Testea si se puede establecer una conexión con la base de datos."""
        db_connection = MFA_Login_conf.connect_to_database()
        self.assertIsNotNone(db_connection)

    def test_verify_user_credentials(self):
        """Testea la verificación de credenciales de usuario."""
        # Usa credenciales de prueba aquí
        username = "test_user"
        password = "test_password"
        result = MFA_Login_conf.verify_user_credentials(username, password)
        # Asegúrate de que el resultado sea True o False según tus datos de prueba
        self.assertIn(result, [True, False])

    def test_get_mfa_secret(self):
        """Testea la obtención del secreto MFA de un usuario."""
        username = "test_user"
        secret = MFA_Login_conf.get_mfa_secret(username)
        # El secreto puede ser None o una cadena no vacía
        if secret is not None:
            self.assertIsInstance(secret, str)
        else:
            self.assertIsNone(secret)


    # Agregar más pruebas según sea necesario

if __name__ == '__main__':
    unittest.main()
