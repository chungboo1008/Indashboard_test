
  // const username = '{{ username }}';  
  function showLoading(){
    $('#loadingPanel').modal({
      backdrop: 'static',
      keyboard: false,
    });
  }
  window.onload = function()
  {
    
      let urlParams = new URLSearchParams(window.location.search);
      if(urlParams.get('step')==null & urlParams.get('step')==null & urlParams.get('value')==null){
        this.app.step = 0;
        this.app.mode = 'exeUpload';
        this.app.value = '';
      }
      else{
        console.log(urlParams.get('step')); 
        console.log(urlParams.get('mode')); 
        console.log(urlParams.get('value'));
        this.app.step = urlParams.get('step')
        this.app.mode = urlParams.get('mode')
        this.app.value = urlParams.get('value')
        var parameter = {
          "username":'hsin'
        }
        const _this = this
        $.ajax({
          url: "http://140.112.26.237:8002/api/file/get_file_permission/",
          type: "POST",
          contentType: false,
          data : JSON.stringify(parameter),
          processData: false,
          async: false,
          dataType: "json",
          beforeSend: function(){
           
          },
          success: function (data) {
            file_list = data.files
            doc_path = data.docs
            output1 = data.output1
            output2 = data.output2

            for (i = 0; i < file_list.length; i++){
                  file_info = {
                    value: i,
                    label: file_list[i],
                    doc:doc_path[i],
                    output1:output1[i],
                    output2:output2[i]
                  }
                  console.log(file_info)
                  _this.app.options.push(file_info)
            }

          },
          error: function(xhr, ajaxOptions, thrownError) {      
            console.log('error')
            console.log(thrownError);
          },
          complete: function(){
           
          }
        });
     

      }

    
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
        mode:'exeUpload',
        value:'',
        options:[],
        message:'',
        x:'',
        des:'',
        url:'',
        fan:'',
        file_id:'',
        model_id:'',
        step: 0,
        plan: "0",
        label:'',
        uploadData: '',
        inputData:'',
        datas : [],
        filename:'',
        filepath:'',
        docpath:[],
        docname:'',
        image_path:'',
        ajaxing: false,
        output1:'result.txt',
        output2:'windfarm.bmp',
        plan_id:0
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
          _this.username = username
          _this.plan_id = plan_id
            console.log("PI", _this.plan_id)
          if(this.step == 1){
            console.log(this.mode);
            var parameter = {
              "username":username
            }
            if (this.mode =='exeExecution'){
              $.ajax({
                      url: "http://140.112.26.237:8002/api/file/get_file_permission/",
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
                        file_list = data.files
                        doc_path = data.docs
                        output1 = data.output1
                        output2 = data.output2
                        for (i = 0; i < file_list.length; i++){
                              file_info = {
                                value: i,
                                label: file_list[i],
                                doc:doc_path[i],
                                output1:output1[i],
                                output2:output2[i]
                              }
                              _this.options.push(file_info)
                        }
                        console.log(_this.options)

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
          }else if(this.step == 2){
            if (this.mode == 'exeUpload'){
                var formData = new FormData();
                formData.append('exe', document.getElementById("exe").files[0])
                if (document.getElementById("input").files[0]!=undefined){
                    formData.append('input',document.getElementById("input").files[0])
                }
                var upload_file = $.ajax({
                      url: "http://140.112.26.237:8002/api/file/upload_exe_file/",
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
                          _this.filename = data.file_name;
                          _this.filepath = data.file_path;
                          _this.docname = data.doc_name;
                          _this.docpath = data.doc_path;
                          console.log("成功儲存，檔名",_this.filename);
                          console.log(_this.docpath)
                          alert('儲存成功');
                        }
                        else{
                          console.log(data);
                          alert('儲存失敗，檔案格式有誤');
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
                $.when(upload_file).done(function(){
                    console.log(_this.username)
                    console.log(_this.filename)
                    console.log(_this.filepath)
                    console.log(_this.docname)
                    console.log(_this.docpath)
                    var file_info = {
                      "username": _this.username,
                      "file_name": _this.filename,
                      "file_path": _this.filepath,
                      "doc_name":_this.docname,
                      "doc_path":_this.docpath,
                      "table_name": "file",
                      "description": "abc is my description",
                      "permission_name": "No permission",
                      "plan_id":_this.plan_id
                    }
                    $.ajax({
                        url: "http://140.112.26.237:8002/api/file/insert_file_info/",
                        type: "POST",
                        contentType: false,
                        data : JSON.stringify(file_info),
                        processData: false,
                        async: false,
                        dataType: "json",
                        beforeSend: function(){
                          _this.ajaxing = true;
                        },
                        success: function (data) {
                          if(data.status=='ok'){
                            _this.filename=data.file_name;
                            console.log("成功儲存至資料庫");
                            alert('儲存成功');
                            window.location.reload();
                          }
                          else{
                            console.log(data)
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
                        }
                      });

                }).fail(function(){
                    console.log("Error happening");
                    
                });
            }
            else{
              console.log(this.options)
              for(i = 0;i<_this.options.length;i++){
                if(_this.options[i].label == _this.value){
                  _this.docname = "http://140.112.26.237:8002" + _this.options[i].doc
                  _this.output1 = _this.options[i].output1
                  _this.output2 = _this.options[i].output2
                }
                }
            }
          }else if(this.step == 3){
            // upload input.excel
            
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
                      _this.filename = data.file_name;
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
                  }
            });
            
            
            var input = {
              "exeFile":this.value,
              "inputFile":this.filename,
              "outputFile1":this.output1,
              "outputFile2":this.output2

            }
            console.log(input)
            if (this.mode == 'exeExecution'){
              
             
              $.ajax({
                  url: "http://140.112.26.237:8002/api/batch/execute_wine/",
                  type: "POST",
                  dataType: "json",
                  data:JSON.stringify(input),
                  async:true,
                  beforeSend: function(){
                    _this.ajaxing = true;
                    showLoading();
                  },
                  success: function (data) {
                      var status = data['status']
                      var outputFile = data['outputFile']
                      var outputImage = data['outputImage']
                      
                      // var chart=Highcharts.chart('chart',temp);
                      if ( status !='ok' ){
                        alert("程式執行錯誤，請檢查輸入檔案是否有誤！")
                      }
                      else{
                         // for table
                          // for( i = 1; i<datas[0]['Wave.Height (m) '].length; i++ ){
                            
                          //   var data = {
                          //     "a":datas[0][title_name[0]][i],
                          //     "b":datas[0][title_name[1]][i],
                          //     "c":datas[0][title_name[2]][i],
                          //     "d":datas[0][title_name[3]][i]
                          //   }
                          //   _this.datas.push(data)
                          // }
                          // // for drawing chart
                          // for (i = 0;i<title_name.length ;i ++ ){
                          //     let s = {
                          //       name:title_name[i],
                          //       data:datas[0][title_name[i]]
                          //     }
                          //     chart.addSeries(s);
                          //     temp.series.push(s);
                          // }
                          _this.url = outputFile
                          _this.image_path = outputImage
                          console.log( _this.url)
                          console.log(_this.image_path)

                      }
                     
                      // console.log(_this.datas)
                     
                  },
                  error: function(xhr, ajaxOptions, thrownError) {
                    console.log('error');
                    console.log(thrownError);
                  },
                  complete: function(){
                      console.log('Execution Finish!');
                      _this.ajaxing = false;
                      hideLoading();
                  }
              });

              
            }
           
          }

        },
      },
   })

   function fillFilename() {
    $('.custom-file-input').on('change', function() { 
      
      let fileName = $(this).val().split('\\').pop(); 
      console.log(fileName)
      $(this).next('.custom-file-label').addClass("selected").html(fileName); 
   });
  }

