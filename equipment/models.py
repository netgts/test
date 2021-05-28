import re
from equipment import db


# поскольку проект маленький, то поместим модели таблиц и функции в один файл


# описываем таблицы для работы с ORM
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_num = db.Column(db.String(15))
    id_equip = db.Column(db.Integer)


class TypeEquip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_equip = db.Column(db.String(50))
    sn_mask = db.Column(db.String(15))


# -- Регулярка --
# Проверку введенных пользователем серийных номеров проверям через рег.выражения сравнивая
# c шаблоном маски прописанным в БД. Это даст гибкость в редактировании маски серийных номеров.
# Т.е., нет необходимости после изменения шаблона маски в БД где то еще править код.

# Принцип проверки строим следующим образом:
#   - в БД, в таб."type_equip" в поле "sn_mask" прописываем тип маски
#   - каждый полученный серийный номер сравниваем с этой маской
#     - создаем 'словарь' регулярных выражений, по соответствию: 'N' = [0-9], 'A' = [A-Z] и т.д.
#     - получаем маску по ID оборудования
#     - в цикле, посимвольно, сравниваем по индексу [i] как маску так и полученный сер.номер

# Словарь описывающий регулярку для вводимых символов.
mask = {'N': '[0-9]', 'A': '[A-Z]', 'a': '[a-z]', 'X': '[A-Z0-9]', 'Z': '[-_@]'}


# проверка сер.номера соответствию маски
def regex_mask(id_equip, sn_num):
    # шаблон маски из БД по id оборудования
    db_mask = ''.join(db.session.query(TypeEquip.sn_mask).filter_by(id=id_equip).first())

    for i, ms in enumerate(sn_num):
        sym_mask = db_mask[i]  # берем символ маски из БД
        re_mask = mask[sym_mask]  # получаем регулярку по нему из словаря

        # 1.проверяем, есть ли такой ключ в словаре || 2.подходит ли серийник под регулярку
        if (not mask.get(sym_mask)) or (not re.match(re_mask, sn_num[i])):
            return False
    return True


# запись в БД
def record_db(id_equip, serial_num):
    # проверка повторной записи
    res = db.session.query(Equipment.serial_num).filter_by(serial_num=serial_num).first()
    if res is None:
        try:  # добавляем исключение
            db.session.add(Equipment(id_equip=id_equip, serial_num=serial_num))
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False
    else:
        return False
    return True


# основная функция (check & regex & record)
def record_serial_num(id_equip, serial_num):
    fail_sn_num = []  # запишем какие номера не удалось записать в БД
    repit_sn_num = [] # повтор серийного номера
    for sn in serial_num:
        if (re.match("^[A-z0-9_@-]+$", sn)) and (len(sn) == 10):  # проверка на корректность и длину ввода символов
            if regex_mask(id_equip, sn):    # номер прошел проверку по маске
                if not record_db(id_equip, sn):  # пишем номер в БД
                    repit_sn_num.append(sn)  # Серийный номер есть в базе данных
            else:
                fail_sn_num.append(sn)  # Серийный номер не соответствует требуемой маске
        else:
            fail_sn_num.append(sn)  # Некорректный набор серийного номера - присутствуют недопустимые символы

    # добавим собщение для пользователя о некорректных номерах
    msg = ''
    if len(fail_sn_num) > 0:
        msg = 'Некорректный ввод данных: ' + ', '.join(fail_sn_num)
    if len(repit_sn_num) > 0:
        msg = 'Данный номер уже есть в базе'

    return msg
