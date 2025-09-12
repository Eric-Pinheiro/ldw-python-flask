from flask import render_template, request, redirect, url_for
import urllib
import json


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