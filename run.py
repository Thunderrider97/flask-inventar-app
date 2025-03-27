from app import create_app

#Generiert die App
app = create_app()

#Führt die App aus
if __name__ == "__main__":
    app.run(debug=True)