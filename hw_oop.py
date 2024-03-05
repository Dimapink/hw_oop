"""
В рамках поставленной задачи не учтен тот факт, что студент может выставлять оценку за одну лекцию несколько раз.
Если оценками за курс у лекторов будет список, то есть вероятность 'занижения' оценки лектора выставлением
большого количества низких оценок одним студентом. Хранить индекс оценки в списке не удобно и не логично. 
Для избежания дублирования оценок пользователей студентам добавлен атрибут id, который присваивается студенту
(порядковые номера с 1 без ограничения по максимальному значению)

Для корректного подсчета, оценки студента за прослушанные лекции вынесены в отдельный атрибут класса (словарь)
listener_lecture_grades, а структура данных для их хранения у лектора изменена:
{
 Название курса_1:{
                   id_студента1: оценка за лекцию, 
                   id_студента2: оценка за лекцию
                   },
 Название курса_2:{id_студента1: оценка за лекцию}
}

Таким образом при повторном проставлении студентом оценки за уже оцененную лекцию, она будет перезаписана,
а не добавлена в общий пул оценок лектора.

Сейчас программа работает как положено по заданию, чтобы включить обработку последовательных оценок от одного студента,
необходимо раскомментировать код в функциях rate_lecture и get_avg_score и закомментировать соответствующие
открытые строки в которых есть комментарий.
"""


class CounterId:
    def __init__(self):
        self.start = 0

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        return self.start


class Student:
    id_iter = CounterId()

    def __init__(self, name, surname, gender):
        self.id = next(self.id_iter)
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.listener_lecture_grades = {}

    def __str__(self):
        try:
            avg_hw_score = self.get_avg_grade()
        except ZeroDivisionError:
            avg_hw_score = "Оценок за домашние задания пока нет"

        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашнее задание: {avg_hw_score}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def get_avg_grade(self):
        total_grade = sum(*self.grades.values())
        total_len = len(self.grades.values())
        avg_grade = round(total_grade/total_len, 2)
        return avg_grade

    def __eq__(self, other):
        return self.get_avg_grade() == other.get_avg_grade()

    def __ne__(self, other):
        return self.get_avg_grade() != other.get_avg_grade()

    def __lt__(self, other):
        return self.get_avg_grade() < other.get_avg_grade()

    def __gt__(self, other):
        return self.get_avg_grade() > other.get_avg_grade()

    def __le__(self, other):
        return self.get_avg_grade() <= other.get_avg_grade()

    def __ge__(self, other):
        return self.get_avg_grade() >= other.get_avg_grade()

    def rate_lecture(self, grade: int, course: str, lector) -> None:
        """
        Метод лоя оценки лекции студентом
        :param grade: оценка от 0 до 10, иначе будет ошибка
        :param course: курс, преподаватель должен читать на этом курсе, а студет должен на нем обучаться, иначе ошибка
        :param lector: Лектор которому будет проставлена оценка
        :return:
        """
        if course not in self.courses_in_progress + self.finished_courses:
            raise ValueError("Нельзя ставить оценки лекциям не по своим курсам")
        if grade not in list(range(0, 11)):
            raise ValueError("Оценка должна быть числом от 0 до 10")
        if not isinstance(lector, Lecturer) or course not in lector.courses_attached:
            raise ValueError("Лектор не читает на данном курсе")
        self.listener_lecture_grades[course] = grade
        lector.lecture_grades.setdefault(course, []).append(grade)   # закомментировать тут
        # lector.lecture_grades.setdefault(course, {}).update({f"id_{self.id}": self.listener_lecture_grades[course]})


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lecture_grades = {}

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.get_avg_score()}"

    def get_avg_score(self):
        """
        Метод получения средней оценки Лектора по всем его курсам
        :return:
        """
        total_score = 0
        total_len = 0
        for i in self.lecture_grades.values():  # закомментировать тут
            total_len += len(i)                 # закомментировать тут
            total_score += sum(i)               # закомментировать тут
        # for course in self.lecture_grades.values():
        #     score_per_course = sum([grade for grade in course.values()])
        #     total_score += score_per_course
        #     total_len += len(course)
        return total_score / total_len

    def __eq__(self, other):
        return self.get_avg_score() == other.get_avg_score()

    def __ne__(self, other):
        return self.get_avg_score() != other.get_avg_score()

    def __lt__(self, other):
        return self.get_avg_score() < other.get_avg_score()

    def __gt__(self, other):
        return self.get_avg_score() > other.get_avg_score()

    def __le__(self, other):
        return self.get_avg_score() <= other.get_avg_score()

    def __ge__(self, other):
        return self.get_avg_score() >= other.get_avg_score()


class Reviewer(Mentor):
    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def get_avg_student_score_by_course(students: list[Student], course: str) -> float | str:
    """
    Функция для получения средней оценки указанных студентов по курсу
    :param students: список студентов
    :param course: курс по которому будет браться оценка
    :return: средняя оценка: float
    """
    total_score = 0
    for student in students:
        if student.grades:  # если у студента нет оценок по данному курсу, то он не учитывается
            total_score += student.grades.get(course)
    if total_score == 0:
        return "У перечисленных студентов пока нет оценок по данному курсу"
    return round(total_score/len(students), 2)


def get_avg_lecturer_score_by_course(lecturers: list[Lecturer], course: str) -> float | str:
    """
    Функция получения средней оценки лектора за курс
    :param lecturers: список лекторов
    :param course: курс по которому будет браться оценка
    :return: средняя оценка: float
    """
    total_score = 0
    for lecturer in lecturers:
        if lecturer.lecture_grades:
            # если выключено обновление оценок, то значения будут списом
            if isinstance(lecturer.lecture_grades.values(), list):
                total_score += sum(lecturer.lecture_grades.get(course))
            # если включено обновление оценок, то значения будут словарем
            else:
                total_score += sum(lecturer.lecture_grades.get(course).values())
            if total_score == 0:
                return "У лектора пока нет оценок за лекции"
    return round(total_score/len(lecturers), 2)


lecturer_1 = Lecturer("Лектор_1", "Фамилия_1")
lecturer_1.courses_attached += ["Python", "Java"]
l_2 = Lecturer("Лектор_2", "Фамилия_1")
l_2.courses_attached += ["Python"]
reviewer = Reviewer("Ревьюер_1", "Фамилия_1")
reviewer.courses_attached = ['Python', "java"]
best_student = Student('Ruoy', 'Eman', 'М')
best_student.courses_in_progress += ['Python']
x_student = Student('Студент_1', 'Фамилия_Студента', 'Ж')
x_student.courses_in_progress += ['Python', "java"]
x_student.rate_lecture(1, "Python", l_2)
best_student.rate_lecture(10, "Python", lecturer_1)
x_student.rate_lecture(2, "Python", lecturer_1)
x_student.finished_courses.append("Django")
reviewer.rate_hw(x_student, "java", 2)
reviewer.rate_hw(best_student, "Python", 5)
print(lecturer_1)
print("-----")
print(x_student)
print("-----")
print(reviewer)
print("-----")
print(lecturer_1 > l_2, f"({lecturer_1.get_avg_score()} > {l_2.get_avg_score()})")
print(lecturer_1 < l_2, f"({lecturer_1.get_avg_score()} < {l_2.get_avg_score()})")
print(lecturer_1 != l_2, f"({lecturer_1.get_avg_score()} != {l_2.get_avg_score()})")
print(best_student > x_student, f"({best_student.get_avg_grade()} > {x_student.get_avg_grade()})")
print(best_student < x_student, f"({best_student.get_avg_grade()} > {x_student.get_avg_grade()})")
print(best_student != x_student, f"({best_student.get_avg_grade()} != {x_student.get_avg_grade()})")
