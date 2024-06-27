https://www.pythonanywhere.com/user/nurlanbek/consoles/31268760/

1 -pwd
-ls
2 -git clone -b main https://github.com/nurlanek/ulanlif.git

if
after sign in to git whit personle token
3 -git remote set-url origin https://nurlanek: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@github.com/nurlanek/repo.git

4 - create vitual env
    - mkvirtualenv --python=/usr/bin/python3.10.5 venv
    - clear
5- pip install -r requirements.txt
jazmin paketi ayri kurulmalidir requ tte kurulmuyor
    -pip install -U django-jazzmin

6- web-app
    -set virtaulenv : venv
7- WSGI configuration file:/var/www/nurlanbek_pythonanywhere_com_wsgi.py
    only
    # +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#Burayai wsc
## assuming your django settings file is at '/home/nurlanbek/mysite/mysite/settings.py'
## and your manage.py is is at '/home/nurlanbek/mysite/manage.py'
path = '/home/nurlanbek/procrm/procrm/pocrm'
if path not in sys.path:
    sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'pocrm.settings'
#
## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

8- auth_user table ilk migrationda sorun cikartiyor.
o yuzden sadece bir modeli(tabloyu) migrate edip,
superuser yarattiktan sonra diger tablolari migrate etmek gerekiyr

9- if static is not loading

python manage.py collectstatic

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/images/"


venv aktiv etmek icin
source .virtualenvs/venv/bin/activate
js kodlari kullanildiysa consolden  bu yapilmasi gerek

/home/ulanlife
03:38 ~ $ git
en sonuncusu
cd

db ulanlife
pass suvorov1046

Database host address:ulanlife.mysql.pythonanywhere-services.com
Username:ulanlife

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ulanlife$default',
        'USER': 'ulanlife',
        'PASSWORD': 'suvorov1046',
        'HOST': 'ulanlife.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional'
        }
    }
}

