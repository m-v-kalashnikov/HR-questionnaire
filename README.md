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
python3 manage.py flush --no-input
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

Теперь, когда у нас есть работающая система аутентификации пользователей, давайте создадим простую модель `Questionnaire` в новом приложении под названием `make_questionnaire`.

Создайте приложение `make_questionnaire` в нашем проекте Django с помощью `docker exec`, как мы делали раньше:
 
```bash
$ docker exec -it web-dev /bin/sh
/code # cd backend
/code/backend # python ./manage.py startapp make_questionnaire
/code/backend # 
```

Сразу же поменяем права доступа:

```bash
$ sudo chown -R $USER:$USER .
```

Вместо простого добавления `make_questionnaire` в `INSTALLED_APPS` мы добавим `make_questionnaire.apps.MakeQuestionnaireConfig`, а так же в `make_questionnaire/apps` в `MakeQuestionnaireConfig` добавим строчку:

```python
    verbose_name = "Создание опроса"
```

Так у нас в админке это приложение будет отображаться с тем названием которое мы указали.

Также в `settings.py` в переменной `LANGUAGE_CODE` поставим значение `'ru'` это сделает наше приложение 'заточеным' под русско-говорящих. И свяжите URL-адреса в `backend` с помощью:

```python
urlpatterns = [
  ...
  path('api/', include('make_questionnaire.urls', namespace="make_questionnaire_app")),
]
```

Теперь таже сделаем довольно интересную штуку. Удалим файл `models.py` и вместо него добавим пакет `models` и вместо того чтобы прописывать все модели в одном файле мы для каждой модели будем делать свой файл, а в `__init__.py` будем импортировать эти модели. Тем самым все по использованию моделей останется таким же только файл с моделями не будет вмещать в себе кучу строк кода в которых легко потеряться.

В этом пакете создадим файл `questionnaire_model` со следующим содержимым:

```python
import itertools
from django.db import models
from django.utils.text import slugify
from googletrans import Translator


class Questionnaire(models.Model):
    title = models.CharField('название', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(default='',
                            editable=False,
                            max_length=256,
                            )


    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return self.title

    def _generate_slug(self):
        max_length = self._meta.get_field('slug').max_length
        value = Translator().translate('{}'.format(self.title), dest='en').text
        slug_candidate = slug_original = slugify(value, allow_unicode=True)
        for i in itertools.count(1):
            if not Questionnaire.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()

        super().save(*args, **kwargs)
```

А в `__init__.py` добавим импорм толькочто созданой модели:

```python
from .questionnaire_model import Questionnaire
```

В моделе мы добавили только базовые поля которые будут использоваться в любом случае остачу полей будем добавлятьпо мере надобности. `created_at` и `updated_at` это служебные поля которые отвечают за отображение когда опрос был создан и обновлен, а `slug` будет хранить строку которая будет отображаться в адресной строке припопыке входа на детальный просмотр этого опроса.

Также мы добавили функцию `_generate_slug` которую я поаимствовал [тут](https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/#all-together). Единственное это мы добавили клиент для Google Translate указали чтобы значение поля `title` перед тем как слагифицировать переводилось на английский. Тем самым мы будем получать красивое значение в адресной строке.

Добавим пакет для работы Google Translate в `requirements.txt`

```requirements.txt
...
googletrans==2.4.0
```

Далее давайте зарегистрируем это приложение `admin.py`:

```python
from django.contrib import admin
from .models import Questionnaire

admin.site.register(Questionnaire)
```

Тут мы делаем покачто только отображение, но в дальнейшем мы скорее всего заменим это.

Затем добавим сериализатор для этой модели, создав `serializers.py` в папке `make_questionnaire`:

```python
from rest_framework import serializers
from .models import Questionnaire


class QuestionnaireSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='make_questionnaire_app:questionnaire-detail',
        lookup_field='slug'
    )
    class Meta:
        model = Questionnaire
        fields = ['url', 'title', 'created_at', 'updated_at']
```

В сериализаторе мы использовали `HyperlinkedModelSerializer` который автоматически досоздает поле `url` которое отображает ссылку на этот обьект. Мы его только до настроим указав какой путь использовать в роутинге и поле которое будет использоваться для поиска.

После чего добавим viewsets по которым будем делать отображение:

```python
from rest_framework import viewsets
from .models import Questionnaire
from .serializers import QuestionnaireSerializer


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    lookup_field = 'slug'
```

И наконец-то в `urls.py` добавим роутинг:

```python
from rest_framework import routers
from .views import QuestionnaireViewSet

app_name = 'make_questionnaire_app'

router = routers.DefaultRouter()
router.register(r'questionnaire', QuestionnaireViewSet, basename='questionnaire')

urlpatterns = router.urls
```

Теперь мы можем добавить опросники через админ-панель. Для удобства разработки поправим наш `start.sh` чтобы при старте контейнера сразу создавался и суперпользователь:

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
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'a@a.com', 'admin')" | python3 manage.py shell
python3 manage.py runserver 0.0.0.0:8000
```

После добавления опросников давайте перейдем по адресу http://0.0.0.0:8000/api/questionnaire/ где вы должны увидеть опросники, созданные вами в админке. Теперь давайте посмотрим на кое-что. Ранее мы установили переменную `REST_FRAMEWORK` в `settings.py`. Давайте посмотрим, что она делает, удаляя сеанс и обычную аутентификацию:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}
```

После можно вернуть переменную к первозданной форме.

Прежде чем мы начнем работать над нашим форнтендом, давайте напишем несколько тестов, чтобы убедиться, что доступ к нашим сообщениям ограничен запросами, которые приходят с действительным токеном.

**make_questionnaire/tests.py**

```python
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from rest_framework_jwt.settings import api_settings


class TestQuestionnaires(TestCase):
    """Questionnaire Tests"""

    def test_get_questionnaires(self):
        """
        Unauthenticated users should not be able to access questionnaires via APIListView
        """
        url = reverse('make_questionnaire_app:questionnaire-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_header_for_token_verification(self):
        """
        https://stackoverflow.com/questions/47576635/django-rest-framework-jwt-unit-test
        Tests that users can access questionnaires with JWT tokens
        """

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = User.objects.create_user(username='user', email='user@foo.com', password='pass')
        user.is_active = True
        user.save()
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)


        verify_url = reverse('api-jwt-verify')
        credentials = {
            'token': token
        }

        resp = self.client.post(verify_url, credentials, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
```

Поскольку мы можем аутентифицироваться только с помощью веб-токенов JSON, нам следует подумать о добавлении нашего frontend-а. Это позволит нам отправлять POST-запросы к маршруту аутентификации бэкэнда из формы входа в frontend, сохранять возвращенные токены в локальном хранилище, а также отправлять токен в виде заголовка с каждым исходящим запросом, который можно использовать для предоставления разрешения для защищенных ресурсов. Мы скоро доберемся до этого, но сначала нам нужно добавить наш frontend.

На данный момент, мы можем сказать, что самые основы нашего бэкэнд-приложения завершены. Мы можем получить токены для доступа к защищенным ресурсам. В настоящее время мы не можем ничего сделать с этими токенами, кроме как включить их в наши тесты. Давайте закоммитим наши изменения и сделаем merge из нашей ветки `djangoapp` в ветку `develop`.


```bash
$ git add .
$ git commit -m "added questionnaire model and tests for users accessing questionnaires"
$ git checkout develop
$ git merge djangoapp
```

# Frontend

Теперь мы готовы построить наш frontend. Во-первых, давайте создадим ветвь функции под названием vueapp, которую мы разветвляем из нашей текущей ветки develop.

```bash
$ git checkout -b vueapp develop

$ git lg2
* 67cf4e8 - Wed, 27 May 2020 07:50:18 +0300 (11 часов назад) (HEAD -> vueapp, djangoapp, develop)
|           added questionnaire model and tests for users accessing questionnaires - Michael Kalashnikov
* e4e503e - Wed, 27 May 2020 07:48:15 +0300 (11 часов назад)
|           added questionnaire model and tests for users accessing questionnaires - Michael Kalashnikov
* 39047c9 - Wed, 27 May 2020 07:47:43 +0300 (11 часов назад)
* 67cf4e8 - Wed, 27 May 2020 07:50:18 +0300 (11 часов назад) (HEAD -> vueapp, djangoapp, develop)
|           added questionnaire model and tests for users accessing questionnaires - Michael Kalashnikov
* e4e503e - Wed, 27 May 2020 07:48:15 +0300 (11 часов назад)
|           added questionnaire model and tests for users accessing questionnaires - Michael Kalashnikov
* 39047c9 - Wed, 27 May 2020 07:47:43 +0300 (11 часов назад)
|           added questionnaire model and tests for users accessing questionnaires - Michael Kalashnikov
* e7b9d11 - Sun, 24 May 2020 16:55:56 +0300 (3 дня назад) (origin/djangoapp)
|           Adding DRF to project, updating README.md - m-v-kalashnikov
* e19b440 - Sun, 24 May 2020 16:51:45 +0300 (3 дня назад)
|           Adding DRF to project, updating README.md - m-v-kalashnikov
* c34964a - Sun, 24 May 2020 16:46:44 +0300 (3 дня назад)
|           Adding DRF to project, updating README.md - m-v-kalashnikov
* 4d9fde1 - Sun, 24 May 2020 16:44:56 +0300 (3 дня назад)
|           Adding DRF to project, updating README.md - m-v-kalashnikov
* 626c140 - Sun, 24 May 2020 16:41:38 +0300 (3 дня назад)
|           Adding DRF to project, updating README.md - m-v-kalashnikov
* 0106a0d - Sun, 24 May 2020 16:38:21 +0300 (3 дня назад)
|           Adding DRF to project - m-v-kalashnikov
* 8479c1f - Fri, 22 May 2020 06:39:47 +0300 (6 дней назад)
|           created django project and docker files, updated README - m-v-kalashnikov
* fd00a82 - Fri, 22 May 2020 06:38:54 +0300 (6 дней назад)
|           created django project and docker files, updated README - m-v-kalashnikov
* 58acc30 - Thu, 21 May 2020 21:38:12 +0300 (6 дней назад) (origin/master, origin/HEAD, master)
|           Initial commit - m-v-kalashnikov
* a126273 - Wed, 20 May 2020 19:39:10 +0300 (7 дней назад)
            Initial commit - Kalashnikov Michael
```

Давайте создадим папку верхнего уровня под названием `frontend`, которая будет содержать наше приложение Vue. Вместо запуска `mkdir frontend`, мы хотим, чтобы эта папка и ее файлы были сгенерированы Docker. Нам для этого нужен контейнер с node.

Давайте начнем с `Dockerfile` в нашей папке верхнего уровня. Этот файл будет иметь только одну строку:

```Dockerfile
FROM node:14.3.0-alpine
```

Далее мы запустим следующую команду (но естественно вы указываете свой путь к root дирекрорию):

```bash
$ docker run --rm -it -v /home/michael/PycharmProjects/HR-questionnaire/frontend/:/code node:14.3.0-alpine /bin/sh
```

Эта команда запустит контейнер с node и поделит нашу папку `frontend` с новой папкой, которую мы создаем в контейнере под названием `/code`. Как только мы окажемся внутри контейнера, мы можем установить следующие пакеты с помощью `npm` (который уже установлен, поскольку мы используем `node: 9.11.1-alpine` в качестве базового образа для этого контейнера):

- vue
- @vue/cli

Внутри контейнера выполните следующие команды:

```vue
# cd code
# npm i -g vue @vue/cli
# vue create .
```

Это приведет нас в каталог `/code` (который используется совместно с `frontend` на нашей локальной машине - это, по сути, каталог).

Затем мы устанавливаем пакеты с помощью npm глобально и запускаем команду для создания нового проекта VueJS с помощью командной строки. Вот настройки, которые я выберу для этого проекта:

```vue
Vue CLI v4.4.1
? Please pick a preset: Manually select features
? Check the features needed for your project: Babel, Router, Vuex, Linter
? Use history mode for router? (Requires proper server setup for index fallback in production) Yes
? Pick a linter / formatter config: Airbnb
? Pick additional lint features: Lint on save, Lint and fix on commit (requires Git)
? Where do you prefer placing config for Babel, ESLint, etc.? In package.json
? Save this as a preset for future projects? (y/N) n
```

Теперь у нас есть новый проект VueJS на нашей локальной машине. Прежде чем что-то делать, мы должны изменить права доступа к файлам, которые были только что созданы, потому что они были созданы docker и, следовательно, принадлежат пользователю `root`.

Теперь мы почти готовы начать разработку нашего приложения Vue. Но прежде чем мы это сделаем, нам нужно поговорить об окружающей среде.

Приложение VueJS - это не что иное, как `коллекция статических файлов`. Однако при разработке нашего приложения VueJS мы будем работать с файлами `.vue`, которые используют преимущества современных функций Javascript (ES6). Когда мы запускаем `npm run build`, файлы `.vue` и другие файлы объединяются в `коллекцию статических файлов`, которые доставляются в браузер, поэтому они не включают в себя файлы `.vue`. Только файлы `html`, `.js` и `.css`.

Мы хотим воспользоваться возможностью горячей перезагрузки. Это особенность современных сред Javascript, которая позволяет нам просматривать наше приложение по мере его разработки. Это означает, что мы можем вносить изменения в файлы `.vue`, и тогда мы сможем мгновенно увидеть изменения в браузере, который показывает нам предварительный просмотр. Этот «предварительный просмотр» начинается с запуска `npm run serve`. Это режим, который мы будем использовать при разработке нашего приложения. Он не использует `коллекцию статических файлов`, которую мы будем использовать в производстве.

Так как docker - это поддержка одной и той же среды между разработкой, тестированием, подготовкой / QA и производством, мы должны быть осторожны, когда начинаем вводить разные среды. Было бы непрактично запускать `npm run build` после каждого изменения, внесенного нами при разработке нашего приложения - этой команде требуется некоторое время для генерации `коллекции статических файлов`.

Это означает, что нам в конечном итоге потребуются две разные версии нашего существующего файла `docker-compose.yml`:

1. Тот, который служит `коллекцией статических файлов` для производства.
2. Тот, который предлагает нам горячую перезагрузку в процессе разработки.

Мы также сможем использовать verion `1` во время локальной разработки, но наши изменения не будут отражены немедленно. Мы увидим все это в действии через минуту.

Прежде чем мы разделим наш `docker-compose.yml`, давайте закоммитим наши изменения. Еще одна вещь, мы можем удалить Dockerfile, который мы использовали для создания нашего контейнера и для создания файлов и приложения Vue.

```bash
$ rm Dockerfile
$ git add .
$ git commit -m "added VueJS project in frontend"
```

## docker-compose.dev.yml

Поскольку мы будем разбивать наш файл `docker-compose.yml` на версию для разработки и производства (и еще больше версий позже), давайте скопируем его в `docker-compose.dev.yml`:

```bash
$ cp docker-compose.yml docker-compose.dev.yml
```

Наш файл `docker-compose.dev.yml` в настоящее время содержит два сервиса:` db` и `web`. `db` - это сервис, который запускает нашу базу данных Postgres, а `web` - это сервис, который запускает наше приложение Django. Нам нужно будет ввести два новых сервиса: `frontend` и `nginx`. Кроме того, добавим одну или несколько [сетей](https://docs.docker.com/network/), которые помогут нашему сервису автоматически взаимодействовать через механизм докера.

### Networks

Существует несколько типов сетей, которые поддерживает Docker, но мы будем использовать одну из них, называемую «user-defined bridge networks».

> user-defined bridge networks лучше всего подходят, когда вам нужно несколько контейнеров для связи на одном хосте Docker. Мы добавим их в `docker-compose.dev.yml` после того, как добавим сервисы `frontend` и `nginx`.

### frontend

`frontend` будет использовать базовый образ `node` и будет запускать `npm run serve`, чтобы мы могли отслеживать изменения файлов в нашем проекте и мгновенно видеть результат.

Вот как сервис будет выглядеть в `docker-compose.dev.yml`:

```yaml
  frontend:
    container_name: frontend-dev
    build:
      context: ./frontend
    volumes:
      - './frontend:/app/:ro'
      - '/app/node_modules'
    networks:
      - django-nginx
    depends_on:
      - web
    environment:
      - NODE_ENV=development
```

Для этого сервиса мы будем искать `Dockerfile` в `frontend`. Мы знаем это из части `build/context` определения сервиса:

```yaml
    build:
      context: ./frontend
```

Давайте создадим этот `Dockerfile`, а затем продолжим рассмотрение службы` frontend` в `docker-compose.dev.yml`.

### frontend Dockerfile

```Dockerfile
FROM node:14.3.0-alpine

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

# install project dependencies
RUN npm install

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

EXPOSE 8080

CMD ["npm", "run", "serve"]
```

Этот Dockerfile говорит:

- Используйте `node:14.3.0-alpine`,
- В контейнере создайте папку в корне файловой системы с именем `/app` и перейдите в этот каталог
- Скопируйте все файлы которые начинаются на `package` и имеют расширение `.json` с нашего локального компьютера в `/app` (не `/` веть мы установили робочей папкой а тобиш папкой верхнего уровня папку `/app`) в контейнере.
- Установите зависимости в `node_modules`.
- Скопируйте все файлы из нашего проекта в `.`, то есть `/app`, так как мы установили его как `WORKDIR`.
- Сделайте expose пору `8080` в нашем контейнере.
- Запустите `npm run serve` в контейнере.

Давайте продолжим работу с `docker-compose.dev.yml`. После раздела `build` мы видим, что мы монтируем каталог `frontend` с нашего локального компьютера в `/app/frontend`. `ro` указывает, что подключенный том доступен только для чтения. Это нормально, так как мы будем редактировать файлы этого тома с нашего локального компьютера, а не из контейнера докера.

Далее мы видим, что определение сервиса для `frontend` перечисляет `django-nginx` в `networks`. Это означает, что служба совместно использует сеть с другими службами, которые также находятся в `django-nginx`. Мы скоро увидим, почему это так.

`depends_on` перечисляет сервисы, которые должны быть запущены до запуска этого.

Теперь давайте посмотрим на NGINX. NGINX - это веб-сервер и обратный прокси, который будет играть важную роль в нашем приложении. NGINX аналогичен "front desk" в том, что он направляет трафик к указанным URL-адресам файлов или служб. Если вы знакомы с маршрутизацией URL в Django, я думаю, что будет справедливо сказать, что NGINX похож на высокоуровневую версию `urls.py` в том, что он направляет трафик на основе свойств входящих URL.

```yaml
  nginx:
    container_name: nginx-dev
    image: nginx:1.18.0-alpine
    ports:
      - "8000:80"
    depends_on:
      - web
      - frontend
    volumes:
    - ./nginx/nginx_dev.conf:/etc/nginx/nginx.conf:ro
    - django-static:/code/staticfiles
    networks:
      - django-nginx
```

В этом сервисе мы не включаем `build` в определение, потому что мы не модифицируем базовый образ. Поскольку мы не модифицируем его, мы можем просто включить `nginx:1.18.0-alpine`. Так как мы не указываем URL, механизм докера по умолчанию `docker.io` ищет эти изображения. `docker.io` - это частная компания, которая ведет реестр базовых изображений, которые могут использоваться буквально для чего угодно. Загляните в Docker (большая D) Hub, чтобы узнать, что люди и компании делают с докером.

Далее мы указываем порты. Мы хотим сопоставить порт `8000` на нашей локальной машине с портом `80` этого контейнера. Это означает, что когда мы набираем `localhost: 8000` на нашей локальной машине, наши запросы направляются на порт `80` контейнера NGINX, который будет прослушивать этот порт и, соответственно, направлять трафик к месту назначения, указанному в его файле конфигурации.

Мы видим, что этот порт находится в `django-nginx`. Это важно, потому что мы будем делать запросы как к службе `backend` API Django, так и к службе `frontend`, которая работает на нашем сервере разработки для VueJS на node.

Давайте вернемся к `volumes`. Этот раздел определения сервиса говорит, что `nginx_dev.conf` монтируется в `/etc/nginx/nginx.conf`. Это позволяет нам разместить наш файл конфигурации NGINX внутри контейнера в файле, который NGINX обычно ищет для своей конфигурации (`/etc/nginx/nginx.conf`).

Теперь, когда мы закончили анализ определения сервиса NGINX, давайте посмотрим на `nginx_dev.conf`. Это файл конфигурации NGINX, который мы будем использовать в нашей среде разработки. Но сначала давайте создадим эту папку и файл:

```bash
$ mkdir nginx && cat <<EOF > nginx/nginx_dev.conf
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include /etc/nginx/mime.types;
    client_max_body_size 100m;

    upstream web {
        server web:8000;
    }

    upstream frontend {
        server frontend:8080;
    }


    server {
        listen 80;
        charset utf-8;

        # frontend urls
        location / {
            proxy_redirect off;
            proxy_pass http://frontend;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }

        # frontend dev-server
        location /sockjs-node {
            proxy_redirect off;
            proxy_pass http://frontend;
            proxy_set_header X-Real-IP  $remote_addr;
            proxy_set_header X-Forwarded-For $remote_addr;
            proxy_set_header Host $host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # backend urls
        location ~ ^/(admin|api) {
            proxy_redirect off;
            proxy_pass http://web;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }
    }
}
EOF
```

Теперь давайте рассмотрим этот файл конфигурации NGINX подробно. Внутри `http` мы сначала определяем "псевдонимы" для `web` и `frontend`. NGINX называет это `upstream`:

```editorconfig
upstream web {
    server web:8000;
}

upstream frontend {
    server frontend:8080;
}
```

> Обратите внимание, как этот файл ссылается как на `frontend:8080`, так и на` web:8000`. Вот почему сервис `nginx` должен быть в сети` frontend` и `web`. Также обратите внимание, что мы слушаем порт `80` с помощью `listen 80; `.

[Здесь](https://stackoverflow.com/a/5238430/6084948) есть полезное обяснение того, как NGINX обрабатывает несколько блоков `location`.

Кроме того, [здесь](https://stackoverflow.com/questions/40516288/webpack-dev-server-with-nginx-proxy-pass) объяснение блока с `sockjs-node`.

Затем обновите `web` в docker-compose.dev.yml, заменив `ports` на `expose`:

```yaml
  web:
    container_name: web-dev
    build:
      context: ./backend
    command: /start.sh
    volumes:
      - .:/code
    expose:
      - 8000
    env_file:
      - ./.env.dev
    depends_on:
      - db
    networks:
      - django-nginx
```

Теперь порт 8000 открыт только для других сервисов Docker. Порт больше не будет опубликован на хост-машине.

> Для получения дополнительной информации о `ports vs expose` просмотрите [этот](https://stackoverflow.com/questions/40801772/what-is-the-difference-between-docker-compose-ports-vs-expose) вопрос на Stack Overflow.

На данный момент мы должны проверить, все ли работает. Этот шаг сложен, потому что есть несколько движущихся частей, которые должны быть выполнены одновременно. Поэтому тавайте сверим то что у нас в `docker-compose.dev.yml`

**docker-compose.dev.yml**

```yaml
version: '3'

services:
  db:
    container_name: db-dev
    image: postgres:12.3-alpine
    env_file:
      - ./.env.dev.db
    networks:
      - django-nginx

  web:
    container_name: web-dev
    build:
      context: ./backend
    command: /start.sh
    volumes:
      - .:/code
    expose:
      - 8000
    env_file:
      - ./.env.dev
    depends_on:
      - db
    networks:
      - django-nginx

  frontend:
    container_name: frontend-dev
    build:
      context: ./frontend
    volumes:
      - './frontend:/app/:ro'
      - '/app/node_modules'
    networks:
      - django-nginx
    depends_on:
      - web
    environment:
      - NODE_ENV=development

  nginx:
    container_name: nginx-dev
    image: nginx:1.18.0-alpine
    ports:
      - "8000:80"
    depends_on:
      - web
      - frontend
    volumes:
    - ./nginx/nginx_dev.conf:/etc/nginx/nginx.conf:ro
    networks:
      - django-nginx

volumes:
  django-static:

networks:
  django-nginx:
    driver: bridge
```

```bash
$ docker-compose -f docker-compose.dev.yml down -v
$ docker-compose -f docker-compose.dev.yml up -d --build
```

Это создаст наши четыре контейнера:

- `db-dev`
- `web-dev`
- `frontend-dev`
- `nginx-dev`

Также будут настроены сети, которые мы упоминали ранее.

Обратите внимание, что `frontend` понимает, что мы запускаем Vue CLI внутри контейнера.

Теперь у нас есть рабочий `frontend` и рабочий `web`. Тем не менее, эти службы еще не общаются друг с другом. Давайте соединим наш `web` с нашим `frontend`, отображая `questionnaires` из нашего Django API на новой странице в нашем приложении VueJS. 

На этом этапе вся наша напряженная работа по настройке нашего локального сервера разработки начнет окупаться. Почему? Потому что теперь мы сможем редактировать исходный код наших приложений VueJS и Django, и мы увидим изменения, отраженные в обоих приложениях, без необходимости перезапуска наших док-контейнеров. 

**Примечание**: это наша **среда разработки**. Она не подойдет для продакшена.

А сейчас давайте сосредоточимся на соединении нашего `web` и `frontend`. Сначала добавим следующее в наше приложение VueJS:

**src/router/index.js**

```javascript
  {
    path: '/questionnaire',
    name: 'Questionnaire',
    component: () => import(/* webpackChunkName: "Questionnaire" */ '../views/Questionnaire.vue'),
  },
```

**src/App.vue**

```vue
      <router-link to="/">Home</router-link> |
      <router-link to="/questionnaire">Questionnaire</router-link> |
      <router-link to="/about">About</router-link>
```

**src/views/Questionnaire.vue**

```vue
<template>
  <div>
    <div v-for="(questionnaire, i) in questionnaires" :key="i">
      <h1 :key="i">{{ questionnaire.title }}</h1>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      questionnaires: [],
    };
  },
  mounted() {
    this.fetchQuestionnaires();
    document.title = 'Questionnaires';
  },
  methods: {
    fetchQuestionnaires() {
      fetch('http://localhost:8000/api/questionnaire/', {
        method: 'GET',
        headers: {
          Accept: 'application/json',
        },
      })
        .then((response) => {
          if (response.ok) {
            response.json().then((json) => {
              this.questionnaires = json;
            });
          }
        });
    },
  },
};
</script>

<style scoped>
  h1:hover {
    color: #42b983;
  }
</style>
```

Для того чтобы мы увидели опросники нам нужно либо:

1. Внедрить систему авторизации, которая получит токен и передаст токен в заголовке всех последующих запросов.

2. Мы могли бы изменить разрешения для модели questionnaire, чтобы любой пользователь мог получить доступ к `/api/questionnaire/`.

Давайте покачтопройтем по пути `2` и позже всеже добавим авторизацию.

Все, что нам нужно сделать, это изменить `REST_FRAMEWORK` в наших настройках:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}
```

Теперь, когда мы закомментировали все классы разрешений и аутентификации, мы должны видеть наши сообщения в нашем VueJS.

Если вы все ещё не видите ничего, убедитесь, что у вас есть записи в вашей базе данных. Вы можете проверить ваши опросники, перейдя к `localhost:8000/api/questionnaire/`.

Вы, вероятно, не видите статических файлов в доступном для просмотра API. Давайте исправим это, добавив `python3 manage.py collectstatic --no-input --clear` в `start.sh` контейнера:

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
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input --clear
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'a@a.com', 'admin')" | python3 manage.py shell
python3 manage.py runserver 0.0.0.0:8000
```

Вы можете увидеть следующую ошибку:

```bash
django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.
```

Давайте добавим следующее в конец `settings.py`:

```python
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
```

И на дальнейшее добавим возможность просматривать медиа файлы добавив в конец `urls.py` следующее:

```python
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**docker-compose.dev.yml**

```yaml
version: '3'

services:
  db:
    container_name: db-dev
    image: postgres:12.3-alpine
    env_file:
      - ./.env.dev.db
    networks:
      - django-nginx

  web:
    container_name: web-dev
    build:
      context: ./backend
    command: /start.sh
    volumes:
      - .:/code
      - django-static:/backend/staticfiles
    expose:
      - 8000
    env_file:
      - ./.env.dev
    depends_on:
      - db
    networks:
      - django-nginx

  frontend:
    container_name: frontend-dev
    build:
      context: ./frontend
    volumes:
      - './frontend:/app/:ro'
      - '/app/node_modules'
    networks:
      - django-nginx
    depends_on:
      - web
    environment:
      - NODE_ENV=development

  nginx:
    container_name: nginx-dev
    image: nginx:1.18.0-alpine
    ports:
      - "8000:80"
    depends_on:
      - web
      - frontend
    volumes:
    - ./nginx/nginx_dev.conf:/etc/nginx/nginx.conf:ro
    - django-static:/code/staticfiles
    networks:
      - django-nginx

volumes:
  django-static:

networks:
  django-nginx:
    driver: bridge
```

Также, давайте создадим файл `.gitignore` и поместим в него `staticfiles`:

```bash
$ echo "staticfiles" > backend/.gitignore
$ echo "mediafiles" > backend/.gitignore
```

Нам также нужно добавить следующий блок `location` в нашу конфигурацию NGINX:

```editorconfig
    location /staticfiles {
        proxy_pass http://web;
    }
```

[Разберите](https://docs.docker.com/compose/reference/down/) контейнеры для разработки (и связанные тома с флагом `-v`):

```bash
$ docker-compose down -v
```

Затем создайте его снова:

```bash
$ docker-compose -f docker-compose.dev.yml up -d --build
```

Отлично, теперь мы должны видеть наши сообщения в нашем приложении VueJS.

Давайте закоммитим эту работу, а затем настроим наш продакшн `docker-compose` с nginx и frontend.

```bash
$ git status
На ветке vueapp
Изменения, которые будут включены в коммит:
  (use "git restore --staged <file>..." to unstage)
        новый файл:    .dockerignore
        новый файл:    backend/.dockerignore
        новый файл:    backend/.gitignore
        новый файл:    docker-compose.dev.yml
        новый файл:    frontend/.dockerignore
        новый файл:    frontend/Dockerfile
        новый файл:    frontend/src/views/Questionnaire.vue
        новый файл:    nginx/nginx_dev.conf

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (use "git restore <file>..." to discard changes in working directory)
        изменено:      README.md
        изменено:      backend/.dockerignore
        изменено:      backend/.gitignore
        изменено:      backend/backend/scripts/start.sh
        изменено:      backend/backend/settings.py
        изменено:      backend/backend/urls.py
        изменено:      docker-compose.dev.yml
        изменено:      frontend/.dockerignore
        изменено:      frontend/Dockerfile
        изменено:      frontend/src/App.vue
        изменено:      frontend/src/router/index.js
        изменено:      frontend/src/views/Questionnaire.vue
$ git add .
$ git commit -m "completed development environemnt: added nginx, connected frontend and backend, fixed static files"
```

## Production development environment

Мы закончили настройку `docker-compose.dev.yml`. Мы будем запускать `docker-compose` с этим файлом при разработке нашего приложения. Чтобы начать разработку, все что нам нужно сделать, это запустить: 

```bash
$ docker-compose -f docker-compose.dev.yml up
```

Когда мы вносим какие-либо изменения в наши docker-compose или Dockerfiles, или в скрипты и команды, используемые для запуска наших docker-контейнеров, нам нужно будет добавить флаг `--build`. Если мы забудем добавить флаг сборки после редактирования файла, связанного с Docker, механизм Docker будет использовать кэшированную версию наших контейнеров.

```bash
$ docker-compose -f docker-compose.dev.yml up --build
```

Это заставит механизм докера искать любые изменения и перестраивать измененные слои. Это одна из лучших особенностей докера.

Однако, когда мы запускаем это приложение в продакшн, мы не хотим использовать `npm run serve`, мы также не хотим использовать команду `runserver` Django; эта команда не предназначена для этого (Django - это платформа для создания веб-приложений, а не веб-сервер). Вместо этого мы будем раздавать `коллекцию статических файлов`, оптимизированную для продакшна. Эта `коллекция статических файлов` генерируется с помощью `npm run build` и находится в папке `dist` в `frontend`. А для Django мы заменим `runserver` на [**gunicorn**](https://gunicorn.org/).

Давайте вернемся к `docker-compose.yml` и подумаем о том, что нам нужно. Во-первых, нам не нужен сервис `frontend`, который мы добавили в `docker-compose.dev.yml`. Нам понадобится NGINX, но в нашем конфигурационном файле NGING для прода нам не нужно слушать `/sockjs-node`.

Чтобы уточнить, нам нужно отредактировать существующий файл `docker-compose.yml` для прода, а также нам нужно будет создать новый файл с именем `nginx_prod.conf` для замены `nginx_dev.conf` в нашей продакшн среде. Давайте сначала посмотрим на `docker-compose.yml`, а затем `nginx_prod.conf`, и, наконец, мы создадим `Dockerfile`, который объединяет создание `коллекции статических файлов` (которая будет нашим продакшн приложением VueJS) с запуском нашего контейнер NGINX.

А также мы добавим продакшн `Dockerfile` для `web` сервиса чтобы сделать итоговое приложение более качественным.

Начнем с `Dockerfile`. Здесь мы будем использовать [многоэтапную сборку](https://docs.docker.com/develop/develop-images/multistage-build/) Docker, чтобы уменьшить окончательный размер образа. По сути, `builder` - это временный образ, который используется для сборки Python wheels. Затем wheels копируются в конечный продакшн образ, а образ `builder` отбрасывается.

> Вы могли бы пойти дальше к [многоэтапному подходу](https://stackoverflow.com/a/53101932/1799408) к сборке и использовать один Dockerfile вместо создания двух Dockerfile. Подумайте о плюсах и минусах использования этого подхода для двух разных файлов.

**Dockerfile.prod**

```Dockerfile
##########################
###### BUILD STAGE #######
##########################

# pull official base image
FROM python:3.8.3-alpine as builder

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install --upgrade pip

# lint
RUN pip install flake8
COPY . /code/
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /code/wheels -r requirements.txt


##########################
#### PRODUCTION STAGE ####
##########################

# pull official base image
FROM python:3.8.3-alpine

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./backend/scripts/start_prod.sh /

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
```

Вы заметили, что мы создали пользователя без полномочий root? По умолчанию Docker запускает контейнерные процессы как root внутри контейнера. Это плохая практика, поскольку злоумышленники могут получить root-доступ к хосту Docker, если им удастся вырваться из контейнера. Если вы root в контейнере, вы будете root на хосте.  

Обновите `web` в файле `docker-compose.yml` для сборки с помощью `Dockerfile.prod`:

```yaml
  web:
    container_name: web-prod
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: /start_prod.sh
    volumes:
      - .:/code
      - django-static:/home/app/web/staticfiles
      - django-media:/home/app/web/mediafiles
    expose:
      - 8000
    env_file:
      - ./.env.prod
    depends_on:
      - db
    networks:
      - django-nginx
```

Вы моглы заметить что мы заменили `command:`, а также `django-static:` и `django-media:`. В последних двух мы просто указали путь к директориям которые используются для хранения медиа и статики. А в `start_prod.sh` мы уберем команду [flush](https://docs.djangoproject.com/en/2.2/ref/django-admin/#flush) и установим запуск сервера через gunicorn.

**start_prod.sh**

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

python3 manage.py makemigrations
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input --clear
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$ADMIN_USER', '$ADMIN_MAIL', '$ADMIN_PASSWORD', first_name='$ADMIN_FIRST_NAME', last_name='$ADMIN_LAST_NAME')" | python3 manage.py shell
gunicorn backend.wsgi -b 0.0.0.0:8000
```

Мы добавили возможность указывать основные данные суперпользователя указывая соответствующие переменные в `.env.prod`. 

Также нам нужно сделать `start_prod.sh` исполняемым:

```bash
$ sudo chmod +x backend/backend/scripts/start_prod.sh
```

И добавить gunicorn в `requirements.txt`:

```requirements.txt
Django==3.0.6
psycopg2-binary==2.8.5
djangorestframework==3.11.0
markdown==3.2.2
django-filter==2.2.0
djangorestframework-jwt==1.11.0
googletrans==2.4.0
gunicorn==20.0.4
```

Теперь давайте посмотрим на `docker-compose.yml`.

**docker-compose.yml**

```yaml
version: '3'

services:
  db:
    container_name: db-prod
    image: postgres:12.3-alpine
    env_file:
      - ./.env.prod.db
    networks:
      - django-nginx

  web:
    container_name: web-prod
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: /start_prod.sh
    volumes:
      - .:/code
      - django-static:/home/app/web/staticfiles
      - django-media:/home/app/web/mediafiles
    expose:
      - 8000
    env_file:
      - ./.env.prod
    depends_on:
      - db
    networks:
      - django-nginx

  nginx:
    container_name: nginx-prod
    build:
      context: .
      dockerfile: nginx/Dockerfile
    ports:
      - 800:80
    depends_on:
      - web
    volumes:
    - ./nginx/nginx_prod.conf:/etc/nginx/nginx.conf:ro
    - django-static:/home/app/web/staticfiles
    - django-media:/home/app/web/mediafiles
    networks:
      - django-nginx

volumes:
  django-static:
  django-media:

networks:
  django-nginx:
    driver: bridge
```

Обратите внимание на две вещи:

1. Мы не определяем службу `frontend` в файле `docker-compose.yml`. Также мы монтируем другой файл конфигурации для службы NGINX. Давайте посмотрим на этот файл, `nginx_prod.conf`:

2. Важные различия между нашим файлом `docker-compose.dev.yml` и этим файлом` docker-compose.yml`:

**docker-compose.dev.yml**

```yaml
  nginx:
    image: nginx:1.18.0-alpine
```

**docker-compose.yml**

```yaml
  nginx:
    build:
      context: .
      dockerfile: nginx/Dockerfile
```

Это означает, что мы используем собственный `Dockerfile` для нашей производственной среды и базовый образ `nginx:1.18.0-alpine` для нашей среды разработки. Мы посмотрим на этот Dockerfile после того, как посмотрим на файл конфигурации NGINX: 

**nginx_prod.conf**

```editorconfig
user  nginx;
worker_processes  1;

events {
    worker_connections  1024;
}

http {
    include /etc/nginx/mime.types;
    client_max_body_size 100m;

    upstream web {
        server web:8000;
    }

    server {
        listen 80;
        charset utf-8;

        root /dist/;
        index index.html;


        # backend urls
        location ~ ^/(api) {
            proxy_redirect off;
            proxy_pass http://web;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
        }

        # backend static
        location /staticfiles/ {
            autoindex on;
            alias /home/app/web/staticfiles/;
        }

        # backend madia
        location /mediafiles/ {
            autoindex on;
            alias /home/app/web/mediafiles/;
        }

        # frontend urls
        location / {
            try_files $uri $uri/ @rewrites;
        }

        location @rewrites {
            rewrite ^(.+)$ /index.html last;
        }
    }
}
```

В этом файле конфигурации NGINX мы направляем трафик в наш контейнер Django только для запросов `api` (или любого другого запроса, который мы хотим определить вручную), а весь остальной трафик направляется в `index.html`, где наш VueJS приложение берет на себя маршрутизацию (например, с маршрутом `/questionnaire`, который мы определили ранее). Вход в админку мы сделали через `api` и дальше путь который мы определим в переменной `ADMIN_PANEL_URL` в нашем `.env.prod`. Сделано это так как не очень хорошо если каждый будет знать как зайти в админку и сам Django нам рекомендует изменить путь по которому будет осуществляться доступ в админку.

```python
    path('api/{}/'.format(os.getenv('ADMIN_PANEL_URL')), admin.site.urls),
```

Теперь давайте посмотрим на `Dockerfile` для нашего сервиса NGINX. Здесь мы также используем многоэтапную сборку но ту которая указана в [документации](https://vuejs.org/v2/cookbook/dockerize-vuejs-app.html) VueJS:

**nginx/Dockerfile**

```Dockerfile
##########################
###### BUILD STAGE #######
##########################

FROM node:14.3.0-alpine as build-stage
WORKDIR /app/
COPY frontend/package*.json /app/
RUN npm install
COPY frontend /app/
RUN npm run build


##########################
#### PRODUCTION STAGE ####
##########################

FROM nginx:1.18.0-alpine as production-stage
COPY nginx/nginx_prod.conf /etc/nginx/nginx.conf
COPY --from=build-stage /app/dist /dist/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Раздел `build stage` этого Dockerfile отвечает за сборку нашей `коллекции статических файлов`, которую мы будем использовать в работе. `build stage` берет `коллекцию статических файлов` (созданную с помощью `npm run build`) из `/app/dist` нашего `build stage` и копирует этот каталог в папку `/dist` нашего контейнера NGINX, где они обслуживаются NGINX.

Теперь давайте запустим наш производственный файл `docker-compose`, чтобы проверить его:

```bash
$ docker-compose up --build
```

Вы должны увидеть, что что-то не работает должным образом: запросы в нашу службу `backend` не выполняются:

```bash
GET http://localhost:8000/api/questionnaire/ net::ERR_CONNECTION_REFUSED
```

Во-первых, добавьте `django-cors-headers` в `requirements.txt`.

```requirements.txt
django-cors-headers==3.3.0
```

Затем в `settings.py` добавьте `'corsheaders',` в `INSTALLED_APPS` и добавьте `'corsheaders.middleware.CorsMiddleware',` в `MIDDLEWARE`.

Теперь давайте запустим наше приложение и проверим, нет ли у нас ошибки с `CORS` при попытке доступа к нашему `backend` API:

```bash
$ docker-compose up --build
```

Теперь мы должны видеть наши сообщения без ошибок `CORS`. Мы уже сильно изменились с момента нашего последнего коммита. Давайте закоммиттим наши изменения сейчас. 

```bash
$ git status
На ветке vueapp
Изменения, которые будут включены в коммит:
  (use "git restore --staged <file>..." to unstage)
        удалено:       .dockerignore
        новый файл:    .env.prod
        новый файл:    .env.prod.db
        удалено:       backend/.dockerignore
        новый файл:    backend/Dockerfile.prod
        новый файл:    backend/backend/scripts/start_prod.sh
        новый файл:    nginx/Dockerfile
        новый файл:    nginx/nginx_prod.conf

Изменения, которые не в индексе для коммита:
  (используйте «git add <файл>…», чтобы добавить файл в индекс)
  (use "git restore <file>..." to discard changes in working directory)
        изменено:      .env.prod
        изменено:      .gitignore
        изменено:      README.md
        изменено:      backend/.gitignore
        изменено:      backend/Dockerfile
        изменено:      backend/Dockerfile.prod
        изменено:      backend/backend/scripts/start_prod.sh
        изменено:      backend/backend/settings.py
        изменено:      backend/backend/urls.py
        изменено:      backend/make_questionnaire/models/questionnaire_model.py
        изменено:      backend/make_questionnaire/serializers.py
        изменено:      backend/make_questionnaire/tests.py
        изменено:      backend/requirements.txt
        изменено:      docker-compose.yml
        изменено:      frontend/src/views/Questionnaire.vue
        изменено:      nginx/Dockerfile
        изменено:      nginx/nginx_prod.conf
```
