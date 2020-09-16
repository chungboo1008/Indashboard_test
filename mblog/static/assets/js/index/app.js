
$(document).ready(function () {
    $("#sidebar").mCustomScrollbar({
        theme: "minimal"
    });

    $('#dismiss, .overlay').on('click', function () {
        $('#sidebar').removeClass('active');
        $('.overlay').removeClass('active');
    });

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').addClass('active');
        $('.overlay').addClass('active');
        $('.collapse.in').toggleClass('in');
        $('a[aria-expanded=true]').attr('aria-expanded', 'false');
    });
});
function showLoading(){
$('#loadingPanel').modal({
backdrop: 'static',
keyboard: false,
});
}

function hideLoading(){
$('#loadingPanel').modal('hide');
}

function initApp(){
app = new Vue(
{
el:'#app',
data: {
circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
plan: '',
ajaxing: false,
mode: 'normal',
$mainContain: null,
$grid: null,
dashboarddata: [],
modeltypes: [
  {
    name: 'text',
    showName: '文字',
  },{
    name: 'image',
    showName: '圖像',
  },{
    name: 'chart',
    showName: '資料視覺化',
  },
  {
    name: 'video',
    showName: 'Youtube影片',
  },
],
selectingtype: '',
widgeSizeW: 3,
widgeSizeH: 6,
widgeSizeH_chart:3,
widgeSizeW_chart:6,
textContent: '',
textSize: '.10em',
imgurl: '',
videourl: '',
editingObjId: '',
editingBgColor: 'rgb(255,255,255)',
editingFtColor: 'rgb(0,0,0)',
theme:[],
select_color:'ui',
},
watch: {
widgeSizeW: function(val){
            let tmp = parseInt(val);
            if(isNaN(tmp)){
                this.widgeSizeW = 1;
            }else{
    if(tmp > 0 && tmp<=12){
      this.widgeSizeW = tmp;
    }else{
      this.widgeSizeW = 1;
    }
            }
        },
widgeSizeH: function(val){
            let tmp = parseInt(val);
            if(isNaN(tmp)){
                this.widgeSizeH = 1;
            }else{
    if(tmp>0 && tmp<=6){
      this.widgeSizeH = tmp;
    }else{
      this.widgeSizeH = 1;
    }

            }
        },
widgeSizeH_chart: function(val){
  let tmp = parseInt(val);
  if(isNaN(tmp)){
    this.widgeSizeH_chart = 3;
  }else{
    if(tmp>0 && tmp<=6){
      this.widgeSizeH_chart = tmp;
    }else{
      this.widgeSizeH_chart = 3;
    }

  }
},
widgeSizeW_chart: function(val){
  let tmp = parseInt(val);
  if(isNaN(tmp)){
    this.widgeSizeW_chart = 6;
  }else{
    if(tmp>1 && tmp<=12){
      this.widgeSizeW_chart = tmp;
    }else{
      this.widgeSizeW_chart = 6;
    }

  }
 },
},
computed:{
videoInputID: function(){
  name = 'v';
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(this.videourl);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
},
editingObj: function(){
  for(var i=0;i<this.dashboarddata.length;i++){
    if(this.dashboarddata[i].eleId && this.dashboarddata[i].eleId == this.editingObjId){
      return this.dashboarddata[i];
    }
  }
  return null;
},
},
methods:{
setSize: function(newW, newH){
  this.widgeSizeW = newW;
  this.widgeSizeH = newH;
},
toEditMode: function(){
  if(this.mode == 'normal'){
    const itemList = this.$grid.getItems();
    for(var i in itemList){
      const ele = itemList[i];
      $(ele._element).addClass('edit-style');
    }
    this.mode = 'edit';
  }
},
endEditMode: function(){
  if(this.mode == 'edit'){
    const itemList = this.$grid.getItems();
    for(var i in itemList){
      const ele = itemList[i];
      $(ele._element).removeClass('edit-style');
    }
    this.mode = 'normal';
  }
  this.$grid.synchronize();
  this.saveDashboard();
},
generateOuter: function(obj, id){
  var $div = $('<div></div>');
  $div.addClass('item');
  $div.attr('id', id);
  obj.eleId = id;

  $div.addClass('sw' + obj.slotW);
  $div.addClass('sh' + obj.slotH);

  var $inner = $('<div></div>');
  $inner.addClass('item-content');

  if(obj.bgColor){
    $inner.css('background-color', obj.bgColor);
  }

  if(obj.ftColor){
    $inner.css('color', obj.ftColor);
  }

  var $del = $('<span></span>');
  $del.addClass('editmode-model');
  $del.addClass('del-model');
  $del.text('X');

  var $edit = $('<span></span>');
  $edit.addClass('editmode-model');
  $edit.addClass('edit-model');
  $edit.text('編輯');

  $div.append($inner);
  $div.append($edit);
  $div.append($del);

  $del.on('click', removeBtnClicked);
  $edit.on('click', editBtnClicked);

  return $div;
},


parseTextElement: function(obj, index){

  var $div = $('<div></div>');
  var $t = $('<span></span>');
  $t.css('font-size', obj.size);
  $t.css('text-align', 'left');
  $t.text(obj.text);
  $div.append($t);
  $div.css('display', 'flex');
  $div.css('justify-content', 'left');
  $div.css('align-items', 'center');

  return $div;
},

parseImageElement: function(obj){
  var $img = $('<img/>');
  $img.attr('src', obj.url);
  $img.addClass('item-img');
  return $img;
},

parseChartElement: function(obj){
  var $chartdiv = $('<div></div>');
  $chartdiv.addClass('chart-div');
  $chartdiv.attr('id', 'chart_' + obj.eleId);
  return $chartdiv;
},

parseVideoElement: function(obj){
  var $t = $('<div class="videoWrapper"></div>');
  var $v = $('<iframe src="https://www.youtube.com/embed/'+obj.videoId+'?rel=0&showinfo=0" frameborder="0" allow="encrypted-media" allowfullscreen></iframe>');
  $t.append($v);
  return $t;
},

parseElement: function(obj, id){
  var $outer = this.generateOuter(obj, id);
  var $content;

  if(obj.type == 'text'){
    $content = this.parseTextElement(obj);
  }else if(obj.type == 'image'){
    $content = this.parseImageElement(obj);
  }else if(obj.type == 'chart'){
    $content = this.parseChartElement(obj);
  }else if(obj.type == 'video'){
    $content = this.parseVideoElement(obj);
  }else {
    return null;
  }
  $outer.find('.item-content').append($content);
  return $outer;
},
readDashboard: function(plan_id){
  const _this = this;
  $.ajax({
    url: "http://localhost:8002/api/dashboard/query/?plan_id="+plan_id,
    type: "GET",
    dataType: "json",
    beforeSend: function(){
          _this.ajaxing = true;
        },
    success: function (data) {
      // console.log(data[0].dashboard);
      _this.dashboarddata = data[0].dashboard;
      // console.log(_this.dashboarddata);
      _this.dashboardInit();

            },
            error: function(xhr, ajaxOptions, thrownError) {
                console.log('error');
                console.log(thrownError);
            },
        complete: function(){
          _this.ajaxing = false;
        }
  });
},
getDashboardDataByDragSort: function(){
  let res = [];
  const sortItem = this.$grid.getItems();
  for(let i = 0; i<sortItem.length;i++){
    const ele = sortItem[i]._element;
    for(let j=0;j<this.dashboarddata.length;j++){
      if(ele == this.dashboarddata[j].ele){
        let temp = {...this.dashboarddata[j]};
        temp.ele = undefined;
        res.push(temp);
        break;
      }
    }
  }
  return res;
},

saveDashboard: function(){
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  const sortedData = this.getDashboardDataByDragSort();
  const saveData = {
    plan_id: '{{ plan_id }}',
    dashboard: sortedData,
    csrfmiddlewaretoken:'{{ csrftoken }}',
  };
  const _this = this;
  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
  $.ajax({
    url: "http://localhost:8002/api/dashboard/{{ plan_id_id }}/save/",
    type: "POST",
    contentType: 'application/json; charset=utf-8',
    data :JSON.stringify(saveData),
    dataType: "json",

    beforeSend: function(){
      console.log(csrftoken);
          _this.ajaxing = true;
        },
    success: function (data) {
                    console.log(data);
     


            },
            error: function(xhr, ajaxOptions, thrownError) {
      console.log(JSON.stringify(saveData));
                console.log('error');
                console.log(thrownError);
            },
        complete: function(){
          _this.ajaxing = false;
        }
  });
},

dashboardInit: function(){
  const _this = this;
  $('.grid *').remove(); // all widget remove

  for(var i in this.dashboarddata){

    var obj = this.dashboarddata[i];
    var $ele = this.parseElement(obj, 'item-'+i);
    // console.log($ele);

    if($ele != null){
      $('.grid').append($ele);

      obj.ele = $ele[0];
      if(obj.type == 'chart'){
        Highcharts.chart('chart_' + obj.eleId, obj.chartdata);

      }
    }
  }

  for(var i in this.dashboarddata){
    var obj = this.dashboarddata[i];
    var ele = obj.ele;

  }

  this.$grid = new Muuri('.grid', {
    dragEnabled: true,
    dragStartPredicate: function (item, event) {
      // Prevent first item from being dragged.
      if (app.mode != 'edit') {
        return false;
      }
      // For other items use the default drag start predicate.
      return Muuri.ItemDrag.defaultStartPredicate(item, event);
    },
  });
},

addPanelInit: function(){
  this.widgeSizeW = 1;
  this.widgeSizeH = 1;
  this.selectingtype = this.modeltypes[0].name;
  this.textContent = '';
  this.textSize = '.7em';
  this.imgurl = '';
  this.videoInputID = '';
},

addTextModel: function(){
  var temp = {};
  temp.type = 'text';
  temp.text = this.textContent;
  temp.size = this.textSize;
  temp.slotW = this.widgeSizeW;
  temp.slotH = this.widgeSizeH;
  //console.log(temp);
  this.pushModel(temp);
},

addVideoModel: function(){
  var temp = {};
  temp.type = 'video';
  temp.videoId = this.videoInputID;
  temp.slotW = this.widgeSizeW;
  temp.slotH = this.widgeSizeH;
  //console.log(temp);
  this.pushModel(temp);
},

addChartModel:function() {
  const _this = this;
  $.ajax({
    url: "http://140.112.26.237:8002/api/dashboard/query/?plan_id={{ plan_id }}",
    type: "GET",
    dataType: "json",
    beforeSend: function(){
      _this.ajaxing = true;
    },
    success: function (data) {
      console.log(data[0].dashboard);
      _this.chartData = data[0].dashboard[1];
      console.log(_this.chartdata);


    },
    error: function(xhr, ajaxOptions, thrownError) {
      console.log('error');
      console.log(thrownError);
    },
    complete: function(){
      _this.ajaxing = false;
    }
  });
  var temp={};
  temp.type='chart';
  temp.chartData=this.chartData;
  temp.slotW = this.widgeSizeW;
  temp.slotH = this.widgeSizeH;
},

addImageModel: function(){
  showLoading();
  const _this = this;
  var formData = new FormData();
  formData.append('image', document.getElementById("image").files[0])
   $.ajax({
        url: "http://140.112.26.237:8002/api/file/upload_image/",
        type: "POST",

        contentType: false,
        data :formData,
        processData:false,
        dataType: "json",
        async: false,
        beforeSend: function(){
          _this.ajaxing = true;
        },
        success: function (response) {
          if(response.status=='ok'){
             var url=response.url;

             var temp = {};
             temp.type = 'image';
             temp.url = response.url;
             temp.slotW = _this.widgeSizeW;
             temp.slotH = _this.widgeSizeH;
             console.log(temp);
             _this.pushModel(temp);

          }
          else{
            alert('儲存失敗');
          }

        },
        error: function(xhr, ajaxOptions, thrownError) {

          console.log('error');
          console.log(thrownError);
        },
        complete: function(){
          _this.ajaxing = false;
        }
      });

},

pushModel: function(m){
  const _this = this;
  var $ele = this.parseElement(m, this.dashboarddata.length);

  if($ele != null){
    this.$grid.add($ele[0]);
    m.ele = $ele[0];
  }
  this.dashboarddata.push(m);
  this.saveDashboard();
  this.closePanel();
},

closePanel: function(){
  $('#addContent').modal('hide');
},

showEditModal: function(eleId){
  this.editingObjId = eleId;
  showLoading();
    const _this=this;
    $.ajax({
        url: "http://colormind.io/list/",
        type: "GET",
        dataType: "json",
        async: false,
        beforeSend: function(){
          _this.ajaxing = true;
        },
        success: function (response) {
          console.log(response.result);
          _this.theme=response.result;
              
        },
        error: function(xhr, ajaxOptions, thrownError) {

          console.log('error');
          console.log(thrownError);
        },
        complete: function(){
          _this.ajaxing = false;
        }
    });

  //這邊將現有內容同步給編輯中物件
  if(this.editingObj.bgColor){
    this.editingBgColor = this.editingObj.bgColor;
  }else{
    this.editingBgColor = 'rgb(255,255,255)';
  }
  if(this.editingObj.ftColor){
    this.editingFtColor = this.editingObj.ftColor;
  }else{
    this.editingFtColor = 'rgb(0,0,0)';
  }
  $('#editContent').modal('show');
},

applyEdit: function(){
  this.editingObj.bgColor = this.editingBgColor;
  this.editingObj.ftColor = this.editingFtColor;
  $(this.editingObj.ele).find('.item-content').css('background-color', this.editingObj.bgColor);
  $(this.editingObj.ele).find('.item-content').css('color', this.editingObj.ftColor);
  $('#editContent').modal('hide');
},
generateColor: function(){
    const _this=this;
    saveData={
        model:_this.select_color
    }
    showLoading();
   $.ajax({
        url: "http://colormind.io/api/",
        type: "POST",
        data :JSON.stringify(saveData),
        dataType: "json",
        async: false,
        beforeSend: function(){
          _this.ajaxing = true;
        },
        success: function (response) {
          for(i=0;i<5;i++){
            console.log(response.result[i]);    
          }
          var colorArray=response.result[0]
          console.log(colorArray[0]);
          console.log(colorArray[1]);
          console.log(colorArray[2]);
          var rgb="rgb("+colorArray[0]+","+colorArray[1]+","+colorArray[2]+")"
          console.log(rgb)
          _this.editingBgColor=rgb
              
        },
        error: function(xhr, ajaxOptions, thrownError) {

          console.log('error');
          console.log(thrownError);
        },
        complete: function(){
          _this.ajaxing = false;
        }
      });
},
resetColor: function(){
  this.editingBgColor = 'rgb(255,255,255)';
  this.editingFtColor = 'rgb(0,0,0)';
},
},
});
}


function addBtnClick(){
app.addPanelInit();
$('#addContent').modal('show');
}

var $t;
function removeBtnClicked(evt){
var r = confirm("確定刪除此元件?");
if (r == true) {
$t = $(evt.currentTarget).parent();
for(var i in app.dashboarddata){
if(app.dashboarddata[i].ele == $t[0]){
  app.dashboarddata.splice(i, 1);
  break;
}
}
app.$grid.remove($t[0],{removeElements: true});
}
}

function editBtnClicked(evt){
var $temp = $(evt.currentTarget).parent();
// console.log($temp.attr('id'));
app.showEditModal($temp.attr('id'));


}

$(document).ready(function(){
initApp();
app.readDashboard('{{plan_id}}');
// app.dashboardInit();
/*
串接成功後，上面這一行改為：
app.readDashboard();
*/

});