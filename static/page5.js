// 14/09/2023
// Dossier : c:/javascript/
// Fichier : UtilisationDataMYSQL
// Objet   : Supprimer dans MYSQL 
// Mot clé : MYSQL

//var myblogModal = new bootstrap.Modal(document.getElementById("blogModal"), {});


function fetchPost(p_url, p_formdata) {
    const monObjetRequest = {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'tintin':'milou',
            'apiKey':1234 },
        body: JSON.stringify(p_formdata)
    };
    fetch(p_url, monObjetRequest)
        .then(function(responseObject){
            return responseObject.json()
        })
        .then(function(jsonData){
            let d = jsonData
            console.log("Voici la data json : ",jsonData)
        });
    };


function envoyer(){
    var f = new FormData (document.getElementById("monForm"))
    console.log("f : ",f)
    fetchPost("http://localhost:5000/fd", f) 
    document.getElementById("client_id").value = f["nom"]
}

//envoyer()

var dict = []
function test02(){
    var f = new FormData (document.getElementById("monForm"))
    console.log("f : ",f)
    fetchPost("http://localhost:5000/fd", f) 
    dict.push(f)
    document.getElementById("client_id").value = f["nom"]
}

// const formData = new FormData(formulaire);
 const monObjetRequest = {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'tintin':'milou',
            'apiKey':1234 },
        body: JSON.stringify({ title: 'React POST Request Example', name : 'Doriath' })
    };

///////////////////////////////////////////////////

var dict1 = [];
//La requete fetch permet d'affiché les id de la table "clients_pro"
fetch("http://localhost:5000/id_clients")
        .then(function(responseObject){
            return responseObject.json()
        })
        .then(function(jsonData){
            let d = jsonData
            console.log("Voici la data json : ",jsonData)
            dict1.push(d)
            document.getElementById("client_id").innerHTML = dict1.toString()
            document.getElementById("client_id_article").innerHTML = dict1.toString()
        });
    ;


var dict2 = [];
//La requete fetch permet d'affiché les id de la table "commandespro"
fetch("http://localhost:5000/id_commandes")
        .then(function(responseObject){
            return responseObject.json()
        })
        .then(function(jsonData){
            let d = jsonData
            console.log("Voici la data json : ",jsonData)
            dict2.push(d)
            document.getElementById("commande_id").innerHTML = dict2.toString()
        });
    ;



let reponseServeur = ""
let url = "/ajouterarticle"

async function fetchPost(p_contenu){
  let response = await fetch(url,{
    method:"POST",
    headers: {
        "Content-Type": "application/json",
        "tintin":"milou"
      },
      body: JSON.stringify(p_contenu), 
      // ici le type de données doit être identique à la ligne 8
  });
  reponseServeur = await response.json();
  console.log("N°2 Voici le json après le code : ",reponseServeur)  
}

fetchPost({'contenu': '<p>texte 1 </p><p>texte 2<br></p>', 'titre': 'Le titre de la page'})