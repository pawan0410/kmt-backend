from app.application import application

application = application('local')


if __name__ == '__main__':
    application.run(host='0.0.0.0', threaded=True)
