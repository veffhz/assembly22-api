from application import create_app
from config import DevelopmentConfig

app = create_app(config_class=DevelopmentConfig)

if __name__ == "__main__":
    app.run()
