
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
        checkValue:[],
        checkValue2:[],
        checkValue3:[],
        checkValue4:[],
        checkValue5:[],
        method:'regression',
        regression_algotype:'linear-regression',
        abnormal_algotype:'svm',
        cluster_algotype:'birch',
        classification_algotype:'knn',
        message:'',
        x:'',
        des:'',
        url:'',
        image_path:'',
        mse:'',
        file_id:'',
        model_id:'',
        step: 1,
        plan: "0",
        fan: '',
        case:'',
        label:'',
        cols: [
          {
            name: 'JT_G01_COSPHI',
            selected: true,
          },
          {
            name: 'JT_G01_DAYAVA',
            selected: true,
          },
          {
            name: 'JT_G01_FREQ',
            selected: true,
          },
          {
            name: 'JT_G01_MONTHAVA',
            selected: true,
          },
          {
            name: 'JT_G01_NOMP',
            selected: true,
          },
          {
            name:'JT_G01_NROTOR',
            selected:true,
          },
          { 
            name:'JT_G01_VANE',
            selected:true,
          },
          {
            name: 'JT_G01_I_L1',
            selected: true,
          },
        ],
        cols1: [ 'JT_G01_COSPHI','JT_G01_DAYAVA','JT_G01_FREQ','JT_G01_MONTHAVA','JT_G01_NOMP','JT_G01_NROTOR','JT_G01_VANE','JT_G01_I_L1'],
        chartStartTime: "2015-06-09T02:00",
        chartEndTime: "2015-06-16T00:00",
        uploadData: '',
        checked : false,
        checked5: false,
        checked4: false,
      },
      computed:{
        selectedCol: function(){
          var temp = 0;
          for( var i in this.cols){
            if(this.cols[i].selected){
              temp += 1;
            }
          }
          return temp;
        },
      },
      watch:{
         checkValue(curVal){
           if(curVal.length == this.cols.length){  
                        this.checked = true  
                    }else{  
                        this.checked = false  
                    }  

        },
        checkValue3(curVal){
          if(curVal.length == this.checkValue2.length){  
                        this.checked4 = true  
                    }else{  
                        this.checked4 = false  
                    }  
        },
        checkValue4(curVal){
          if(curVal.length == this.checkValue3.length){  
                        this.checked5 = true  
                    }else{  
                        this.checked5 = false  
                    }  
        }
      },
      methods:{
        selectAll(event){
                        if (!event.currentTarget.checked) {
                            this.checkValue = [];
                        } else { 
                            this.checkValue = [];
                            this.cols.forEach((item, i) =>{
                                this.checkValue.push(item.name);
                            });
                        }
        },
        selectAll4(event){
                        if (!event.currentTarget.checked) {
                            this.checkValue3 = [];
                        } else { 
                            this.checkValue3 = [];
                            this.checkValue2.forEach((item, i) =>{
                                this.checkValue3.push(item);
                            });
                        }
        },
        selectAll5(event){
                        if (!event.currentTarget.checked) {
                            this.checkValue4 = [];
                        } else { 
                            this.checkValue4 = [];
                            this.checkValue3.forEach((item, i) =>{
                                this.checkValue4.push(item);
                            });
                        }
        },
        saveToDashboard:function() {
          // body...
           const _this = this;
          $.ajax({
            url: "http://140.112.26.237:8002/api/dashboard/query/?plan_id={{ plan_id}}",
            type: "GET",
            dataType: "json",
            async:false,
            beforeSend: function(){

              _this.ajaxing = true;
            },
            success: function (data) {
              
              _this.dashboarddata = data[0].dashboard;
               console.log(_this.dashboarddata);
                var image=new Object;
                image.type='image';
                image.slotW=6;
                image.slotH=4;
                image.url=_this.image_path;
                _this.temp=image;
              

              const newDashboardData = data[0].dashboard;
              
          

              newDashboardData.push(_this.temp);
              const saveDashboardData = {
                plan_id: '{{ plan_id }}',
                dashboard: newDashboardData,
                // csrfmiddlewaretoken:'{{ csrftoken }}',
              };
              $.ajax({
                url: "http://140.112.26.237:8002/api/dashboard/1/save/",
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
         },
        nextStep: function(){
          console.log(this.step);
          let _this = this;
          if(this.step == 1){
            initMap();
            _this.step++;
            $('#setFan').modal('hide');
            console.log(this.method);
          }else if(this.step == 2){
            for(var i=0;i<this.checkValue.length;i++){
              this.checkValue2.push(this.checkValue[i]);     
            }
            for(var i=0;i<this.checkValue2;i++){
              console.log(this.checkValue2[i]); //for next input
            }            
            showLoading();
            const _this=this;
            const file_parameter = {
                filename:"output.csv",
                start_time:_this.chartStartTime,
                end_time:_this.chartEndTime,
                checkValue:_this.checkValue
            };
            $.ajax({
                url: "http://140.112.26.237:8002/api/file/download_file/",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(file_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {   
                    _this.url=data.url;// assign url
                    console.log(_this.url);
                    hideLoading();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
             _this.step++;
          }else if(this.step == 3){ 
            //(1) 資料上傳  此動作會產生file_id供下一步使用
            const _this=this;
            console.log(this.method);
            if(_this.method=='cluster'){//clustering parameter
                var csv_parameter = {
                    download_url: _this.url,
                    file_name: "csv_file.csv",
                    user_id: "alice",
                    project_id: "my_project",
                    project_type:"clustering",
                    stage: "data-preprocess",
                    label: ""
                    };
            
            }else{
                var csv_parameter = {
                    download_url: _this.url,
                    file_name: "csv_file.csv",
                    user_id: "alice",
                    project_id: "my_project",
                    project_type:_this.method,
                    stage: "data-preprocess",
                    label: _this.label.toLowerCase() 
                };
            }
            console.log()
            $.ajax({
                url: "http://140.112.26.241:8002/csv",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(csv_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                    var status=data.status;
                    var des=data.description;
                    var file_id=data.file_id;
                    _this.file_id=data.file_id;//file_id
                    console.log("(資料上傳)"+"Status:"+status+",Description:"+des+".File ID:"+file_id);
                    hideLoading();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
             _this.step++;
          }else if(this.step == 4){
             //(2.0)pre-save
             for(var i=0;i<this.checkValue3.length;i++){
                this.checkValue3[i]=this.checkValue3[i].toLowerCase();
             }
            showLoading();
            const _this=this;
            const save_parameter = {
                new_file_name: "pr_file.csv",
                normalize: "MinMaxScaler",
                feature_list: _this.checkValue3
            };
            const pre_parameter={
                feature_name: _this.label.toLowerCase(),
                filter_std: 1,
                missing_value: true,
                interval_number: 10
            };
            $.ajax({
                url: "http://140.112.26.241:8002/preprocess-preview/"+_this.file_id,
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(pre_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                    var status=data.status;
                    var des=data.description;
                    var file_id=data.tmp_file_id;
                    console.log("(前處理預覽)"+"Status:"+status+",Description:"+des+".File ID:"+file_id);
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
            $.ajax({
                url: "http://140.112.26.241:8002/preprocess-save/"+_this.file_id,
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(save_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                    var status=data.status;
                    var des=data.description;
                    var file_id=data.new_file_id;
                    //_this.file_id=file_id;
                    console.log("(前處理儲存)"+"Status:"+status+",Description:"+des+".File ID:"+file_id);
                    _this.step++;
                    hideLoading();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
          }else if(this.step == 5){
            // training
            for(var i=0;i<this.checkValue3.length;i++){
                this.checkValue3[i]=this.checkValue3[i].toLowerCase();
             }
            showLoading();
            if(this.method=='abnormal-detection'){
                const algo_parameter={
                  file_id: _this.file_id,
                  new_file_name: "selected_feature", 
                  model_name: "svm_model",
                  arguments: {
                    gamma: 0.5,
                    nu: 0.5,
                    kernel: 'rbf',
                    degree: 3
                  }
                };
                $.ajax({
                  url: "http://140.112.26.241:8002/algo/one-class_SVM/do",
                  type: "POST",
                  contentType: 'application/json; charset=utf-8',
                  data :JSON.stringify(algo_parameter),
                  dataType: "json",
                  async:false,
                  beforeSend: function(){
                    _this.ajaxing = true;       
                  },
                  success: function (data) {
                    var status=data.status;
                    var des=data.description;
                    _this.model_id=data.model_id; //model id
                    console.log("(執行演算法)"+"Status:"+status+",Description:"+des);
                    console.log("XXXX!!");
                    hideLoading();
                  },
                  error: function(xhr, ajaxOptions, thrownError) {
                    console.log('error');
                    console.log(thrownError);
                  },
                  complete: function(){
                    _this.ajaxing = true;
                  }
                });
                const model_pr_parameter={
                  model_id: _this.model_id,
                  x_axis: _this.x.toLowerCase(),
                  y_axis: "jt_g01_cosphi"
                };
                // model preview
                $.ajax({
                    url: "http://140.112.26.241:8002/model-preview/"+_this.file_id,
                    type: "POST",
                    contentType: 'application/json; charset=utf-8',
                    data :JSON.stringify(model_pr_parameter),
                    dataType: "json",
                    async:false,
                    beforeSend: function(){
                      _this.ajaxing = true;       
                    },
                    success: function (data) {
                        var status=data.status;
                        var des=data.description;
                        var preurl='http://140.112.26.241:8002';
                        _this.image_path=preurl+data.image_path;
                        console.log("(模型預覽)"+"Status:"+status+",Description:"+des+"  "+_this.image_path);
                        //(5)資料預測 吃三種變數 一種是訓練模型所產生的model id 另外一個是前處理產生的file_id 最後一種是演算法種類
                        //最後會生MSE
                        hideLoading();
                        _this.step++;
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                      console.log('error');
                      console.log(thrownError);
                    },
                    complete: function(){
                      _this.ajaxing = true;
                    }
                });   
            }else if(this.method=='cluster'){
                const algo_parameter={
                    file_id: _this.file_id,
                    new_file_name: "selected_feature", 
                    model_name: "birch_model",
                    arguments: {
                      branching_factor:50,
                      n_clusters:3,
                      threshold:0.5
                    }
                };
                console.log(algo_parameter);
                $.ajax({
                    url: "http://140.112.26.241:8002/algo/birch_R06546014/do",
                    type: "POST",
                    contentType: 'application/json; charset=utf-8',
                    data :JSON.stringify(algo_parameter),
                    dataType: "json",
                    async:false,
                    beforeSend: function(){
                        _this.ajaxing = true;       
                    },
                    success: function (data) {
                        console.log("Doing Clustering");
                        var status=data.status;
                        var des=data.description;
                        _this.model_id=data.model_id; //model id
                        console.log("(執行演算法)"+"Status:"+status+",Description:"+des);
                        hideLoading();
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                        console.log('error');
                        console.log(thrownError);
                    },
                    complete: function(){
                        _this.ajaxing = true;
                    }
                    });
                var model_pr_parameter={
                    model_id: _this.model_id,
                    x_axis: _this.x.toLowerCase(),
                    y_axis: _this.label.toLowerCase() 
                };
                $.ajax({
                    url: "http://140.112.26.241:8002/model-preview/"+_this.file_id,
                    type: "POST",
                    contentType: 'application/json; charset=utf-8',
                    data :JSON.stringify(model_pr_parameter),
                    dataType: "json",
                    async:false,
                    beforeSend: function(){
                       _this.ajaxing = true;       
                    },
                    success: function (data) {
                        var status=data.status;
                        var des=data.description;
                        var preurl='http://140.112.26.241:8002';
                        _this.image_path=preurl+data.image_path;
                        console.log("(模型預覽)"+"Status:"+status+",Description:"+des+"  "+_this.image_path);
                        _this.step++;
                        console.log(_this.step)
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                      console.log('error');
                      console.log(thrownError);
                    },
                    complete: function(){
                       _this.ajaxing = true;
                    }
                });
            }else{
                  const algo_parameter={
                    file_id: _this.file_id,
                    new_file_name: "selected_feature", 
                    model_name: "linear_model",
                    arguments: {
                      fit_intercept:true,
                      normalize: true,
                      copy_X: true,
                      n_jobs: 1
                    }
                  };
            $.ajax({
                url: "http://140.112.26.241:8002/algo/linear-regression/do",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(algo_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                  var status=data.status;
                  var des=data.description;
                  _this.model_id=data.model_id; //model id
                  console.log("(執行演算法)"+"Status:"+status+",Description:"+des);
                  hideLoading();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
            const model_pr_parameter={
                  model_id: _this.model_id,
                  x_axis: _this.x.toLowerCase(),
                  y_axis: _this.label.toLowerCase() 
            };
            // model preview
            $.ajax({
                url: "http://140.112.26.241:8002/model-preview/"+_this.file_id,
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(model_pr_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                    var status=data.status;
                    var des=data.description;
                    var preurl='http://140.112.26.241:8002';
                    _this.image_path = preurl + data.image_path;
                    console.log("(模型預覽)"+"Status:"+status+",Description:"+des+"  "+_this.image_path);
                    _this.step++;
                    console.log(_this.step)
                    hideLoading();
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });
            const model_predict_parameter={
                  model_id: _this.model_id,
                  file_id: _this.file_id 
            };
            $.ajax({
                url: "http://140.112.26.241:8002/model-predict/regression",
                type: "POST",
                contentType: 'application/json; charset=utf-8',
                data :JSON.stringify(model_predict_parameter),
                dataType: "json",
                async:false,
                beforeSend: function(){
                   _this.ajaxing = true;       
                },
                success: function (data) {
                      var status=data.status;
                      var des=data.description;
                      var mse=data.performance.mean_square_error;
                      _this.mse=mse.toFixed(4);
                      console.log("(模型預測)"+"Status:"+status+",Description:"+des+",MSE:"+mse);
                      _this.step++;
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                   _this.ajaxing = true;
                }
            });

            }


        
          }
        }
      },
   })


   function selectFanDialog(){
     $('#setFan').modal({
       keyboard: false
     });
   }