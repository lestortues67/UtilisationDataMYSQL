// 14/09/2023
// Dossier : c:/javascript/
// Fichier : UtilisationDataMYSQL
// Objet   : Supprimer dans MYSQL 
// Mot clé : MYSQL

//var myblogModal = new bootstrap.Modal(document.getElementById("blogModal"), {});


function eventManager(){
    //window.location.reload()
    console.log("je suis dans eventManager")

    setTimeout(function() {
        location.reload();
        }, 10); // Actualise la page après 1 seconde (1000 millisecondes)
    console.log("j'ai actualisé")
}
   










var btn = document.getElementById("btnSave")
btn.addEventListener('click',eventManager,false)

