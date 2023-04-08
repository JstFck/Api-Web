from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'type_your_secret_key_there'


def main():
    app.run()


if __name__ == '__main__':
    main()
