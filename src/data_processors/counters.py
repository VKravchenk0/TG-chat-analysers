from abc import ABC, abstractmethod
from datetime import timedelta, datetime


def percentage(part, whole):
    return 100 * float(part) / float(whole)


class AbstractLanguagePercentageCounter(ABC):

    @abstractmethod
    def count_language_percentages(self, messages):
        pass


class DefaultLanguagePercentageCounter(AbstractLanguagePercentageCounter):
    def count_language_percentages(self, messages):
        number_of_messages_by_weeks = self.count_number_of_messages_by_time_period(messages)
        lang_percentage_by_weeks = self.count_percentages(number_of_messages_by_weeks)
        result = self.convert_to_result_dto(lang_percentage_by_weeks)
        return result

    def count_number_of_messages_by_time_period(self, messages):
        minimized_messages = list(map(self.extract_lang_and_date, enumerate(messages)))
        number_of_messages_by_weeks = {}
        for m in minimized_messages:
            if m['beginning_of_week_str'] not in number_of_messages_by_weeks:
                number_of_messages_by_weeks[m['beginning_of_week_str']] = {'uk': 0, 'ru': 0}
            number_of_messages_by_weeks[m['beginning_of_week_str']][m['lang']] = \
                number_of_messages_by_weeks[m['beginning_of_week_str']][m['lang']] + 1
        return number_of_messages_by_weeks

    def extract_lang_and_date(self, index_message_tuple):
        index = index_message_tuple[0]
        message = index_message_tuple[1]
        dt = datetime.fromisoformat(message["date"])
        week_start = dt - timedelta(days=dt.weekday())
        result = {
            'lang': message["detected_lang"],
            'date': dt,
            'beginning_of_week': week_start,
            'beginning_of_week_str': week_start.strftime("%d/%m/%Y"),
        }
        return result

    def count_percentages(self, number_of_messages_by_weeks):
        messages_percentage = {}
        for week_start, messages_counts in number_of_messages_by_weeks.items():
            if week_start not in messages_percentage:
                messages_percentage[week_start] = {'uk': 0.0, 'ru': 0.0}
            total_number_of_messages_per_week = messages_counts['uk'] + messages_counts['ru']
            uk_percentage = percentage(messages_counts['uk'], total_number_of_messages_per_week)
            ru_percentage = percentage(messages_counts['ru'], total_number_of_messages_per_week)
            messages_percentage[week_start]['uk'] = uk_percentage
            messages_percentage[week_start]['ru'] = ru_percentage
            print(
                f"Week: {week_start}. Total number of messages: {total_number_of_messages_per_week}. Uk: {messages_counts['uk']}. Ru: {messages_counts['ru']}. Uk percentage: {uk_percentage}. Ru percentage: {ru_percentage}")
        return messages_percentage

    def convert_to_result_dto(self, messages_percentage):
        result = {
            'week_start': [],
            'uk_percentage': [],
            'ru_percentage': []
        }
        for week_start, language_percentages in messages_percentage.items():
            result['week_start'].append(week_start)
            result['uk_percentage'].append(language_percentages['uk'])
            result['ru_percentage'].append(language_percentages['ru'])
        return result