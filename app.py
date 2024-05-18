import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pymysql

app = Flask(__name__)
app.secret_key = 'prj_intg'


def findConnection():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='projet_integration'
    )
    return connection


@app.route('/login_page_admin')
def login_page_admin():
    session.pop('user_admin', None)
    return render_template('login_admin.html')


@app.route('/login_admin_request', methods=['POST'])
def login_user():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    email = data.get('email')
    mdp = data.get('mdp')
    print(email, mdp)
    cursor.execute(f"SELECT * FROM Administrateur WHERE Email = '{email}' AND MDP = '{mdp}'")
    user = cursor.fetchone()
    print(user)
    cursor.close()
    mydb.close()
    if user is None:
        return jsonify({'status': 'error'})
    session['user_admin'] = user
    return jsonify({'status': 'success', 'user': user})


@app.route('/profile/<int:id>', methods=['GET'])
def profile(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    if session['user_admin'][0] != id:
        return redirect(url_for('profile', id=session['user_admin'][0]))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Administrateur WHERE IDAdministrateur = {id}")
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    return render_template('profile_admin.html', user=user)


@app.route('/')
def table_vol():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM Vols")
    l = list(cursor.fetchall())
    data = []
    for i in l:
        print(i)
        cursor.execute("SELECT Nom FROM Aeroport WHERE IDAeroport = %s", (i[1],))
        a = cursor.fetchone()
        x = list(i)
        x[1] = a[0]
        cursor.execute("SELECT Nom FROM Aeroport WHERE IDAeroport = %s", (i[2],))
        a = cursor.fetchone()
        x[2] = a[0]
        cursor.execute("SELECT Nom FROM Compagnie WHERE IDCompagnie = %s", (i[6],))
        a = cursor.fetchone()
        x.append(x[6])
        x[6] = a[0]
        data.append(x)
        print(data)
    cursor.execute("SELECT IDAeroport, Nom FROM Aeroport")
    arpts = cursor.fetchall()
    print(data[0])
    cursor.close()
    mydb.close()
    return render_template('tableVol.html', data=data, arpts=arpts, user=session['user_admin'])


@app.route('/aeroport')
def table_aeroport():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT A.Nom, P.Nom, V.Nom, Email, Tel, A.IDAeroport FROM Aeroport A, Ville V , Pays P WHERE A.idVille = V.IDVille AND V.IDPays = P.IDPays")
    data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return render_template('tableAeroport.html', data=data, user=session['user_admin'])


@app.route('/passager')
def table_passager():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(
        "SELECT `IDPassager`, P.Nom, `Prenom`, `Tel`, `CIN`, `MDP`, `Passeport`, `Genre`, PY.Nom, Adresse FROM Passager P, Pays PY WHERE P.Nationalite = PY.IDPays")
    data = cursor.fetchall()
    cursor.close()
    mydb.close()
    return render_template('tablePassager.html', data=data, user=session['user_admin'])


@app.route('/forgot_password', methods=['GET'])
def forgot_password():
    return render_template('mdp_oublie.html')


@app.route('/find-passager-nom', methods=['POST'])
def find_passager_nom():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    key = data.get('key')
    cursor.execute(
        f"SELECT `IDPassager`, P.Nom, `Prenom`, `Tel`, `CIN`, `MDP`, `Passeport`, `Genre`, PY.Nom, Adresse FROM Passager P, Pays PY WHERE P.Nationalite = PY.IDPays AND P.Nom LIKE '%{key}%'")
    cursor.close()
    mydb.close()
    data = {
        'liste': cursor.fetchall()
    }
    return jsonify(data)


@app.route('/find-passager-cin', methods=['POST'])
def find_passager_cin():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    key = data.get('key')
    cursor.execute(
        f"SELECT `IDPassager`, P.Nom, `Prenom`, `Tel`, `CIN`, `MDP`, `Passeport`, `Genre`, PY.Nom, Adresse FROM Passager P, Pays PY WHERE P.Nationalite = PY.IDPays AND P.CIN LIKE '%{key}%'")
    cursor.close()
    mydb.close()
    data = {
        'liste': cursor.fetchall()
    }
    return jsonify(data)


@app.route('/find-aeroport', methods=['POST'])
def find_aeroport():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    key = data.get('key')
    cursor.execute(
        f"SELECT A.Nom, P.Nom, V.Nom, Email, Tel, A.IDAeroport FROM Aeroport A, Ville V , Pays P WHERE A.IDVille = V.IDVille AND V.IDPays = P.IDPays AND A.Nom LIKE '%{key}%'")
    cursor.close()
    mydb.close()
    data = {
        'liste': cursor.fetchall()
    }
    return jsonify(data)


@app.route('/find-vol', methods=['POST'])
def find_vol():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    d = data.get('keyD')
    a = data.get('keyA')
    add = ""
    if d != "0":
        add += f"WHERE IDAeroportDepart = '{d}'"
    if a != '0':
        add += f"AND IDAeroportArrive = '{a}'"
    if add.find("WHERE") == -1:
        add.replace("AND", "WHERE")
    req = (f"""SELECT * FROM Vols {add} """)
    print(req)
    cursor.execute(req)
    l = list(cursor.fetchall())
    data = []
    for i in l:
        print(i)
        cursor.execute("SELECT Nom FROM Aeroport WHERE IDAeroport = %s", (i[1],))
        a = cursor.fetchone()
        x = list(i)
        x[1] = a[0]
        cursor.execute("SELECT Nom FROM Aeroport WHERE IDAeroport = %s", (i[2],))
        a = cursor.fetchone()
        x[2] = a[0]
        cursor.execute("SELECT Nom FROM Compagnie WHERE IDCompagnie = %s", (i[6],))
        a = cursor.fetchone()
        cursor.execute("SELECT Nom FROM Compagnie WHERE IDCompagnie = %s", (i[6],))
        a = cursor.fetchone()
        x.append(x[6])
        x[6] = a[0]
        x[4] = str(x[4])
        x[5] = str(x[5])
        data.append(x)
        print(data)
    cursor.close()
    mydb.close()
    data_return = {
        'liste': data,
        'user': session['user_admin']
    }
    print(data)
    return jsonify(data_return)


@app.route('/ajouter-aeroport', methods=['GET'])
def ajouter_aeroport():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT IDPays, Nom FROM Pays")
    pys = cursor.fetchall()
    cursor.execute("SELECT IDVille, Nom, IDPays FROM Ville")
    vls = cursor.fetchall()
    cursor.close()
    mydb.close()
    return render_template('ajout_aeroport.html', pys=pys, vls=vls, user=session['user_admin'])


@app.route('/find-ville-par-pays', methods=['POST'])
def find_ville_par_pays():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    key = data.get('key')
    cursor.execute(f"SELECT IDVille, Nom FROM Ville WHERE IDPays = {key}")
    cursor.close()
    mydb.close()
    data = {
        'liste': cursor.fetchall()
    }
    return jsonify(data)


@app.route('/create-aeroport', methods=['POST'])
def create_aeroport():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')
    tel = data.get('tel')
    ville = data.get('ville')
    cursor.execute(
        "INSERT INTO Aeroport (IDAeroport, IDVille, Nom, Email, Tel, Longitude, Lontitude) VALUES (NULL, %s, %s, %s, %s, '','')",
        (ville, nom, email, tel))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/delete-aeroport/<int:id>', methods=['POST', 'DELETE'])
def delete_aeroport(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    cursor.execute(f"DELETE FROM Aeroport WHERE IDAeroport = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/modifier-aeroport/<int:id>', methods=['GET'])
def open_edit_aeroport(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT IDPays, Nom FROM Pays")
    pys = cursor.fetchall()
    cursor.execute("SELECT IDVille, Nom, IDPays FROM Ville")
    vls = cursor.fetchall()
    cursor.execute(
        f"SELECT A.Nom, P.IDPays, V.IDVille, Email, Tel, A.IDAeroport FROM Aeroport A, Ville V , Pays P WHERE A.IDVille = V.IDVille AND V.IDPays = P.IDPays AND A.IDAeroport = {id}")
    data = cursor.fetchone()
    cursor.close()
    mydb.close()
    return render_template('edit_aeroport.html', data=data, pys=pys, vls=vls, user=session['user_admin'])


@app.route('/edit-aeroport/<int:id>', methods=['PUT'])
def edit_aeroport(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')
    tel = data.get('tel')
    ville = data.get('ville')
    cursor.execute("UPDATE Aeroport SET  IDVille=%s, Nom=%s, Email=%s, Tel=%s WHERE IDAeroport=%s",
                   (ville, nom, email, tel, id))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/ajouter-vol', methods=['GET'])
def ajouter_vol():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT IDAeroport, Nom, IDVille FROM Aeroport")
    arpts = cursor.fetchall()
    cursor.execute("SELECT IDCompagnie, Nom FROM Compagnie")
    cmps = cursor.fetchall()
    cursor.execute("SELECT IDPays, Nom FROM Pays")
    pys = cursor.fetchall()
    cursor.execute("SELECT IDVille, Nom, IDPays FROM Ville")
    vls = cursor.fetchall()
    cursor.close()
    mydb.close()
    return render_template('ajout_vol.html', arpts=arpts, cmps=cmps, pys=pys, vls=vls, user=session['user_admin'])


@app.route('/find-aeroport-par-ville/<int:id>', methods=['GET'])
def find_aeroport_par_ville(id):
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT IDAeroport, Nom, IDVille FROM Aeroport WHERE IDVille = {id}")
    arpts = cursor.fetchall()
    cursor.close()
    mydb.close()
    data = {
        'liste': arpts
    }
    return jsonify(data)


@app.route('/create-vol', methods=['POST'])
def create_vol():
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    print("aaaaaaaaaa", session['user_admin'])
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    depart = data.get('dep')
    arrive = data.get('arr')
    date = data.get('date')
    hdep = data.get('hdep')
    harr = data.get('harr')
    nb = data.get('nb')
    prix = data.get('prix')
    cursor.execute(
        "INSERT INTO Vols (IDVol, IDAeroportDepart, IDAeroportArrive, Date, HeurD, HeurA, Nb_Places, PrixPlace, IDCompagnie) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)",
        (depart, arrive, date, hdep, harr, nb, prix, session['user_admin'][6]))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/delete-vol/<int:id>', methods=['POST', 'DELETE'])
def delete_vol(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM Vols WHERE IDVol = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/modifier-vol/<int:id>', methods=['GET'])
def open_edit_vol(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute("SELECT IDAeroport, Nom, IDVille FROM Aeroport")
    arpts = cursor.fetchall()
    cursor.execute("SELECT IDCompagnie, Nom FROM Compagnie")
    cmps = cursor.fetchall()
    cursor.execute("SELECT IDPays, Nom FROM Pays")
    pys = cursor.fetchall()
    cursor.execute("SELECT IDVille, Nom, IDPays FROM Ville")
    vls = cursor.fetchall()
    cursor.execute(f"SELECT * FROM Vols WHERE IDVol = {id}")
    data = cursor.fetchone()
    cursor.execute("SELECT V.IDVille, V.IDPays FROM Aeroport A, Ville V WHERE IDAeroport = %s AND V.IDVille=A.IDVille",
                   (data[1],))
    vdc = cursor.fetchone()
    cursor.execute("SELECT V.IDVille, V.IDPays FROM Aeroport A, Ville V WHERE IDAeroport = %s AND V.IDVille=A.IDVille",
                   (data[2],))
    vac = cursor.fetchone()
    cursor.close()
    mydb.close()
    return render_template('edit_vol.html', data=data, arpts=arpts, cmps=cmps, pys=pys, vls=vls, vdc=vdc, vac=vac,
                           id=id, user=session['user_admin'])


@app.route('/edit-vol/<int:id>', methods=['POST'])
def edit_vol(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    print("aaaaaaaaaa", session['user_admin'])
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    depart = data.get('dep')
    arrive = data.get('arr')
    date = data.get('date')
    hdep = data.get('hdep')
    harr = data.get('harr')
    nb = data.get('nb')
    prix = data.get('prix')
    cursor.execute(
        "UPDATE Vols SET IDAeroportDepart=%s, IDAeroportArrive=%s, Date=%s, HeurD=%s, HeurA=%s, Nb_Places=%s, PrixPlace=%s WHERE IDVol=%s",
        (depart, arrive, date, hdep, harr, nb, prix, id))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/edit-profile-admin/<int:id>', methods=['POST'])
def edit_profile_admin(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    nom = data.get('nom')
    email = data.get('email')
    prenom = data.get('prenom')
    cin = data.get('cin')
    cursor.execute("UPDATE Administrateur SET Nom=%s, Prenom=%s, Email=%s, CIN=%s WHERE IDAdministrateur=%s",
                   (nom, prenom, email, cin, id))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'ok'})


@app.route('/upload-image/<int:id>', methods=['POST'])
def upload_image(id):
    if 'user_admin' not in session or not session['user_admin']:
        return redirect(url_for('login_page_admin'))
    file = request.files['file']
    print('file', file)
    file.save(f'static/images/users/{id}.jpeg')
    return jsonify({'status': 'ok'})


def send_email(s, mail, text):
    config = configparser.ConfigParser()
    config.read('config_file.ini')
    outlook_email = config.get('Mail Sender', 'adresse')
    app_password = config.get('Mail Sender', 'mdp')
    recipient_email = mail
    message = MIMEMultipart()
    message["From"] = outlook_email
    message["To"] = recipient_email
    message["Subject"] = s
    body = text
    message.attach(MIMEText(body, "plain"))
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(outlook_email, app_password)
        server.sendmail(outlook_email, recipient_email, message.as_string())


@app.route('/send_reset_password', methods=['POST'])
def send_reset_password():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    email = data.get('email')
    cursor.execute(f"SELECT * FROM Administrateur WHERE Email = '{email}'")
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    print(user)
    if user is None:
        return jsonify({'status': 'error'})
    send_email("Réinitialisation de mot de passe", email,
               f"Bonjour {user[1]} {user[2]},\n\nPour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant: http://192.168.1.16:8086/reset_password_config/{user[0]}\n\nCordialement.")
    return jsonify({'status': 'success'})


@app.route('/reset_password_config/<int:id>', methods=['GET'])
def reset_password_config(id):
    return render_template('reset_password.html', id=id)


@app.route('/action_reset_password/<int:id>', methods=['PUT'])
def action_reset_password(id):
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    mdp = data.get('mdp')
    cursor.execute(f"UPDATE Administrateur SET MDP = '{mdp}' WHERE IDAdministrateur = {id}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'success'})


@app.route('/welcome', methods=['GET'])
def welcome_page():
    if 'user_client' not in session or not session['user_client']:
        session['user_client'] = None
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM Pays")
    pays = cursor.fetchall()
    cursor.execute("SELECT * FROM Classe")
    cls = cursor.fetchall()
    cursor.execute(f"SELECT VL.IDVol, C.Nom , VL.PrixPlace, V.IDPays FROM Vols VL, Compagnie C, Ville V, Aeroport A WHERE A.IDVille=V.IDVille AND A.IDAeroport=VL.IDAeroportArrive AND C.IDCompagnie=VL.IDCompagnie ORDER BY (VL.IDVol) DESC LIMIT 6 ")
    data = cursor.fetchall()
    cursor.close()
    mydb.close()
    print(session['user_client'])
    return render_template('index.html', pays=pays, cls=cls, data=data, client=session['user_client'])


@app.route('/chercher-vols-client', methods=['POST'])
def chercher_vols_client():
    data = request.get_json()
    paysActuel = data.get('paysActuel')
    dateDepart = data.get('dateDepart')
    paysDestination = data.get('paysDestination')
    print(paysActuel, dateDepart)
    mydb = findConnection()
    cursor = mydb.cursor()
    req = (
        f"SELECT VL.IDVol, C.Nom , VL.PrixPlace FROM Vols VL, Compagnie C WHERE VL.IDAeroportArrive IN (SELECT IDAeroport FROM Aeroport A, Ville V WHERE A.IDVille=V.IDVille AND V.IDPays='{paysDestination}') AND VL.IDAeroportDepart IN (SELECT IDAeroport FROM Aeroport A, Ville V WHERE A.IDVille=V.IDVille AND C.IDCompagnie=VL.IDCompagnie AND V.IDPays='{paysActuel}') AND `Date`='{dateDepart}' ")
    print(req)
    cursor.execute(req)
    resultat = cursor.fetchall()
    cursor.execute("SELECT * FROM Pays WHERE IDPays = %s", (paysDestination,))
    res = cursor.fetchone()
    cursor.close()
    mydb.close()
    data = {
        'status': 'success',
        'data': resultat,
        'res': res
    }
    print(data)
    return jsonify(data)


@app.route('/details-reservation/<int:id>', methods=['GET'])
def details_reservation(id):
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(
        f"SELECT `Date`, HeurD, HeurA, C.NOM, PrixPlace, V.NB_Places, IDAeroportDepart, IDAeroportArrive FROM Vols V, Compagnie C WHERE V.IDCompagnie=C.IDCompagnie AND IDVol = {id}")
    data = cursor.fetchone()
    cursor.execute(f"SELECT COUNT(T.NbrPlace) FROM Ticket T WHERE T.IDVol = {id}")
    nbr = cursor.fetchone()
    x = data[5] - nbr[0]
    cursor.execute(
        f"SELECT A.Nom, V.Nom, P.Nom FROM Aeroport A, Ville V, Pays P WHERE A.IDAeroport = {data[6]} AND A.IDVille = V.IDVille AND V.IDPays = P.IDPays")
    dep = cursor.fetchone()
    cursor.execute(
        f"SELECT A.Nom, V.Nom, P.Nom, P.IDPays FROM Aeroport A, Ville V, Pays P WHERE A.IDAeroport = {data[7]} AND A.IDVille = V.IDVille AND V.IDPays = P.IDPays")
    arr = cursor.fetchone()
    cursor.close()
    mydb.close()
    return render_template("details_page.html", id=id, data=data, nbr=x, arr=arr, dep=dep)


@app.route('/login-client', methods=['GET'])
def login_client():
    if 'user_client' in session or session['user_client']:
        session['user_client'] = None
    return render_template('login.html')


@app.route('/sign-up-client', methods=['GET'])
def sign_up_client():
    return render_template('registration.html')


@app.route('/login-client-action', methods=['POST'])
def login_client_action():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    email = data.get('email')
    mdp = data.get('mdp')
    cursor.execute(f"SELECT * FROM Passager WHERE Mail = '{email}' AND MDP = '{mdp}'")
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    if user is None:
        return jsonify({'status': 'error'})
    session['user_client'] = user
    return jsonify({'status': 'success', 'user': user})


@app.route('/sign-up-client-action', methods=['POST'])
def sign_up_client_action():
    mydb = findConnection()
    cursor = mydb.cursor()
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    tel = data.get('tel')
    cin = data.get('cin')
    mdp = data.get('mdp')
    passeport = data.get('passeport')
    genre = data.get('genre')
    nationalite = data.get('nationalite')
    adresse = data.get('adresse')
    cursor.execute(
        "INSERT INTO Passager (IDPassager, Nom, Prenom, Mail, Tel, CIN, MDP, Passeport, Genre, Nationalite, Adresse) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (nom, prenom, email, tel, cin, mdp, passeport, genre, nationalite, adresse))
    mydb.commit()
    cursor.close()
    mydb.close()
    return jsonify({'status': 'success'})


@app.route('/action-reservation', methods=['POST'])
def action_reservation():
    data = request.get_json()
    id = data.get('id')
    nbr = data.get('nbr')
    session['reservation_en_cours'] = {
        'id': id,
        'nbr': nbr
    }
    return jsonify({'status': 'success'})


@app.route('/payer-reservation', methods=['GET'])
def payer_reservation():
    if 'reservation_en_cours' not in session or not session['reservation_en_cours']:
        return redirect(url_for('welcome_page'))
    if 'user_client' not in session or not session['user_client']:
        return redirect(url_for('welcome_page'))
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(f"SELECT PrixPlace FROM Vols WHERE IDVol = {session['reservation_en_cours']['id']}")
    prix = cursor.fetchone()
    print(prix, session['reservation_en_cours']['nbr'])
    cursor.close()
    mydb.close()
    return render_template('payment_page.html', nbr=int(session['reservation_en_cours']['nbr']), prix=prix[0],
                           prixT=float(prix[0]) * int(session['reservation_en_cours']['nbr']))


@app.route('/payer-reservation-action', methods=['POST'])
def payer_reservation_action():
    mydb = findConnection()
    cursor = mydb.cursor()
    cursor.execute(
        "INSERT INTO Ticket (IDTicket, IDVol, IDPassager, NbrPlace, `Type`) VALUES (NULL, %s, %s, %s, %s)",
        (session['reservation_en_cours']['id'], session['user_client'][0], session['reservation_en_cours']['nbr'], 1))
    mydb.commit()
    lid = cursor.lastrowid
    cursor.close()
    mydb.close()
    session.pop('reservation_en_cours', None)
    send_email("Confirmation de réservation", session['user_client'][3],
               "Bonjour,\n\nVotre réservation a été confirmée avec succès.\n\nCordialement.")
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(port=8086, debug=True, host="0.0.0.0")
