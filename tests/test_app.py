import unittest
from unittest.mock import patch

import app as app_module


class AppStartupTests(unittest.TestCase):
    def test_initialize_database_handles_unavailable_database(self):
        with patch.object(app_module, "wait_for_db", side_effect=RuntimeError("db down")):
            app_module.initialize_database()

        self.assertFalse(app_module.DATABASE_READY)
        self.assertIsNotNone(app_module.DB_INIT_ERROR)


if __name__ == "__main__":
    unittest.main()
