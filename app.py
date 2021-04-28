from flaskyBlogger import create_app
app = create_app()
# if running this file directly using python then the below condition is true
if __name__ == '__main__':
    app.run(debug=True)
