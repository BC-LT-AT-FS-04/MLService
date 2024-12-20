import unittest
from unittest.mock import Mock, patch

from models.Recognizer.ObjectRecognizer import ObjectRecognizerYolo

class ObjectRecognizerTest(unittest.TestCase):
    def setUp(self):
        self.instance = ObjectRecognizerYolo()
        self.model_path = 'models/Recognizer/yolo11n.pt'

    #Successful Model Loading
    def test_load_model_success(self):
        self.instance.model_path = self.model_path
        self.instance.load_model()
        self.assertIsNotNone(self.instance.loaded_model)
        print("El modelo se cargó exitosamente.")

    #Failed Model Loading
    def test_load_model_failure(self):
        self.instance.model_path = 'yolo12n.pt'
        with self.assertRaises(RuntimeError) as context:
            self.instance.load_model()

        # Verify that the exception message contains "Error al cargar el modelo"
        self.assertIn("Error al cargar el modelo", str(context.exception))

    #Loading model labels
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='{"0": "cat", "1": "dog", "3": "person"}')
    def test_load_labels(self, mock_open):
        # Test to verify loading labels from a JSON file
        labels = self.instance.load_labels("fake_labels_path")
        mock_open.assert_called_once_with("fake_labels_path", 'r')
        self.assertEqual(labels, {"0": "cat", "1": "dog", "3": "person"})

    # Verify that the word ID is correct
    def test_word_id_success(self):
        word_id = self.instance.get_word_id("person")
        self.assertEqual(word_id, 0)

    # Verify that an exception is raised if the word does not exist in labels
    def test_word_id_failure(self):
        with self.assertRaises(ValueError) as context:
            self.instance.get_word_id("fish")
        self.assertIn("La palabra clave 'fish' no está en la lista de etiquetas.", str(context.exception))

     # Verify that an exception is raised if the word parameter is missing
    def test_recognize_missing_word(self):
        with self.assertRaises(ValueError) as context:
            self.instance.recognize("test_path", confidence_threshold=0.1)
        self.assertIn("The 'word' parameter is required.", str(context.exception))

    #Verify that the model recognizes correctly
    def test_recognize(self):
        image_path = 'uploads/Filexample/1.jpeg'
        result = self.instance.recognize(image_path, confidence_threshold=0.5, word='person')

        self.assertIsNotNone(result)
        self.assertEqual(result.word, 'person')
        self.assertTrue(result.percentage >= 0.5)
        self.assertEqual(result.path, '1.jpeg')
        self.assertEqual(result.algorithm, "Yolo11")
        self.assertEqual(result.time, "1")