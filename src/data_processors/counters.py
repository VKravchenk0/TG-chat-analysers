from abc import ABC, abstractmethod
from datetime import timedelta, datetime

from enum import Enum


def percentage(part, whole):
    return 100 * float(part) / float(whole)


class LanguagePercentageCounterType(Enum):
    SIMPLE = 1
    WEIGHTED = 2


class TimeSpanType(Enum):
    WEEK = 1
    MONTH = 2


class AbstractLanguagePercentageCounter(ABC):

    @abstractmethod
    def count_language_percentages(self, messages, timespan_type: TimeSpanType):
        pass


class SimpleLanguagePercentageCounter(AbstractLanguagePercentageCounter):
    def count_language_percentages(self, messages, timespan_type: TimeSpanType):
        number_of_messages_by_timespans = self.count_number_of_messages_by_time_period(messages)
        lang_percentage_by_timespans = self.count_percentages(number_of_messages_by_timespans)
        result = self.convert_to_result_dto(lang_percentage_by_timespans)
        return result

    def count_number_of_messages_by_time_period(self, messages):
        minimized_messages = list(map(self.extract_lang_and_date, enumerate(messages)))
        number_of_messages_by_timespans = {}
        for m in minimized_messages:
            if m['beginning_of_timespan_str'] not in number_of_messages_by_timespans:
                number_of_messages_by_timespans[m['beginning_of_timespan_str']] = {'uk': 0, 'ru': 0}
            number_of_messages_by_timespans[m['beginning_of_timespan_str']][m['lang']] = \
                number_of_messages_by_timespans[m['beginning_of_timespan_str']][m['lang']] + 1
        return number_of_messages_by_timespans

    def extract_lang_and_date(self, index_message_tuple):
        index = index_message_tuple[0]
        message = index_message_tuple[1]
        dt = datetime.fromisoformat(message["date"])
        timespan_start = dt - timedelta(days=dt.weekday())
        result = {
            'lang': message["detected_lang"],
            'date': dt,
            'beginning_of_timespan': timespan_start,
            'beginning_of_timespan_str': timespan_start.strftime("%d/%m/%Y"),
        }
        return result

    def count_percentages(self, number_of_messages_by_timespans):
        messages_percentage = {}
        for timespan_start, messages_counts in number_of_messages_by_timespans.items():
            if timespan_start not in messages_percentage:
                messages_percentage[timespan_start] = {'uk': 0.0, 'ru': 0.0}
            total_number_of_messages_per_timespan = messages_counts['uk'] + messages_counts['ru']
            uk_percentage = percentage(messages_counts['uk'], total_number_of_messages_per_timespan)
            ru_percentage = percentage(messages_counts['ru'], total_number_of_messages_per_timespan)
            messages_percentage[timespan_start]['uk'] = uk_percentage
            messages_percentage[timespan_start]['ru'] = ru_percentage
            print(
                f"Timespan: {timespan_start}. Total number of messages: {total_number_of_messages_per_timespan}. Uk: {messages_counts['uk']}. Ru: {messages_counts['ru']}. Uk percentage: {uk_percentage}. Ru percentage: {ru_percentage}")
        return messages_percentage

    def convert_to_result_dto(self, messages_percentage):
        result = {
            'timespan_start': [],
            'uk_percentage': [],
            'ru_percentage': []
        }
        for timespan_start, language_percentages in messages_percentage.items():
            result['timespan_start'].append(timespan_start)
            result['uk_percentage'].append(language_percentages['uk'])
            result['ru_percentage'].append(language_percentages['ru'])
        return result


class WeightedLanguagePercentageCounter(AbstractLanguagePercentageCounter):
    def count_language_percentages(self, messages, timespan_type: TimeSpanType):

        # split into timespan chunks
        messages_by_timespans = self.get_messages_by_timespans(messages, timespan_type)
        lang_by_users = self.get_language_by_users(messages_by_timespans)
        # count percentage for each timespan
        percentages_by_timespans = self.count_percentages_by_timespans(lang_by_users)
        result = self.convert_to_expected_format(percentages_by_timespans)
        return result

    def get_messages_by_timespans(self, messages, timespan_type: TimeSpanType):
        messages_by_timespans = {}
        for message in messages:
            timespan_start_str = self.get_timespan_start_date(message, timespan_type)
            if timespan_start_str not in messages_by_timespans:
                messages_by_timespans[timespan_start_str] = []
            messages_by_timespans[timespan_start_str].append(message)
        return messages_by_timespans

    def get_timespan_start_date(self, message, timespan_type):
        dt = datetime.fromisoformat(message["date"])
        # beginning of the week by default
        timespan_start = dt - timedelta(days=dt.weekday())
        if timespan_type == TimeSpanType.MONTH:
            # beginning of the month
            timespan_start = dt - timedelta(days=(dt.day - 1))
        timespan_start_str = timespan_start.strftime("%d/%m/%Y")
        return timespan_start_str

    def get_language_by_users(self, messages_by_timespans):
        result = {}
        for timespan_start, messages in messages_by_timespans.items():
            r = self.count_messages_by_user_in_a_timespan_chunk(messages)
            result[timespan_start] = r
            
        return result

    def count_messages_by_user_in_a_timespan_chunk(self, messages):
        result = {}
        for m in messages:
            if m['from_id'] not in result:
                result[m['from_id']] = {'uk': 0, 'ru': 0}
            result[m['from_id']][m['detected_lang']] = result[m['from_id']][m['detected_lang']] + 1

        flatten_dict = self.flatten_dict(result)
        return flatten_dict

    def flatten_dict(self, input_dict):
        result = []
        for user_id, lang_percentages in input_dict.items():
            lang_percentages['user_id'] = user_id
            result.append(lang_percentages)
            
        return result

    def count_percentages_by_timespans(self, lang_by_users):
        result = {}
        for timespan_start, users_lang_percentage in lang_by_users.items():
            print("---------------")
            print(f"Timespan start: {timespan_start}")
            total_percentages = self.count_percentage_by_timespan(users_lang_percentage)
            result[timespan_start] = total_percentages
        return result

    def count_percentage_by_timespan(self, input_list):
        avg_messages_per_user = (sum(u['uk'] + u['ru'] for u in input_list)) / len(input_list)
        print(f'Average number of messages per user: {avg_messages_per_user}')

        for u in input_list:
            id = u['user_id']
            messages_total = u['uk'] + u['ru']
            u['weight'] = avg_messages_per_user / messages_total

        weighted_messages_per_language = {
            'uk': 0,
            'ru': 0
        }

        print('----- Counting weights')
        for u in input_list:
            print('')
            weight = u['weight']
            print(f'User: {u}')
            print(f"Weight for user {u['user_id']}: {u['weight']}")
            weighted_uk_messages = u['uk'] * weight
            print(f"weighted uk messages: {weighted_uk_messages}")
            weighted_messages_per_language['uk'] = weighted_messages_per_language['uk'] + weighted_uk_messages

            weighted_ru_messages = u['ru'] * weight
            print(f"weighted ru messages: {weighted_ru_messages}")
            weighted_messages_per_language['ru'] = weighted_messages_per_language['ru'] + weighted_ru_messages

        print(f"weighted messages per language: {weighted_messages_per_language}")

        total_number_of_weighted_messages = weighted_messages_per_language['uk'] + weighted_messages_per_language['ru']
        print(f"Total number of weighted messages: {total_number_of_weighted_messages}")

        lang_percentages = {
            'uk': 0,
            'ru': 0
        }

        lang_percentages['uk'] = percentage(weighted_messages_per_language['uk'], total_number_of_weighted_messages)
        lang_percentages['ru'] = percentage(weighted_messages_per_language['ru'], total_number_of_weighted_messages)

        print(lang_percentages)
        return lang_percentages

    def convert_to_expected_format(self, percentages_by_timespans):
        result = {
            'timespan_start': [],
            'uk_percentage': [],
            'ru_percentage': []
        }
        for timespan_start, percentages in percentages_by_timespans.items():
            result['timespan_start'].append(timespan_start)
            result['uk_percentage'].append(percentages['uk'])
            result['ru_percentage'].append(percentages['ru'])
        return result


