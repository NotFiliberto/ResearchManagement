# dev branch vineet

from website import create_app

app = create_app()


# prevent running additional servers if you 
# import something from
if __name__ == '__main__':  
    app.run(debug=True)