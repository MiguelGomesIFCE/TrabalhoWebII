from flask import render_template, request, redirect, url_for
from models.modelo import db, Tarefa
from werkzeug.utils import secure_filename
import os

def init_app(app):

    @app.route("/")
    def index():
        busca = request.args.get("busca", "")
        categoria = request.args.get("categoria", "")
        
        tarefas = Tarefa.query
        
        if busca:
            tarefas = tarefas.filter(Tarefa.titulo.ilike(f"%{busca}%"))
        
        if categoria:
            tarefas = tarefas.filter_by(categoria=categoria)

        tarefas = tarefas.order_by(Tarefa.data_criacao.desc()).all()
        return render_template("index.html", tarefas=tarefas)

    @app.route("/adicionar", methods=["GET", "POST"])
    def adicionar():
        if request.method == "POST":
            titulo = request.form["titulo"]
            descricao = request.form.get("descricao", "")
            categoria = request.form.get("categoria", "")
            imagem = None

            if "imagem" in request.files:
                file = request.files["imagem"]
                if file.filename != "":
                    filename = secure_filename(file.filename)
                    filepath = os.path.join("static/img", filename)
                    file.save(filepath)
                    imagem = filename

            nova = Tarefa(titulo=titulo, descricao=descricao,
                          categoria=categoria, imagem=imagem)
            db.session.add(nova)
            db.session.commit()

            return redirect(url_for("index"))
        
        return render_template("adicionar.html")

    @app.route("/editar/<int:id>", methods=["GET", "POST"])
    def editar(id):
        tarefa = Tarefa.query.get_or_404(id)

        if request.method == "POST":
            tarefa.titulo = request.form["titulo"]
            tarefa.descricao = request.form["descricao"]
            tarefa.categoria = request.form["categoria"]

            db.session.commit()
            return redirect(url_for("index"))

        return render_template("editar.html", tarefa=tarefa)

    @app.route("/concluir/<int:id>")
    def concluir(id):
        tarefa = Tarefa.query.get_or_404(id)

        tarefa.concluida = not tarefa.concluida
        db.session.commit()
        return redirect(url_for("index"))

    @app.route("/deletar/<int:id>")
    def deletar(id):
        tarefa = Tarefa.query.get_or_404(id)
        db.session.delete(tarefa)
        db.session.commit()
        return redirect(url_for("index"))