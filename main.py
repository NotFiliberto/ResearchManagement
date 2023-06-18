# dev branch vineet
# Testing info: vineet.cesca@gmail.com password Paul1234

from website import create_app

app = create_app()


<<<<<<< HEAD
# prevent running additional servers if you 
# import something from
if __name__ == '__main__':  
    app.run(debug=True)
=======
if __name__ == '__main__':  # prevent running additional servers if you import something from
    app.run(debug=True)
>>>>>>> 9b262272dc9553e341a170a440fa45d30ab7a82c
