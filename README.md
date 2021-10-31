# astreya-take-home
Astreya Take Home Exam


# Django Backend
## Prepping the Backend
1) I assume you have **virtualenv** and **virtualenvwrapper** installed. If you don't, download and install it now.
2) Create a virtualenv for this Django backend Projects and activate it.

```shell
mkvirtualenv --python=python3 astreya
workon astreya
```

3) Navigate to ***django_backend\/*** and simply run
```shell
pip install -r requirements
```

4) Introduce the migrations
```shell
python manage.py migrate
```

5) Run the server
```shell
python manage.py runserver 8000
```