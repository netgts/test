---
Общая информация
---

Разработка интерфейса для добавления оборудования разрабатывалась во фреймворке Flask (python 3.8)
Необходимые пакеты для виртуального окружения (requirment.txt):
```
- Flask==2.0.0
- Flask-SQLAlchemy==2.5.1
- mysqlclient
```

Интерфейс разработан по следующему принципу:
1. Выбирается наименование оборудования из выпадающего списка;
2. В поле "textarea" вводятся серийные номера по заданной маске, как в одном экземпляре, так и списком;
3. До записи номеров в базу данных, проводится проверка номеров:
 - **корректность символов** (допускаются символы латиницы, цифры и спецсимволы: "@ _ -");
 - **длина номера** (исходя из статичности длины серийных номеров принятых вендорами = 10);
 - **повтор записи** (т.е. проверка номера в базе данных);
 - **проверка по заданной маске** относительно типа выбранного оборудования.
4. В случае прохождения проверки производится запись в БД. В противном случае пользователю выводится сообщение о причине отказа записи: "некорректный ввод", "данный номер уже есть в базе данных".


Проверка по "маске" основана на поле "sn_mask", таблицы "type_equip", где заносится шаблон маски. Сделано это для того, чтобы получить гибкий и независимый (при изменении шаблона нет необходимости править код приложения) способ редактирования маски в БД. Основная функция проверки по регулярным выражениям "regex_mask" использует массив (ключ-значение) сравнивая поиндексно символы введенного пользователем серийного номера с шаблоном маски из БД.


Установку приложения осуществим на базе **MySql** + **NGINX** + **Linux(Ubuntu)**.<br>
Домашний каталог приложения в os Linux - **/home/www/equip**.<br>
Работаем под пользователем 'user' c правами sudo


В git-репозитории каталоги расположены в следующем порядке:
* equipment - каталог проекта приложения на фреймворке Flask
* App - каталог проекта приложения на фреймворке Flask
* еquipment.sql - скрипт установки базы данных проекта
* requirements.txt - список необходимых пакетов для виртуального окружения python <br>



---
**1. Установка и настройка MySQL (v.8)**
---
```bash
$ sudo apt install mysql-server			

# скрипт безопасности			
$ sudo mysql_secure_installation    	

Заливаем скрипт 'equipment.sql' в каталог /home/www/equip
# логинимся под root
$ mysql -u root -p	

# разворачиваем базу
$ > source /home/www/equip/equipment.sql;	
```

Добавляем пользователя
```bash
Отключаем политику паролей (поочередно запускаем команды):
$ root mysql -h localhost -u root -p
$ uninstall plugin validate_password;

В случае несработки прошлой команды (может возникнуть из-за более новой версии сервера), поэтому: 
$ UNINSTALL COMPONENT 'file://component_validate_password';

$ CREATE USER 'developer'@'localhost' IDENTIFIED BY '111';

# Установка всех привилегий
$ GRANT ALL PRIVILEGES ON *.* TO 'developer'@'localhost' WITH GRANT OPTION;  	

# Просмотр привилегий
$ SHOW GRANTS FOR 'developer'@'localhost';  	
```



---
**2. Установка Flask, настройка каталога проекта**
---

**Устанавливаем общие системные пакеты для Python**
```bash
$ sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
$ sudo apt-get install python-dev libmysqlclient-dev
$ pip3 install virtualenv
```

**Создаем директорию, в которой будем размещать проект (сайт)**
```bash
$ sudo mkdir /home/www/equip  
```

**Настраиваем разрешения доступа**
```bash
# создадим группу для www
$ sudo groupadd www-data 

# добавим пользователя в группу
$ sudo gpasswd -a user www-data 					

# права данной группе на запись в каталог
$ sudo chown -R www-data /home/www/equip/

# накидываем права для 'user'
$ sudo chown -R user:www-data /home/www/equip/		

# read write execute для пользователя и группы и read + execute для всех остальных
$ sudo chmod 775 /home/www/equip/
```

**Устанавливаем необходимые пакеты для проекта**
```bash
$ cd /home/www/equip

# Создаем виртуальное окружение для нашего проекта
$ python3 -m virtualenv equipenv		

# До установки необходимых пакетов активировируем виртуальное окружение
$ source equipenv/bin/activate			

# Устанавливаем пакеты
$ pip install wheel
$ pip install gunicorn flask
$ pip install Flask-SQLAlchemy
$ pip install mysqlclient

# создаем файлик с указанием зависимостей проекта
$ pip freeze > requirements.txt 	

# выходим из env (виртуального окружения)
$ deactivate						
```



---
**3. Установка и настройка NGINX (gunicorn)**
---
```bash
$ sudo apt-get install nginx
$ sudo systemctl enable nginx
```

**Создаем файл служебной единицы 'systemd'**
```bash
$ sudo nano /etc/systemd/system/equip.service
```

Пишем в файл следующие настройки:

```bash
[Unit]
Description=Ginicorn instance to serve equip
After=network.target

[Service]
User=user
Group=www-data
WorkingDirectory=/home/www/equip
Environment="PATH=/home/www/equip/equipenv/bin"
ExecStart=/home/www/equip/equipenv/bin/gunicorn --workers 3 --bind unix:equip.sock -m 007 main:app
# main - в данном случае имя 'точки входа', т.е. в нашем случае файл 'main.py'

[Install]
WantedBy=multi-user.target
```

Запускаем службу и добавляем ее в автозапуск:
```bash
$ sudo systemctl start equip
$ sudo systemctl enable equip
```

**Настройка Nginx для запросов прокси**

Создаем новый файл конфигурации серверного блока в sites-available в каталоге Nginx (работаем под root)
```bash
$ nano /etc/nginx/sites-available/equip
```

Пишем в файл следующие настройки:
```bash
server {
  listen 80;
  server_name 192.168.55.34; # либо: mysite  mysite.com

  location / {
    include proxy_params;
    proxy_pass http://unix:/home/www/equip/equip.sock;
  }
}
```

**Связываем конфигурацию с каталогом 'sites-enabled'**
```bash
$ sudo ln -s /etc/nginx/sites-available/equip /etc/nginx/sites-enabled
```

**Проверяем ошибки конфигурации**
```bash
$ sudo nginx -t
```

**Перезапускаем процесс Nginx, чтобы прочитать новую конфигурацию**
```bash
$ sudo systemctl restart nginx	
```

**Настраиваем фаервол**
```bash
$ sudo ufw allow 'Nginx Full'
```


---
**4. Загрузка проекта, тестирование**
---

Загружаем в /home/www/equip/ файлы проекта: пакет 'equipment' и 'main.py'
Проверяем в браузере: http://192.168.55.34

**после замены файлов в проекте на сервере перезапускаем сервис:** 
```bash
$ sudo systemctl start equip
```
