Установка и запуск приложения "Shortener" 
=========================================

Требования:
python 3.7

###Скопировать проект 
git clone https://github.com/BorisKoval/coin32_test.git

###Создать виртуальное окружение 
sudo pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv coin32_test --python=python3.7
workon coin32_test

###Установить зависимости
cd ./coin32_test
pip install -r requirements.txt


### Создать базу данных
sudo apt update
sudo apt install mysql-server

sudo mysql

CREATE USER '<user>'@'<localhost>' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON *.* TO '<user>'@'<localhost>' WITH GRANT OPTION;

create database shortener

### Создать конфиг файл и отредактировать его в соотвествии с настройками БД выше
mkdir config
cp shortener.conf config/


### Экспортировать переменные окружения
export DJANGO_SETTINGS_MODULE=coin32_test.settings
export PYTHONPATH=/home/boris/PycharmProjects/coin32_test/

### Выполнить миграции
cd coin32_test/
python manage.py migrate

### Запустить приложение
python manage.py runserver

### Запустить celery для переодических задач
/home/boris/.virtualenvs/coin32_test/bin/celery -A shortener worker --loglevel=INFO
/home/boris/.virtualenvs/coin32_test/bin/celery -A shortener beat -l debug --scheduler django_celery_beat.schedulers:DatabaseScheduler

