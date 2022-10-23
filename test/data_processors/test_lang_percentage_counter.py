import json
import unittest

from src.data_processors.lang_percentage_counter import count_lang_percentage
from src.data_processors.counters import LanguagePercentageCounterType


RESOURCE_DIR = '../resources/lang_percentage_counter'


class LangPercentageCounterTest(unittest.TestCase):

    def test_count_lang_percentage(self):
        input_data = self.load_data_from_file(f'{RESOURCE_DIR}/test_count_lang_percentage/input.json')
        actual_result = count_lang_percentage(input_data, LanguagePercentageCounterType.WEIGHTED)
        print(f"result: {actual_result}")
        expected_result = self.load_data_from_file(f'{RESOURCE_DIR}/test_count_lang_percentage/expected_result.json')
        self.assertEqual(expected_result, actual_result)

    def load_data_from_file(self, file_location):
        f = open(file_location)
        data = json.load(f)
        f.close()
        return data
