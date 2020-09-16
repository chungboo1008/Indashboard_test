
  // var Dict = {{ Dict|safe }};
  
  
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
        mode:'tableSearch',
        step: 0,
        plan_id:'',
        fan: '',
        uploadData: '',
        url:'http://140.112.26.237:8002/media/clean_data.csv',
        imgurl:'http://140.112.26.237:8002/media/format.jpg',
        filename:'',
        listData: [],
        username:'',
        description:''
      },
      compute:{

      },
      methods:{
        go_to_home: function(){
          window.location.reload();
        },
        handleEdit(index, row) {
          console.log(index, row);
         },
        move_to_success:function(){
         alert("SUCCESS");
        },
        nextStep: function(){
          this.username = username;
          this.plan_id = plan_id;
          console.log(this.step);
          this.step++;
      
          if(this.step == 0){
           
          }
          if(this.step == 1){
            console.log(this.username);
            console.log(this.mode);
            
            const _this = this
            if (this.mode =='tableSearch'){
              const Data = {
                username: this.username,
                plan_id:this.plan_id
              }
              console.log(Data)
              $.ajax({
                    url: "http://140.112.26.237:8002/get_table_permission/",
                    type: "POST",
                    contentType: false,
                    data:JSON.stringify(Data),
                    processData:false,
                    async:false,
                    dataType: "json",
                    beforeSend: function(){
                      _this.ajaxing = true;
                    },
                    success: function (data) {
                      console.log("Success");
                      table_list = data.tables
                      alias_tables_list = data.alias_tables
                      for (i = 0; i < table_list.length; i++){
                            table_info = {
                              "id": i,
                              "table_name": table_list[i],
                              "alias_table_name":alias_tables_list[i]
                            }
                            _this.listData.push(table_info)
                            console.log(_this.listData)
                      }


                      // if(data.status=='ok'){
                      //   for (i = 0 ; i < table_list.length ; i++) {
                      //       console.log(table_list[i][0]);
                      //       table_infos = {
                      //         "id": i+1,
                      //         "table_name": table_list[i][0]
                      //       }
                      //       _this.listData.push(table_infos)
                      //   }
                        
                      // }
                      // else{
                      //   alert('您上傳的資料不是這支風機的資料表');
                      //   window.location.reload();
                      // }
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
           
          }
          if(this.step == 2){
           
          const _this = this;
          var formData = new FormData();
          formData.append('xml', document.getElementById("xml").files[0])
          $.ajax({
                url: "http://140.112.26.237:8002/api/file/upload_xml_file/",
                type: "POST",
                contentType: false,
                data :formData,
                processData:false,
                async:false,
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
                    alert('儲存失敗');
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
              const _this = this;
              saveData = {
                filename:this.filename,
                plan_id:this.plan_id,
                description:this.description
              }
              var create_table = $.ajax({
              
                url: "http://140.112.26.237:8002/api/file/create_table/",
                type: "POST",
                contentType: false,
                data:JSON.stringify(saveData),
                processData:false,
                async:false,
                dataType: "json",
                beforeSend: function(){
                  _this.ajaxing = true;
                },
                success: function (data) {
                  if(data.status == 'ok'){
                    
                    alert('您上傳的資料表成功');
                    window.location.reload();
                  }
                  else{
                    alert('您上傳的資料表失敗');
                    window.location.reload();
                  }
                },
                error: function(xhr, ajaxOptions, thrownError) {

                  console.log('error');
                  console.log(thrownError);
                  window.location.reload();// move to complete
                },
                complete: function(){
                  _this.ajaxing = false;
                  
                }
              });    
          }

          $('#setFan').modal('hide');
        },

      },
   })

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

