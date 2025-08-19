from flask import Flask, render_template  # importando o flask
from controllers import routes
app = Flask(__name__, template_folder='views')

# definindo a rota principal da aplicação '/'


routes.init_app(app)

# se for executado diretamente pelo interpretador
if __name__ == '__main__':
    # inciando servidor
    app.run(host='localhost', port=5000, debug=True)
