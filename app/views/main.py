# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, flash,url_for
from app.models.bann import Enfant, Contrat
from app import app, db

@app.route('/', methods=['GET'])
def index():
    return "<h1>Hello World</h1>"

@app.route('/list', methods=['GET'])
def list_enfant():
    return render_template(
        'list.html',
        categories=[],
        enfants=Enfant.query.all())

@app.route('/ajout-enfant', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        enfant = Enfant(prenom=request.form['prenom'], nom= request.form['nom'])
        db.session.add(enfant)
        db.session.commit()
        flash('Ajout d\'enfant réussi')
        return redirect(url_for('list_enfant'))
    else:
        return render_template(
            'new-child.html')
