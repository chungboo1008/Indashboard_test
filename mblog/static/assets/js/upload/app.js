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
        step: 1,
        plan: "0",
        fan: '',
        username:'',
        plan_id:'',
        uploadData: '',
        url:'http://140.112.26.237:8002/media/clean_data.csv',
        imgurl:'http://140.112.26.237:8002/media/format.jpg',
        filename:'',    
        turbine:'',
        alias_table_name:[],
        tables_name:[],
        windfarm:''
      },
      compute:{

      },
      methods:{
        
        nextStep: function(){
          console.log(this.step)
          this.step++;
          if(this.step == 1){
           
          }
          if(this.step == 2){
          
            const _this = this;
            this.username = username
              this.plan_id = plan_id
              console.log(this.plan_id )
            
            var formData = new FormData();
            formData.append('excel', document.getElementById("excel").files[0])
            $.ajax({
                  url: "http://140.112.26.237:8002/api/file/upload_file/",
                  type: "POST",
                  contentType: false,
                  data : formData,
                  processData: false,
                  async: false,
                  dataType: "json",
                  beforeSend: function(){
                    _this.ajaxing = true;
                  },
                  success: function (data) {
                    if(data.status=='ok'){
                      _this.filename=data.file_name;
                      console.log(_this.filename);
                      alert('儲存成功');
                    }
                    else{
                      alert('儲存失敗，檔案格式有誤');
                      window.location.reload();
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
          if(this.step == 3){
            console.log(this.step)
            if (this.table =='other'){
                alert("其他風場系統開發中...")
            }
            // initMap();
            const _this = this;
            
              const Data = {
                    username: this.username,
                    plan_id:this.plan_id
              }
              console.log(Data)
              var getTables = $.ajax({
                    url: "http://140.112.26.237:8002/get_table_permission/",
                    type: "POST",
                    contentType: false,
                    data:JSON.stringify(Data),
                    processData:false,
                    async:true,
                    dataType: "json",
                    beforeSend: function(){
                      _this.ajaxing = true;
                    },
                    success: function (data) {
                      _this.tables_name = data.tables
                      
                    },
                    error: function(xhr, ajaxOptions, thrownError) {

                      console.log('error');
                      console.log(thrownError);
                    },
                    complete: function(){
                      _this.ajaxing = false;
                    }
                });
                $.when(getTables).done(function(){
                    var saveData = {
                        filename:_this.filename,
                        table:_this.turbine
                    }
                    console.log(saveData)
                    $.ajax({
                        url: "http://140.112.26.237:8002/api/file/upload_to_db/",
                        type: "POST",
                        contentType: false,
                        data:JSON.stringify(saveData),
                        processData:false,
                        async:true,
                        dataType: "json",
                        beforeSend: function(){
                                           
                          _this.ajaxing = true;
                        },
                        success: function (data) {
                          if(data.status=='ok'){
                            alert("成功輸入資料庫") 
                            window.location.reload();
                          }
                          else{
                            alert('您上傳的資料的資料有誤，請重新檢查一次');
                            window.location.reload();
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
                  }).fail(function(){
                        console.log("Error happening");
                });
             
             
        
       
          }
         
          
          $('#setFan').modal('hide');
        },
        
      },
   })

   console.log(app)
    var map;
   function initMap() {
     var center = {lng:120.686 , lat: 24.137};
     var fanImg = 'http://140.112.26.237:8002/media/disp_img/fan.png';
     var fake1 = {lng: 120.212, lat: 23.817};
     var fake2 = {lng: 121.752, lat: 25.153};
     map = new google.maps.Map(document.getElementById('map'), {
       center: {lng: 120.957929, lat: 23.469896},
       zoom: 8
     });
     var fmarker1 = new google.maps.Marker({position: fake1, map: map, icon: fanImg});
     fmarker1.addListener('click', function(evt){
       app.fan = '麥寮風場';
       app.table='mli';
       const Data = {
        username: app.username,
        plan_id:app.plan_id
        }

        $.ajax({
                url: "http://140.112.26.237:8002/get_table_permission/",
                type: "POST",
                contentType: false,
                data:JSON.stringify(Data),
                processData:false,
                async:false,
                dataType: "json",
                beforeSend: function(){
                
                },
                success: function (data) {
                    app.tables_name = data.tables_name
                    console.log(data.tables)
                    console.log(app.tables_name )

                },
                error: function(xhr, ajaxOptions, thrownError) {

                console.log('error');
                console.log(thrownError);
                },
                complete: function(){
                
                }
            });
       selectFanDialog();
     });
     var fmarker2 = new google.maps.Marker({position: fake2, map: map, icon: fanImg});
     fmarker2.addListener('click', function(evt){
       app.fan = '其他風場';
       app.table='other';
       selectFanDialog();
     });
   }

   function selectFanDialog(){
     $('#setFan').modal({
       keyboard: false
     });
   }
   function selectUploadDialog(){
     $('#uploadStatus').modal({
       keyboard: false
     });
   }
   function fillFilename() {
     $('.custom-file-input').on('change', function() { 
       let fileName = $(this).val().split('\\').pop(); 
       $(this).next('.custom-file-label').addClass("selected").html(fileName); 
    });
   }