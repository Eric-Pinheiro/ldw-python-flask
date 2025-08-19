from flask import render_template


def init_app(app):
    @app.route('/')
    def home():  # função que será executada ao acessar a rota
        return render_template('index.html')


    @app.route('/games')
    def games():  # função que será executada ao acessar a rota
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        players = ['yan', 'ferrari', 'valeria', 'amanda']
        console = {'name': 'playstation 5', 'manufacturer': 'sony', 'year': 2020}
        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)
