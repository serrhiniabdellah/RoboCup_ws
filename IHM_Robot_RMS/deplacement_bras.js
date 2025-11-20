//Lien du serveur 
var ros = new ROSLIB.Ros({

      url : 'ws://192.168.137.82:9090'

    });
    
    
// Création du Topic
var topic = new ROSLIB.Topic({
  ros: ros,
  name: '/data',
  messageType: 'std_msgs/Float64MultiArray'
});

// État global pour les valeurs des sliders
var sliderValues = {
  ax7: 0,
  ax6: 0,
  ax5: 0,
  ax4: 0,
  ax3: 0,
  ax2: 0, 
  ax1 : 0,
  reboot : 0
};

// Fonction pour mettre à jour l'état des sliders et envoyer le message
function updateSlidersAndSend() {
  var message = new ROSLIB.Message({
    layout: {
      dim: [],
      data_offset: 0,
    },
    data: [
      sliderValues.ax7,
      sliderValues.ax6,
      sliderValues.ax5,
      sliderValues.ax4,
      sliderValues.ax3,
      sliderValues.ax2, 
      sliderValues.ax1, 
      sliderValues.reboot
    ]
  });

  topic.publish(message);
  console.log('Valeur des sliders envoyée: ', sliderValues);
}

// Fonctions pour chaque déplacement ou rotation
function axe1() {
  sliderValues.ax1 = parseFloat(document.getElementById('axe1').value);
  updateSlidersAndSend();
}

function axe2() {
  sliderValues.ax2 = parseFloat(document.getElementById('axe2').value);
  updateSlidersAndSend();
}

function axe3() {
  sliderValues.ax3 = parseFloat(document.getElementById('axe3').value);
  updateSlidersAndSend();
}

function axe4() {
  sliderValues.ax4 = parseFloat(document.getElementById('axe4').value);
  updateSlidersAndSend();
}

function axe5() {
  sliderValues.ax5 = parseFloat(document.getElementById('axe5').value);
  updateSlidersAndSend();
}

function axe6() {
  sliderValues.ax6 = parseFloat(document.getElementById('axe6').value);
  updateSlidersAndSend();
}

function axe7() {
  sliderValues.ax7 = parseFloat(document.getElementById('axe7').value);
  updateSlidersAndSend();
}

function reboot() {
  sliderValues.reboot = 1;
  updateSlidersAndSend();
  sliderValues.reboot = 0; // Remettre à zéro après envoi si nécessaire
}

function rangement() {
  sliderValues.ax1 = 1;
  sliderValues.ax2 = 1;
  sliderValues.ax3 = 1;
  sliderValues.ax4 = 1;
  sliderValues.ax5 = 1;
  sliderValues.ax6 = 1;
  sliderValues.ax7 = 1;
  updateSlidersAndSend();
}

function deploiement() {
  sliderValues.ax1 = 0;
  sliderValues.ax2 = 0;
  sliderValues.ax3 = 0;
  sliderValues.ax4 = 0;
  sliderValues.ax5 = 0;
  sliderValues.ax6 = 0;
  sliderValues.ax7 = 0;
  updateSlidersAndSend();
}


// Cette fonction ajuste la valeur du slider en fonction des bouttons + et -.
function changeSliderValue(sliderId, increment) {
    var slider = document.getElementById(sliderId);
    var currentValue = parseFloat(slider.value);
    var newValue = currentValue + increment;

    slider.value = newValue; // Met à jour la valeur du slider
    axe1();
    axe2();
    axe3();
    axe4();
    axe5();
    axe6();
    axe7();
}

