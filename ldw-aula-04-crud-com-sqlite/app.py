from flask import Flask, render_template  # importando o flask
from controllers import routes
from models.database import db

import os

app = Flask(__name__, template_folder='views')

# definindo a rota principal da aplicação '/'

routes.init_app(app)
dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(dir, 'models/games.sqlite3')
# criando o arquivo do banco 

# se for executado diretamente pelo interpretador
if __name__ == '__main__':
    db.init_app(app=app)
    #verificar o inicio da aplicação no inicio da aplicação se o BD já existe. Se não, ele cria.
    with app.test_request_context():
        db.create_all()
        
    # inciando servidor
    app.run(host='0.0.0.0', port=5000, debug=True)
