// =================== Connexion ROS ===================
var ROS_URL = localStorage.getItem('ros_url') || 'ws://192.168.137.82:9090';

var ros = new ROSLIB.Ros({ url: ROS_URL });

ros.on('connection', function () {
  console.log('[LIDAR] Connecté au serveur ROS.');
  var status = document.getElementById('ros-status');
  if (status) { status.textContent = '🟢 Connecté'; status.style.color = '#4caf50'; }
});

ros.on('error', function (error) {
  console.log('[LIDAR] Erreur de connexion:', error);
  var status = document.getElementById('ros-status');
  if (status) { status.textContent = '🔴 Déconnecté'; status.style.color = '#f44336'; }
});

ros.on('close', function () {
  console.log('[LIDAR] Connexion fermée.');
  var status = document.getElementById('ros-status');
  if (status) { status.textContent = '🔴 Déconnecté'; status.style.color = '#f44336'; }
});

// =================== Canvas LIDAR ===================
var canvas, ctx, W, H;

window.addEventListener('DOMContentLoaded', function () {
  canvas = document.getElementById('lidar-canvas');
  if (!canvas) return;
  ctx = canvas.getContext('2d');
  W = canvas.width;
  H = canvas.height;

  // Fond initial
  drawBackground();
  drawIdleMessage();
});

function drawBackground() {
  ctx.fillStyle = '#0a0a1a';
  ctx.fillRect(0, 0, W, H);

  // Cercles de distance
  var cx = W / 2, cy = H / 2;
  var maxR = Math.min(W, H) / 2 - 10;
  ctx.strokeStyle = 'rgba(0, 200, 255, 0.15)';
  ctx.lineWidth = 1;
  for (var i = 1; i <= 4; i++) {
    ctx.beginPath();
    ctx.arc(cx, cy, maxR * i / 4, 0, 2 * Math.PI);
    ctx.stroke();
    // Labels de distance
    ctx.fillStyle = 'rgba(0, 200, 255, 0.4)';
    ctx.font = '10px monospace';
    ctx.fillText((i * 2.5).toFixed(1) + 'm', cx + maxR * i / 4 + 3, cy - 3);
  }

  // Lignes de quadrant
  ctx.strokeStyle = 'rgba(0, 200, 255, 0.08)';
  ctx.beginPath(); ctx.moveTo(cx, 10); ctx.lineTo(cx, H - 10); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(10, cy); ctx.lineTo(W - 10, cy); ctx.stroke();

  // Point central (robot)
  ctx.fillStyle = '#00e5ff';
  ctx.beginPath();
  ctx.arc(cx, cy, 5, 0, 2 * Math.PI);
  ctx.fill();

  // Labels Nord/Sud/Est/Ouest
  ctx.fillStyle = 'rgba(0, 200, 255, 0.6)';
  ctx.font = 'bold 11px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('AVANT', cx, 16);
  ctx.fillText('ARRIÈRE', cx, H - 4);
  ctx.textAlign = 'left';
  ctx.fillText('G', 4, cy + 4);
  ctx.textAlign = 'right';
  ctx.fillText('D', W - 4, cy + 4);
  ctx.textAlign = 'left';
}

function drawIdleMessage() {
  ctx.fillStyle = 'rgba(0, 200, 255, 0.3)';
  ctx.font = '13px monospace';
  ctx.textAlign = 'center';
  ctx.fillText('En attente du topic /scan...', W / 2, H / 2 + 25);
  ctx.textAlign = 'left';
}

function drawScan(ranges, angleMin, angleIncrement, rangeMax) {
  drawBackground();

  var cx = W / 2, cy = H / 2;
  var maxR = Math.min(W, H) / 2 - 10;
  var scale = maxR / rangeMax;

  ctx.save();
  for (var i = 0; i < ranges.length; i++) {
    var r = ranges[i];
    if (!isFinite(r) || r <= 0 || r > rangeMax) continue;

    var angle = angleMin + i * angleIncrement;
    // ROS: angle 0 = avant (axe Y canvas inversé), positif = gauche
    var x = cx + Math.sin(angle) * r * scale;
    var y = cy - Math.cos(angle) * r * scale;

    // Couleur selon la distance (rouge=proche, vert=loin)
    var ratio = r / rangeMax;
    var red = Math.round(255 * (1 - ratio));
    var green = Math.round(255 * ratio);
    ctx.fillStyle = 'rgb(' + red + ',' + green + ',100)';
    ctx.fillRect(x - 2, y - 2, 4, 4);
  }
  ctx.restore();
}

// =================== Subscriber /scan ===================
var scanSubscriber = new ROSLIB.Topic({
  ros: ros,
  name: '/scan',
  messageType: 'sensor_msgs/LaserScan',
  throttle_rate: 100  // ms entre messages
});

scanSubscriber.subscribe(function (msg) {
  drawScan(
    msg.ranges,
    msg.angle_min,
    msg.angle_increment,
    Math.min(msg.range_max, 10.0)
  );

  // Mise à jour compteur de points
  var validCount = msg.ranges.filter(function (r) {
    return isFinite(r) && r > 0 && r <= msg.range_max;
  }).length;
  var counter = document.getElementById('lidar-points');
  if (counter) counter.textContent = validCount + ' pts';
});

// =================== Configuration IP ===================
function updateRosUrl() {
  var input = document.getElementById('ros-ip-input');
  if (!input) return;
  var newUrl = 'ws://' + input.value + ':9090';
  localStorage.setItem('ros_url', newUrl);
  ros.close();
  ros = new ROSLIB.Ros({ url: newUrl });
  scanSubscriber.ros = ros;
  console.log('[LIDAR] Reconnexion vers', newUrl);
}
