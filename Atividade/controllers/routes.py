from flask import render_template, request, redirect, url_for

def init_app(app):
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