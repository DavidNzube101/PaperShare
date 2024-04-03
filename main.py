
from website import initialize_app

app = initialize_app()

if __name__ == '__main__':
  app.run(debug="True", host="0.0.0.0", port=9081)

    