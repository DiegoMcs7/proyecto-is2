#! /bin/bash

path=$(realpath gestorProyectos.sql)
sudo apt-get install python3-pip apache2 libapache2-mod-wsgi-py3
git pull origin main
virtualenv -p python3.8.10 env_desarrollo
envProyecto_path=$(realpath env_desarrollo)
echo "-------------------Activar Entorno-----------------------------"
source ./env_desarrollo/bin/activate
cd proyecto-is2/proyecto
ls
pip install -r requirements.txt
echo "--------------------------Tag----------------------------------"
read -p "Nombre del tag: " name
echo $name
git checkout $name
echo "----------------------Base de datos----------------------------"
sudo su - postgres <<EOF
psql -U postgres -f $path gestorProyectos
EOF
echo "-----------------------Produccion------------------------------"
proyecto_path=$(pwd)
sudo apt-get install libbz2-dev
python3 manage.py collectstatic
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
deactivate
sudo bash -c "
	printf '<VirtualHost *:80>
	\tServerAdmin admin@djangoproject.localhost
	\tServerName djangoproject.localhost.com
	\tServerAlias www.djangoproject.localhost.com
	\tDocumentRoot $proyecto_path
	\tErrorLog \${APACHE_LOG_DIR}/error.log
	\tCustomLog \${APACHE_LOG_DIR}/access.log combined

	\tAlias /static $proyecto_path/static
	\t<Directory $proyecto_path/static>
		\t\tRequire all granted
	\t</Directory>

	\tAlias /static $proyecto_path/media
	\t<Directory $proyecto_path/media>
		\t\tRequire all granted
	\t</Directory>

	\t<Directory $proyecto_path/proyecto>
		\t\t<Files wsgi.py>
			\t\t\tRequire all granted
		\t\t</Files>
	\t</Directory>

	\tWSGIDaemonProcess django_project python-path=$proyecto_path python-home=$envProyecto_path
	\tWSGIProcessGroup django_project
	\tWSGIScriptAlias / $proyecto_path/proyecto/wsgi.py
</VirtualHost>' > /etc/apache2/sites-available/djangoproject.conf"
cd /etc/apache2/sites-available
sudo a2ensite djangoproject.conf
if grep -q "127.0.0.1 djangoproject.localhost.com" "/etc/hosts"; then
  	echo 'Ya existe'
else
    sudo bash -c 'printf "127.0.0.1 djangoproject.localhost.com" >> /etc/hosts'
fi

sudo ufw allow 'Apache Full'
sudo apache2ctl configtest
cd $proyecto_path
cd ..
cd ..
source ./env_desarrollo/bin/activate
cd proyecto-is2/proyecto
python3 manage.py runserver
sudo service apache2 restart




