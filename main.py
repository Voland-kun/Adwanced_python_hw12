import csv


class ValidateText:
    def __set_name__(self, owner, name):
        self.param_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        # self.validate(value)
        # setattr(instance, self.param_name, value)
        setattr(instance, self.param_name, self.validate(value))

    def __delete__(self, instance):
        raise AttributeError(f'Свойство "{self.param_name}" нельзя удалять')

    @staticmethod
    def validate(value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError(f'Значение {value} должно быть текстом')
            if not value.isalpha():
                raise ValueError(f'В значении {value} должны быть только буквы')
            if not value.istitle():
                return value.capitalize()
                # raise ValueError(f'В значение {value} должна быть первая заглавная буква')
            return value
    # класс скопирован с лекции, не знаю уместно ли при валидации возвращать значения или только поднимать ошибку
    # закомменченный код возвращает как было т.е. сообщение о заглавной букве


class Student:
    firstname = ValidateText()
    lastname = ValidateText()
    surname = ValidateText()

    def __init__(self, firstname: str, lastname: str, surname=None, *, subjects=None):
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.subjects = subjects
        self.av_score = None

    @property
    def av_score(self):
        return self._av_score

    @av_score.setter
    def av_score(self, value):
        self._av_score = value

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, subjects):
        if subjects is None:
            self._subjects = None
        else:
            self._subjects = {}
            with open(subjects, 'r', encoding='utf-8') as f:
                filereader = csv.reader(f)
                for line in filereader:
                    self._subjects[line[0]] = {'scores': [], 'test_scores': [], 'av_test_score': None}

    def _add_score(self, subject: str, value: list | int | float, sc_type=None):
        if subject not in self._subjects.keys():
            print(self._subjects.keys())
            raise AttributeError("Нет в списке предметов")
        if sc_type is None:
            if 2 <= value <= 5:
                self._subjects[subject]['scores'].append(value)
                count = 0
                average_score = 0
                for i in self._subjects:
                    if self._subjects[i]['scores']:
                        average_score += self.average(self._subjects[i]['scores'])
                        count += 1
                if count > 0:
                    self.av_score = average_score/count
            else:
                raise ValueError("Оценка должна быть от 2 до 5")
        elif sc_type.lower() == 'test':
            if 0 <= value <= 100:
                self._subjects[subject]['test_scores'].append(value)
                self._subjects[subject]['av_test_score'] = self.average(self._subjects[subject]['test_scores'])
            else:
                raise ValueError("Оценка должна быть от 0 до 100")
        else:
            raise ValueError("Некорректный тип оценки")

    def add_score_var(self, subject: str, value: list | int | float, sc_type=None):
        if isinstance(value, list):
            for i in value:
                self._add_score(subject, i, sc_type)
        else:
            try:
                val = int(value)
                if value == val:
                    self._add_score(subject, val, sc_type)
                else:
                    raise ValueError("Оценка должна быть целым числом")
            except Exception:
                raise ValueError("Оценка должна быть целым числом")

    @staticmethod
    def average(subjects):
        return sum(subjects) / len(subjects)

    def __repr__(self):
        sur = f' {self.surname if self.surname is not None else ""}'
        av_subj_list = 'Средние баллы тестов: \n'
        for i in self._subjects:
            av_subj_list += f'{i}: {self._subjects[i]["av_test_score"]}\n'
        return f'Студент: {self.firstname} {self.lastname}{sur}\n' \
               f'{av_subj_list}Средний балл по предметам: {self.av_score}\n'


std = Student('иванов', 'Иван', subjects='subjects.csv')
print(std)
std.add_score_var('математика', [15, 20, 25, 30, 35], 'test')
std.add_score_var('химия', 80, 'test')
std.add_score_var('химия', 72, 'test')
std.add_score_var('физика', [2, 2, 3, 4])
std.add_score_var('математика', [3, 5, 5, 4])
std.add_score_var('русский язык', 3)
print(std)
