function navigate_aeroport() {
    window.location.href = '/aeroport';
}

function navigate_passager() {
    window.location.href = '/passager';
}

function navigate_vols() {
    window.location.href = '/';
}

function navigate_login_admin() {
    window.location.href = '/login_page_admin';
}

function navigate_profile_content(id) {
    window.location.href = '/profile/' + id;
}

function navigate_to_sign_up() {
    window.location.href = '/sign-up-client';

}

function navigate_to_login() {
    window.location.href = '/login-client';
}

function navigate_to_payement() {
    window.location.href = '/payer-reservation';

}

function requestLogin() {
    email = document.getElementById('email').value;
    mdp = document.getElementById('password').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/login_admin_request', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                window.location.href = '/';
            } else {
                alert('Email ou mot de passe incorrect');
            }
        }
    };
    xhr.send(JSON.stringify({email: email, mdp: mdp}));
}

function findPassagerNom() {
    key = document.getElementById('cherche-passager-nom').value;


    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-passager-nom', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_passager(response.liste)

        }
    };
    xhr.send(JSON.stringify({key: key}));
}

function findPassagerCIN() {
    key = document.getElementById('cherche-passager-cin').value;


    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-passager-cin', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_passager(response.liste)

        }
    };
    xhr.send(JSON.stringify({key: key}));
}

function load_given_data_passager(data) {
    var table = document.getElementById('dataTable-content');
    table.innerHTML = ` <thead>
                                        <tr data-aos="fade-up" data-aos-once="true">
                                            <th>Nom</th>
                                            <th>CIN</th>
                                            <th>Passport</th>
                                            <th>Adresse</th>
                                            <th>Nationalité</th>
                                            <th>Numéro Téléphone</th>
                                            <th>Genre</th>
                                        </tr>
                                    </thead>`;
    data.forEach(function (element) {
        table.innerHTML += ` <tbody>
                                <tr data-aos="fade-up" data-aos-once="true">
                                    <td> ${element[1]} ${element[2]} </td>
                                    <td> ${element[4]} </td>
                                    <td> ${element[6]} </td>
                                    <td> ${element[9]} </td>
                                    <td> ${element[8]} </td>
                                    <td> ${element[3]}</td>
                                    <td> ${element[7]}</td>
                                    <td></td>
                                </tr>
                            </tbody>`;
    });

}

function findAeroport() {
    key = document.getElementById('cherche-aeroport').value;


    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-aeroport', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_aeroport(response.liste)

        }
    };
    xhr.send(JSON.stringify({key: key}));
}

function load_given_data_aeroport(data) {
    var table = document.getElementById('dataTable-content');
    table.innerHTML = ` <thead>
                                        <tr data-aos="fade-up" data-aos-once="true">
                                            <th>Nom</th>
                                            <th>Pays</th>
                                            <th>Ville</th>
                                            <th>Email</th>
                                            <th>Téléphone</th>
                                            <th>Modifier</th>
                                            <th>Supprimer</th>
                                        </tr>
                                    </thead>`;
    data.forEach(function (element) {
        table.innerHTML += ` <tbody>
                                <tr data-aos="fade-up" data-aos-once="true">
                                    <td> ${element[0]} </td>
                                    <td> ${element[1]} </td>
                                    <td> ${element[2]} </td>
                                    <td> ${element[3]} </td>
                                    <td> ${element[4]} </td>
                                    <td><button class="btn btn-success" onclick="openModify(${element[5]})" >Modifier</button></td>
                                    <td><button class="btn btn-danger" onclick="openDelete(${element[5]})">Supprimer</button></td>
                                </tr>
                            </tbody>`;
    });
}

function findVol() {
    keyD = document.getElementById('cherche-vol-dep').value;
    keyA = document.getElementById('cherche-vol-arr').value;
    console.log('dep : ' + keyD + ' arr : ' + keyA)

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-vol', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_vol(response.liste, response.user)

        }
    };
    xhr.send(JSON.stringify({keyD: keyD, keyA: keyA}));

}

function findVolArr() {
    key = document.getElementById('cherche-vol-arr').value;
    console.log('arr : ' + key)
}

function load_given_data_vol(data, usr) {
    var table = document.getElementById('dataTable-content');
    table.innerHTML = ` <thead>
                                        <tr data-aos="fade-up" data-aos-once="true">
                                            <th>ID VOL</th>
                                            <th>Aéroport de départ</th>
                                            <th>Aéroport d'arrivé</th>
                                            <th>Date</th>
                                            <th>Heur de départ</th>
                                            <th>Heur d'arrivé</th>
                                            <th>Compagnie</th>
                                            <th>Nombre de places</th>
                                            <th>Prix par place</th>
                                        </tr>
                                    </thead>`;

    data.forEach(function (element) {
        let ch = '';
        if (element[9] === usr[6]) {
            ch = `<td><button class="btn btn-success" onclick="openModifyVol(${element[0]})" >Modifier</button></td>
                  <td><button class="btn btn-danger" onclick="openDeleteVol(${element[0]})">Supprimer</button></td>`;
        }
        table.innerHTML += ` <tbody>
                                <tr data-aos="fade-up" data-aos-once="true">
                                    <td> ${element[0]} </td>
                                    <td> ${element[1]} </td>
                                    <td> ${element[2]} </td>
                                    <td> ${element[3]} </td>
                                    <td> ${element[4]} </td>
                                    <td> ${element[5]} </td>
                                    <td> ${element[6]} </td>
                                    <td> ${element[7]} </td>
                                    <td> ${element[8]} </td>
                                    ${ch}
                                    <td></td>
                                </tr>
                            </tbody>`;
    });

}

function changer_ville(p) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-ville-par-pays', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_ville(response.liste)

        }
    };
    xhr.send(JSON.stringify({key: p}));
}

function load_given_data_ville(data) {
    s = document.getElementById('ville-select-list');
    s.innerHTML = '';
    data.forEach(function (element) {
        s.innerHTML += `<option value="${element[0]}">${element[1]}</option>`;
    });
}

function changer_ville_vol(p, ch, ch1) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/find-ville-par-pays', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_ville_vol(response.liste, ch, ch1)

        }
    };
    xhr.send(JSON.stringify({key: p}));
}

function load_given_data_ville_vol(data, ch, ch1) {
    s = document.getElementById(ch);
    s.innerHTML = '';
    data.forEach(function (element) {
        s.innerHTML += `<option value="${element[0]}">${element[1]}</option>`;
    });
    changer_aeroport(data[0][0], ch1);
}

function changer_aeroport(p, ch) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/find-aeroport-par-ville/' + p, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            load_given_data_aeroport_vol(response.liste, ch)

        }
    };
    xhr.send(JSON.stringify({key: p}));
}

function load_given_data_aeroport_vol(data, ch) {
    s = document.getElementById(ch);
    s.innerHTML = '';
    data.forEach(function (element) {
        s.innerHTML += `<option value="${element[0]}">${element[1]}</option>`;
    });
}

function ajout_aeroport() {
    window.location.href = '/ajouter-aeroport';

}

function createAirport() {
    nom = document.getElementById('nom-aeroport').value;
    pays = document.getElementById('pays-aeroport').value;
    ville = document.getElementById('ville-select-list').value;
    email = document.getElementById('email-aeroport').value;
    tel = document.getElementById('tel-aeroport').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/create-aeroport', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = '/aeroport';
        }
    };
    xhr.send(JSON.stringify({nom: nom, pays: pays, ville: ville, email: email, tel: tel}));
}

function openDelete(id) {
    conf = confirm('Voulez-vous vraiment supprimer cet aeroport ?');
    if (conf) {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/delete-aeroport/' + id, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                window.location.href = '/aeroport';
            }
        };
        xhr.send(JSON.stringify({id: id}));
    }
}

function openModify(id) {
    window.location.href = '/modifier-aeroport/' + id;
}

function modifyAirport(id) {
    nom = document.getElementById('nom-aeroport').value;
    pays = document.getElementById('pays-aeroport').value;
    ville = document.getElementById('ville-select-list').value;
    email = document.getElementById('email-aeroport').value;
    tel = document.getElementById('tel-aeroport').value;


    var xhr = new XMLHttpRequest();
    xhr.open('PUT', '/edit-aeroport/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = '/aeroport';
        }
    };
    xhr.send(JSON.stringify({nom: nom, pays: pays, ville: ville, email: email, tel: tel}));
}

function openModifyVol(id) {
    window.location.href = '/modifier-vol/' + id;
}

function openDeleteVol(id) {
    conf = confirm('Voulez-vous vraiment supprimer ce vol ?');
    if (conf) {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/delete-vol/' + id, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                window.location.href = '/';
            }
        };
        xhr.send(JSON.stringify({id: id}));
    }
}

function ajout_vol() {
    window.location.href = '/ajouter-vol';
}

function createVol() {
    dep = document.getElementById('aeroport-dep').value;
    arr = document.getElementById('aeroport-arr').value;
    date = document.getElementById('date-vol').value;
    hdep = document.getElementById('hd-vol').value;
    harr = document.getElementById('ha-vol').value;
    nb = document.getElementById('nb-place-vol').value;
    prix = document.getElementById('prix-place-vol').value;

    if (dep === arr) {
        alert('L\'aéroport de départ doit être différent de l\'aéroport d\'arrivé');
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/create-vol', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = '/';
        }
    };
    xhr.send(JSON.stringify({dep: dep, arr: arr, date: date, hdep: hdep, harr: harr, nb: nb, prix: prix}));
}

function updateVol(id) {
    dep = document.getElementById('aeroport-dep').value;
    arr = document.getElementById('aeroport-arr').value;
    date = document.getElementById('date-vol').value;
    hdep = document.getElementById('hd-vol').value;
    harr = document.getElementById('ha-vol').value;
    nb = document.getElementById('nb-place-vol').value;
    prix = document.getElementById('prix-place-vol').value;

    if (dep === arr) {
        alert('L\'aéroport de départ doit être différent de l\'aéroport d\'arrivé');
        return;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit-vol/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = '/';
        }
    };
    xhr.send(JSON.stringify({dep: dep, arr: arr, date: date, hdep: hdep, harr: harr, nb: nb, prix: prix}));
}

function saveProfileAdmin(id) {
    nom = document.getElementById('nom').value;
    prenom = document.getElementById('prenom').value;
    email = document.getElementById('email').value;
    cin = document.getElementById('cin').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit-profile-admin/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            window.location.href = '/';
        }
    };
    xhr.send(JSON.stringify({nom: nom, prenom: prenom, email: email, cin: cin}));
}

function handleFile(id) {
    var file = document.getElementById('fileInput').files[0];
    if (!file) {
        alert('Veuillez choisir une image');
        return;
    }

    var formData = new FormData();
    formData.append('file', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/upload-image/' + id, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                window.location.href = '/';
            } else {
                alert('Error uploading file: ' + xhr.statusText);
            }
        }
    };
    xhr.send(formData);
}

function navigate_forgot_password() {
    window.location.href = '/forgot_password';
}

function send_email_mdp_forgot() {
    email = document.getElementById('frgt-email').value;
    console.log(email)
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/send_reset_password', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                alert('Un email a été envoyé à votre adresse email');
                window.location.href = '/';
            } else {
                alert('Email incorrect');
            }
        }
    };
    xhr.send(JSON.stringify({email: email}));
}

function action_reset(id) {
    mdp = document.getElementById('mdp').value;
    mdp1 = document.getElementById('cmdp').value;

    if (mdp !== mdp1) {
        alert('Les mots de passe ne correspondent pas');
        return;
    } else {
        var xhr = new XMLHttpRequest();
        xhr.open('PUT', '/action_reset_password/' + id, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    alert('Mot de passe changé avec succès');
                    window.location.href = '/';
                } else {
                    alert('Erreur');
                }
            }
        };
        xhr.send(JSON.stringify({mdp: mdp}));
    }
}


function chercher_vols_client() {
    console.log('eeeeeeeeee')
    paysActuel = document.getElementById('loacl-voyage').value;
    dateDepart = document.getElementById('depart-voyage').value;

    paysDestination = document.getElementById('destination-voyage').value;
    classe = document.getElementById('classe-voyage').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/chercher-vols-client', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {

                //window.location.href = '/';
                load_given_data_client_search(response.data, response.res)
            } else {
                alert('Erreur');
            }
        }
    };
    xhr.send(JSON.stringify({
        paysActuel: paysActuel,
        dateDepart: dateDepart,
        paysDestination: paysDestination,
        classe: classe
    }));
}

function load_given_data_client_search(data, r) {
    var search_container = document.getElementById('search-container');
    search_container.innerHTML = '';
    data.forEach(function (element) {

        search_container.innerHTML += `
                <div class="col-md-4 col-sm-6">
                            <div class="single-package-item">
                                <img src="./images/villes/1.jpg" alt="package-place">
                                <div class="single-package-item-txt">
                                    <h3>${r[1]} <span class="pull-right">${element[2]} TND</span></h3>
                                    <div class="packages-para">
                                        <p>
        \t\t\t\t\t\t\t\t\t\t\t<span>
        \t\t\t\t\t\t\t\t\t\t\t\t<i class="fa fa-angle-right"></i> ${element[1]}
        \t\t\t\t\t\t\t\t\t\t\t</span>
                                        </p>
                                    </div><!--/.packages-para-->
                                   
                                    <div class="about-btn">
                                        <button class="about-view packages-btn" onclick="open_details_result(${element[0]})">
                                            Voir détails
                                        </button>
                                    </div><!--/.about-btn-->
                                </div><!--/.single-package-item-txt-->
                            </div><!--/.single-package-item-->
        
                        </div>
            `;
    });

}

function open_details_result(id) {
    window.location.href = '/details-reservation/' + id;
}

function login_client_action() {
    email = document.getElementById('email').value;
    mdp = document.getElementById('password').value;

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/login-client-action', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.status === 'success') {
                    window.location.href = '/welcome';
                } else {
                    alert('Email ou mot de passe incorrect');
                }
            }
        };
        xhr.send(JSON.stringify({email: email, mdp: mdp}));
}

function action_reservation(id) {
    nbr = document.getElementById('nbr-place').value;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/action-reservation', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                //alert('Réservation effectuée avec succès');
                //window.location.href = '/welcome';
                navigate_to_payement();
            } else {
                alert('Erreur');
            }
        }
    };
    xhr.send(JSON.stringify({nbr: nbr, id: id}));
}

function proceed_reservation() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/payer-reservation-action', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.status === 'success') {
                alert('Un Email a été envoyé à votre adresse email');
                window.location.href = '/welcome';
            } else {
                alert('Erreur');
            }
        }
    };
    xhr.send();
}