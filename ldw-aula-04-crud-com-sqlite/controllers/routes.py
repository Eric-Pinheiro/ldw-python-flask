from flask import render_template, request, redirect, url_for
import urllib
import json
from models.database import Game, db

def init_app(app):
    players = ['yan', 'ferrari', 'valeria', 'amanda']
    gamelist = [{'Título': 'Slime Rancher',
                 'Ano': 2015, 'Categoria': 'Casual'}]

    @app.route('/')
    def home():  # função que será executada ao acessar a rota
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():  # função que será executada ao acessar a rota
        title = 'Tarisland'
        year = 2022
        category = 'MMORPG'
        console = {'name': 'playstation 5',
                   'manufacturer': 'sony', 'year': 2020}
        # tratando um req post com request
        if request.method == 'POST':
            # coletando o texto da input
            if request.form.get('player'):
                players.append(request.form.get('player'))
                return redirect(url_for('games'))

        return render_template('games.html', title=title, year=year, category=category, players=players, console=console)

    @app.route('/newgame', methods=['GET', 'POST'])
    def newgame():

        if request.method == 'POST':
            if request.form.get('title') and request.form.get('year') and request.form.get('category'):
                gamelist.append({"Título": request.form.get('title'), "Ano": request.form.get(
                    'year'), "Categoria": request.form.get('category')})
                return redirect(url_for('newgame'))
        return render_template('newGame.html', gamelist=gamelist)

    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gameList = json.loads(data)
        #verificando se o parametro foi enviado
        if id:
            gameInfo = []
            for game in gameList:
                if game['id'] == id:
                    gameInfo = game
                    break
            if gameInfo:
                return render_template('gameInfo.html', gameInfo=gameInfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'
        else:
            return render_template('apigames.html', gameList=gameList)
    
        
    @app.route('/estoque', methods=['GET','POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            #selecionando o jogo pelo id
            game = Game.query.get(id)
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
            
        if request.method == 'POST':
            newGame = Game(request.form['title'], request.form['year'], request.form['category'], request.form['platform'],request.form['price'],request.form['quantity'])
            db.session.add(newGame)
            db.session.commit()#seleciona todos os registros
            return redirect(url_for('estoque'))
        gamesEstoque = Game.query.all() #query.all() é um metodo do sql alchemy 
        #seleciona todos os registros
        return render_template('estoque.html', gamesEstoque=gamesEstoque)
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        game = Game.query.get(id)
        if request.method == 'POST':
            game.title = request.form['title']
            game.year = request.form['year']
            game.category = request.form['category']
            game.platform = request.form['platform']
            game.price = request.form['price']
            game.quantity = request.form['quantity']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)