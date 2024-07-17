#!/bin/bash

echo "User data start"
apt-get update
apt-get upgrade -y

cd /home/ubuntu
git clone https://github.com/GanatraJay2000/Roulettech-Inc-RecipeApp-VPC-Backend.git

mv Roulettech-Inc-RecipeApp-VPC-Backend recipe_app

cd recipe_app

apt-get install python3-venv -y

python3 -m venv env

source env/bin/activate

pip3 install -r requirements.txt

mkdir data

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

deactivate
echo "Server Created"

apt-get install -y nginx

cp /home/ubuntu/recipe_app/nginx/nginx.conf /etc/nginx/nginx.conf

cp /home/ubuntu/recipe_app/nginx/django.conf /etc/nginx/sites-available/django.conf

ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/

nginx -t

service nginx restart

apt-get install supervisor -y

cp /home/ubuntu/recipe_app/nginx/gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf

mkdir /var/log/gunicorn

supervisorctl reread
supervisorctl update
supervisorctl status

service nginx restart

echo "User Data End"