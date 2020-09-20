var app=new Vue(
    {
        el:'#app',
        data: {
          turbine:'mainsite_mli_g01',
          columns:[],
          width:'',
          hight:'',
          value9: [0, 1440],
          xColumns:[],
          yColumns:[],
          xData:[],
          yData:[],
          values:[],
          checkValue:[],
          tables_name:[],
          selected: [],
          step: 1,
          ajaxing: false,
          plan: "0",
          fan: '',
          temp:[],
          dashboarddata: [],
          charttype: 'line',
          chartStartTime: "2014-01-01T02:00",
          chartEndTime: "2014-01-01T12:00",
          uploadData: '',
          checked : false ,
          plan_id:'plan1'
        },
        watch:{
          turbine: function(value){
            this.change_columns(value);
          },
          values:function(value){
            this.changeX(value)
          },
        
        },
        computed:{
        },
        methods:{
          change_columns: function(turbine){
            header_parameter = {
                table:turbine,
            }
            const _this = this;
            
            $.ajax({
              //url: "http://140.112.26.237:8002/api/file/get_columns/",
              url: "http://127.0.0.1:8002/api/file/get_columns/",
              type: "POST",
              contentType: 'application/json; charset=utf-8',
              data :JSON.stringify(header_parameter),
              dataType: "json",
              async:true,
              beforeSend: function(){
                 _this.ajaxing = true;
              },
              success: function (data) {
                  _this.yColumns = []
                  _this.xColumns = []
                  for (i = 0; i < data.length ; i++){
                     var columns_info = {
                       id:i,
                       name:data[i]
                     }
                     _this.yColumns.push(columns_info)
                     _this.xColumns.push(columns_info)
                  }
                  console.log('print1');
                  console.log(_this.yColumns);
                  console.log(_this.xColumns);
              },
              error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
              },
              complete: function(){
                  _this.ajaxing = false;
                
              }
          });+
          console.log(_this.yColumns)
            
          },
          changeX :function(x){
            console.log("x?", x);
            this.yColumns=[] 
             
             for (i = 0;i<this.xColumns.length;i++){
               if (this.xColumns[i].name == x){
               }
               else{
                 this.yColumns.push(this.xColumns[i])
               }
              
             }
             console.log('print2');
            console.log(this.yColumns);
          },
          handleChange(value, direction, movedKeys) {
                console.log(value, direction, movedKeys);
                 if(direction === "right") {
                  console.log(this.yData)
                 }
                 if(direction === "left") {
                    
                 }
                    
          },
          nextStep: function(){
            console.log(this.step)
            this.step++;
            console.log(this.step)
            const _this = this
            if(this.step == 1){
              initMap();
            }
            else if(this.step == 2){
                  
            const header_parameter = {
              
              username:"admin",
              plan_id:1
            
            }
              $.ajax({
                  // url: "http://140.112.26.237:8002/get_table_permission/",
                  url: "http://127.0.0.1:8002/get_table_permission/",
                  type: "POST",
                  contentType: 'application/json; charset=utf-8',
                  data :JSON.stringify(header_parameter),
                  dataType: "json",
                  async:true,
                  beforeSend: function(){
                    _this.ajaxing = true;
                  },
                  success: function (data) {
                      _this.tables_name = data.tables_name                     
                      // console.log( _this.tables_name)
                      for (i = 0; i < _this.tables_name.length ; i++){
                      // console.log(_this.tables_name)
                        if(_this.turbine ==_this.tables_name[i].table_name){
                          for (j = 0 ;j < _this.tables_name[i].columns.length ; j++){ 
                                var columns_info = {
                                  id:j,
                                  name:_this.tables_name[i].columns[j].column_name
                                }
                                _this.yColumns.push(columns_info)
                                _this.xColumns.push(columns_info)
                          }
                        }  
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
                
            }else if(this.step == 3){
               console.log("type:",this.charttype);
              this.chartStartTime=this.chartStartTime.replace("T"," ")+":00"
              this.chartEndTime=this.chartEndTime.replace("T"," ")+":00"
              if(this.charttype=='line'){
                  var temp = {
                    "chart": {
                      "type": 'spline',
                      "zoomType":'y',
                    },
                    "title": {
                      'text': '風機資料'
                    },
                    'subtitle': {
                      
                    },
                    'xAxis': {
                     'type' : 'datetime',
                     'dateTimeLabelFormats': {
                        'second': '%e of %b'
                     },
                     'reversed': false,
                     'title': {
                       'enabled': true,
                       'text': 'X數值'
                     },
                     'labels': {
                        'format': '{value:%m-%d %H:%M}'//'{value:%y-%m-%d %H:%M}'
                     },
                     'maxPadding': 0.05,
                     'showLastLabel': true
                   },
                  'yAxis': {
                      'title': {
                        'text': 'Y數值'
                      },
                      'labels': {
                        'format': '{value}'
                      },
                      'lineWidth': 2
                    },
                    'legend': {
                      'enabled':true
                    },
                    'tooltip': {
                      'headerFormat': '<b>{series.name}</b><br/>',
                      'pointFormat': 'X={point.x:%Y-%m-%d %H:%M:%S} : Y={point.y}'
                    },
                    'plotOptions': {
                      'spline': {
                        'marker': {
                          'enable': true
                        }
                      },
                    },
                    'series': []
                    };
                  var json = temp;   
                  $('#chart').highcharts(json);  
                  var chart=new Object;
                  chart.type='chart';
                  chart.slotW=6;
                  chart.slotH=3;
                  chart.chartdata=json;
                  this.temp=chart;
                  console.log("cahrt", this.temp);
              }else if(this.charttype=='pie'){
                var chart = {
                     plotBackgroundColor: null,
                     plotBorderWidth: null,
                     plotShadow: false
                 };
                 var title = {
                    text: '風機資料'   
                 };      
                 var tooltip = {
                    pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
                 };
                 var plotOptions = {
                    pie: {
                       allowPointSelect: true,
                       cursor: 'pointer',
                       dataLabels: {
                          enabled: true,
                          format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
                          style: {
                             color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                          }
                       }
                    }
                 };
                 var series= [{
                    type: 'pie',
                    name: '各欄位比值',
                    data: [
                       ['JT_G01_COSPHI',   45.0],
                       ['JT_G01_DAYAVA',   26.8],
                       ['JT_G01_FREQ',     12.8],
                       ['JT_G01_MONTHAVA', 8.5],
                       ['JT_G01_NOMP',     6.9],
                       
                    ]
                 }];     
                    
                 var json = {};   
                 json.chart = chart; 
                 json.title = title;     
                 json.tooltip = tooltip;  
                 json.series = series;
                 json.plotOptions = plotOptions;
                 $('#chart').highcharts(json);  
                  var chart=new Object;
                  chart.type='chart';
                  chart.slotW=6;
                  chart.slotH=3;
                  chart.chartdata=json;
                  this.temp=chart;
                  
              }else if(this.charttype=='area'){
                var temp={
                   "chart" : {
                      "type": 'area',
                      "zoomType":'y'
                   },
                   "title" : {
                      "text": '風機資料面積圖'   
                   },
                   "subtitle":{
                     
                   },
                   "xAxis":{
                      "type":"datetime",
                      "dateTimeLabelFormats":{
                          "millisecond": '%H:%M:%S.%L',
                          "second": '%H:%M:%S',
                          "minute": '%H:%M',
                          "hour": '%H:%M',
                          "day": '%m-%d',
                          "week": '%m-%d',
                          "month": '%Y-%m',
                          "year": '%Y'
                      },
                   },
                   "yAxis":{
                      "title":{
                                  "text":'數值'
                              },
                      "min":null
  
                      
                      
                    },
                   "tooltip" : {
                      "pointFormat": '{series.name} produced <b>{point.y:,.2f}</b><br/>warheads in {point.x}'
                   },
                   "plotOptions" : {
                     "series": {
                        "pointStart": this.chartStartTime, // 开始值
                        "pointInterval": 10*60*1000 // 间隔一s
                      },
                      "area": {
                         "pointStart":  this.chartStartTime,
                         "marker": {
                            "enabled": false,
                            "symbol": 'circle',
                            "radius": 2,
                            "states": {
                               "hover": {
                                 "enabled": true
                               }
                            }
                         }
                      }
                   },
                   "series": []
                }
              }else if(this.charttype=='bar'){
                 var cha = {
                    type: 'column'
                 };
                 var title = {
                    text: '風機資料'   
                 };
                 var subtitle = {
                 };
                 var xAxis = {
                    categories: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
                    crosshair: true
                };
                 var yAxis = {
                    min: 0,
                    title: {
                       text: '數值'         
                    }      
                 };
                 var tooltip = {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                       '<td style="padding:0"><b>{point.y:.1f} </b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                 };
                 var plotOptions = {
                    column: {
                       pointPadding: 0.2,
                       borderWidth: 0
                    }
                 };  
                 var credits = {
                    enabled: false
                 };
                 
                 var series= [{
                      name: 'JT_G01_COSPHI',
                          data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
                      }, {
                          name: 'JT_G01_DAYAVA',
                          data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
                      }, {
                          name: 'JT_G01_FREQ',
                          data: [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6, 52.4, 65.2, 59.3, 51.2]
                      }, {
                          name: 'JT_G01_NOMP',
                          data: [42.4, 33.2, 34.5, 39.7, 52.6, 75.5, 57.4, 60.4, 47.6, 39.1, 46.8, 51.1]
                 }];     
                   var json = {};   
                   json.chart = cha; 
                   json.title = title;   
                   json.subtitle = subtitle; 
                   json.tooltip = tooltip;
                   json.xAxis = xAxis;
                   json.yAxis = yAxis;  
                   json.series = series;
                   json.plotOptions = plotOptions;  
                   json.credits = credits;
                   $('#chart').highcharts(json); 
                    var chart=new Object;
                    chart.type='chart';
                    chart.slotW=6;
                    chart.slotH=3;
                    chart.chartdata=json;
                    this.temp=chart;                 
  
              }else if(this.charttype=='scatter'){
                 var chart = {
                    type: 'scatter',
                  zoomType: 'xy'
                 };
                 var title = {
                    text: '風機資料-以X值為基底'   
                 };
                 var subtitle = {
                    text: 'Source: Heinz  2003'  
                 };
                 var xAxis = {
                    title: {
                    enabled: true,
                       text: this.values
                    },
                    startOnTick: true,
                    endOnTick: true,
                    showLastLabel: true
                 };
                 var yAxis = {
                    title: {
                       text: 'Y值'
                    }
                 };
                 var legend = {   
                    layout: 'vertical',
                    align: 'left',
                    verticalAlign: 'top',
                    x: 100,
                    y: 70,
                    floating: true,
                    backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
                    borderWidth: 1
                 }  
                 var plotOptions = {
                    scatter: {
                       marker: {
                          radius: 5,
                          states: {
                             hover: {
                                enabled: true,
                                lineColor: 'rgb(100,100,100)'
                             }
                          }
                       },
                       states: {
                          hover: {
                             marker: {
                                enabled: false
                             }
                          }
                       },
                       tooltip: {
                          headerFormat: '<b>{series.name}</b><br>',
                          pointFormat: '{point.x} cm, {point.y} kg'
                       }
                    }
                 };
                 var series= [];     
        
               var temp = {};   
               temp.chart = chart; 
               temp.title = title;   
               temp.subtitle = subtitle; 
               temp.legend = legend;
               temp.xAxis = xAxis;
               temp.yAxis = yAxis;  
               temp.series = series;
               temp.plotOptions = plotOptions;
               console.log(temp)
               $('#chart').highcharts(json);
                var chart=new Object;
                chart.type='chart';
                chart.slotW=6;
                chart.slotH=3;
                chart.chartdata=json;
                this.temp=chart;
    
              }else if(this.charttype=='combination'){
                 var title = {
                    text: '散佈圖加回歸線'   
                 };
                 var xAxis = {
                    min: -0.5,
                    max: 7
                 };
                 var yAxis= {
                    min: 0
                 };
                 var series= [{
                          type: 'line',
                          name: '回歸線',
                          data: [[0, 1.11], [7, 4.51]],
                          marker: {
                              enabled: false
                          },
                          states: {
                              hover: {
                                  lineWidth: 0
                              }
                          },
                          enableMouseTracking: false
                      }, {
                          type: 'scatter',
                          name: 'JT_G01_COSPHI',
                          data: [1, 1.5,2.1,2.8, 3.5, 3.9, 4.2,5.0],
                          marker: {
                              radius: 4
                          }
                      }
                 ];     
                    
                 var json = {};   
                 json.title = title;
                 json.xAxis = xAxis;
                 json.yAxis = yAxis;
                 json.series = series;
                 $('#chart').highcharts(json);
                var chart=new Object;
                chart.type='chart';
                chart.slotW=6;
                chart.slotH=3;
                chart.chartdata=json;
                this.temp=chart;  
              }else if(this.charttype=='wind_rose'){
                  var temp = {

                    chart: {
                        polar: true,
                        type: 'column'
                    },
            
                    title: {
                        text: '風花圖'
                    },
                    pane: {
                        size: '85%'
                    },
            
                    legend: {
                        reversed: true,
                        align: 'right',
                        verticalAlign: 'top',
                        y: 100,
                        layout: 'vertical'
                    },
                    xAxis: {
                        min: 0,
                        max: 360,
                        type: "",
                        tickInterval: 22.5,
                        tickmarkPlacement: 'on',
                    
                    },
                    yAxis: {
                        min: 0,
                        endOnTick: false,
                        showLastLabel: true,
                        title: {
                            text: 'Value'
                        },
                        labels: {
                            formatter: function () {
                                return this.value;
                            }
                        }
                    },
            
                    tooltip: {
                        valueSuffix: '%',
                        followPointer: true
                    },
            
                    plotOptions: {
                        series: {
                            stacking: 'normal',
                            shadow: false,
                            groupPadding: 0,
                            pointPlacement: 'on'
                        }
                    },
                    series: []
                  }
                  var json = temp;   
                  $('#chart').highcharts(json);  
                  var chart=new Object;
                  chart.type='chart';
                  chart.slotW=6;
                  chart.slotH=3;
                  chart.chartdata=json;
                  this.temp=chart;
              }else if(this.charttype=='heat_map'){
                 var chart = {      
                    type: 'heatmap',
                    marginTop: 40,
                    marginBottom: 80
                 };
                 var title = {
                    text: '風機欄位值熱區'   
                 };     
  
                 var xAxis = {
                    categories: ['JT_G01_COSPHI', 'JT_G01_DAYAVA', 'JT_G01_FREQ', 'JT_G01_MONTHAVA', 'JT_G01_NOMP', 'JT_G01_NROTOR', 'JT_G01_VANE', 'JT_G01_VWIND', 'JT_G01_GOPOS', 'JT_G01_Ambient_Temp']
                 };
                 
                 var yAxis = {
                    categories: ['Jun-16', 'Jul-16', 'Aug-16', 'Sep-16', 'Oct-16'],
                    title: null
                 };
                 
                 var colorAxis = {
                    min: 0,
                    // minColor: '#1ecc44',
                    // maxColor: '#f20c0c'
                    minColor: '#FFFFFF',
                    maxColor: '#fc0202'
                 };
  
                 var legend = {
                    align: 'right',
                    layout: 'vertical',
                    margin: 0,
                    verticalAlign: 'top',
                    y: 25,
                    symbolHeight: 280
                 };
  
                 var tooltip = {
                    formatter: function () {
                       return '<b>' + this.series.xAxis.categories[this.point.x] + '</b> sold <br><b>' +
                       this.point.value + '</b> items on <br><b>' + this.series.yAxis.categories[this.point.y] + '</b>';
                    }
                 };
  
                 var series= [{
                    name: 'Sales per employee',
                    borderWidth: 1,
                    data: [[0, 0, 10], [0, 1, 19], [0, 2, 8], [0, 3, 24], [0, 4, 67], [1, 0, 92], [1, 1, 58], [1, 2, 78], [1, 3, 117], [1, 4, 48], [2, 0, 35], [2, 1, 15], [2, 2, 123], [2, 3, 64], [2, 4, 52], [3, 0, 72], [3, 1, 132], [3, 2, 114], [3, 3, 19], [3, 4, 16], [4, 0, 38], [4, 1, 5], [4, 2, 8], [4, 3, 117], [4, 4, 115], [5, 0, 88], [5, 1, 32], [5, 2, 12], [5, 3, 6], [5, 4, 120], [6, 0, 13], [6, 1, 44], [6, 2, 88], [6, 3, 98], [6, 4, 96], [7, 0, 31], [7, 1, 1], [7, 2, 82], [7, 3, 32], [7, 4, 30], [8, 0, 85], [8, 1, 97], [8, 2, 123], [8, 3, 64], [8, 4, 84], [9, 0, 47], [9, 1, 114], [9, 2, 31], [9, 3, 48], [9, 4, 91]],
                    dataLabels: {
                       enabled: true,
                       color: '#000001'
                    }
                 }];    
                 var json={}; 
                 json.chart = chart; 
                 json.title = title;       
                 json.xAxis = xAxis; 
                 json.yAxis = yAxis; 
                 json.colorAxis = colorAxis; 
                 json.legend = legend; 
                 json.tooltip = tooltip; 
                 json.series = series;   
                 $('#chart').highcharts(json);
                var chart=new Object;
                chart.type='chart';
                chart.slotW=6;
                chart.slotH=3;
                chart.chartdata=json;
                this.temp=chart; 
  
              }else if(this.charttype=='polar_chart'){
                var temp = {
                  chart: {
                      polar: true
                  },
              
                  title: {
                      text: 'Highcharts Polar Chart'
                  },
              
                  subtitle: {
                      text: 'Also known as Radar Chart'
                  },
              
                  pane: {
                      startAngle: 0,
                      endAngle: 360
                  },
              
                  xAxis: {
                      tickInterval: 45,
                      min: 0,
                      max: 360,
                      labels: {
                          format: '{value}°'
                      }
                  },
              
                  yAxis: {
                      min: 0
                  },
              
                  plotOptions: {
                      series: {
                          pointStart: 0,
                          pointInterval: 45
                      },
                      column: {
                          pointPadding: 0,
                          groupPadding: 0
                      }
                  },
              
                  series: [{
                      type: 'column',
                      name: 'Column',
                      data: [8, 7, 6, 5, 4, 3, 2, 1],
                      pointPlacement: 'between'
                  }, {
                      type: 'line',
                      name: 'Line',
                      data: [1, 2, 3, 4, 5, 6, 7, 8]
                  }, {
                      type: 'area',
                      name: 'Area',
                      data: [1, 8, 2, 7, 3, 6, 4, 5]
                  }]
              }
                 var json={}; 
                 json.chart = chart; 
                 json.title = title; 
                 json.pane=pane;      
                 json.xAxis = xAxis; 
                 json.yAxis = yAxis; 
                 json.plotOptions = plotOptions; 
                 json.series = series;   
                 $('#chart').highcharts(json);
                var chart=new Object;
                chart.type='chart';
                chart.slotW=6;
                chart.slotH=3;
                chart.chartdata=json;
                this.temp=chart;
                            
              }
              const _this = this;
              var columns = _this.yData.concat(_this.values)
              const parameter = {
                columns:columns,
                table:_this.turbine,
                start_time:_this.chartStartTime,
                end_time:_this.chartEndTime
              };
              console.log("parameter");
              console.log(parameter);
              $.ajax({
               //  url: "http://140.112.26.237:8002/api/file/mli_to_json/",
                url: "http://127.0.0.1:8002/api/file/mli_to_json/",
                type: "POST",
                dataType: "json",
                data:JSON.stringify(parameter),
                async:false,
                beforeSend: function(){
                    _this.ajaxing = true;
                },
                success: function (data) {
                  console.log(data);
                  // var json = temp.chartdata;
                  if(temp.chart.type === "spline" && _this.values === "date_time"){
                     var chart=Highcharts.chart('chart',temp);
                     console.log(chart);
                     for(i=0;i<_this.yData.length;i++){
                        var arr = []
                        for(j=0;j<data[0][0].length;j++){
                           var tmp = [];
                           var datetime = new Date(data[0][0][j][_this.values]);
                           // var datetime = data[0][0][j][_this.values];
                           tmp.push(datetime);
                           // tmp.push(parseFloat(data[0][0][j][_this.values]));
                           tmp.push(parseFloat(data[0][0][j][_this.yData[i]]));
                           arr.push(tmp);
                        }
                        console.log(parameter.start_time);
                        var startDatetime = splitString(parameter.start_time);
                        var endDateime = splitString(parameter.end_time);

                        var sD = new Date(startDatetime);
                        var eD = new Date(endDateime);
                        var mSecond = eD.getTime() - sD.getTime();
                        console.log(mSecond);

                        function splitString(str){
                        var buf = str.split(" ");
                        var date = buf[0].split("-");
                        var time = buf[1].split(":");
                        var d = new Date();
                        d.setFullYear(date[0]);
                        d.setMonth(date[1]);
                        d.setDate(date[2]);
                        d.setHours(time[0]);
                        d.setMinutes(time[1]);
                        d.setSeconds(time[2]);
                        return d
                        }

                        const s = {
                           name:_this.yData[i],
                           data:arr,
                           pointStart: Date.UTC(startDatetime.getFullYear(), startDatetime.getMonth() - 1, startDatetime.getDate(), startDatetime.getHours(),startDatetime.getMinutes(),startDatetime.getSeconds()),
                           pointInterval: mSecond / data[0][0].length
                        }
                        console.log(s);
                        //   chart.series[i].update(s);
                        console.log(chart);
                        chart.addSeries(s);
                        console.log(chart);
                        //   var parseDate;
                        // //   var convrtDate;
                        for(j=0;j<data[0][0].length;j++){
                           // parseDateObj = parseDate(s.data[j][0]);
                           // convrtDate = new Date(Date.parse(parseDateObj));
                           // chart.series[0].xData[j] = convrtDate;
                           chart.xAxis[0].series[0].data[j].category = s.data[j][0];
                           chart.series[i].points[j].x = s.data[j][0];
                           // chart.series[0].xData[j] = s.data[j][0];
                        }
                        // chart.xAxis[0].options.labels.enabled = true;
                        //   console.log(chart.xAxis[0].options.labels.enabled);
                        // chart.redraw();
                        
                        
                        // console.log(chart);
                        // chart.addSeries(s);
                        // console.log(chart);
                        // // chart.series[0].data.pop();
                        // chart.series[0].data = s.data;
                        // chart.redraw();
                        console.log(chart);
                        temp.series.push(s);
                     
                     }
                     //add get data information
                     // chart.redraw();
                     console.log(temp);
                     temp.parameter = parameter;
                     console.log(temp);

                  }else{
                     var chart=Highcharts.chart('chart',temp);
                     console.log(chart);
                     for(i=0;i<_this.yData.length;i++){
                     var arr = []
                     for(j=0;j<data[0][0].length;j++){
                        var tmp = [];
                        tmp.push(parseFloat(data[0][0][j][_this.values]));
                        tmp.push(parseFloat(data[0][0][j][_this.yData[i]]));
                        arr.push(tmp);
                     }
                     const s = {
                        name:_this.yData[i],
                        data:arr,
                     }
                     console.log(s);
                     chart.addSeries(s);

                     temp.series.push(s);
                     }
                     //add get data information
                     console.log(temp);
                     temp.parameter = parameter;
                     console.log(temp);
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
            }
              $('#setFan').modal('hide');
          },
          saveToDashboard:function() {
             const _this = this;
             console.log("ID", _this.plan_id);
            $.ajax({
            //   url: "http://140.112.26.237:8002/api/dashboard/query/?plan_id="+_this.plan_id,
              url: "http://127.0.0.1:8002/api/dashboard/query/?plan_id="+_this.plan_id,
              type: "GET",
              dataType: "json",
              async:false,
              beforeSend: function(){
                _this.ajaxing = true;
              },
              success: function (data) {
                _this.dashboarddata = data[0].dashboard;
               //  console.log(_this.dashboarddata);
                const newDashboardData = data[0].dashboard;
               //  console.log(_this.temp);
                newDashboardData.push(_this.temp);
               //  console.log(newDashboardData);
                const saveDashboardData = {
                  plan_id: _this.plan_id,
                  dashboard: newDashboardData,
                };
               //  console.log(saveDashboardData);
                $.ajax({
                  // url: "http://140.112.26.237:8002/api/dashboard/1/save/",
                  url: "http://127.0.0.1:8002/api/dashboard/1/save/",
                  type: "POST",
                  contentType: 'application/json; charset=utf-8',
                  data :JSON.stringify(saveDashboardData),
                  dataType: "json",
                  async:false,
                  beforeSend: function(){
                     _this.ajaxing = true;
                  },
                  success: function (data) {
                    console.log(data);
                    console.log("save success");
                    alert("SAVE SUCCESS!");
                  },
                  error: function(xhr, ajaxOptions, thrownError) {
                    //console.log(JSON.stringify(saveData));
                    console.log('error');
                    console.log(thrownError);
                  },
                  complete: function(){
                     _this.ajaxing = true;
                  }
                });
              },
              error: function(xhr, ajaxOptions, thrownError) {
                console.log('error');
                console.log(thrownError);
              },
              complete: function(){
                _this.ajaxing = false;
              }
            });
          }
        },
        }
       
     )
  