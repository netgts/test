from flask import render_template, request
from equipment import app
from equipment.models import *


# список наименования оборудования
rows = db.session.query(TypeEquip.id, TypeEquip.name_equip).all()


# @app.route - декторатор указывающий, какой URL активирует функцию
@app.route('/')
def main():
    return render_template('index.html', rows=rows)


# запись серийников
@app.route('/', methods=['POST'])
def insert_sn():
    if request.form['equip'] != '':  # получены данные от формы
        msg = ''
        serial_num = request.form['equip'].split()
        id_equip = ''.join(request.form['type_equip'].split())
        msg = record_serial_num(id_equip, serial_num)  # запускаем блок 'check & regex & record',
                                                       # получаем ответное сообщение

        return render_template('index.html', rows=rows, msg=msg)
    return render_template('index.html', rows=rows)  # данных нет, поэтому просто "рендерим" страницу
