"""
Date : 21/11/2022
Auteur : Christian Doriath
Dossier : /Python39/MesDEv/Flask/Flask_codebase2023
Fichier : app.py
Description : app "codebase" une base de données qui contient TOUTE notre base des connaissances
de code informatique. 
"""

# -*- coding: utf-8 -*-
import datetime
import string
from flask import Flask, request, render_template, session, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateTimeField
from wtforms.validators import DataRequired,Regexp,IPAddress,Length,Required,InputRequired
from wtforms.validators import Email ,Regexp, EqualTo, NumberRange, NoneOf, URL, AnyOf 
#List of available validators : http://wtforms.simplecodes.com/docs/0.6.1/validators.html
from flask_sqlalchemy import SQLAlchemy
from random import choice
import locale
import time
import pdb
import json 
import os 
import uuid
import pytz
from socket import gethostname # déterminer le nom du serveur pour différencier 'localhost' de paw
from socket import getfqdn


# locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
locale.setlocale(locale.LC_TIME, 'fr_FR') # sur Windows
    
app = Flask(__name__)

from packages.mysql import *
from packages.machine import * 

#Le nom d'utilisateur et le mot de passe mysql est dans le fichier mysql.py
if machine == 'local':
    print("machine sur LOCALHOST")
    chemin_notrecode = "static\\notrecode"
    username_mysql = connection_data['local']['username_mysql']
    password_mysql = connection_data['local']['password_mysql']
    hostname_mysql = connection_data['local']['hostname_mysql']
    databasename_mysql = connection_data['local']['databasename_mysql']

if machine == 'PAW':
    print("machine sur PAW") 
    chemin_notrecode = "codebase/static/notrecode"
    username_mysql = connection_data['paw']['username_mysql']
    password_mysql = connection_data['paw']['password_mysql']
    hostname_mysql = connection_data['paw']['hostname_mysql']
    databasename_mysql = connection_data['paw']['databasename_mysql']
    

# Le code important est dans 'Main' : 
# m = Main(app.config['UPLOAD_FOLDER'])
# m.run() 

print("username_mysql : ",username_mysql ,"\n")
print("password_mysql : ",password_mysql ,"\n")
print("hostname_mysql : ",hostname_mysql ,"\n")
print("databasename_mysql : ",databasename_mysql ,"\n")

app.debug = True
# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'replace with a SUPERsecretKEY '
# source : https://blog.pythonanywhere.com/121
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=username_mysql,
    password=password_mysql,
    hostname=hostname_mysql,
    databasename=databasename_mysql,
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_RECORD_QUERIES'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



# if not app.debug:
#     file_handler = FileHandler('errorlog.txt')
#     file_handler.setLevel(WARNING)
#     app.logger.addHandler(file_handler)


# def dbConnected():
#     try:
#         dd = Langage.query.filter_by().all()
#         return {'tf':True,'data':'TOUT va bien'}
#     except Exception as exception:
#         print("Exception : ",exception)
#         return {'tf':False,'data':exception}




def dateProvider():
    # Fournir immédiatement l'heure et la date de Paris en plusieurs formats : 
    # - en texte long dateLongueTexte. 
    # - un integer pour epoch
    # - un datetime 
    # Utiliser le fuseau horaire local (Paris)
    fuseau_horaire_local = pytz.timezone('Europe/Paris')

    # Obtenir l'heure locale dans le fuseau horaire défini
    heure_locale = datetime.datetime.now(fuseau_horaire_local)

    dateLongueTexte = heure_locale.strftime("%A, %d %B %Y %H:%M:%S")

    epoch = int(heure_locale.timestamp())
    
    return{'date':heure_locale,'texte':dateLongueTexte,'epoch':epoch}


# def randomString(p_length):
#     s = ""
#     #créer un string de p_length lettres
#     for x in range(p_length):
#       s = s + choice(string.ascii_letters)
#     return s


def claire():
    return "il est midi"


class Clients (db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateCreation = db.Column(db.DateTime)
    dateLongueTexteCreation = db.Column(db.Text)
    epochCreation = db.Column(db.Integer)
    commandes = db.relationship('Commandes', backref='clients')

    nom = db.Column(db.Text)
    supprime = db.Column(db.Integer)
    # dossiers = db.relationship("Dossier", backref="langage")
    uuid = db.Column(db.Text)
    def __init__(self, p_nom):
        # Ici on crée une instance de la classe 'Langage'
        # le champ 'id' est généré automatiquement par MySQL

        try:
            self.nom=p_nom
            self.dateCreation= dateProvider()['date']
            self.dateLongueTexteCreation = dateProvider()['texte']
            self.epochCreation = dateProvider()['epoch']
            self.supprime = 0
            return None
        except Exception as exception:
            print("Exception : ",exception)
            return {'tf':False,'data':exception}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    def create(self, p_nom):
        print("self.__table__.columns : ",self.__table__.columns)
        Myadd = Clients(p_nom)
        db.session.add(Myadd)
        db.session.commit() 
        # pour informer des champs des dates donnés par le code python 
        # et l'id donné par mysql je retourne l'enregistrement
        return {'tf':True,'data':Myadd.as_dict()}


class Commandes (db.Model):
    __tablename__ = 'commandes'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True )
    article = db.Column(db.String(20), nullable=False)
    dateCreation = db.Column(db.DateTime)
    dateLongueTexteCreation = db.Column(db.Text)
    epochCreation = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    supprime = db.Column(db.Integer)

    
    def __init__(self, p_article, p_client):
        # Ici on crée une instance de la classe 'Commandes'
        # le champ 'id' est généré automatiquement par MySQL
        try:
            self.article=p_article
            self.dateCreation= dateProvider()['date']
            self.dateLongueTexteCreation = dateProvider()['texte']
            self.epochCreation = dateProvider()['epoch']
            self.client_id = p_client
            self.supprime = 0
            return None
        except Exception as exception:
            print("Exception : ",exception)
            return {'tf':False,'data':exception}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientsPro (db.Model):
    __tablename__ = 'clients_pro'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dateCreation = db.Column(db.DateTime)
    dateLongueTexteCreation = db.Column(db.Text)
    epochCreation = db.Column(db.Integer)
    commandes = db.relationship('CommandesPro', backref='clients_pro')

    nom = db.Column(db.Text)
    supprime = db.Column(db.Integer)
    # dossiers = db.relationship("Dossier", backref="langage")
    uuid = db.Column(db.Text)
    def __init__(self, p_nom):
        # Ici on crée une instance de la classe 'Langage'
        # le champ 'id' est généré automatiquement par MySQL

        try:
            self.nom=p_nom
            self.dateCreation = dateProvider()['date']
            self.dateLongueTexteCreation = dateProvider()['texte']
            self.epochCreation = dateProvider()['epoch']
            self.supprime = 0
            return None
        except Exception as exception:
            print("Exception : ",exception)
            return {'tf':False,'data':exception}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
    def create(self, p_nom):
        print("self.__table__.columns : ",self.__table__.columns)
        Myadd = Clients(p_nom)
        db.session.add(Myadd)
        db.session.commit() 
        # pour informer des champs des dates donnés par le code python 
        # et l'id donné par mysql je retourne l'enregistrement
        return {'tf':True,'data':Myadd.as_dict()}


class CommandesPro (db.Model):
    __tablename__ = 'commandes_pro'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True )
    dateCreation = db.Column(db.DateTime)
    dateLongueTexteCreation = db.Column(db.Text)
    epochCreation = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('clients_pro.id'))
    supprime = db.Column(db.Integer)
    articles = db.relationship('ArticlesPro', backref='commandes_pro') 
    
    def __init__(self, p_client):
        # Ici on crée une instance de la classe 'Commandes'
        # le champ 'id' est généré automatiquement par MySQL
        try:
            self.dateCreation= dateProvider()['date']
            self.dateLongueTexteCreation = dateProvider()['texte']
            self.epochCreation = dateProvider()['epoch']
            self.client_id = p_client
            self.supprime = 0
            return None
        except Exception as exception:
            print("Exception : ",exception)
            return {'tf':False,'data':exception}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
 
class ArticlesPro (db.Model):
    __tablename__ = 'articles_pro'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True )
    article = db.Column(db.String(20), nullable=False)
    dateCreation = db.Column(db.DateTime)
    dateLongueTexteCreation = db.Column(db.Text)
    epochCreation = db.Column(db.Integer)
    commande_id = db.Column(db.Integer, db.ForeignKey('commandes_pro.id'))
    supprime = db.Column(db.Integer)

     
    def __init__(self, p_article, p_commandeId):
        # Ici on crée une instance de la classe 'Commandes'
        # le champ 'id' est généré automatiquement par MySQL
        try:
            self.article=p_article
            self.dateCreation= dateProvider()['date']
            self.dateLongueTexteCreation = dateProvider()['texte']
            self.epochCreation = dateProvider()['epoch']
            self.commande_id = p_commandeId
            self.supprime = 0
            return None
        except Exception as exception:
            print("Exception : ",exception)
            return {'tf':False,'data':exception}

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

#Créer toutes les tables 
db.create_all() 


@app.route('/', methods=['GET', 'POST'])
def myindex():
    return render_template('index.html') 

#Afficher la table clients
@app.route('/page1', methods=['GET', 'POST'])
def mypage1():
    e = Clients.query.filter_by(supprime=0).all()
    print("les datas : ",e,"\n")
    datas = []
    for l in e:
        datas.append(l.as_dict())
        print("Dict : ",l.as_dict(),"\n")
    return render_template('page1.html',datas=datas)   

# 14/09/2023
#Permet d'afficher les datas d'une table mysql
@app.route("/test1")
def mytest1():
    #Filter_by permet de filtrer les lignes d'une table dans une base de données 
    #.all() permet d'ajouter toutes les lignes
    e = Clients.query.filter_by(supprime=0).all()
    print("les lignes : ",e,"\n")
    datas = []
    for ligne in e:
        datas.append(ligne.id)
    print("les datas : ",datas,"\n")
    return jsonify(datas)



# 14/09/2023
#Permet de supprimer un élément de la table
@app.route("/effacer/<id>")
def myeffacer(id):
    try:
        print("Voici ID : ",id,"\n")
        #.first permet de filtrer seulement une ligne
        e = Clients.query.filter_by(id=id).first()
        print("Voici enregistrement : ",e,"\n")
        print("Voici enregistrement : ",e.id,"\n")
        e.supprime = 1
        db.session.commit() 
        return jsonify({'tf':True,'data':'Ok'})
    except:
        return jsonify({'tf':False,'data':'Impossible ...'})


#Elle permet d'ajouter un élément dans la table
#Les méthodes GET et POST sont très importantes pour l'envoi d'éléments 
@app.route("/page2",methods=['GET','POST'])
def mypage2():
    #print("Voici le chemin absolu : ",os.getcwd())
    print("je suis dans PAGE 2")
    if request.method == 'POST':
        print("je suis dans PAGE 2 / POST")
        mon_uuid = str(uuid.uuid4())
        print("UUID:",mon_uuid)
    
        maValeur = Clients(request.form["nom"])
        #ajouter ma valeur à la table MYSQL 
        db.session.add(maValeur)
        db.session.commit() 
        print("les informations ont été ajoutés !!!! ")  
    return render_template('page2.html') 



@app.route("/modifier",methods=['GET','POST'])
def mymodifier():
    if request.method == 'POST':
        print("je suis dans POST")
        r = request.get_json()
        nom = r['nom']
        id = r['id']
        e = Clients.query.filter_by(id=id).first()
        print("EEEE:",e.as_dict())
        e.nom = nom
        db.session.commit() 
    return jsonify({'nom':nom,'id':id})


#Elle permet de modifier et supprimer une ligne dans une table
@app.route("/page3",methods=['GET','POST'])
def mypage3():
    e = Clients.query.filter_by(supprime=0).all()
    print("les datas : ",e,"\n")
    datas = []
    for l in e:
        datas.append(l.as_dict())
        print("Dict : ",l.as_dict(),"\n")
    return render_template('page3.html',datas=datas) 
    

@app.route("/page4",methods=['GET','POST'])
def mypage4():
    e = Commandes.query.filter_by(supprime=0).all()
    print("les datas : ",e,"\n")
    datas = []
    for l in e:
        datas.append(l.as_dict())
        print("Dict Commandes : ",l.as_dict(),"\n") 


    #print("Voici le chemin absolu : ",os.getcwd())
    print("je suis dans PAGE 4")
    if request.method == 'POST':
        dataDict = request.form.to_dict()
        print("je suis dans PAGE 4 / POST")
        mon_uuid = str(uuid.uuid4())
        print("UUID:",mon_uuid)
        nom = request.form["nom"]
        idClient = request.form["idclient"]
    
        maValeur = Commandes(nom,idClient)
        #ajouter ma valeur à la table MYSQL 
        try:
            db.session.add(maValeur)
            db.session.commit() 
            print("les informations ont été ajoutés !!!! ") 
        except:
            print("les informations n'ont PAS été ajoutés !!!! ") 


    return render_template('page4.html',datas=datas) 

#Elle permet d'ajouter un client , une commande et un article 
#C'est les relations en mysql 
@app.route("/page5",methods=['GET','POST'])
def mypage5():
    return render_template('page5.html') 


#récupérer seulement les id pour les clients pro
@app.route("/id_clients",methods=['GET','POST'])
def myid_clients():
    e = ClientsPro.query.filter_by(supprime=0).all()
    print("les datas : ",e,"\n")
    datas = []
    for l in e:
        datas.append(l.id)
        print("Dict Commandes : ",l.as_dict(),"\n") 
        print("l.id : ",l.id,"\n") 

    if request.method == 'POST':
        dataDict = request.form.to_dict()
        print("dataDict:",dataDict)        
    return jsonify(datas)

#récupérer seulement les id pour les commandes pro
@app.route("/id_commandes",methods=['GET','POST'])
def myid_commandes():
    e = CommandesPro.query.filter_by(supprime=0).all()
    print("les datas : ",e,"\n")
    datas = []
    for l in e:
        datas.append(l.id)
        print("Dict Commandes : ",l.as_dict(),"\n") 
        print("l.id : ",l.id,"\n") 

    if request.method == 'POST':
        dataDict = request.form.to_dict()
        print("dataDict:",dataDict)        
    return jsonify(datas)


#Utilisation de form.to_dict
@app.route("/datas",methods=['GET','POST'])
def mydatas():
    if request.method == 'POST':
        dataDict = request.form.to_dict()
        print("dataDict:",dataDict)        
    return jsonify({'nom':'dd'})


@app.route("/creerclient/<p_nom>",methods=['GET','POST'])
def mycreerclient(p_nom):
    print("nom :",p_nom)        
    return jsonify({'nom':p_nom})


@app.route("/ajouterclientpro",methods=['GET','POST'])
def myajouterclientpro():
    print("je suis dans ajouterclientpro")
    if request.method == 'POST':
        print("je suis dans PAGE ajouterclientpro / POST")
        mon_uuid = str(uuid.uuid4())
        print("UUID:",mon_uuid)
    
        maValeur = ClientsPro(request.form["nom"])
        #ajouter ma valeur à la table MYSQL 
        try:
            db.session.add(maValeur)
            db.session.commit() 
        except:
            return "Erreur"
    return render_template('page5.html') 

@app.route("/ajoutercommande",methods=['GET','POST'])
def myajoutercommande():
    print("je suis dans ajoutercommande")
    if request.method == 'POST':
        print("je suis dans PAGE ajoutercommande / POST")
        mon_uuid = str(uuid.uuid4())
        print("UUID:",mon_uuid)
        maValeur = CommandesPro(request.form["commande"])
        #ajouter ma valeur à la table MYSQL 
        try:
            db.session.add(maValeur)
            db.session.commit() 
        except:
            return "Erreur"
    return render_template('page5.html') 

#Ajouter des valeurs de plusieurs input dans une table
@app.route("/ajouterarticle",methods=['GET','POST'])
def myajouterarticle():
    print("je suis dans ajouterarticle")
    if request.method == 'POST':
        dataDict = request.form.to_dict()
        print("dataDict : ",dataDict)
        maValeur = ArticlesPro(dataDict['article'],dataDict['commande_id'])
        try:
            db.session.add(maValeur)            
            db.session.commit() 

        except:
            return "Erreur"
    return render_template('page5.html')

    

    

  

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500




        
