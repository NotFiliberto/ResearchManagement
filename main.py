# dev branch vineet
# Testing info: vineet.cesca@gmail.com password Paul1234

from website import create_app

app = create_app()


if __name__ == '__main__':  # prevent running additional servers if you import something from
    app.run(debug=True)
