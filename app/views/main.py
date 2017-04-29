# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import render_template, request, redirect, flash,url_for
from app.models.bann import Enfant, Contrat, Horaire
from app import app, db
import math
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

@app.route('/ajout-horaires', methods=['GET', 'POST'])
def add_schedules():
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
            contrat_id = request.form['contrat']
            for horaire in zip(request.form.getlist('jours[]'),
                               request.form.getlist('debuts[]'),
                               request.form.getlist('fins[]'),
                               request.form.getlist('commentaires[]')):
                new_horaire = Horaire(jour=horaire[0],
                                      debut=datetime.strptime(horaire[1], '%H:%M'),
                                      fin=datetime.strptime(horaire[2], '%H:%M'),
                                      commentaire=horaire[3],
                                      contrat_id=contrat_id)
                db.session.add(new_horaire)
            db.session.commit()
            flash('Ajout des horaires réussi')
            return redirect(url_for('add_schedules'))
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

@app.route('/liste-contrat', methods=['GET'])
def list_contract():
    contrat_id = request.args.get('contrat_id')
    if contrat_id is not None:
        days_week = list(calendar.day_name)
        contrat=Contrat.query.filter_by(id=contrat_id).first()
        accueil_hebdomadaire = timedelta()
        jours = set()
        horaires = []
        for horaire in contrat.horaires:
            tmp = []
            tmp.append(days_week[horaire.jour])
            tmp.append(horaire.debut.strftime('%H:%M'))
            tmp.append(horaire.fin.strftime('%H:%M'))
            delta = (horaire.fin - horaire.debut)
            hours, remainder = divmod(delta.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            tmp.append(str(int(hours))+'h'+str(int(minutes)))
            tmp.append(horaire.commentaire);
            horaires.append(tmp)
            accueil_hebdomadaire += delta
            jours.add(horaire.jour)
        hours, remainder = divmod(accueil_hebdomadaire.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        accueil_hebdomadaire = [accueil_hebdomadaire.total_seconds() / 3600, int(hours), int(minutes)]
        salaire_mensuel = (contrat.salaire * accueil_hebdomadaire[0] * float(contrat.nb_semaine)) / 12.0
        heures_normal_mensuel = int(round((accueil_hebdomadaire[0] * float(contrat.nb_semaine)) / 12.0))
        jours_activite=math.ceil(len(jours) * float(contrat.nb_semaine) / 12.0)
        heures_normales=int(round(salaire_mensuel / contrat.salaire))        
        return render_template('list-contract.html', contrats=Contrat.query.filter_by(etat='actif'),
                               selected_contrat=contrat.id,
                               contrat=contrat, horaires=horaires,
                               accueil_hebdomadaire=accueil_hebdomadaire,
                               salaire_mensuel=salaire_mensuel,
                               heures_normal_mensuel=heures_normal_mensuel,
                               nb_jours=len(jours),
                               jours_activite=jours_activite,
                               heures_normales=heures_normales)
    else:
        return render_template('list-contract.html', contrats=Contrat.query.filter_by(etat='actif'))
                               
