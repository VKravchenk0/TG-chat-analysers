import json
import unittest
from parameterized import parameterized

from src.data_processors.lang_percentage_counter import count_lang_percentage
from src.data_processors.counters import LanguagePercentageCounterType, TimeSpanType

RESOURCE_DIR = '../resources/lang_percentage_counter'


class LangPercentageCounterTest(unittest.TestCase):

    params = []

    @parameterized.expand([
        [TimeSpanType.WEEK, 'expected_result_weekly.json'],
        [TimeSpanType.MONTH, 'expected_result_monthly.json']
    ])
    def test_count_lang_percentage(self, time_span_type, result_file_name):
        print()
        print()
        print("---------------------------------------------------")
        print(f"test_count_percentage start: {time_span_type}")
        input_data = self.load_data_from_file(f'{RESOURCE_DIR}/test_count_lang_percentage/input.json')
        actual_result = count_lang_percentage(input_data, LanguagePercentageCounterType.WEIGHTED, time_span_type)
        print(f"result: {actual_result}")
        expected_result = self.load_data_from_file(f'{RESOURCE_DIR}/test_count_lang_percentage/{result_file_name}')
        self.assertEqual(expected_result, actual_result)

    def load_data_from_file(self, file_location):
        f = open(file_location)
        data = json.load(f)
        f.close()
        return data
