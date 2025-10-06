from flask import render_template, request, redirect, url_for
import urllib
import json
from models.database import Maker, Model, db


def init_app(app):
    access_key = 'CFEr1zEUYadOwOEmMovDSqrbSHGFlU69nYPHeQ488CM'
    popular_brands = POPULAR_BRANDS = [
    "TOYOTA",
    "HONDA",
    "VOLKSWAGEN",
    "FORD",
    "CHEVROLET",
    "BMW",
    "MERCEDES-BENZ",
    "NISSAN",
    "AUDI",
    "LEXUS",
    "SUBARU",
    "MAZDA",
    "PORSCHE",
    "MASERATI",
    "FERRARI",
    "LAMBORGHINI",
]
    modelos = ['Deora II']
    carros =[{'Marca':'fiat', 'Modelo':'uno', 'Ano':98}]
    @app.route("/")
    def home():
        return render_template('index.html')
    @app.route("/cars", methods=['GET','POST'])
    def cars():

        if request.method == 'POST':
            # coletando o texto da input
            if request.form.get('modelo'):
                modelos.append(request.form.get('modelo'))
                return redirect(url_for('cars'))
                
        return render_template('cars.html',modelos=modelos, carros=carros)#o que é definido no urlfor é o nome da "def"
    
    @app.route("/newcar", methods=['GET','POST'])
    def newcar():
        if request.method == 'POST':
            if request.form.get('marca') and request.form.get('model') and request.form.get('ano'):
                carros.append({"Marca": request.form.get('marca'), "Modelo": request.form.get(
                    'model'), "Ano": request.form.get('ano')})
                return redirect(url_for('newcar'))

        
        return render_template('newcar.html', carros=carros)
    @app.route('/api_cars')
    @app.route('/api_cars/<int:make_id>')
    def api_cars(make_id=None):
        if make_id:
            # Busca modelos de uma marca específica
            url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformakeid/{make_id}?format=json'
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            models = data.get("Results", [])
            return render_template('models.html', models=models, make_id=make_id, access_key=access_key)
        else:
            # Lista todas as marcas
            url = 'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            makes = data.get("Results", [])
            makes = [m for m in makes if m["Make_Name"] in popular_brands]
            return render_template('makes.html', makes=makes)

    # LISTAR, CADASTRAR E DELETAR MODELOS
    @app.route('/modelos', methods=['GET', 'POST'])
    @app.route('/modelos/delete/<int:id>')
    def modelos(id=None):
        # Exclusão
        if id:
            modelo = Model.query.get(id)
            if not modelo:
                return redirect(url_for('modelos'))
            db.session.delete(modelo)
            db.session.commit()
            
            return redirect(url_for('modelos'))

        # Cadastro
        if request.method == 'POST':
            marca = request.form.get('marca', '').strip()
            modelo_nome = request.form.get('modelo', '').strip()
            ano_raw = request.form.get('ano', '').strip()
            maker_id = request.form.get('maker_id', '').strip()
            image = request.form.get('image', '').strip()

            # Conversões
            try:
                ano = int(ano_raw)
            except ValueError:
                ano = 0

            if not image:
                image = "https://via.placeholder.com/300x300?text=Sem+Imagem"

            if not marca or not modelo_nome or ano <= 0 or not maker_id:
                return redirect(url_for('modelos'))

            novo_modelo = Model(
                marca=marca,
                modelo=modelo_nome,
                ano=ano,
                image=image,
                maker_id=maker_id
            )
            db.session.add(novo_modelo)
            db.session.commit()
            return redirect(url_for('modelos'))

        # Listagem
        page = request.args.get('page', 1, type=int)
        per_page = 4

        search = request.args.get('search', '').strip()
        maker_filter = request.args.get('maker_filter')

        query = Model.query
        if search:
            query = query.filter(Model.modelo.ilike(f"%{search}%"))
        if maker_filter:
            query = query.filter(Model.maker_id == maker_filter)

        modelos_paginados = query.paginate(page=page, per_page=per_page)
        makers = Maker.query.all()

        return render_template('modelos.html', modelos=modelos_paginados, makers=makers)


    # EDITAR MODELOS 
    @app.route('/modelos/edit/<int:id>', methods=['GET', 'POST'])
    def editar_modelo(id):
        modelo = Model.query.get(id)
        if not modelo:
            return f"Modelo com ID {id} não encontrado.", 404

        if request.method == 'POST':
            modelo.marca = request.form['marca']
            modelo.modelo = request.form['modelo']
            modelo.ano = request.form['ano']
            modelo.image = request.form['image']
            modelo.maker_id = request.form['maker_id']

            db.session.commit()
            return redirect(url_for('modelos'))

        makers = Maker.query.all()
        return render_template('edit_modelo.html', modelo=modelo, makers=makers)


    #  LISTAR, CADASTRAR E EXCLUIR FABRICANTES
    @app.route('/fabricantes', methods=['GET', 'POST'])
    @app.route('/fabricantes/delete/<int:id>')
    def fabricantes(id=None):
        if id:
            fabricante = Maker.query.get(id)
            db.session.delete(fabricante)
            db.session.commit()
            return redirect(url_for('fabricantes'))

        if request.method == 'POST':
            nome = request.form['fabricante']
            novo_fabricante = Maker(fabricante=nome)
            db.session.add(novo_fabricante)
            db.session.commit()
            return redirect(url_for('fabricantes'))

        fabricantes = Maker.query.all()
        return render_template('fabricantes.html', fabricantes=fabricantes)


    # EDITAR FABRICANTE 
    @app.route('/fabricantes/edit/<int:id>', methods=['GET', 'POST'])
    def editar_fabricante(id):
        fabricante = Maker.query.get(id)
        if not fabricante:
            return f"Fabricante com ID {id} não encontrado.", 404

        if request.method == 'POST':
            fabricante.fabricante = request.form['fabricante']
            db.session.commit()
            return redirect(url_for('fabricantes'))

        return render_template('edit_fabricante.html', fabricante=fabricante)