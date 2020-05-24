# HR-questionnaire

## Вступление

Этот README.md будет больше похож на туториал о том как запускать связку django-vue-gunicorn-nginx

Причиной этому служит желание самому лучше разобраться как это устроено плюс отсутствием хорошо написаного туториала на русском. Да и на английском я нашел лиш два туториала из которых буду пытаться делать гибрида.

В дальнейшем по идее этот проект до какого-то определенного момента можно будет использовать как сетап для подобных сборок.

Источники откуда брал инфу, ниже. И, да, прибудет с нами сила!

 - [Здесь](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/) мне нравится настройка cтатики, медиа и то как реализован докерфайл
 - [Здесь](https://gitlab.com/briancaffey/docker-nginx-django-vue-architecture/-/blob/master/documentation/README.md) мне нравится методология и стиль разработки, а также структурированость

## Git

Сразу скажу что я буду пытаться придерживаться правильному бенчингу с гитом. В оигинальном туториале ссылка на [эту](https://nvie.com/posts/a-successful-git-branching-model/) статью. 

Создадим ветку develop через корорую будем пропускать дальнейшие измененияв мастер. И также ветку в которой мы будем все это разрабатывать.

```bash
$ git branch develop
$ git checkout -b djangoapp develop
$ git branch
  develop
* djangoapp
  master
```

Далее для использования окружения добавим следующие файлы `Dockerfile`, `docker-compose.yml` и `requirements.txt`:

Во всех моментах с версионностью вы скорее всего захотите использовать свежие версии, а я буду указывать свежие на момент разработки.

**Dockerfile**

```Dockerfile
# pull official base image
FROM python:3.8.3-alpine

# set work directory
RUN mkdir /code
WORKDIR /code

# adding main packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# copy(add) project
ADD . /code/
```
**requirements.txt**

```requirements.txt
Django==3.0.6
psycopg2-binary==2.8.5
```

**docker-compose.yml**

```yaml
version: '3'

services:
  db:
    container_name: db-dev
    image: postgres:12.3-alpine

  web:
    container_name: web-dev
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
      - db
```

Таким образом у нас получается следующая структура файлов

```bash
$ tree
.
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt

0 directories, 4 files
```

Теперь нам нужно начать проект. Мы не будем устанавливать себе django локально так как это не "docker way". Мы должны запустить команду `startproject` изнутри докера. Вот как это реализовать:

```bash
sudo docker-compose run web django-admin.py startproject backend
```
 
Эта команда создаст Django проект в новой папке `backend`. Как говорит автор [туториала](https://gitlab.com/briancaffey/docker-nginx-django-vue-architecture/-/blob/master/documentation/README.md) "Нам не нужно использовать команду с '.' в конце так как это добавит несколько иных файлов в нашем приложении" проверять я это конечноне буду).

Также давайте сверим что у нас получилось используя команду `tree` (если она у вас не установлена то сначала запустите `sudo apt  install tree`)

```bash
$ tree
.
├── backend
│   ├── backend
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── manage.py
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── README.md
└── requirements.txt

2 directories, 11 files
```

А также давайте посмотрим на список файлов в нашей верхнеуровневой директории.

```bash
$ ls -al
итого 80
drwxrwxr-x 5 michael michael  4096 мая 22 06:20 .
drwxrwxr-x 8 michael michael  4096 мая 21 21:19 ..
drwxr-xr-x 3 root    root     4096 мая 22 05:56 backend
-rw-rw-r-- 1 michael michael   279 мая 22 05:40 docker-compose.yml
-rw-rw-r-- 1 michael michael   428 мая 22 05:56 Dockerfile
drwxrwxr-x 8 michael michael  4096 мая 21 22:02 .git
-rw-rw-r-- 1 michael michael  3390 мая 21 21:21 .gitignore
drwxrwxr-x 3 michael michael  4096 мая 22 06:19 .idea
-rw-rw-r-- 1 michael michael 35149 мая 21 21:19 LICENSE
-rw-rw-r-- 1 michael michael  5343 мая 22 06:20 README.md
-rw-rw-r-- 1 michael michael    37 мая 21 22:58 requirements.txt
```

Заметьте что папка backend принадлежит `root`. Это все из-за того что мы запустили команду по созданию проекта внутри докера, а докер запускает все от имени администратора.

Давайте сменим разрешения на все наши файлы следующей командой:

```bash
$ sudo chown -R $USER:$USER .
```

Теперь давайте проверим файлы в директории `backend`:

```bash
$ cd backend && ls -al
итого 16
drwxr-xr-x 3 michael michael 4096 мая 22 05:56 .
drwxrwxr-x 5 michael michael 4096 мая 22 06:28 ..
drwxr-xr-x 2 michael michael 4096 мая 22 05:56 backend
-rwxr-xr-x 1 michael michael  627 мая 22 05:56 manage.py
```

Как вы видите ничего не принадлежит `root` и ето именно то что нам и было нужно.

Давайте проверим какие изменения мы внесли с помощью `git status`:

```bash
$ git status
На ветке djangoapp
Изменения, которые будут включены в коммит:
  (use "git restore --staged <file>..." to unstage)
        новый файл:    ../Dockerfile
        новый файл:    ../docker-compose.yml
        новый файл:    ../requirements.txt

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (use "git restore <file>..." to discard changes in working directory)
        изменено:      ../Dockerfile
        изменено:      ../README.md
        изменено:      ../docker-compose.yml
        изменено:      ../requirements.txt

Неотслеживаемые файлы:
  (используйте «git add <файл>…», чтобы добавить в то, что будет включено в коммит)
        ./
```

Давайте добавим все изменения и закоммитим их в нашу ветку `djangoapp`.

```bash
$ git add . && git commit -m "created django project and docker files, updated README"
```

### Переменные окружения

Дальше чтобы внесем несколько правок в settings.py и добавим файлы переменных окружения.

Для начала обновим переменные `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS` и `DATABASES` переменные в settings.py:

```python
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

...

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE"),
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}
```

Следующим шагом добавим в `docker-compose.yml` файлы пременных.

**docker-compose.yml**

```yaml
version: '3'

services:
  db:
    container_name: db-dev
    image: postgres:12.3-alpine
    env_file:
      - ./.env.dev.db

  web:
    container_name: web-dev
    build: .
    command: python3 manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    env_file:
      - ./.env.dev
    depends_on:
      - db
```

**.env.dev**

```.env
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=questionnaire_db
SQL_USER=michael
SQL_PASSWORD=sezam_unlock
SQL_HOST=db
SQL_PORT=5432
```

**.env.dev.db**

```.env
POSTGRES_USER=michael
POSTGRES_PASSWORD=sezam_unlock
POSTGRES_DB=questionnaire_db
```

Это стандартные настройки безопасности, а также информация для подключения кбазе данных. Заметьте что  `'HOST': 'db'` обращается к `db` который определен в `services` в нашем файле `docker-compose.yml`. Теперь мы можем можем запустить оба наших контейнера.
 
### docker-compose best practices

На этом моменте нам следует вспомнить о хорошем тоне в использавании docker compose. `docker-compose.yml` может быть сложноват по началу. В нем много специальных переменных которые могут менять и определять как он стартует контейнеры, и *где* он будет искать спецефические файлы и скрипты для запуска контейнера.

Давайте укажем значение для `context` другое нежели `.` (текущая директория). `context` говорит нам где искать `Dockerfile`. Я постараюсь организовать наши сервисы как директории верхнего уровня. И как правило, каждая директория верхнего уровня будет содержать свой Dockerfile или Dockerfile-ы.

Если мы укажем в `context` значение `./backend`, тогда нам нужно будет переместить Dockerfile в `backend`:

```bash
$ mv Dockerfile backend/
```
Также нам следует переместить `requirements.txt` в `backend` также.

```bash
$ mv requirements.txt backend/
```

Также, перед тем как мы запустим сервер для разработки (`runserver` command), нам нужно сдалать миграции в базе данных и запустить команду `migrate`. Мы бы могли добавить их непосредственно в `docker-compse.yml`, но тогда у нас файл может быть очень розтянутый что призведет к безпорядку. А так как нам скорее всего прийдется добавлять много дополнительных команд то лучше держать файл в чистоте.

Вместо того чтобы писать:

```yaml
command: python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000
```

мы можем заменить эти связанные команды одним скриптом:

```yaml
command: /start.sh
```

**Dockerfile**

```Dockerfile
# pull official base image
FROM python:3.8.3-alpine

# set work directory
RUN mkdir /code
WORKDIR /code

# adding main packages
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# copy(add) script
COPY ./backend/scripts/start.sh /

# copy(add) project
ADD . /code/
```

**start.sh**

```bash
#!/bin/sh

if [[ "$DATABASE" = "postgres" ]]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd backend || exit
python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py runserver 0.0.0.0:8000
```

Блок кода что находится перед созданием миграций отвечает за то чтобы база уже была готова принимать запросы. И чтобы он корректно работал нужно добавить переменную DATABASE

**.env.dev**

```.env
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1] *
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=questionnaire_db
SQL_USER=michael
SQL_PASSWORD=sezam_unlock
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

Также нам нужно сделать `start.sh` исполняемым:

```bash
$ sudo chmod +x backend/backend/scripts/start.sh
```

На данном этапе у нас должна быть следующая структура файлов:

```bash
$ tree
.
├── backend
│   ├── backend
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── scripts
│   │   │   └── start.sh
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── Dockerfile
│   ├── manage.py
│   └── requirements.txt
├── docker-compose.yml
├── LICENSE
└── README.md

3 directories, 12 files
```

Помимо всего еслинам чтото нужно будет сейчас изменить в файлах проекта мы можем менять и после сохнанения все изменения отобразятся правильно, даже без перезапуска контейнера. Но если мы поменяем что-то в Dockerfile, docker-compose.yml или .env файлах перезапустить всеже прийдется.

## Django ReST Framework

На этом моменте мы начинаем добавлять дополнительные библиотеки для Django которые позволят нам построить мощный API. [Django ReST Framework](https://www.django-rest-framework.org/) будет ответственен за сериализацию и десериализацию наших экземпляров моделей Django в JSON и из него. Он имеет множество мощных функций, которые делают его самой популярной библиотекой для создания API с помощью Django.

В дополнение к Django ReST Framework мы установим еще один пакет для использования веб-токенов JSON для авторизации и управления разрешениями. Этот пакет называется [djangorestframework_jwt](https://github.com/GetBlimp/django-rest-framework-jwt) и поддерживается компанией под названием [Blimp](https://github.com/GetBlimp).

Сначала давайте добавим пакеты в конец файла `requirements.txt`:

```requirements.txt
djangorestframework==3.11.0
markdown==3.2.2
django-filter==2.2.0
djangorestframework-jwt==1.11.0
```

Затем нам нужно добавить следующее в `INSTALLED_APPS`:

```python
    'rest_framework',
```

Затем мы можем добавить следующее в `settings.py` после` DATABASES`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}
```

Теперь у нас есть немного больше работы над бэкэндом. Как только мы создадим систему аутентификации и базовую модель, такую как "Questionnaire", мы будем готовы настроить интерфейс, который будет получать и публиковать данные в нашем внутреннем Django API. Затем мы свяжем бэкэнд и внешний интерфейс с мощным веб-сервером и обратным прокси-сервером: NGINX.

Во-первых, нам нужно новое приложение Django для организации пользователей нашего проекта. Давайте создадим новое приложение под названием `account`. Нам нужно будет выполнить команду `startapp` изнутри нашего контейнера Django, изменить разрешения для этих файлов, а затем добавить имя приложения в` INSTALLED_APPS`, чтобы наш проект узнал об этом. Нам также нужно будет создать эндпоинты API. Давайте сделаем все это шаг за шагом.

Во-первых, давайте сделаем приложение:

```bash
$ docker exec -it web-dev /bin/sh
/code # cd backend/
/code/backend # ./manage.py startapp accounts
/code/backend # 
```

Установите права доступа к файлам в приложении `accounts`:

```bash
$ sudo chown -R $USER:$USER .
[sudo] пароль для michael: 
$
```

Теперь давайте подключим наше приложение `accounts` к остальной части нашего проекта Django.

Добавьте `'accounts'` в `INSTALLED_APPS` и добавьте следующее в файл `urls.py` в `backend`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('admin/', admin.site.urls),
]
```

Теперь к файлу `urls.py` в приложении `accounts` добавьте следующее:

```python
from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    re_path(r'^auth/obtain_token/', obtain_jwt_token, name='api-jwt-auth'),
    re_path(r'^auth/refresh_token/', refresh_jwt_token, name='api-jwt-refresh'),
    re_path(r'^auth/verify_token/', verify_jwt_token, name='api-jwt-verify'),
]
```

Первый маршрут вернет ответ JSON, содержащий специальный токен, когда мы отправим запрос POST с правильными `username` и `password`. На самом деле, `djangorestframework_jwt` поддерживает `AbstractBaseUser`, поэтому мы должны иметь возможность проходить аутентификацию с любой комбинацией учетных данных, но пока мы будем рассматривать только стандартную модель пользователя.

Давайте напишем тест, чтобы увидеть, как это работает в действии. В `accounts/tests.py` напишите следующее:

```python
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


from django.contrib.auth.models import User

class AccountsTests(APITestCase):

    def test_obtain_jwt(self):

        # create an inactive user
        url = reverse('api-jwt-auth')
        u = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        u.is_active = False
        u.save()

        # authenticate with username and password
        resp = self.client.post(url, {'email':'user@foo.com', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        
        # set the user to activate and attempt to get a token from login
        u.is_active = True
        u.save()
        resp = self.client.post(url, {'username':'user', 'password':'pass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']

        # print the token
        print(token)
```

Мы можем запустить этот тест следующим образом:

```bash
$ docker exec -it web-dev /bin/sh
/code # cd backend/
/code/backend # ./manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InVzZXIiLCJleHAiOjE1OTAzMjAwMjUsImVtYWlsIjoidXNlckBmb28uY29tIn0.yL29DzUYglid42OTGBLcC75G8_cvjBeKazsawmePdCU
.
----------------------------------------------------------------------
Ran 1 test in 0.286s

OK
Destroying test database for alias 'default'...
/code/backend # 
```

На этом моменте давайте сделаем паузу и закомиттим наш проект.

# тут
