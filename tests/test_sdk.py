import unittest
from src.sdk import MySDK

class TestMySDK(unittest.TestCase):

    def setUp(self):
        self.sdk = MySDK()

    def test_initialize(self):
        result = self.sdk.initialize()
        self.assertTrue(result)

    def test_execute(self):
        result = self.sdk.execute()
        self.assertEqual(result, "Execution successful")

    def test_shutdown(self):
        result = self.sdk.shutdown()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()