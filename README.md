# HR-questionnaire
Выпускной проект по курсу SkillFactory

##Вступление
Этот README.md будет больше похож на туториал о том как запускать связку django-vue-gunicorn-nginx

Причиной этому служит желание самому лучше разобраться как это устроено плюс отсутствием хорошо написаного туториала на русском. Да и на английском я нашел лиш два туториала из которых буду пытаться делать гибрида.
В дальнейшем по идее этот проект до какого-то определенного момента можно будет использовать как сетап для подобных сборок.
Источники откуда брал инфу, ниже. И, да, прибудет с нами сила!

 - [Здесь](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/) мне нравится настройка cтатики, медиа и то как реализован докерфайл
 - [Здесь](https://gitlab.com/briancaffey/docker-nginx-django-vue-architecture/-/blob/master/documentation/README.md) мне нравится методология и стиль разработки, а также структурированость
  

##Git
Сразу скажу что я буду пытаться придерживаться правильному бенчингу с гитом. В оигинальном туториале ссылка на [эту](https://nvie.com/posts/a-successful-git-branching-model/) статью. 
Создадим ветку develop через корорую будем пропускать дальнейшие измененияв мастер. И также ветку в которой мы будем все это разрабатывать.
```
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

```
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

```
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
```
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
```
$ cd backend && ls -al
итого 16
drwxr-xr-x 3 michael michael 4096 мая 22 05:56 .
drwxrwxr-x 5 michael michael 4096 мая 22 06:28 ..
drwxr-xr-x 2 michael michael 4096 мая 22 05:56 backend
-rwxr-xr-x 1 michael michael  627 мая 22 05:56 manage.py
```
Как вы видите ничего не принадлежит `root` и ето именно то что нам и было нужно.

Давайте проверим какие изменения мы внесли с помощью `git status`:
```
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

```
$ git add . && git commit -m "created django project and docker files, updated README"
```

