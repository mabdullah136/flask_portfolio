from src import create_app

app = create_app()

if __name__ == "__main__":
    
    app.run(host='192.168.100.194', port=5000)



