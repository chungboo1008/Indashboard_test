
  
  function showLoading(){
    $('#loadingPanel').modal({
      backdrop: 'static',
      keyboard: false,
    });
  }

  function hideLoading(){
    $('#loadingPanel').modal('hide');
  }

  function showAlert(msg){
    $('#alertMsg').text(msg);
    $('#msgPanel').modal('show');
  }

  var app=new Vue(
  {
      el:'#app',
      data: {
        ajaxing:false,
        mode:'matlabUpload',
        message:'',
        value:'',
        x:'',
        des:'',
        url:'140.112.26.237',
        port:'9910',
        server_name:'matlab_server1',
        archive_name:'FFT',
        function_name:'fft',
        options:[],
        fan:'',
        image_path:'',
        csv_path:'',
        file_id:'',
        model_id:'',
        step: 0,
        plan: "0",
        label:'',
        uploadData: '',
        datas : [],
        table_data: [],
        username:'',
        parameter:'output.csv output.png'
      },
      computed:{
      },
      watch:{

      },
      methods:{
        nextStep: function(){
          this.step++;
          console.log(this.step);
          let _this = this;
          
          if(this.step == 1){
            _this.username = username
            const parameter = {
              "username":_this.username
            }
            if (this.mode =='exeExecution'){
              $.ajax({
                      url: "http://140.112.26.237:8002/api/file/get_matlab_permission/",
                      type: "POST",
                      contentType: false,
                      data : JSON.stringify(parameter),
                      processData: false,
                      async: false,
                      dataType: "json",
                      beforeSend: function(){
                        _this.ajaxing = true;
                      },
                      success: function (data) {
                        url_list = data.url
                        for (i = 0; i < url_list.length; i++){
                              matlab_info = {
                                value: i,
                                label: url_list[i]
                              }
                              _this.options.push(matlab_info)
                        }

                      },
                      error: function(xhr, ajaxOptions, thrownError) {      
                        console.log('error')
                        console.log(thrownError);
                      },
                      complete: function(){
                        _this.ajaxing = false;
                      }
                    });
            }
            console.log("Select Mode")
          }else if(this.step == 2){
            console.log("Input MATLAB information")
           
          }else if(this.step == 3){
            var formData = new FormData();
            formData.append('excel', document.getElementById("excel").files[0])
            var upload_file = $.ajax({
                  url: "http://140.112.26.237:8002/api/file/upload_file/",
                  type: "POST",
                  contentType: false,
                  data : formData,
                  processData: false,
                  async: true,
                  dataType: "json",
                  beforeSend: function(){
                    _this.ajaxing = true;
                    showLoading();
                  },
                  success: function (data) {
                    if(data.status=='ok'){
                      _this.filename=data.file_name;
                      console.log("成功儲存，檔名",_this.filename);
                      alert('儲存成功');
                    }
                    else{
                      alert('儲存失敗，檔案格式有誤');
                      window.location.reload();
                    }
                    
                  },
                  error: function(xhr, ajaxOptions, thrownError) {      
                    console.log('error')
                    console.log(thrownError);
                  },
                  complete: function(){
                    _this.ajaxing = false;
                    hideLoading();

                  }
              });
            $.when(upload_file).done(function(){
              const parameter = {
                url: _this.url,
                port : _this.port,
                deployable_archive :_this.archive_name,
                function_name :_this.function_name,
                filename : _this.filename
              }
              $.ajax({
                url: "http://140.112.26.237:8002/api/batch/execute_matlab/",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(parameter),
                dataType: "json",
                async:true,
                beforeSend: function(){
                    _this.ajaxing = true;
                    showLoading();
                },
                success: function (data) {
                  _this.table_data = data.data
                  _this.image_path = data.image
                  _this.csv_path = data.csv_file
                  console.log(data.status)
                  console.log(_this.table_data)
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                    _this.ajaxing = false;
                    hideLoading();
                }
              });
            }).fail(function(){
                    console.log("Error happening");
                    alert("Something go wrong! Email to r06525111@ntu.edu.tw")
            });
        }else if(this.step == 4){
          const parameter = {
                "username":_this.username,
                "url": _this.url,
                "port" : _this.port,
                "deployable_archive" :_this.archive_name,
                "function_name" :_this.function_name,
                "filename" : _this.filename,
                "permission_name": "abc is my permission",
                "description": "abc is my description",
                "table_name": "public.matlab_info",
                "is_active": true
            }
              $.ajax({
                url: "http://140.112.26.237:8002/api/file/insert_matlab_info/",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(parameter),
                dataType: "json",
                async:true,
                beforeSend: function(){
                    _this.ajaxing = true;
                    showLoading();
                },
                success: function (data) {
                  console.log(data.status);
                  alert('儲存成功！');
                  window.location.reload();
                  
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                  alert('儲存失敗，檔案格式有誤');
                },
                complete: function(){
                    _this.ajaxing = false;
                    hideLoading();
                }
              });
        }
        },
      },
   })

  function fillFilename() {
    $('.custom-file-input').on('change', function() { 
      let fileName = $(this).val().split('\\').pop(); 
      $(this).next('.custom-file-label').addClass("selected").html(fileName); 
   });
  }

