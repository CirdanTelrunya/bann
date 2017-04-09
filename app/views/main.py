# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template, request, redirect, flash,url_for
from app.models.bann import Enfant, Contrat
from app import app, db
import locale
import calendar
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

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
    
@app.route('/test', methods=['GET', 'POST'])
def test_date():
    if request.method == 'POST':
        
        date_debut = datetime.strptime(request.form['debut'], '%H:%M')
        date_fin = datetime.strptime(request.form['fin'], '%H:%M')
        result = date_fin - date_debut
        hours, remainder = divmod(result.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return '<h1>Hello World</h1><br />'+str(int(hours))+':'+str(int(minutes))
    else:
        return render_template('test.html')

@app.route('/horaire', methods=['GET', 'POST'])
def test_horaire():
    
    if request.method == 'POST':
        if request.form['submit'] == 'add':
            horaires = []            
            for horaire in zip(request.form.getlist('jours[]'),
                               request.form.getlist('debuts[]'),
                               request.form.getlist('fins[]'),
                               request.form.getlist('commentaires[]')):
                tmp = []
                tmp.append(int(horaire[0]))
                tmp.append(datetime.strptime(horaire[1], '%H:%M'))
                tmp.append(datetime.strptime(horaire[2], '%H:%M'))
                tmp.append(horaire[3])
                horaires.append(tmp)
            new_horaire = []
            new_horaire.append(int(request.form['jour']))
            new_horaire.append(datetime.strptime(request.form['debut'], '%H:%M'))
            new_horaire.append(datetime.strptime(request.form['fin'], '%H:%M'))
            new_horaire.append(request.form['commentaire'])
            horaires.append(new_horaire)
            days_week = list(calendar.day_name)
            return render_template('horaire.html', horaires = horaires, days_week = days_week)
        else:
            return '<h1>Hello World</h1><br />'+request.form['submit']
    else:
        return render_template('horaire.html')

@app.route('/ajout-contrat', methods=['GET', 'POST'])
def add_contract():
    if request.method == 'POST':
        return render_template('new-contract.html')
    else:
        return render_template('new-contract.html', enfants=Enfant.query.all())
