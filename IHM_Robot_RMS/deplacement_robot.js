 //Lien du serveur 
var ros = new ROSLIB.Ros({

      url : 'ws://192.168.137.82:9090'

    });

//Declaration du Topic 1
    var topic1 = new ROSLIB.Topic({

      ros : ros,

      name: '/consigne',
  messageType: 'std_msgs/Int16MultiArray'

    });
//Envoi du Topic 1
    function deplacement_avant() {

      var message = new ROSLIB.Message({
    //data: [127, 0, 0, 0, 0, 0, 0, 0, 0]
        data: [-127, 0, 0, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

//Envoi du Topic 2
    function deplacement_arriere() {

      var message = new ROSLIB.Message({
    data: [-127, 0, 0, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }

//Envoi du Topic 3
    function deplacement_droite() {

      var message = new ROSLIB.Message({
    data: [0, -127, 0, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

//Envoi du Topic 4
    function deplacement_gauche() {

      var message = new ROSLIB.Message({
    data: [0, 127, 0, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

//Envoi du Topic 5
    function stop() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }


//-------------------Topics flippers (Valeurs a changer en fonction de l'affectation de la manette)---------------------------------------
//Envoi du Topic 6
    function flipper_hautAVG() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 0, 0, 127, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

//Envoi du Topic 7
    function flipper_basAVG() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 0, 127, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

    //Envoi du Topic 8
    function flipper_hautAVD() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 127, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }

//Envoi du Topic 9
    function flipper_basAVD() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 127, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }

    //Envoi du Topic 10
    function flipper_hautAR() {

      var message = new ROSLIB.Message({
    data: [0, 0, -127, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }

//Envoi du Topic 11
    function flipper_basAR() {

      var message = new ROSLIB.Message({
    data: [0, 0, 127, 0, 0, 0, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }
    
    //Envoi du Topic Diff
    function flipper_haut_AV() {

     var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 127, 0, 127, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }
    
    function flipper_bas_AV() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 127, 0, 127, 0, 0, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');
    }


   
//-----------------------Topics controle de la camera--------------------------------------------------------------------------------------------


//Envoi du Topic 14
    function camera_haut() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 0, 0, 0, 127, 0]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }

//Envoi du Topic 15
    function camera_bas() {

      var message = new ROSLIB.Message({
    data: [0, 0, 0, 0, 0, 0, 0, 0, 127]
  });
  topic1.publish(message);
  console.log('Message publié sur le topic /consigne');

    }



//---------------------------Subscribers ROS-----------------------------------------------------------------------------------------------------------------------


//Definition du Subscriber 1
    var subscriber1 = new ROSLIB.Topic({

      ros : ros,

      name : '/vitesse1',

      messageType : 'std_msgs/Int32'

    });

//Affiche sur la page web du message present dans le Subscriber 1
    subscriber1.subscribe(function(message) {

      console.log('Message reçu :', message.data);
      document.getElementById('vitesse1').innerHTML = message.data;

    });

//Definition du Subscriber 2
    var subscriber2 = new ROSLIB.Topic({

      ros : ros,

      name : '/vitesse2',

      messageType : 'std_msgs/Int32'

    });

//Affiche sur la page web du message present dans le Subscriber 1
    subscriber1.subscribe(function(message) {

      console.log('Message reçu :', message.data);
      document.getElementById('vitesse2').innerHTML = message.data;

    });

//Definition du Subscriber 3
    var subscriber3 = new ROSLIB.Topic({

      ros : ros,

      name : '/inclinaison1',

      messageType : 'std_msgs/Int32'

    });

//Affiche sur la page web du message present dans le Subscriber 1
    subscriber1.subscribe(function(message) {

      console.log('Message reçu :', message.data);
      document.getElementById('inclinaison1').innerHTML = message.data;

    });

//Definition du Subscriber 4
    var subscriber4 = new ROSLIB.Topic({

      ros : ros,

      name : '/inclinaison2',

      messageType : 'std_msgs/Int32'

    });

//Affiche sur la page web du message present dans le Subscriber 1
    subscriber1.subscribe(function(message) {

      console.log('Message reçu :', message.data);
      document.getElementById('inclinaison2').innerHTML = message.data;

    });

    //Definition du Subscriber 5
    var subscriber5 = new ROSLIB.Topic({

      ros : ros,

      name : '/boussole',

      messageType : 'std_msgs/Int32'

    });

//Affiche sur la page web du message present dans le Subscriber 1
    subscriber1.subscribe(function(message) {

      console.log('Message reçu :', message.data);
      document.getElementById('boussole').innerHTML = message.data;

    });

//------------------------------------- Subscribers flippers ----------------------------------------------------------------
//Subscriber codeur 1
    let codeur1 = 0.0; // Initialisation de la valeur de position

    var posSubscriber = new ROSLIB.Topic({
        ros: ros,
        name: '/codeur1', // Nom du topic
        messageType: 'std_msgs/Float32'
    });

    posSubscriber.subscribe(function(message) {
        codeur1 = message.data; // Mise à jour de codeur1 à partir du message reçu
    });


//Subscriber codeur 2
    let codeur2 = 0.0; // Initialisation de la valeur de position

    var posSubscriber = new ROSLIB.Topic({
        ros: ros,
        name: '/codeur2', // Nom du topic
        messageType: 'std_msgs/Float32'
    });

    posSubscriber.subscribe(function(message) {
        codeur2 = message.data; // Mise à jour de codeur2 à partir du message reçu
    });


    //Subscriber codeur 3
    let codeur3 = 0.0; // Initialisation de la valeur de position

    var posSubscriber = new ROSLIB.Topic({
        ros: ros,
        name: '/codeur3', // Nom du topic
        messageType: 'std_msgs/Float32'
    });

    posSubscriber.subscribe(function(message) {
        codeur3 = message.data; // Mise à jour de codeur3 à partir du message reçu
    });

//-----------------------Affectation des actions au clavier--------------------------------------------------------------------------------------------------------------------

let lastSentTime = 0;
const sendInterval = 200; // temps en millisecondes, ici 1 seconde


let modeMontee = true; // true pour montée, false pour descente
let modeDiff = false; // true pour montée, false pour descente

function toggleDifferentialMode() {
  modeDiff = !modeDiff;
  console.log('Mode', modeDiff ? 'Diff' : 'NonDiff');
}

function Codeur() {

  const N = 360; // Nombre de valeurs pour un tour complet de moteur (modulo)
  const targetMin = 0; // Position minimale de la plage cible
  const targetMax = 5; // Position maximale de la plage cible

  //Codeur 1 
  while ((codeur1 % N) < (targetMin % N) || (codeur1 % N) > (targetMax % N)) 
  {
    flipper_hautAVG();
  }

  //Codeur 2 
  while ((codeur2 % N) < (targetMin % N) || (codeur2 % N) > (targetMax % N)) 
  {
    flipper_hautAVD();
  }

  //Codeur 3 
  while ((codeur3 % N) < (targetMin % N) || (codeur3 % N) > (targetMax % N)) 
  {
    flipper_hautAR();
  }

}

document.addEventListener('keydown', function(event) {
switch(event.key) {

    case 'z':
    case 'Z':
        const currentTime = new Date().getTime();
    if (currentTime - lastSentTime > sendInterval) {
        deplacement_avant();
        lastSentTime = currentTime;
    }
        break;
        
    case 's':
    case 'S':
        deplacement_arriere();
        break;
        
    case 'q':
    case 'Q':
        deplacement_gauche();
        break;
        
    case 'd':
    case 'D':
        deplacement_droite();
        break;
        
    case 'a':
    case 'A':
        if (modeDiff) 
        {
            flipper_haut_AV();
        }    
        else 
        {
            flipper_hautAVG();
        }
        break;

    case 'w':
    case 'W':
        if (modeDiff) 
        {
            flipper_bas_AV();
        }    
        else 
        {
            flipper_basAVG();
        }
        break;
        
    case 'e':
    case 'E':
        flipper_hautAVD();
        break;

    case 'c' :
    case 'C':
        flipper_basAVD();
        break;

    case 'r' :
    case 'R':
        flipper_hautAR();
        break;

    case 'v' :
    case 'V':
        flipper_basAR();
        break;
        
    case 'p' :
    case 'P': 
        camera_haut();
        break;
        
    case 'm' :
    case 'M':
        camera_bas();
        break;
        
        
    case ' ':
        stop();
        break;
        
    default:
        stop();
        break;
}
});

document.addEventListener('keyup', function(event) {
// Permet d'arreter le robot quand on relache la touche
if (['z', 's', 'q', 'd', 'a', 'w', 'e', 'c', 'r', 'v', 'Control', ' ', 'p', 'm', 'Z', 'S', 'Q', 'D', 'A', 'W', 'E', 'C', 'R', 'V', 'P', 'M'].includes(event.key)) {
    stop();
    console.log('Le robot s\'arrête');
}
});






