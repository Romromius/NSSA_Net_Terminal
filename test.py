import json


class NSSADataBank:
    def __init__(self):
        """
        Конструктор класса NSSADataBank загружает данные из JSON-файла 'databank.json'.
        Файл должен быть в формате JSON, где ключами являются названия тем,
        а значениями — словари с содержимым для разных языков и паролем.

        Пример структуры файла:
        {
            "topic1": {
                "password": "12345",
                "content": {
                    "english": {
                        "has_password": "This is a protected content in English",
                        "no_password": "This is a public content in English"
                    },
                    "spanish": {
                        "has_password": "Este es un contenido protegido en español",
                        "no_password": "Este es un contenido público en español"
                    }
                }
            }
        }
        """
        # Загружаем данные из файла databank.json
        with open('databank.json', 'r', encoding='utf-8') as f:
            self.data: dict = json.load(f)

    def get_data(self, key, password=None, language='english'):
        """
        Возвращает данные для заданного ключа (key), если такие данные существуют.

        :param key: Ключ, по которому ищется нужная тема в self.data.
        :param password: Пароль для доступа к защищённому контенту (опционально).
        :param language: Язык контента, который нужно вернуть (по умолчанию — 'english').

        :return: Возвращает контент в зависимости от наличия пароля и правильности его ввода:
                 - Если тема существует и язык поддерживается:
                     - Возвращает защищённый контент, если введён верный пароль.
                     - Возвращает публичный контент, если пароль не введён или неверен.
                 - Если язык не поддерживается, возвращает строку 'UNKNOWN LANGUAGE'.
                 - Если ключ не найден, возвращает строку 'NO DATA'.
        """
        # Получаем тему по ключу
        topic = self.data.get(key, None)

        if topic:
            # Проверяем, существует ли контент на указанном языке
            if topic['content'].get(language):
                # Проверяем правильность пароля
                if password == topic['password']:
                    # Возвращаем защищённый контент
                    return topic['content'][language]['has_password']
                else:
                    # Возвращаем публичный контент
                    return topic['content'][language]['no_password']
            else:
                # Если язык не поддерживается
                return 'UNKNOWN LANGUAGE'
        else:
            # Если ключ не найден в базе данных
            return 'NO DATA'


bank = NSSADataBank()
print(bank.get_data('blackout'))
print(bank.get_data('blackout', '1234'))
print(bank.get_data('blackout', '1234', 'russian'))