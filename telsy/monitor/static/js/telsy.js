/**************************************************************************************************/
// Fundacion Cardiovascular de Colombia
// Proyecto Telsy
// Telsy Hogar v17.05.2022
// Ing. Elmer Rocha Jaime
/**************************************************************************************************/
/* Global variables  */
/**************************************************************************************************/
const CONNECTION  = window.navigator.onLine;
const CURRENT_FRAME = document.location.pathname;
// const URI = 'http://3.226.221.181:8082/api/v1'; // Public
const URI = 'http://172.30.19.105:8082/api/v1'; // FCV
/**************************************************************************************************/
/* Global functions  */
/**************************************************************************************************/
if (!CONNECTION) {
  localStorage.setItem('alertId',1);
}
function backHome() {
  window.location.href = '/home/';
}
function circle(animationTime) {
  const graph = document.getElementById('circle-graph');
  const canvas = document.createElement('canvas');
  let currentTime = 0.01;
  const options = {
    percent:  graph.getAttribute('data-percent') || 25,
    size: graph.getAttribute('data-size') || 280,
    lineWidth: graph.getAttribute('data-line') || 15,
    rotate: graph.getAttribute('data-rotate') || 0
  };
  if (typeof(G_vmlCanvasManager) !== 'undefined') {
    G_vmlCanvasManager.initElement(canvas);
  }
  const ctx = canvas.getContext('2d');
  canvas.width = canvas.height = options.size;
  graph.appendChild(canvas);
  ctx.translate(options.size / 2, options.size / 2);
  ctx.rotate((-1 / 2 + options.rotate / 180) * Math.PI);

  const radius = (options.size - options.lineWidth) / 2;
  function drawCircle(color, lineWidth, percent) {
    percent = Math.min(Math.max(0, percent || 1), 1);
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2 * percent, false);
    ctx.strokeStyle = color;
    ctx.lineCap = 'round';
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  }
  function graphFunction() {
    if (currentTime <= 100) {
      setTimeout(graphFunction,100);
    }
    currentTime += 10000/animationTime;
    drawCircle('#BE0C7F', options.lineWidth, currentTime/100);
  }
  graphFunction();
}
function completeActivity() {
  const activityId = parseInt(localStorage.getItem('activityId'));
  $.ajax({
    url: URI+'/patienttasks/'+activityId+'/completed',
    method: 'PUT',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({id:activityId}),
    headers: {'Authorization':'Bearer '+localStorage.getItem('token')},
    async: false,
    timeout: 3000,
    success: function() {
      localStorage.removeItem('activityId');
      saveActivities();
      window.location.href = '/home/';
    },
    error:  function() {
      swal({
        title: 'Error',
        icon: 'error',
        text: 'No fue posible enviar la información.',
        timer: 10000,
        dangerMode: true
      }).then(function() {
          backHome();
      });
    }
  });
}
function createCustomElement(element,elementClass,elementId,content) {
  const customElement = document.createElement(element);
  customElement.className = elementClass;
  customElement.id = elementId;
  customElement.innerHTML = content;
  return customElement;
}
function ecgWave(waveData) {
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  const ecgWidth = canvas.width;
  const ecgHeight = canvas.height;
  const scanBarWidth = 5;
  const data = waveData.split(',');
  const color ='#000000';
  let speed = 0.5;
  let i=0;
  let px = 0;
  let opx = 0;
  let py = ecgHeight/100;
  let opy = py;

  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.setTransform(1,0,0,-1,0,ecgHeight);
  function drawWave() {
    px += speed;
    ctx.clearRect(px, 0, scanBarWidth, ecgHeight);
    ctx.beginPath();
    ctx.moveTo(opx, opy);
    ctx.lineJoin= 'round';
    py=(data[++i>=data.length? i=0 : i++]/(ecgHeight*1.2))-(ecgHeight/1.8);
    ctx.lineTo(px, py);
    ctx.stroke();
    opx = px;
    opy = py;
    if (opx > ecgWidth) {
      px = opx = -speed;
    }
    requestAnimationFrame(drawWave);
  }
  drawWave();
}
function getMethod(url) {
  let result;
  $.ajax({
    url: url,
    async: false,
    timeout: 3000,
    headers: {'Authorization':'Bearer '+localStorage.getItem('token')},
    success: function(data) {
      result = data;
    },
    error: function(error) {
      console.log(error.status + ': ' + error.statusText + ': ' +error.responseText);
    }
  });
  return result;
}
function lastActivitiesUpdate() {
  const lastUpdate = localStorage.getItem('lastUpdate');
  const currentDate = new Date();
  const currentDay = currentDate.getDate().toString();
  const currentMonth = (currentDate.getMonth()+1).toString();
  const currentUpdate = currentDay + currentMonth;
  if (currentUpdate != lastUpdate) {
    localStorage.setItem('lastUpdate',currentUpdate);
    return true;
  } else {
    return false;
  }
}
function loadActivities() {
  const activities = JSON.parse(localStorage.getItem('activities'));
  function splideActivities() {
    $(document).ready(function() {
      new Splide( '#splide-tasks', {
        type:'slide',
        direction: 'ttb',
        height: '280px',
        perPage:3,
        perMove: 1,
        pagination:false,
        padding: 0,
    } ).mount();
    });
  }
  const iconsList = {
    'SYMPTOMS_AM'     : '/static/images/icons/ico-assistant-question.png',
    'WEIGHT'          : '/static/images/icons/ico-weight.png',
    'PHARMACOTHERAPY' : '/static/images/icons/ico-medicine.png',
    'EXERCISE'        : '/static/images/icons/ico-excercise.png',
    'MONITORING'      : '/static/images/icons/ico-monitoring.png',
    'SYMPTOMS_PM'     : '/static/images/icons/ico-assistant-question2.png',
    'GOALS'           : '/static/images/icons/ico-goals.png'
  };
  function iconUrl(key,medicamentName) {
    const icons = {
      'SYMPTOMS_AM'     : '/symptoms/?morning=true',
      'WEIGHT'          : '/weight/',
      'PHARMACOTHERAPY' : '/medicaments/?name='+medicamentName,
      'EXERCISE'        : '/exercise/',
      'MONITORING'      : '/monitor/',
      'SYMPTOMS_PM'     : '/symptoms/?morning=false'
    };
    return icons[key];
  }
  function customizeHour(data) {
    const hour = parseInt(data.split('T')[1].split(':')[0]);
    const minute = parseInt(data.split('T')[1].split(':')[1]);
    let tmpHour,hourText,minuteText,secondText;
    if (hour == 0) {
      tmpHour = 12;
    } else if (hour > 12) {
      tmpHour = hour - 12;
    } else {
      tmpHour = hour;
    }
    if (tmpHour < 10) {
      hourText = '0' + tmpHour;
    } else {
      hourText = tmpHour;
    }
    if (minute < 10) {
      minuteText = '0' + minute;
    } else {
      minuteText = minute;
    }
    if (hour >= 12) {
      secondText = ' PM';
    }
    if (hour < 12) {
      secondText = ' AM';
    }
    return hourText + ':' + minuteText + secondText;
  }
  function onClickActivity(id,href){
    localStorage.setItem('activityId',id);
    window.location.href = href;
  }
  function createActivities() {
    const today = new Date();
    const activityClass = 'card-task d-flex align-items-center';
    let newA;
    const divActivities = document.getElementById('splide-list');
    divActivities.innerHTML = '';//Clear activities list
    for (let i=0; i<activities.length; i++) {
      const activityExecution = activities[i]['execution'].split('T')[1].split(':')[0];
      const iconHref = iconUrl(activities[i]['type'], activities[i]['description']);
      const newLi = createCustomElement('li','splide__slide','','');
      if (activityExecution == today.getHours()) {
        // Flag activity with current time
        newA = createCustomElement('a',activityClass+' selected','','');
      } else {
        newA = createCustomElement('a',activityClass,'','');
      }
      if (activities[i]['completedAt']) {
        // Flag activity as completed
        newA.className = activityClass+' check';
      } else if ((CURRENT_FRAME != '/measuring/') && (activityExecution <= today.getHours())) {
        // Do not redirect if the activity is future or during a measurement
        newA.onclick=onClickActivity.bind(this, activities[i]['id'], iconHref);
      }
      newA.href = '#';
      const newDiv = createCustomElement('div','icon my-auto','','');
      const newImg = createCustomElement('img','','','');
      const newP = createCustomElement('p','labe my-auto','',customizeHour(activities[i]['execution']));
      newImg.src = iconsList[activities[i]['type']];

      newDiv.appendChild(newImg);
      newA.appendChild(newDiv);
      newA.appendChild(newP);
      newLi.appendChild(newA);
      divActivities.appendChild(newLi);
    }
    if (CURRENT_FRAME != '/measuring/') {
      // Updates every minute
      setTimeout(createActivities,60000);
    }
    splideActivities();
  }
  createActivities();
}
function postMethod(url,dataToSend,successFunction) {
  $.ajax({
    url: url,
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(dataToSend),
    async: false,
    timeout: 3000,
    headers: {'Authorization':'Bearer '+localStorage.getItem('token')},
    success: function(data) {
      successFunction();
    },
    error:  function() {
      swal({
        title: 'Error',
        icon: 'error',
        text: 'No fue posible enviar la información.',
        timer: 10000,
        dangerMode: true
      }).then(function() {
          backHome();
      });
    }
  });
}
function saveActivities() {
  if (localStorage.getItem('token')) {
    const activities = getMethod(URI+'/patienttasks');
    localStorage.setItem('activities',JSON.stringify(activities));
  }
}
function updateClock() {
  const today = new Date();
  const day = today.getDate();
  const hour = today.getHours();
  const minute = today.getMinutes();
  let dataToSend, serverDay, serverHour, serverMinute;

  const data = getMethod(URI+'/welcomemessages/currenttime');
  if (data) {
    serverDay = parseInt(data.split('T')[0].split('-')[2]);
    serverHour = parseInt(data.split('T')[1].split('.')[0].split(':')[0]);
    serverMinute = parseInt(data.split('T')[1].split('.')[0].split(':')[1]);
  }

  if ((day!=serverDay) || (hour!=serverHour) || (minute!=serverMinute)) {
    dataToSend = data;
  } else {
    dataToSend = '0';
  }
  document.getElementById('current-time').value = dataToSend;
  document.getElementById('update-time').submit();
}
/**************************************************************************************************/
/* Cancel */
/**************************************************************************************************/
if (CURRENT_FRAME == '/cancel/') {
  function link() {
    window.location.href = '/home/';
  }
  setTimeout(link, 5000);//Wait for 5 seconds to redirect
}
/**************************************************************************************************/
/* Connected */
/**************************************************************************************************/
if (CURRENT_FRAME == '/connected/') {
  if (CONNECTION && lastActivitiesUpdate()) saveActivities();
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Connecting */
/**************************************************************************************************/
function showPasswordNetwork() {
  const pass = document.getElementById('network-password');
  if (pass.type == 'password') {
    pass.type = 'text';
  } else {
    pass.type = 'password';
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Data */
/**************************************************************************************************/
if (CURRENT_FRAME == '/data/') {
  const signsData = getMethod(URI+'/vitalsignrecords/last');
  const ecgWaveData = signsData['ECG'];
  const vitalSigns = ['Pulse', 'SPO2', 'RR', 'Systolic', 'Diastolic', 'MAP'];
  const signsDiv = document.getElementById('signs-div');
  let newDiv1, newDiv2, newDiv3, newImg, newDiv4, newP1, newH2, newP2, newP3;
  let divEcg0, divEcg1, divEcg2, divEcg3, imgEcg, pEcg0, pEcg1, canvasEcg;
  const signIcon = {
    'RR': '/static/images/icons/ico-resp.png',
    'SPO2': '/static/images/icons/ico-spo2.png',
    'Pulse': '/static/images/icons/ico-ekg-2.png',
    'Systolic': '/static/images/icons/ico-pni.png',
    'Diastolic': '/static/images/icons/ico-pni.png',
    'MAP': '/static/images/icons/ico-pni.png'
  };
  const signText = {
    'RR': 'Frec. Respiratoria',
    'SPO2': 'Saturación oxígeno',
    'Pulse': 'Pulso',
    'Systolic': 'Presión Sistólica',
    'Diastolic': 'Presión Diastólica',
    'MAP': 'Presión Media'
  };
  const signUnit = {
    'RR': 'bpm',
    'SPO2': '%',
    'Pulse': 'bpm',
    'Systolic': 'mmHg',
    'Diastolic': 'mmHg',
    'MAP': 'mmHg'
  };
  for (let i=0; i<vitalSigns.length; i++) {
    if ((signsData[vitalSigns[i]]) && (parseInt(signsData[vitalSigns[i]]) != 0)) {
      newDiv1 = createCustomElement('div','card card-data bor bor-grey bor-med padding-4 m-1','','');
      newDiv2 = createCustomElement('div','d-flex align-items-center','','');
      newDiv3 = createCustomElement('div','ico my-auto','','');
      newImg = createCustomElement('img','','','');
      newImg.src = signIcon[vitalSigns[i]];
      newDiv4 = createCustomElement('div','content my-auto margin-left-10','','')
      newP1 = createCustomElement('p','','',signText[vitalSigns[i]]);
      newH2 = createCustomElement('h2','d-inline','',signsData[vitalSigns[i]]+' ');
      newP2 = createCustomElement('p','d-inline','',signUnit[vitalSigns[i]]);
      newP3 = createCustomElement('p','small txt-grey-dark','','<span>Fecha: </span> '+customizeDate(signsData.createdAt));

      newDiv4.appendChild(newP1);
      newDiv4.appendChild(newH2);
      newDiv4.appendChild(newP2);
      newDiv4.appendChild(newP3);
      newDiv3.appendChild(newImg);
      newDiv2.appendChild(newDiv3);
      newDiv2.appendChild(newDiv4);
      newDiv1.appendChild(newDiv2);
      signsDiv.appendChild(newDiv1);
    }
  }
  function customizeDate(currentDate) {
    const date = currentDate.split('T')[0].split('-');
    return date[2]+'/'+date[1]+'/'+date[0];
  }
  // ECG Canvas
  if (signsData['ECG'] != '0') {
    divEcg0 = createCustomElement('div','card card-data3 bor bor-grey bor-med padding-4 m-1','','');
    divEcg1 = createCustomElement('div','d-flex align-items-center','','');
    divEcg2 = createCustomElement('div','ico my-auto','','');
    imgEcg = createCustomElement('img','','','');
    imgEcg.src = '/static/images/icons/ico-ekg.png';
    divEcg3 = createCustomElement('div','content my-auto margin-left-10','','');
    pEcg0 = createCustomElement('p','','','Electrocardiograma');
    pEcg1 = createCustomElement('p','small txt-grey-dark','','<span>Fecha: </span> '+customizeDate(signsData.createdAt));
    canvasEcg = document.createElement('canvas');
    canvasEcg.width = 469;
    canvasEcg.height = 40;
    canvasEcg.id='canvas';

    divEcg2.appendChild(imgEcg);
    divEcg3.appendChild(pEcg0);
    divEcg3.appendChild(pEcg1);
    divEcg1.appendChild(divEcg2);
    divEcg1.appendChild(divEcg3);
    divEcg0.appendChild(divEcg1);
    divEcg0.appendChild(canvasEcg);
    signsDiv.appendChild(divEcg0);

    //ECG Wave
    ecgWave(ecgWaveData);
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Exercise */
/**************************************************************************************************/
if (CURRENT_FRAME == '/exercise/') {
  const currentTime = document.getElementById('timer');
  const exerciseTime = parseInt(localStorage.getItem('exerciseTime'));
  let startTime = 0;
  let time, minutes, seconds, txtMin, txtSec;
  if (exerciseTime) {
    document.getElementById('timer').innerHTML = exerciseTime+':00';
    time = exerciseTime * 60 * 1000;
    startTime = exerciseTime * 60 * 1000;
  } else {
    document.getElementById('timer').innerHTML = '15:00';
    time = 15 * 60 * 1000;
    startTime = 15 * 60 * 1000;
  }
  function timer() {
    time-= 1000;
    minutes =  parseInt((time / 1000) / 60);
    seconds = parseInt((time / 1000) % 60);
    if (minutes < 10) {
      txtMin = '0'+minutes.toString();
    } else {
      txtMin = minutes.toString();
    }
    if (seconds < 10) {
      txtSec = '0'+seconds.toString();
    } else {
      txtSec = seconds.toString();
    }
    currentTime.innerHTML = txtMin + ':' + txtSec;

    if (time > 0) {
      setTimeout(timer, 1000);
    } else {
      localStorage.setItem('alertId',4);
      if (localStorage.getItem('activityId')) {
        completeActivity();
      } else {
        window.location.href = '/home/';
      }
    }
  }
  function animateExercise() {
    document.getElementById('start-button').className = 'row-hidden';
    timer();
    circle(startTime);
  }
  loadActivities();
}
/**************************************************************************************************/
/* Goals */
/**************************************************************************************************/
if (CURRENT_FRAME == '/goals/') {
  const goalsData = getMethod(URI+'/patientgoals/'+localStorage.getItem('userId'));
  localStorage.setItem('goals',JSON.stringify(goalsData));
  function putDescription(data,dataId) {
    for (let i=0; i<data.length; i++) {
      if (data[i].id==dataId) {
        return data[i].description;
      }
    }
  }
  document.getElementById('Selfcare').innerHTML = putDescription(goalsData,1);
  document.getElementById('Exercise').innerHTML = putDescription(goalsData,2);
  document.getElementById('Diets').innerHTML = putDescription(goalsData,3);
  document.getElementById('Quality').innerHTML = putDescription(goalsData,4);
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* GoalsD */
/**************************************************************************************************/
if (CURRENT_FRAME == '/goalsd/') {
  const urlId = new URLSearchParams(window.location.search);
  const goalId = parseInt(urlId.get('id'));
  const goalData = JSON.parse(localStorage.getItem('goals'));
  for (let i=0; i<goalData.length; i++) {
    if (goalData[i]['id'] == goalId) {
      document.getElementById('goal-description').innerHTML = goalData[i]['detail'];
      document.getElementById('goal-video').href = '/goalsv/?id='+goalId;
    }
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* GoalsV */
/**************************************************************************************************/
if (CURRENT_FRAME == '/goalsv/') {
  const urlId = new URLSearchParams(window.location.search);
  const goalId = parseInt(urlId.get('id'));
  const goalData = JSON.parse(localStorage.getItem('goals'));
  for (let i=0; i<goalData.length; i++) {
    if (goalData[i]['id'] == goalId) {
      document.getElementById('detail-vid').src = 'https://www.youtube.com/embed/'+goalData[i]['video'].split('=')[1].split('&')[0];
    }
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Home */
/**************************************************************************************************/
if (CURRENT_FRAME == '/home/') {
  function updateDate() {
    const days = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];
    const months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
    const today = new Date();
    document.getElementById('day-week').innerHTML = days[today.getDay()];
    document.getElementById('date').innerHTML = giveDate(today.getDate(),today.getMonth(),today.getFullYear());
    document.getElementById('hour').innerHTML = giveHour(today.getHours(),today.getMinutes());
    document.getElementById('am-pm').innerHTML = giveAmPm(today.getHours());
    function giveDate(day,month,year) {
      return day+' de '+months[month]+' de '+year;
    }
    function giveHour(hour,minute) {
      let tmpHour, hourText, minuteText;
      if (hour == 0) {
        tmpHour = 12;
      } else if (hour > 12) {
        tmpHour = hour - 12;
      } else {
        tmpHour = hour;
      }
      if (tmpHour < 10) {
        hourText = '0' + tmpHour;
      } else {
        hourText = tmpHour;
      }
      if (minute < 10) {
        minuteText = '0' + minute;
      } else {
        minuteText = minute;
      }
      return hourText + ':' + minuteText;
    }
    function giveAmPm(hour) {
      let amPm
      if (hour >= 12) {
        amPm = 'PM';
      }
      if (hour < 12) {
        amPm = 'AM';
      }
      return amPm;
    }
    if ((today.getHours() == 0) && (today.getMinutes() >= 55)) {
      // Update next day acitivites at 00:55
      saveActivities();
    }
    setTimeout(updateDate,5000);//It updates every 5 seconds.
  }
  function thereIsUser() {
    if (localStorage.getItem('token')) {
      window.location.href = '/menu/';
    } else {
      window.location.href = '/login/';
    }
  }
  function batteryCapacity() {
    const capacity = parseInt(document.getElementById('battery-capacity').innerHTML);
    const battery = document.getElementById('battery');
    const classNames = [
      'fa-battery-empty', //% < 20
      'fa-battery-quarter', //20 <= % < 40
      'fa-battery-half', //40 <= % < 60
      'fa-battery-three-quarters', //60 <= & < 80
      'fa-battery-full', //% > 80
      'fa-battery-full' //% == 100
    ];
    battery.className = classNames[parseInt(capacity/20)];
  }
  function homeAlert() {
    const alertId = parseInt(localStorage.getItem('alertId'));
    const alertText = document.getElementById('alert-text');
    const alertUrl  = document.getElementById('url-text');
    const alertImage= document.getElementById('img-path');
    const alertHide = document.getElementById('div-alert');
    switch(alertId) {
      case 0://Review-correct user
        alertText.innerHTML = 'Revisa tu usuario';
        alertUrl.onclick = function() {clickButton('/login/');};
        alertImage.src = '/static/images/assistant/assistant-warning-1.png';
        alertHide.className = 'row';
        break;
      case 1://Lost connection
        alertText.innerHTML = `<img src="/static/images/icons/ico-wifi.png"> Revisa tu red`;
        alertUrl.onclick = function() {clickButton('/network/');};
        alertImage.src = '/static/images/assistant/assistant-warning-1.png';
        alertHide.className = 'row';
        break;
      case 2://Taking medicine
        alertText.innerHTML = `<img src="/static/images/icons/ico-medicine.png"> Tomaste `+localStorage.getItem('titleAlert');
        alertUrl.onclick = function() {clickButton('/home/');};
        alertImage.src = '/static/images/assistant/assistant-smile-small-I.png';
        alertHide.className = 'row';
        break;
      case 3://Vital signs saved
        alertText.innerHTML = `<img src="/static/images/icons/ico-monitoring.png"> Tus signos vitales han sido guardados`;
        alertUrl.onclick = function() {clickButton('/data/');};
        alertImage.src = '/static/images/assistant/assistant-warning-1.png';
        alertHide.className = 'row';
        break;
      case 4://Exercise
        alertText.innerHTML = 'Hiciste '+localStorage.getItem('exerciseTime')+' minutos de ejercicio';
        alertUrl.onclick = function() {clickButton('/home/');};
        alertImage.src = '/static/images/assistant/assitant-excercise-I.png';
        alertHide.className = 'row';
        break;
      case 5://Weight
        alertText.innerHTML = `<img src="/static/images/icons/ico-weight.png"> Tu peso ha sido guardado`;
        alertUrl.onclick = function() {clickButton('/home/');};
        alertImage.src = '/static/images/assistant/assistant-warning-1.png';
        alertHide.className = 'row';
        break;
      case 6://Morning Symptoms
        alertText.innerHTML = `Se han guardado tus síntomas`;
        alertUrl.onclick = function() {clickButton('/home/');};
        alertImage.src = '/static/images/assistant/assistant-question-l.png';
        alertHide.className = 'row';
        break;
      case 7://Evening Symptoms
        alertText.innerHTML = `Se han guardado tus síntomas`;
        alertUrl.onclick = function() {clickButton('/home/');};
        alertImage.src = '/static/images/assistant/assistant-question-l2.png';
        alertHide.className = 'row';
        break;
      default:
        alertHide.className ='row-hidden';
    }
    function clickButton(urlTxt) {
      localStorage.removeItem('alertId');
      localStorage.removeItem('titleAlert');
      window.location.href = urlTxt;
    }
    setTimeout(function() {clickButton('/home/');}, 60000);
  }
  //Alerts
  if (localStorage.getItem('token')) {
    loadActivities();
  } else {
    localStorage.setItem('alertId',0);
  }
  if (localStorage.getItem('alertId')) {
    homeAlert();
  }
  if (CONNECTION && lastActivitiesUpdate()) {
    saveActivities();
  }
  batteryCapacity();
  updateDate();
}
/**************************************************************************************************/
/* Index */
/**************************************************************************************************/
if (CURRENT_FRAME == '/') {
  function link() {
    if (CONNECTION) {
      if (localStorage.getItem('token')) {
        updateClock();
      } else {
        window.location.href = '/login/';
      }
      if (lastActivitiesUpdate()) {
        saveActivities();
      }
    } else {
      window.location.href = '/network/';
    }
  }
  setTimeout(link, 3000);//Wait for 3 seconds to redirect
}
/**************************************************************************************************/
/* Information */
/**************************************************************************************************/
if (CURRENT_FRAME == '/information/') {
  loadActivities();
  setTimeout(backHome, 60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Login */
/**************************************************************************************************/
if (CURRENT_FRAME == '/login/') {
  if (localStorage.getItem('token')) {
    window.location.href = '/user/';
  }
  function loginUser() {
    const credentials = {
      email: document.getElementById('email').value,
      password: document.getElementById('user-password').value
    };
    $.ajax({
      url: URI.substring(0,25)+'/auth/signin',
      method: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(credentials),
      async: false,
      timeout: 3000,
      success: function(data) {
        localStorage.setItem('token', data.token);
        window.location.href = '/user/';
      },
      error: function(error) {
        document.getElementById('error-div').className = 'card-dialog shadow d-flex align-items-center';
        console.log(error.status + ': ' + error.statusText + ' ' +error.responseText);
      }
    });
  }
  function showPasswordUser() {
    const pass = document.getElementById('user-password');
    if (pass.type == 'password') {
      pass.type = 'text';
    } else {
      pass.type = 'password';
    }
  }
  function backLoginButton() {
    if (localStorage.getItem('token')) {
      backHome();
    }
  }
  setTimeout(backHome,120000);//Wait for 2 minute to redirect
}
/**************************************************************************************************/
/* Measuring */
/**************************************************************************************************/
if (CURRENT_FRAME == '/measuring/') {
  const currentTime = document.getElementById('timer');
  const startTime = 71000;
  let time = startTime;
  let minutes, seconds, txtMin, txtSeg;
  function timer() {
    time -= 1000;
    minutes =  parseInt((time / 1000) / 60);
    seconds = parseInt((time / 1000) % 60);
    if (minutes < 10) {
      txtMin = '0' + minutes.toString();
    } else {
      txtMin = minutes.toString();
    }
    if (seconds < 10) {
      txtSeg = '0' + seconds.toString();
    } else {
      txtSeg = seconds.toString();
    }
    currentTime.innerHTML = txtMin + ':' + txtSeg;
    if (time > 0) {
      setTimeout(timer, 1000);
    } else {
      window.location.href = '/results/';
    }
  }
  timer();
  circle(startTime);
  loadActivities();
}
/**************************************************************************************************/
/* Medicaments  */
/**************************************************************************************************/
if (CURRENT_FRAME == '/medicaments/') {
  const urlName = new URLSearchParams(window.location.search);
  const medicamentName = urlName.get('name');
  document.getElementById('medicament-title').innerHTML = medicamentName;
  localStorage.setItem('titleAlert', medicamentName);
  function acceptButton() {
    localStorage.setItem('alertId',2);
    if (localStorage.getItem('activityId')) {
      completeActivity();
    } else {
      window.location.href = '/home/';
    }
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Medicine */
/**************************************************************************************************/
if (CURRENT_FRAME == '/medicine/') {
  let medicineData;
  try {
    medicineData = getMethod(URI+'/pharmacotherapies/users/'+localStorage.getItem('userId'));
  } catch(error) {
    medicineData = null;
    console.log(error);
  }
  // const medicineData = getMethod(URI+'/pharmacotherapies/users/'+localStorage.getItem('userId'));
  const medicines = document.getElementById('medicine-div');
  let newDiv, newH3, newUl1, newLi, liDosage, newUl2, newLi0, nLi1, nLi2, nLi3, hour, tmpHour;
  if(medicineData) {
    for (let i=0; i<medicineData.length; i++) {
      newDiv = createCustomElement('div','card padding-10 margin-bottom-20','','');
      newH3 = createCustomElement('h3','margin-bottom-20','',medicineData[i].drugName);
      newUl1 = createCustomElement('ul','horizontal margin-bottom-10','','');
      newLi = createCustomElement('li','label','','Dósis:');
      liDosage = createCustomElement('li','','',medicineData[i].dosage);
      newUl2 = createCustomElement('ul','horizontal','','');
      newLi0 = createCustomElement('li','label','','Horas');
      nLi1 = createCustomElement('li','','',hourConversion(medicineData[i].hour1));
      nLi2 = createCustomElement('li','','',hourConversion(medicineData[i].hour2));
      nLi3 = createCustomElement('li','','',hourConversion(medicineData[i].hour3));
  
      newUl1.appendChild(newLi);
      newUl1.appendChild(liDosage);
      newUl2.appendChild(newLi0);
      newUl2.appendChild(nLi1);
      newUl2.appendChild(nLi2);
      newUl2.appendChild(nLi3);
      newDiv.appendChild(newH3);
      newDiv.appendChild(newUl1);
      newDiv.appendChild(newUl2);
      medicines.appendChild(newDiv);
    }
  }
  function hourConversion(time) {
    if (time == null) {
      return '';
    } else {
      hour = time.split(':');
      if (parseInt(hour[0]) > 12) {
        tmpHour = parseInt(hour[0])-12;
        result = tmpHour.toString() + ':' + hour[1] + ' PM';
      } else {
        result = hour[0] + ':' + hour[1] + ' AM';
      }
      return result;
    }
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Menu */
/**************************************************************************************************/
if (CURRENT_FRAME == '/menu/') {
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Monitor */
/**************************************************************************************************/
if (CURRENT_FRAME == '/monitor/') {
  loadActivities();
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Monitoring */
/**************************************************************************************************/
if (CURRENT_FRAME == '/monitoring/') {
  const urlI = new URLSearchParams(window.location.search);
  const index = parseInt(urlI.get('s'));
  const unic = parseInt(urlI.get('u'));
  const signsList = [
    {
      'title' : 'Electrocardiograma',
      'sensor': '/static/images/illustrations/monitoring-sensor-ekg.png',
      'person': '/static/images/illustrations/monitoring-ekg.png',
      'button': 'Continuar',
      'class' : 'button square s60 yellow margin-right-20'
    }, {
      'title' : 'Presión arterial',
      'sensor': '/static/images/illustrations/monitoring-sensor-pni.png',
      'person': '/static/images/illustrations/monitoring-pni.png',
      'button': 'Continuar',
      'class' : 'button square s60 yellow margin-right-20'
    }, {
      'title' : 'Pulso oximetría',
      'sensor': '/static/images/illustrations/monitoring-sensor-spo2.png',
      'person': '/static/images/illustrations/monitoring-spo2.png',
      'button': 'Continuar',
      'class' : 'button square s60 yellow margin-right-20'
    }, {
      'title' : 'Empezar monitoreo',
      'sensor': '/static/images/illustrations/monitoring-sensor-all.png',
      'person': '/static/images/illustrations/monitoring-all2.png',
      'button': 'Empezar',
      'class' : 'row-hidden'
    }
  ];
  document.getElementById('sign-title').innerHTML = signsList[index]['title'];
  document.getElementById('sensor-img').src = signsList[index]['sensor'];
  document.getElementById('person-img').src = signsList[index]['person'];
  document.getElementById('info-button').className = signsList[index]['class'];
  if (unic) {
    document.getElementById('next-button').innerHTML = 'Empezar';
  } else {
    document.getElementById('next-button').innerHTML = signsList[index]['button'];
  }
  function backButton() {
    if (unic) {
      window.location.href= '/menu/'
    } else {
      if (index == 0) {
        window.location.href= '/monitor/';
      } else {
        window.location.href= '/monitoring/?s='+(index-1)+'&u=0';
      }
    }
  }
  function nextButton() {
    if (unic) {
      if (index == 1) {
        document.getElementById('measure-value').value=1;
      } else {
        document.getElementById('measure-value').value=0;
      }
      document.getElementById('start-measuring').submit();
    } else {
      if (index == signsList.length-1) {
        document.getElementById('measure-value').value=1;
        document.getElementById('start-measuring').submit();
      } else {
        window.location.href= '/monitoring/?s='+(index+1)+'&u=0';
      }
    }
  }
  function infoButton() {
    window.location.href= '/monitoringinfo/?s='+index;
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* MonitoringInfo */
/**************************************************************************************************/
if (CURRENT_FRAME == '/monitoringinfo/') {
  const urlI = new URLSearchParams(window.location.search);
  const index = urlI.get('s');
  const signsList = [
    {
      'title' : 'Electrocardiograma',
      'img'   : '/static/images/illustrations/monitoring-ekg.png',
      'text'  : `
      Información de ayuda de posicionamiento de latiguillos y gráfica representativa del cable del parámetro.
      <img class="img-fluid" src="/static/images/instructions/ecg.png">
      <img class="img-fluid" src="/static/images/instructions/5-leads.png">
      `
    }, {
      'title' : 'Presión arterial',
      'img'   : '/static/images/illustrations/monitoring-pni.png',
      'text'  : `
      Información de ayuda del posicionamiento de la manga de presión y gráfica representativa del cable del parámetro
      <img class="img-fluid" src="/static/images/instructions/nibp.png">
      <img class="img-fluid" src="/static/images/instructions/nibpsensor.jpg">
      `
    }, {
      'title' : 'Pulso oximetría',
      'img'   : '/static/images/illustrations/monitoring-spo2.png',
      'text'  : `
      Información de ayuda de uso correcto del sensor y gráfica representativa del cable del parámetro
      <img class="img-fluid" src="/static/images/instructions/spo2.png">
      <img class="img-fluid" src="/static/images/instructions/spo2sensor.jpg">
      `
    }, {
      'title' : 'Monitoreo',
      'img'   : '/static/images/illustrations/monitoring-all.png',
      'text'  : 'Información monitoreo'
    }
  ];
  document.getElementById('monitor-title').innerHTML = signsList[index]['title'];
  document.getElementById('monitor-img').src = signsList[index]['img'];
  document.getElementById('monitor-description').innerHTML = signsList[index]['text'];
  function videoButton() {
    window.location.href = '/monitoringinfov/?s='+index;
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* MonitoringInfoV */
/**************************************************************************************************/
if (CURRENT_FRAME == '/monitoringinfov/') {
  const urlI = new URLSearchParams(window.location.search);
  const index = urlI.get('s');
  const signsList = [
    {
      'title' : 'Electrocardiograma',
      'video' : 'https://www.youtube.com/embed/2aBI9FQQu44'
    }, {
      'title' : 'Presión arterial',
      'video' : 'https://www.youtube.com/embed/2FMmAsHEYuE'
    }, {
      'title' : 'Pulso oximetría',
      'video' : 'https://www.youtube.com/embed/nVYgQS_XFJc'
    }, {
      'title' : 'Monitoreo',
      'video' : 'https://www.youtube.com/embed/s142yyS5rRE'
    }
  ];
  document.getElementById('video-title').innerHTML = signsList[index]['title'];
  document.getElementById('detail-vid').src = signsList[index]['video'];
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Network */
/**************************************************************************************************/
if (CURRENT_FRAME == '/network/') {
  new Splide( '#splide-network', {
    type:'slide',
    direction: 'ttb',
    height: '210px',
    autoHeight: true,
    perPage:3,
    perMove: 1,
    pagination:false,
  }).mount();
  function reloadPage() {
    window.location.href = '/network/';
  }
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Results */
/**************************************************************************************************/
if (CURRENT_FRAME == '/results/') {
  let pulse=0,spo2=0,rr=0,systole=0,diastole=0,mean=0,ecgWaveData=0;
  if (document.getElementById('result-pulse')) {
    pulse = parseInt(document.getElementById('result-pulse').textContent);
  }
  if (document.getElementById('result-spo2')) {
    spo2 = parseInt(document.getElementById('result-spo2').textContent);
  }
  if (document.getElementById('result-rr')) {
    rr = parseInt(document.getElementById('result-rr').textContent);
  }
  if (document.getElementById('result-systole')) {
    systole = parseInt(document.getElementById('result-systole').textContent);
  }
  if (document.getElementById('result-diastole')) {
    diastole = parseInt(document.getElementById('result-diastole').textContent);
  }
  if (document.getElementById('result-mean')) {
    mean = parseInt(document.getElementById('result-mean').textContent);
  }
  if (document.getElementById('result-ecg')) {
    ecgWaveData = document.getElementById('result-ecg').textContent;
  }
  function sendVitalSigns() {
    const dataToSend = {
      patient: {id:parseInt(localStorage.getItem('userId'))},
      RR: rr,
      SPO2: spo2,
      Pulse: pulse,
      Systolic: systole,
      Diastolic: diastole,
      MAP: mean,
      ECG: ecgWaveData
    };
    function successFunction() {
      localStorage.setItem('alertId',3);
      if (localStorage.getItem('activityId')) {
        completeActivity();
      } else {
        window.location.href = '/home/';
      }
    }
    postMethod(URI+'/vitalsignrecords',dataToSend,successFunction);
  }
  if (ecgWaveData != '0') {
    ecgWave(ecgWaveData);
  }
  setTimeout(sendVitalSigns,10000);//Send data after 10 seconds
}
/**************************************************************************************************/
/* Symptoms  */
/**************************************************************************************************/
if (CURRENT_FRAME == '/symptoms/') {
  const urlMorning = new URLSearchParams(window.location.search);
  const morning = urlMorning.get('morning');
  if (morning == 'true') {
    document.getElementById('morning-icon').src = '/static/images/assistant/assistant-question-l.png';
  } else {
    document.getElementById('morning-icon').src = '/static/images/assistant/assistant-question-l2.png';
  }
  const symptomsData = getMethod(URI+'/symptoms?morning='+morning);
  let index = 0;
  function loadSymptoms(I) {
    document.getElementById('symptom-title').innerHTML = symptomsData[I].description;
    document.getElementById('symptom-image').src = URI.substring(0,25) + symptomsData[I].image;
  }
  function noSymptom() {
    if (index < (symptomsData.length-1)) {
      index++;
      loadSymptoms(index);
    } else {
      if (morning == 'true') {
        localStorage.setItem('alertId',6);
      } else {
        localStorage.setItem('alertId',7);
      }
      if (localStorage.getItem('activityId')) {
        completeActivity();
      } else {
        window.location.href = '/home/';
      }
    }
  }
  function yesSymptom() {
    swal({
      title: '¿Estás seguro de enviar el síntoma?',
      icon: 'warning',
      buttons: {
        cancel: 'No',
        catch: {value:true, text:'Sí'},
    }}).then((value) => {
        if (value) {
          yesSend();
        } else {
          noSend();
        }
    });
    function yesSend() {
      if (index < (symptomsData.length-1)) {
        saveSymptom(index);
        index++;
        loadSymptoms(index);
      } else {
        if (morning=='true') {
          localStorage.setItem('alertId',6);
        } else {
          localStorage.setItem('alertId',7);
        }
        if (localStorage.getItem('activityId')) {
          completeActivity();
        } else {
          window.location.href = '/home/';
        }
      }
    }
    function noSend() {
      if (index < (symptomsData.length-1)) {
        index++;
        loadSymptoms(index);
      } else {
        if (morning=='true') {
          localStorage.setItem('alertId',6);
        } else {
          localStorage.setItem('alertId',7);
        }
        if (localStorage.getItem('activityId')) {
          completeActivity();
        } else {
          window.location.href = '/home/';
        }
      }
    }
  }
  function saveSymptom(symptomId) {
    const dataToSend = {
      patient: {id:parseInt(localStorage.getItem('userId'))},
      symptom: {id:symptomsData[symptomId]['id']}
    };
    function successFunction() {}
    postMethod(URI+'/patientsymptoms',dataToSend,successFunction);
  }
  loadSymptoms(index);
  loadActivities();
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* User */
/**************************************************************************************************/
if (CURRENT_FRAME == '/user/') {
  const userData = getMethod(URI+'/users/profile');
  localStorage.setItem('userId', userData.id);
  document.getElementById('fullname').innerHTML = userData.name + ' ' + userData.lastName;
  document.getElementById('email').innerHTML = 'Correo: ' + userData.email;
  document.getElementById('age').innerHTML = 'Edad: ' + userData.age;
  document.getElementById('cc').innerHTML = userData.identificationType.name + ': ' + userData.identificationNumber;
  document.getElementById('telephone').innerHTML = 'Teléfono: ' + userData.phone;
  document.getElementById('ubication').innerHTML = 'Ubicación: '+ userData['city'].name+', '+userData['city']['department'].name;
  document.getElementById('photo').src = userData.image;

  const userData2 = getMethod(URI+'/patientgoals/'+userData.id);
  for (let i=0; i<userData2.length; i++) {
    if (userData2[i].id == 2) {
      localStorage.setItem('exerciseTime', userData2[i].minutes);
    }
  }
  function logoutUser() {
    localStorage.clear();
    window.location.href = '/login/';
  }
  function accept() {
    updateClock();
  }
  saveActivities();
  setTimeout(accept,7000);//Wait for 7 seconds to redirect
}
/**************************************************************************************************/
/* Weight */
/**************************************************************************************************/
if (CURRENT_FRAME == '/weight/') {
  let weight;
  if (localStorage.getItem('weight')) {
    document.getElementById('weight').innerHTML = parseFloat(localStorage.getItem('weight')).toFixed(1);
    localStorage.removeItem('weight');
  } else {
    weightData = getMethod(URI+'/weigthrecords/last');
    if (!weightData) {
      document.getElementById('weight').innerHTML = 50.1;
    } else {
      document.getElementById('weight').innerHTML = parseFloat(weightData.weigth).toFixed(1);
    }
  }
  function addWeight() {
    weight = parseFloat(document.getElementById('weight').innerHTML);
    document.getElementById('weight').innerHTML = (weight+0.1).toFixed(1);
  }
  function subtractWeight() {
    weight = parseFloat(document.getElementById('weight').innerHTML);
    document.getElementById('weight').innerHTML = (weight-0.1).toFixed(1);
  }
  function saveWeight() {
    weight = document.getElementById('weight').innerHTML;
    localStorage.setItem('weight', weight);
  }
  loadActivities();
  setTimeout(backHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* WeightC */
/**************************************************************************************************/
if (CURRENT_FRAME == '/weightc/') {
  const weight = parseFloat(localStorage.getItem('weight')).toFixed(1);
  document.getElementById('weight').innerHTML = weight;
  function sendWeight() {
    const dataToSend = {
      patient: {
        id:parseInt(localStorage.getItem('userId'))
      },
      weigth: weight};
    function successFunction() {
      localStorage.removeItem('weight');
      localStorage.setItem('alertId',5);
      if (localStorage.getItem('activityId')) {
        completeActivity();
      } else {
        window.location.href = '/home/';
      }
    }
    postMethod(URI+'/weigthrecords',dataToSend,successFunction());
  }
  loadActivities();
  setTimeout(sendWeight,10000);//Wait for 10 seconds to redirect
}
/**************************************************************************************************/
