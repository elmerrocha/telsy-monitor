/**************************************************************************************************/
/* Global variables  */
/**************************************************************************************************/
var Connection  = window.navigator.onLine;
var CurrentFrame = document.location.pathname;
var URLServer = "http://54.159.156.165:8082";
/**************************************************************************************************/
/* Global methods  */
/**************************************************************************************************/
if(!Connection) localStorage.setItem("IDAlert",1);
function BackHome() {
  window.location.href="/home/";
}
function BatteryCapacity() {
  Capacity = parseInt(document.getElementById("BatteryCap").innerHTML);
  Battery = document.getElementById("Battery");
  ClassNames = [
    "fa-battery-empty",//% < 20
    "fa-battery-quarter",//20 <= % < 40
    "fa-battery-half",//40 <= % < 60
    "fa-battery-three-quarters",//60 <= & < 80
    "fa-battery-full",//% > 80
    "fa-battery-full"//% == 100
  ];
  Battery.className = ClassNames[parseInt(Capacity/20)];
}
function Circle(TimeX) {
  var Graph = document.getElementById("CircleGraph");
  var options = {
    percent:  Graph.getAttribute('data-percent') || 25,
    size: Graph.getAttribute('data-size') || 280,
    lineWidth: Graph.getAttribute('data-line') || 15,
    rotate: Graph.getAttribute('data-rotate') || 0
  }
  var canvas = document.createElement('canvas');
  if (typeof(G_vmlCanvasManager) !== 'undefined') {
    G_vmlCanvasManager.initElement(canvas);
  }
  var ctx = canvas.getContext('2d');
  canvas.width = canvas.height = options.size;
  Graph.appendChild(canvas);
  ctx.translate(options.size / 2, options.size / 2);
  ctx.rotate((-1 / 2 + options.rotate / 180) * Math.PI);
  var radius = (options.size - options.lineWidth) / 2;
  var drawCircle = function(color, lineWidth, percent) {
    percent = Math.min(Math.max(0, percent || 1), 1);
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2 * percent, false);
    ctx.strokeStyle = color;
    ctx.lineCap = 'round';
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  };
  var X = 0.01;
  function GraphF() {
    if(X<=100) {
      setTimeout(GraphF,100);
    }
    X+=10000/TimeX;
    drawCircle('#BE0C7F', options.lineWidth, X/100);
  }
  GraphF();
}
function CreateElement(ElementN,ClassN,IDN,ContentN) {
  E = document.createElement(ElementN);
  C = E.className = ClassN;
  I = E.id = IDN;
  E.innerHTML = ContentN;
  return E;
}
function ECGWave(DataWave) {
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");
  var w = canvas.width;
  h = canvas.height;
  speed = 0.5;
  scanBarWidth = 5;
  i=0;
  data = DataWave.split(',');
  color='#000000';
  var px = 0;
  var opx = 0;
  var py = h/100;
  var opy = py;
  ctx.strokeStyle = color;
  ctx.lineWidth = 2;
  ctx.setTransform(1,0,0,-1,0,h);
  function drawWave() {
    px += speed;
    ctx.clearRect(px, 0, scanBarWidth, h);
    ctx.beginPath();
    ctx.moveTo(opx, opy);
    ctx.lineJoin= 'round';
    py=(data[++i>=data.length? i=0 : i++]/(h*1.2))-(h/1.8);
    ctx.lineTo(px, py);
    ctx.stroke();
    opx = px;
    opy = py;
    if (opx > w) px = opx = -speed;
    requestAnimationFrame(drawWave);
  }
  drawWave();
}
function GETMethod(URL) {
  var result="";
  $.ajax({
    url: URL,
    async: false,
    headers: {'Authorization':'Bearer '+localStorage.getItem("token")},
    success: function(data) {
      result = data;
    },
    error: function(error) {
      alert(error.status + " " + error.statusText + " " +error.responseText);
    }
  });
  return result;
}
function HomeAlert() {
  ID = parseInt(localStorage.getItem("IDAlert"));
  AText = document.getElementById("AlertText");
  AUrl  = document.getElementById("UrlText");
  AImage= document.getElementById("ImgPath");
  AHide = document.getElementById("DivAlert");
  switch(ID) {
    case 0://Review user
      AText.innerHTML = "Revisa tu usuario";
      AUrl.onclick = function() { ClickButton("/login/"); };
      AImage.src = "/static/images/assistant/assistant-warning-1.png";
      AHide.className = "row";
      break;
    case 1://Lost connection
      AText.innerHTML = `<img src="/static/images/icons/ico-wifi.png"> Revisa tu red`;
      AUrl.onclick = function() { ClickButton("/network/"); };
      AImage.src = "/static/images/assistant/assistant-warning-1.png";
      AHide.className = "row";
      break;
    case 2://Taking medicine
      AText.innerHTML = `<img src="/static/images/icons/ico-medicine.png"> Tomaste `+localStorage.getItem("TitleAlert");
      AUrl.onclick = function() { ClickButton("/home/"); };
      AImage.src = "/static/images/assistant/assistant-smile-small-I.png";
      AHide.className = "row";
      break;
    case 3://Vital signs saved
      AText.innerHTML = `<img src="/static/images/icons/ico-monitoring.png"> Tus signos vitales han sido guardados`;
      AUrl.onclick = function() { ClickButton("/data/"); };
      AImage.src = "/static/images/assistant/assistant-warning-1.png";
      AHide.className = "row";
      break;
    case 4://Exercise
      AText.innerHTML = "Hiciste "+localStorage.getItem("tExercise")+" minutos de ejercicio";
      AUrl.onclick = function() { ClickButton("/home/"); };
      AImage.src = "/static/images/assistant/assitant-excercise-I.png";
      AHide.className = "row";
      break;
    case 5://Weight
      AText.innerHTML = `<img src="/static/images/icons/ico-weight.png"> Tu peso ha sido guardado`;
      AUrl.onclick = function() { ClickButton("/home/"); };
      AImage.src = "/static/images/assistant/assistant-warning-1.png";
      AHide.className = "row";
      break;
    case 6://Morning Symptoms
      AText.innerHTML = `Se han guardado tus síntomas`;
      AUrl.onclick = function() { ClickButton("/home/"); };
      AImage.src = "/static/images/assistant/assistant-question-l.png";
      AHide.className = "row";
      break;
    case 7://Evening Symptoms
      AText.innerHTML = `Se han guardado tus síntomas`;
      AUrl.onclick = function() { ClickButton("/home/"); };
      AImage.src = "/static/images/assistant/assistant-question-l2.png";
      AHide.className = "row";
      break;
    default:
      AHide.className="row-hidden";
  }
  function ClickButton(URLTxt) {
    localStorage.removeItem("IDAlert");
    localStorage.removeItem("TitleAlert");
    window.location.href = URLTxt;
  }
  setTimeout(function(){
    ClickButton("/home/");
  }, 60000);
}
function LoadActivities() {
  DataAct = JSON.parse(localStorage.getItem("Activities"));
  function SplideActivities() {
    $(document).ready(function() {
      new Splide( '#splide-tasks', {
        type:"slide",
        direction: 'ttb',
        height: '280px',
        perPage:3,
        perMove: 1,
        pagination:false,
        padding: 0,
    } ).mount();
    });
  }
  IconList = {
    "SYMPTOMS_AM"     : "/static/images/icons/ico-assistant-question.png",
    "WEIGHT"          : "/static/images/icons/ico-weight.png",
    "PHARMACOTHERAPY" : "/static/images/icons/ico-medicine.png",
    "EXERCISE"        : "/static/images/icons/ico-excercise.png",
    "MONITORING"      : "/static/images/icons/ico-monitoring.png",
    "SYMPTOMS_PM"     : "/static/images/icons/ico-assistant-question2.png",
    "GOALS"           : "/static/images/icons/ico-goals.png"
  };
  function IconURL(key,MedName) {
    Icons = {
      "SYMPTOMS_AM"     : "/symptoms/?morning=true",
      "WEIGHT"          : "/weigth/",
      "PHARMACOTHERAPY" : "/medicaments/?name="+MedName,
      "EXERCISE"        : "/exercise/",
      "MONITORING"      : "/monitor/",
      "SYMPTOMS_PM"     : "/symptoms/?morning=false"
    };
    return Icons[key];
  }
  function GiveHour(data) {
    hour = parseInt(data.split("T")[1].split(":")[0]);
    minute = parseInt(data.split("T")[1].split(":")[1]);
    if(hour == 0) ht=12;
    else if(hour > 12) ht=hour-12;
    else ht=hour;
    if(ht < 10) h="0"+ht;
    else h=ht;
    if(minute < 10) m="0"+minute;
    else m=minute;
    if(hour >= 12) s=" PM";
    if(hour < 12) s=" AM";
    return h+":"+m+s;
  }
  function OnClickActivity(ID,H){
    localStorage.setItem("IDActivity",ID);
    window.location.href = H;
  }
  function CreteActivities() {
    Today = new Date();
    ActivitiesDiv = document.getElementById("ulVar");
    ActivitiesDiv.innerHTML = "";//Clear activities list
    for(i=0; i<DataAct.length; i++) {
      ActivityExecution = DataAct[i]["execution"].split("T")[1].split(":")[0];
      IconHref = IconURL(DataAct[i]["type"], DataAct[i]["description"]);
      newLi = CreateElement("li","splide__slide","","");
      if(ActivityExecution == Today.getHours()) newA = CreateElement("a","card-task d-flex align-items-center selected","","");//Mark actvitie's hour
      else newA = CreateElement("a","card-task d-flex align-items-center","","");
      if(DataAct[i]["completedAt"]) newA.className="card-task d-flex align-items-center check";//Mark as completed activity
      else if((CurrentFrame != "/measuring/") && (ActivityExecution <= Today.getHours())) newA.onclick=OnClickActivity.bind(this, DataAct[i]["id"], IconHref);//Don't link future activities
      newA.href="#";
      newDiv = CreateElement("div","icon my-auto","","");
      newImg = CreateElement("img","","","");
      newImg.src = IconList[DataAct[i]["type"]];
      newP = CreateElement("p","labe my-auto","",GiveHour(DataAct[i]["execution"]));

      newDiv.appendChild(newImg);
      newA.appendChild(newDiv);
      newA.appendChild(newP);
      newLi.appendChild(newA);
      ActivitiesDiv.appendChild(newLi);
    }
    if(CurrentFrame != "/measuring/") setTimeout(CreteActivities,60000);//Updates every minute
    SplideActivities();
  }
  CreteActivities();
}
function POSTMethod(URL,Data,SuccessFunction,ErrorFunction) {
  var result="";
  $.ajax({
    url: URL,
    method: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(Data),
    async: false,
    headers: {'Authorization':'Bearer '+localStorage.getItem("token")},
    success: function(data) {
      SuccessFunction();
      result = data;
    },
    error:  function(error) {
      ErrorFunction();
      alert(error.status + " " + error.statusText + " " +error.responseText);
    }
  });
  return result;
}
function PUTMethod(URL,Data,SuccessFunction) {
  $.ajax({
    url: URL,
    method: 'PUT',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify(Data),
    headers: {'Authorization':'Bearer '+localStorage.getItem("token")},
    async: false,
    success: function() {
      SuccessFunction();
    },
    error:  function(error) {
      alert(error.status + " " + error.statusText + " " +error.responseText);
    }
  });
}
function RegisterActivities() {
  ID = parseInt(localStorage.getItem("IDActivity"));
  DataSend = {id:ID};
  function Sucess() {
    localStorage.removeItem("IDActivity");
    SaveActivities();
    window.location.href="/home/";
  }
  PUTMethod(URLServer+"/api/v1/patienttasks/"+ID+"/completed",DataSend,Sucess);
}
function SaveActivities() {
  if(localStorage.getItem("token")) {
    DataActivities = GETMethod(URLServer+"/api/v1/patienttasks");
    localStorage.setItem("Activities",JSON.stringify(DataActivities));
  }
}
function UpdateClock() {
  Today = new Date();
  TDay = Today.getDate();
  THour = Today.getHours();
  TMinute = Today.getMinutes();

  Data = GETMethod(URLServer+"/api/v1/welcomemessages/currenttime");
  DDay = parseInt(Data.split("T")[0].split("-")[2]);
  DHour = parseInt(Data.split("T")[1].split(".")[0].split(":")[0]);
  DMinute = parseInt(Data.split("T")[1].split(".")[0].split(":")[1]);

  if((TDay!=DDay) || (THour!=DHour) || (TMinute!=DMinute)) DataSend=Data;
  else DataSend=0;

  document.getElementById("CurrentClock").value = DataSend;
  document.getElementById("UpdateClock").submit();
}
/**************************************************************************************************/
/* Cancel */
/**************************************************************************************************/
if (CurrentFrame == "/cancel/") {
  function Link() {
    window.location.href="/home/";
  }
  setTimeout(Link, 5000);//Wait for 5 seconds to redirect
}
/**************************************************************************************************/
/* Connected */
/**************************************************************************************************/
if (CurrentFrame == "/connected/") {
  new Splide( '#splide-network', {
    type:"slide",
    direction: 'ttb',
    height: '210px',
    autoHeight: true,
    perPage:3,
    perMove: 1,
    pagination:false,
  }).mount();
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Connecting */
/**************************************************************************************************/
function showPasswordNetwork() {
  Pass = document.getElementById("ppasw");
  if (Pass.type === "password") Pass.type = "text";
  else Pass.type = "password";
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Data */
/**************************************************************************************************/
if (CurrentFrame == "/data/") {
  Data = GETMethod(URLServer+"/api/v1/vitalsignrecords/last");
  ECGw = Data["ECG"];

  DataIcons = {
    "RR" : "/static/images/icons/ico-resp.png",
    "SPO2" : "/static/images/icons/ico-spo2.png",
    "Pulse" : "/static/images/icons/ico-ekg-2.png",
    "Systolic" : "/static/images/icons/ico-pni.png",
    "Diastolic" : "/static/images/icons/ico-pni.png",
    "MAP" : "/static/images/icons/ico-pni.png"
  };
  DataText = {
    "RR" : "Frec. Respiratoria",
    "SPO2" : "Saturación oxígeno",
    "Pulse" : "Pulso",
    "Systolic" : "Presión Sistólica",
    "Diastolic" : "Presión Diastólica",
    "MAP" : "Presión Media"
  };
  DataUnits = {
    "RR" : "bpm",
    "SPO2" : "%",
    "Pulse" : "bpm",
    "Systolic" : "mmHg",
    "Diastolic" : "mmHg",
    "MAP" : "mmHg"
  };

  Signs = document.getElementById("DivVar");
  VitalSigns = ["Pulse", "SPO2", "RR", "Systolic", "Diastolic", "MAP"];
  for(i=0; i<VitalSigns.length; i++) {
    if(Data[VitalSigns[i]] && parseInt(Data[VitalSigns[i]]) != 0) {
      newDiv1 = CreateElement("div","card card-data bor bor-grey bor-med padding-4 m-1","","");
      newDiv2 = CreateElement("div","d-flex align-items-center","","");
      newDiv3 = CreateElement("div","ico my-auto","","");
      newImg = CreateElement("img","","","");
      newImg.src = DataIcons[VitalSigns[i]];
      newDiv4 = CreateElement("div","content my-auto margin-left-10","","")
      newP1 = CreateElement("p","","",DataText[VitalSigns[i]]);
      newH2 = CreateElement("h2","d-inline","",Data[VitalSigns[i]]+" ");
      newP2 = CreateElement("p","d-inline","",DataUnits[VitalSigns[i]]);
      newP3 = CreateElement("p","small txt-grey-dark","","<span>Fecha: </span> "+GiveDate(Data.createdAt));

      newDiv4.appendChild(newP1);
      newDiv4.appendChild(newH2);
      newDiv4.appendChild(newP2);
      newDiv4.appendChild(newP3);
      newDiv3.appendChild(newImg);
      newDiv2.appendChild(newDiv3);
      newDiv2.appendChild(newDiv4);
      newDiv1.appendChild(newDiv2);
      Signs.appendChild(newDiv1);
    }
  }

  function GiveDate(date) {
    f = date.split("T")[0].split("-");
    return f[2]+"/"+f[1]+"/"+f[0];
  }
  //ECG Canvas
  if(Data["ECG"] != "0") {
    DivECG0 = CreateElement("div","card card-data3 bor bor-grey bor-med padding-4 m-1","","");
    DivECG1 = CreateElement("div","d-flex align-items-center","","");
    DivECG2 = CreateElement("div","ico my-auto","","");
    ImgECG = CreateElement("img","","","");
    ImgECG.src = "/static/images/icons/ico-ekg.png";
    DivECG3 = CreateElement("div","content my-auto margin-left-10","","");
    PeCG0 = CreateElement("p","","","Electrocardiograma");
    PeCG1 = CreateElement("p","small txt-grey-dark","","<span>Fecha: </span> "+GiveDate(Data.createdAt));
    CanvECG = document.createElement("canvas");
    CanvECG.width = 469;
    CanvECG.height = 40;
    CanvECG.id="canvas";

    DivECG2.appendChild(ImgECG);
    DivECG3.appendChild(PeCG0);
    DivECG3.appendChild(PeCG1);
    DivECG1.appendChild(DivECG2);
    DivECG1.appendChild(DivECG3);
    DivECG0.appendChild(DivECG1);
    DivECG0.appendChild(CanvECG);
    Signs.appendChild(DivECG0);

    //ECG Wave
    ECGWave(ECGw);
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Exercise */
/**************************************************************************************************/
if (CurrentFrame == "/exercise/") {
  var StartTime = 0;
  CurrentTime = document.getElementById("timer");
  ExerciseTime = parseInt(localStorage.getItem("tExercise"));
  if (ExerciseTime) {
    document.getElementById("timer").innerHTML = ExerciseTime+":00";
    var Time = ExerciseTime * 60 * 1000;
    StartTime = ExerciseTime * 60 * 1000;
  } else {
    document.getElementById("timer").innerHTML = "15:00";
    var Time = 15 * 60 * 1000;
    StartTime = 15 * 60 * 1000;
  }
  function Timer() {
    Time-= 1000;
    Minutes =  parseInt((Time / 1000) / 60);
    Seconds = parseInt((Time / 1000) % 60);
    if (Minutes < 10) txtMin = "0"+Minutes.toString();
    else txtMin = Minutes.toString();
    if (Seconds < 10) txtSec = "0"+Seconds.toString();
    else txtSec = Seconds.toString();
    CurrentTime.innerHTML = txtMin + ":" + txtSec;

    if (Time > 0) setTimeout(Timer, 1000);
    else {
      localStorage.setItem("IDAlert",4);
      if (localStorage.getItem("IDActivity")) RegisterActivities();
      else window.location.href="/home/";
    }
  }
  function Animate() {
    document.getElementById("StartButton").className = "row-hidden";
    Timer();
    Circle(StartTime);
  }
  LoadActivities();
}
/**************************************************************************************************/
/* Goals */
/**************************************************************************************************/
if (CurrentFrame == "/goals/") {
  Data = GETMethod(URLServer+"/api/v1/patientgoals/"+localStorage.getItem("uid"));
  localStorage.setItem("Goals",JSON.stringify(Data));
  document.getElementById("Selfcare").innerHTML = Description(Data,1);
  document.getElementById("Exercise").innerHTML = Description(Data,2);
  document.getElementById("Diets").innerHTML = Description(Data,3);
  document.getElementById("Quality").innerHTML = Description(Data,4);
  function Description(data,ID) {
    for(i=0; i<data.length; i++) if(data[i].id==ID) return data[i].description;
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* GoalsD */
/**************************************************************************************************/
if (CurrentFrame == "/goalsd/") {
  urlID = new URLSearchParams(window.location.search);
  GoalID = parseInt(urlID.get("id"));
  Data = JSON.parse(localStorage.getItem("Goals"));
  for(i=0; i<Data.length; i++) {
    if (Data[i]["id"] == GoalID) {
      document.getElementById("GoalDescription").innerHTML = Data[i]["detail"];
      document.getElementById("GoalVideo").href = "/goalsv/?id="+GoalID;
    }
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* GoalsV */
/**************************************************************************************************/
if (CurrentFrame == "/goalsv/") {
  urlID = new URLSearchParams(window.location.search);
  GoalID = parseInt(urlID.get("id"));
  Data = JSON.parse(localStorage.getItem("Goals"));
  for(i=0; i<Data.length; i++) {
    if (Data[i]["id"] == GoalID) {
      document.getElementById("DetailVid").src = "https://www.youtube.com/embed/"+Data[i]["video"].split("=")[1].split("&")[0];
    }
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Home */
/**************************************************************************************************/
if (CurrentFrame == "/home/") {
  function UpdateDate() {
    Days = ["Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado"];
    Months = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"];
    Today = new Date();
    document.getElementById("DayWeek").innerHTML = Days[Today.getDay()];
    document.getElementById("Date").innerHTML = GiveDate(Today.getDate(),Today.getMonth(),Today.getFullYear());
    document.getElementById("Hour").innerHTML = GiveHour(Today.getHours(),Today.getMinutes());
    document.getElementById("AMPM").innerHTML = GiveAMPM(Today.getHours());
    function GiveDate(day,month,year) {
      return day+" de "+Months[month]+" de "+year;
    }
    function GiveHour(hour,minute) {
      if(hour == 0) ht=12;
      else if(hour > 12) ht=hour-12;
      else ht=hour;
      if(ht < 10) h="0"+ht;
      else h=ht;
      if(minute < 10) m="0"+minute;
      else m=minute;
      return h+":"+m;
    }
    function GiveAMPM(hour) {
      if(hour >= 12) AMPM="PM";
      if(hour < 12) AMPM="AM";
      return AMPM;
    }
    if((Today.getHours() == 0) && (Today.getMinutes()>=55)) SaveActivities();//Update next day acitivites
    setTimeout(UpdateDate,5000);//It updates every 5 seconds.
  }
  function ThereisUser() {
    if(localStorage.getItem("token")) window.location.href="/menu/";
    else window.location.href="/login/";
  }
  //Alerts
  if(localStorage.getItem("token")) LoadActivities();
  else localStorage.setItem("IDAlert",0);
  if(localStorage.getItem("IDAlert")) HomeAlert();
  BatteryCapacity();
  UpdateDate();
}
/**************************************************************************************************/
/* Index */
/**************************************************************************************************/
if (CurrentFrame == "/") {
  function Link() {
    if (Connection) {
      if(localStorage.getItem("token")) UpdateClock();
      else window.location.href="/login/";
    }
    else window.location.href="/network/";
  }
  setTimeout(Link, 5000);//Wait for 5 seconds to redirect
}
/**************************************************************************************************/
/* Login */
/**************************************************************************************************/
if (CurrentFrame == "/login/") {
  if(localStorage.getItem("token")) window.location.href="/user/";
  function LoginUser() {
    Credentials = {email: document.getElementById("email").value, password: document.getElementById("password").value};
    function Success() {
      window.location.href="/user/";
    }
    function ErrorF() {
      document.getElementById("DivError").className = "card-dialog shadow d-flex align-items-center";
    }
    Data = POSTMethod(URLServer+"/auth/signin",Credentials,Success,ErrorF);
    localStorage.setItem("token", Data.token);
  }
  function showPasswordUser() {
    Pass = document.getElementById("password");//El id del cajón de contraseña
    if (Pass.type == "password") Pass.type = "text";
    else Pass.type = "password";
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Measuring */
/**************************************************************************************************/
if (CurrentFrame == "/measuring/") {
  CurrentTime = document.getElementById("timer");
  var StartTime = 71000;
  var Time = StartTime;
  function Timer() {
    Time-= 1000;
    Minutes =  parseInt((Time / 1000) / 60);
    Seconds = parseInt((Time / 1000) % 60);
    if (Minutes < 10) txtMin = "0"+Minutes.toString();
    else txtMin = Minutes.toString();
    if (Seconds < 10) txtSeg = "0"+Seconds.toString();
    else txtSeg = Seconds.toString();
    CurrentTime.innerHTML = txtMin + ":" + txtSeg;
    if (Time > 0) setTimeout(Timer, 1000);
    else window.location.href="/results/";
  }
  Timer();
  Circle(StartTime);
  LoadActivities();
}
/**************************************************************************************************/
/* Medicaments  */
/**************************************************************************************************/
if (CurrentFrame == "/medicaments/") {
  urlName = new URLSearchParams(window.location.search);
  Name = urlName.get("name");
  document.getElementById("MTitle").innerHTML = Name;
  localStorage.setItem("TitleAlert",Name);
  function AcceptButton() {
    localStorage.setItem("IDAlert",2);
    if (localStorage.getItem("IDActivity")) RegisterActivities();
    else window.location.href="/home/";
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Medicine */
/**************************************************************************************************/
if (CurrentFrame == "/medicine/") {
  Data = GETMethod(URLServer+"/api/v1/pharmacotherapies/users/"+localStorage.getItem("uid"));
  Medicines = document.getElementById("divVar");
  for (i=0; i<Data.length; i++) {
    newDiv = CreateElement("div","card padding-10 margin-bottom-20","","");
    newH3 = CreateElement("h3","margin-bottom-20","",Data[i].drugName);
    newUL1 = CreateElement("ul","horizontal margin-bottom-10","","");
    newLI = CreateElement("li","label","","Dósis:");
    LIDose = CreateElement("li","","",Data[i].dosage);
    newUL2 = CreateElement("ul","horizontal","","");
    newLI0 = CreateElement("li","label","","Horas");
    nLI1 = CreateElement("li","","",HourConversion(Data[i].hour1));
    nLI2 = CreateElement("li","","",HourConversion(Data[i].hour2));
    nLI3 = CreateElement("li","","",HourConversion(Data[i].hour3));

    newUL1.appendChild(newLI);
    newUL1.appendChild(LIDose);
    newUL2.appendChild(newLI0);
    newUL2.appendChild(nLI1);
    newUL2.appendChild(nLI2);
    newUL2.appendChild(nLI3);
    newDiv.appendChild(newH3);
    newDiv.appendChild(newUL1);
    newDiv.appendChild(newUL2);
    Medicines.appendChild(newDiv);
  }
  function HourConversion(Hour) {
    if(Hour == null) {
      return "";
    }
    else {
      nHour = Hour.split(":");
      if(parseInt(nHour[0]) > 12) {
        temp = parseInt(nHour[0])-12;
        result = temp.toString()+":"+nHour[1]+" PM";
      } else result = nHour[0]+":"+nHour[1]+" AM";
      return result;
    }
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Menu */
/**************************************************************************************************/
if (CurrentFrame == "/menu/") {
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Monitor */
/**************************************************************************************************/
if (CurrentFrame == "/monitor/") {
  LoadActivities();
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Monitoring */
/**************************************************************************************************/
if (CurrentFrame == "/monitoring/") {
  urlI = new URLSearchParams(window.location.search);
  index = parseInt(urlI.get("s"));
  unic = parseInt(urlI.get("u"));
  ElementsList = [
    {
      "title" : "Electrocardiograma",
      "Img1"  : "/static/images/illustrations/monitoring-sensor-ekg.png",
      "Img2"  : "/static/images/illustrations/monitoring-ekg.png",
      "button": "Continuar",
      "class" : "button square s60 yellow margin-right-20"
    }, {
      "title" : "Presión arterial",
      "Img1"  : "/static/images/illustrations/monitoring-sensor-pni.png",
      "Img2"  : "/static/images/illustrations/monitoring-pni.png",
      "button": "Continuar",
      "class" : "button square s60 yellow margin-right-20"
    }, {
      "title" : "Pulso oximetría",
      "Img1"  : "/static/images/illustrations/monitoring-sensor-spo2.png",
      "Img2"  : "/static/images/illustrations/monitoring-spo2.png",
      "button": "Continuar",
      "class" : "button square s60 yellow margin-right-20"
    }, {
      "title" : "Empezar monitoreo",
      "Img1"  : "/static/images/illustrations/monitoring-sensor-all.png",
      "Img2"  : "/static/images/illustrations/monitoring-all2.png",
      "button": "Empezar",
      "class" : "row-hidden"
    }
  ];
  document.getElementById("MTitle").innerHTML = ElementsList[index]["title"];
  document.getElementById("img1").src = ElementsList[index]["Img1"];
  document.getElementById("img2").src = ElementsList[index]["Img2"];
  document.getElementById("InfoButton").className = ElementsList[index]["class"];
  if(unic) document.getElementById("NextButton").innerHTML = "Empezar";
  else document.getElementById("NextButton").innerHTML = ElementsList[index]["button"];
  function MBack() {
    if (unic) window.location.href= "/menu/"
    else {
      if (index == 0) window.location.href= "/monitor/";
      else window.location.href= "/monitoring/?s="+(index-1)+"&u=0";
    }
  }
  function MNext() {
    if (unic) {
      if(index == 1) document.getElementById("MeasureValue").value=1;
      else document.getElementById("MeasureValue").value=0;
      document.getElementById("StartMeasuring").submit();
    }
    else {
      if (index == ElementsList.length-1) {
        document.getElementById("MeasureValue").value=1;
        document.getElementById("StartMeasuring").submit();
      }
      else window.location.href= "/monitoring/?s="+(index+1)+"&u=0";
    }
  }
  function InfoButton() {
    window.location.href= "/monitoringinfo/?s="+index;
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Monitoringinfo */
/**************************************************************************************************/
if (CurrentFrame == "/monitoringinfo/") {
  urlI = new URLSearchParams(window.location.search);
  index = urlI.get("s");
  ElementsList = [
    {
      "Title" : "Electrocardiograma",
      "Img"   : "/static/images/illustrations/monitoring-ekg.png",
      "Text"  : `
      Información de ayuda de posicionamiento de latiguillos y gráfica representativa del cable del parámetro.
      <img class="img-fluid" src="/static/images/instructions/ecg.png">
      <img class="img-fluid" src="/static/images/instructions/5-leads.png">
      `
    }, {
      "Title" : "Presión arterial",
      "Img"   : "/static/images/illustrations/monitoring-pni.png",
      "Text"  : `
      Información de ayuda del posicionamiento de la manga de presión y gráfica representativa del cable del parámetro
      <img class="img-fluid" src="/static/images/instructions/nibp.png">
      <img class="img-fluid" src="/static/images/instructions/nibpsensor.jpg">
      `
    }, {
      "Title" : "Pulso oximetría",
      "Img"   : "/static/images/illustrations/monitoring-spo2.png",
      "Text"  : `
      Información de ayuda de uso correcto del sensor y gráfica representativa del cable del parámetro
      <img class="img-fluid" src="/static/images/instructions/spo2.png">
      <img class="img-fluid" src="/static/images/instructions/spo2sensor.jpg">
      `
    }, {
      "Title" : "Monitoreo",
      "Img"   : "/static/images/illustrations/monitoring-all.png",
      "Text"  : "Información monitoreo"
    }
  ];
  document.getElementById("MonitorTitle").innerHTML = ElementsList[index]["Title"];
  document.getElementById("ImgMonitor").src = ElementsList[index]["Img"];
  document.getElementById("MonitorDescription").innerHTML = ElementsList[index]["Text"];
  function VideoButton() {
    window.location.href= "/monitoringinfov/?s="+index;
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* MonitoringinfoV */
/**************************************************************************************************/
if (CurrentFrame == "/monitoringinfov/") {
  urlI = new URLSearchParams(window.location.search);
  index = urlI.get("s");
  ElementsLis = [
    {
      "Title" : "Electrocardiograma",
      "Video" : "https://www.youtube.com/embed/2aBI9FQQu44"
    }, {
      "Title" : "Presión arterial",
      "Video" : "https://www.youtube.com/embed/2FMmAsHEYuE"
    }, {
      "Title" : "Pulso oximetría",
      "Video" : "https://www.youtube.com/embed/nVYgQS_XFJc"
    }, {
      "Title" : "Monitoreo",
      "Video" : "https://www.youtube.com/embed/s142yyS5rRE"
    }
  ];
  document.getElementById("VTitle").innerHTML = ElementsLis[index]["Title"];
  document.getElementById("DetailVid").src = ElementsLis[index]["Video"];
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Network */
/**************************************************************************************************/
if (CurrentFrame == "/network/") {
  new Splide( '#splide-network', {
    type:"slide",
    direction: 'ttb',
    height: '210px',
    autoHeight: true,
    perPage:3,
    perMove: 1,
    pagination:false,
  }).mount();
  function reloadPage() {
    window.location.href="/network/";
  }
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* Results */
/**************************************************************************************************/
if (CurrentFrame == "/results/") {
  Pulse=0,Spo2=0,Rr=0,Systole=0,Diastole=0,Mean=0,ECGw=0;
  if(document.getElementById("Pulse")) Pulse = parseInt(document.getElementById("Pulse").textContent);
  if(document.getElementById("SPO2")) Spo2 = parseInt(document.getElementById("SPO2").textContent);
  if(document.getElementById("RR")) Rr = parseInt(document.getElementById("RR").textContent);
  if(document.getElementById("Systole")) Systole = parseInt(document.getElementById("Systole").textContent);
  if(document.getElementById("Diastole")) Diastole = parseInt(document.getElementById("Diastole").textContent);
  if(document.getElementById("Mean")) Mean = parseInt(document.getElementById("Mean").textContent);
  if(document.getElementById("ECG")) ECGw = document.getElementById("ECG").textContent;
  function SendVitalSigns() {
    DataSend = {patient: {id:parseInt(localStorage.getItem("uid"))}, RR:Rr, SPO2:Spo2, Pulse:Pulse, Systolic:Systole, Diastolic:Diastole, MAP:Mean, ECG:ECGw};
    function Success() {
      localStorage.setItem("IDAlert",3);
      if (localStorage.getItem("IDActivity")) RegisterActivities();
      else window.location.href="/home/";
    }
    function ErrorF() {}
    POSTMethod(URLServer+"/api/v1/vitalsignrecords",DataSend,Success,ErrorF);
  }
  if(ECGw != "0") ECGWave(ECGw);
  setTimeout(SendVitalSigns,10000);//Send data after 10 seconds
}
/**************************************************************************************************/
/* Symptoms  */
/**************************************************************************************************/
if (CurrentFrame == "/symptoms/") {
  urlMorning = new URLSearchParams(window.location.search);
  Morning = urlMorning.get("morning");
  if(Morning == 'true') document.getElementById("iconMorning").src = "/static/images/assistant/assistant-question-l.png"
  else document.getElementById("iconMorning").src = "/static/images/assistant/assistant-question-l2.png"
  Data = GETMethod(URLServer+"/api/v1/symptoms?morning="+Morning);
  var index = 0;
  function LoadSymptoms(I) {
    document.getElementById("STitle").innerHTML = Data[I].description;
    document.getElementById("SImage").src = URLServer + Data[I].image;
  }
  function NoSymptom() {
    if(index < (Data.length-1)) {
      index++;
      LoadSymptoms(index);
    }
    else {
      if(Morning=="true") localStorage.setItem("IDAlert",6);
      else localStorage.setItem("IDAlert",7);
      if (localStorage.getItem("IDActivity")) RegisterActivities();
      else window.location.href="/home/";
    }
  }
  function YesSymptom() {
    swal("¿Estás seguro de enviar el síntoma?", {
      icon: "warning",
      buttons: {
        cancel: "No",
        catch: {value:true, text:"Sí"},
    }})
      .then((value) => {
        if(value) yesSend();
        else noSend();
    });
    function yesSend() {
      if(index < (Data.length-1)) {
        SaveSymptom(index);
        index++;
        LoadSymptoms(index);
      }
      else {
        if(Morning=="true") localStorage.setItem("IDAlert",6);
        else localStorage.setItem("IDAlert",7);
        if (localStorage.getItem("IDActivity")) RegisterActivities();
        else window.location.href="/home/";
      }
    }
    function noSend() {
      if(index < (Data.length-1)) {
        index++;
        LoadSymptoms(index);
      }
      else {
        if(Morning=="true") localStorage.setItem("IDAlert",6);
        else localStorage.setItem("IDAlert",7);
        if (localStorage.getItem("IDActivity")) RegisterActivities();
        else window.location.href="/home/";
      }
    }
  }
  function SaveSymptom(I) {
    data = {patient: {id:parseInt(localStorage.getItem("uid"))}, symptom: {id:Data[I]["id"]}};
    function Success() {}
    function ErrorF() {}
    POSTMethod(URLServer+"/api/v1/patientsymptoms",data,Success,ErrorF);
  }
  LoadSymptoms(index);
  LoadActivities();
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* User */
/**************************************************************************************************/
if (CurrentFrame == "/user/") {
  Data = GETMethod(URLServer+"/api/v1/users/profile");
  localStorage.setItem("uid", Data.id);
  document.getElementById("fullname").innerHTML = Data.name + " " + Data.lastName;
  document.getElementById("email").innerHTML = "Correo: " + Data.email;
  document.getElementById("age").innerHTML = "Edad: " + Data.age;
  document.getElementById("cc").innerHTML = Data.identificationType.name + ": " + Data.identificationNumber;
  document.getElementById("telephone").innerHTML = "Teléfono: " + Data.phone;
  document.getElementById("ubication").innerHTML = "Ubicación: "+ Data["city"].name+", "+Data["city"]["department"].name;
  document.getElementById("photo").src = Data.image;

  Data2 = GETMethod(URLServer+"/api/v1/patientgoals/"+Data.id);
  for(i=0; i<Data2.length; i++) {
    if (Data2[i].id == 2) localStorage.setItem("tExercise", Data2[i].minutes);
  }
  function LogoutUser() {
    localStorage.clear();
    window.location.href="/login/";
  }
  function Accept() {
    UpdateClock();
  }
  SaveActivities();
  setTimeout(Accept,7000);//Wait for 7 seconds to redirect
}
/**************************************************************************************************/
/* Weigth */
/**************************************************************************************************/
if (CurrentFrame == "/weigth/") {
  if(localStorage.getItem("weigth")) {
    document.getElementById("weigth").innerHTML = parseFloat(localStorage.getItem("weigth")).toFixed(1);
    localStorage.removeItem("weigth");
  } else {
    Data = GETMethod(URLServer+"/api/v1/weigthrecords/last");
    debugger
    if (!Data) document.getElementById("weigth").innerHTML = 50.1;
    else document.getElementById("weigth").innerHTML = parseFloat(Data.weigth).toFixed(1);
  }
  function AddWeight() {
    Weigth = parseFloat(document.getElementById("weigth").innerHTML);
    document.getElementById("weigth").innerHTML = (Weigth+0.1).toFixed(1);
  }
  function SubtractWeight() {
    Weigth = parseFloat(document.getElementById("weigth").innerHTML);
    document.getElementById("weigth").innerHTML = (Weigth-0.1).toFixed(1);
  }
  function SaveWeight() {
    Weigth = document.getElementById("weigth").innerHTML;
    localStorage.setItem("weigth", Weigth);
  }
  LoadActivities();
  setTimeout(BackHome,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
/* WeigthC */
/**************************************************************************************************/
if (CurrentFrame == "/weigthc/") {
  Weigth = parseFloat(localStorage.getItem("weigth")).toFixed(1);
  document.getElementById("weigth").innerHTML = Weigth;
  function SendWeigth() {
    Data = {patient: {id:parseInt(localStorage.getItem("uid"))}, weigth: Weigth};
    function Success() {
      localStorage.removeItem("weigth");
      localStorage.setItem("IDAlert",5);
      if (localStorage.getItem("IDActivity")) RegisterActivities();
      else window.location.href="/home/";
    }
    function ErrorF() {}
    POSTMethod(URLServer+"/api/v1/weigthrecords",Data,Success,ErrorF);
  }
  LoadActivities();
  setTimeout(SendWeigth,60000);//Wait for 1 minute to redirect
}
/**************************************************************************************************/
