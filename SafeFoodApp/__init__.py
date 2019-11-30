from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"]= '6a8a66928be4f34f3a91662bfc24debc'


from SafeFoodApp import routes
