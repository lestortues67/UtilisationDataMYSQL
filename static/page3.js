// 14/09/2023
// Dossier : c:/javascript/
// Fichier : UtilisationDataMYSQL
// Objet   : Supprimer dans MYSQL 
// Mot clé : MYSQL

var myblogModal = new bootstrap.Modal(document.getElementById("blogModal"), {});


function eventManager(p_event){
    if(p_event.target.id=="btnDelete"){
        console.log("p_event.target : ",p_event.target);    
        var i =  p_event.target.dataset.id
        //La requete fetch va permettre à supprimer une ligne dans la table 
        fetch("/effacer/"+i)
            .then(response => {
            if (!response.ok) {
              throw new Error('Erreur HTTP : ' + response.status);
            }
            return response.json(); // Pour récupérer le contenu brut
            })
            .then(data => {

            console.log(data);
            //actualiser la page 
            window.location.reload();
            })
            .catch(error => {
            console.error('Erreur : ' + error);
            });
    }
    //Modifier une ligne dans la table
    if(p_event.target.id=="btnEdit"){
        //La modal va s'ouvrir 
        myblogModal.show()
        document.getElementById("texteDescription").value = p_event.target.dataset.nom 
        console.log("btnEdit");   
        document.getElementById("btnEnregistrer").dataset.id=  p_event.target.dataset.id
    }

   
    //Les modifications vont etre enregistrées
    if (p_event.target.id == "btnEnregistrer"){
        console.log("btnEnregistrer - Modal")
        var nom = document.getElementById("texteDescription").value
        var myId = document.getElementById("texteDescription")    
        myId.dataset.id = parseInt(p_event.target.dataset.id);
        console.log("nom:",nom)
        console.log("ID:",myId.dataset.id)

        let reponseServeur = ""
        let url = "/modifier" 


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
          // Fermer la modal 
          myblogModal.hide()
          //Actualiser la page
          window.location.reload()
        }
        fetchPost({'id': myId.dataset.id, 'nom': nom})
    }
}









var mesBtnDelete = document.getElementsByClassName("btn")
for (var indexBtn = 0; indexBtn < mesBtnDelete.length; indexBtn++) {
    var btn = mesBtnDelete[indexBtn]
    btn.addEventListener('click',eventManager,false)
}
