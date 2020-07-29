from flask import Blueprint, render_template, request
from mock import objs
from flask_login import login_required
from sqlalchemy import text
from controller.database import Database

engine = Database().engine

historico = Blueprint('Historico', __name__)


@historico.route('/historico', methods=['GET'])
@login_required
def index():
    idUsuario = request.args.get('idUsuario')
    sectionName = request.args.get('sectionName')
    view = request.args.get('view')

    sql = text("SELECT * FROM {}".format(view))
    result = engine.execute(sql)

    print([i[0] for i in result])

    historico = {
        "label": sectionName,
        "content": result
    }

    return render_template('historico.html', historico=historico)
