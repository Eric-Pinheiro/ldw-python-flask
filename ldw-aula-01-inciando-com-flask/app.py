from flask import Flask, render_template  # importando o flask

app = Flask(__name__, template_folder='views')

# definindo a rota principal da aplicação '/'


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


# se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # inciando servidor
    app.run(host='localhost', port=5000, debug=True)
