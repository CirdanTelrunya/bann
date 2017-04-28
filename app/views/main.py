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
            return render_template('horaire.html', horaires = horaires, days_week = days_week, selected_contrat=int(request.form['contrat']), contrats=Contrat.query.filter_by(etat='actif'))
        else:
            return '<h1>Hello World</h1><br />'+request.form['submit']
    else:
        return render_template('horaire.html', contrats=Contrat.query.filter_by(etat='actif'))

@app.route('/ajout-contrat', methods=['GET', 'POST'])
def add_contract():
    if request.method == 'POST':
        contrat = Contrat()
        contrat.enfant_id = int(request.form['enfant'])
        contrat.anniversaire = datetime.strptime(request.form['anniversaire'], '%d/%m/%Y')
        contrat.nb_semaine = int(request.form['nb_semaine'])
        contrat.salaire = float(request.form['salaire'])
        contrat.indemnite = float(request.form['indemnite'])
        contrat.etat = 'actif'
        db.session.add(contrat)
        db.session.commit()
        flash('Ajout de contrat réussi')
        return redirect(url_for('add_contract'))
    else:
        date_now = datetime.now().strftime('%d/%m/%Y')
        return render_template('new-contract.html', enfants=Enfant.query.all(), date_now=date_now)
