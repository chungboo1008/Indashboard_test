var map;
function initMap() {
  
  var center = {lng:120.686 , lat: 24.137};
  var fanImg = 'http://140.112.26.237:8002/media/disp_img/fan.png';
  var fake1 = {lng: 120.212, lat: 23.817};
  var fake2 = {lng: 121.752, lat: 25.153};
 //  var fake3 = {lng: 119.611, lat: 23.619};
 //  var fake4 = {lng: 120.376, lat: 24.083};
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lng: 120.957929, lat: 23.469896},
    zoom: 8
  });
  var fmarker1 = new google.maps.Marker({position: fake1, map: map, icon: fanImg});
  fmarker1.addListener('click', function(evt){
    app.fan = '麥寮風場';
    selectFanDialog();
  });
  var fmarker2 = new google.maps.Marker({position: fake2, map: map, icon: fanImg});
  fmarker2.addListener('click', function(evt){
    app.fan = '其他風場';
    selectFanDialog();
  });
    
}

function selectFanDialog(){
  $('#setFan').modal({
    keyboard: false
  });
}