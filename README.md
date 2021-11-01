# astreya-take-home
Astreya Take Home Exam

# Specifications
* A player will need to input his name before proceeding with the game (User's entered name should be saved in DB)
* The player will be battling against a bot by selecting one of three buttons (Rock, Paper, or Scissor)
* The player's score, player's and bot's move in every round should be saved in a log.
* The player will be prompted either he / she wins or loses based on the results of the best of 3 rounds.
* The player can either start a new game, or end it, returning to the user's name in put window.


# Django Backend
Open this in a separate terminal
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


# React Frontend
Also run the following in a separate terminal.
## Prepping the Frontend
1) Navigate to ***astreya-take-home\/react_frontend\/*** and run
```shell
npm install
```
2) Then do the same inside ***astreya-take-home\/react_frontend\/janken\/***
```shell
npm install
```
3) Then start a development build.
```
npm start
```
4) The site should be available at **localhost:3000**