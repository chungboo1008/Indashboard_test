
function showLoading(){
    $('#loadingPanel').modal({
      backdrop: 'static',
      keyboard: false,
    });
}

function hideLoading(){
  $('#loadingPanel').modal('hide');
}
  
var app=new Vue(
  {
      el:'#app',
      data: {
        columns:[],
        column_info:[],
        checkedColumn:['date_time'],
        step: 1,
        ajaxing: false,
        plan: "0",
        chartStartTime: "2014-01-01T02:00",
        chartEndTime: "2014-01-01T12:00",
        uploadData: '',
        checked : false ,
        fan:'',
        table:'mli',
        turbine: 'mainsite_mli_g01',
        gt:[],
        datas:[],
        tables_name:[],
        table_info:[],
        alias_column_name:[],
        unit:[],
        yesData: [0]
      },
      watch:{
        turbine: function(value){
          this.change_columns(value);
        }
      },
      computed:{
      },
      methods:{
        
        handleChange(value, direction, movedKeys) {
            console.log(value, direction, movedKeys);
             //可以通过direction回调right/left 来进行操作，right：把数字移到右边，left把数据移到左边
             if(direction === "right") {
                
             }
             if(direction === "left") {
                
             }
                
        },
        change_columns: function(turbine){
          header_parameter = {
              table:turbine,
          }
          const _this = this;
          
          $.ajax({
            url: "http://140.112.26.237:8002/api/file/get_columns/",
            type: "POST",
            contentType: 'application/json; charset=utf-8',
            data :JSON.stringify(header_parameter),
            dataType: "json",
            async:true,
            beforeSend: function(){
               _this.ajaxing = true;
            },
            success: function (data) {
                _this.columns = []
                for (i = 0; i < data.length ; i++){
                   var columns_info = {
                     id:i,
                     name:data[i]
                   }
                   _this.columns.push(columns_info)
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
        
        csvExport(arrData) {
          let csvContent = "data:text/csv;charset=utf-8,";
          csvContent += [
            Object.keys(arrData[0]).join(","),
            ...arrData.map(item => Object.values(item).join(","))
          ]
          .join("\n")
          .replace(/(^\[)|(\]$)/gm, "");
          const data = encodeURI(csvContent);
          const link = document.createElement("a");
          link.setAttribute("href", data);
          link.setAttribute("download", "export.csv");
          link.click();
        },
        nextStep: function(){
          console.log(this.step)
          this.step++;

          if(this.step == 1){
            initMap(); 
            
          }
          else if(this.step==2){
            console.log(this.windfarm)
            if(this.windfarm=='other'){
              alert("該風場開發中...")
              window.location.reload();
            }
            const _this = this;
            $('#setFan').modal('hide');
            console.log(_this.turbine);
            console.log(this.table)
            
            const header_parameter = {
              
                username:"admin",
                plan_id:1
              
            }
            $.ajax({
                url: "http://140.112.26.237:8002/get_table_permission/",
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
                              _this.columns.push(columns_info)
                        }
                      }
                      
                        // console.log(_this.tables_name[i].columns[j].column_name)
                        // console.log(_this.tables_name[i].columns[j].alias_colum_name)
                        // _this.columns.append(_this.tables_name[i].columns[j].column_name)
                        // _this.column_name.append(_this.tables_name[i].columns[j].alias_colum_name)

                        
                      }
                      
                    
                     console.log(_this.columns);
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
            if (this.table =='other'){
              alert("系統開發中");
              location.reload();
            }         
            const _this=this;
            this.checkedColumn = []
            for (i = 0; i<this.yesData.length; i++){
                console.log(this.columns[this.yesData[i]].name);
                this.checkedColumn.push(this.columns[this.yesData[i]].name)
            }
            for (i = 0; i < _this.tables_name.length ; i++){
              if(_this.turbine ==_this.tables_name[i].table_name){
                _this.table_info = _this.tables_name[i]
              }
            }
            console.log("選中的",_this.table_info)
            for (k = 0;k<_this.checkedColumn.length;k++){
              console.log("cheC",_this.checkedColumn[k])
              for(j = 0;j<_this.table_info.columns.length;j++){
                if (_this.checkedColumn[k]==_this.table_info.columns[j].column_name){
                  // console.log("A",_this.table_info.columns[j])
                  var obj = {
                    "label":_this.table_info.columns[j].alias_colum_name,
                    "father":[{"label":_this.table_info.columns[j].unit,"children":[ {"label":_this.table_info.columns[j].column_name}]}],
                  }
                  _this.alias_column_name.push(obj)
                }
                  
                  _this.unit.push(_this.table_info.columns[j].unit)
                }
              }
               
              
                
          
            console.log(this.checkedColumn)
            console.log("Adasdf",_this.alias_column_name)
            console.log("Unit",_this.unit)

            const parameter = {
              columns:this.checkedColumn,
              table:this.turbine,
              start_time:this.chartStartTime,
	            end_time:this.chartEndTime
            };
            console.log(parameter)
            if (this.checkedColumn.length < 2){
              alert("至少選兩個")
              location.reload();
            }
            $.ajax({
              url: "http://140.112.26.237:8002/api/file/mli_to_json/",
              type: "POST",
              contentType: 'application/json; charset=utf-8',
              data :JSON.stringify(parameter),
              dataType: "json",
              async:false,
              beforeSend: function(){
                  _this.ajaxing = true;
              },
              success: function (data) {
                console.log(data);
                _this.datas=data[0][0];
                console.log(_this.datas)          
              },
              error: function(xhr, ajaxOptions, thrownError) {
                console.log('error');
                console.log(thrownError);
              },
              complete: function(){
                _this.ajaxing = false;
                
              }
            });

           

          
            // showLoading();
            // var get_header = $.ajax({
            //     url: "http://140.112.26.237:8002/api/file/header_to_json/",
            //     type: "POST",
            //     contentType: 'application/json; charset=utf-8',
            //     data :JSON.stringify(header_parameter),
            //     dataType: "json",
            //     async:true,
            //     beforeSend: function(){
            //        _this.ajaxing = true;
            //     },
            //     success: function (data) {
            //         data = JSON.stringify(data);
            //         data = data.replace(/[\[\]]/g,"");               
            //         data = JSON.parse(data);
            //         _this.column = data;
            //         // console.log(_this.column);
            //         _this.column = JSON.parse(_this.column);
            //         console.log(_this.column);
            //         // hideLoading();

            //     },
            //     error: function(xhr, ajaxOptions, thrownError) {
            //       console.log('error');
            //       console.log(thrownError);
            //     },
            //     complete: function(){
            //       _this.ajaxing = false;
                  
            //     }
            // });

            // $.when(get_header).done(function(){
            //   $.ajax({
            //     url: "http://140.112.26.237:8002/api/file/mli_to_json/",
            //     type: "POST",
            //     contentType: 'application/json; charset=utf-8',
            //     data :JSON.stringify(parameter),
            //     dataType: "json",
            //     async:true,
            //     beforeSend: function(){
            //        _this.ajaxing = true;
            //     },
            //     success: function (data) {
            //       _this.datas=data[0];
            //       console.log(_this.datas)          
            //     },
            //     error: function(xhr, ajaxOptions, thrownError) {
            //       console.log('error');
            //       console.log(thrownError);
            //     },
            //     complete: function(){
            //       _this.ajaxing = false;
                  
            //     }
            //   });
            // }).fail(function(){
            //   console.log("Error happening");
            //   alert("Something go wrong! Email to r06525111@ntu.edu.tw")
            // });
            // 在這裡已上是原本的
            //this.column=JSON.parse(this.column);// from string convert to a object 
            // console.log(this.column);
            // console.log(this.column_name);
            $('#setFan').modal('hide');
          }else if(this.step == 4){
            location.reload();
          }
      },
     
      }
      
   
   
  })


   
  