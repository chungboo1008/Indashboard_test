


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
      step: 1,
      text:'',
      ajaxing:false,
      loading: false,
      search_result:[],
      device_result:[],
      tableData: {},
      scenery:'search',
      search_mode:'tableSearch',
      links: [],
      state: '',
      timeout:  null,
      keywords:[],
      loading: true,
      device_name: '',
      value2: 1,
      colors: ['#99A9BF', '#F7BA2A', '#FF9900'],
      fb_url1:  null,
      fb_url2:  null,
      iframe_url : null,
      textarea:'',
      tableData: [{
        "methods":"AAAA"
      }],
      recommand_methods: [],
      recommand_papers:[],
      select_papers:[],
      select_usecases:[],
      dialogVisible:false,
      dialogVisibleUseCase:false,
      DialogVisibleMode:false
    },
    methods:{
      handleMore(index, row) {
        this.dialogVisible = true;
        this.select_papers = []
        for (i = 0; i<this.recommand_papers.length; i++){
          if (row.methods == this.recommand_papers[i].method){
              console.log(this.recommand_papers[i].method)
              console.log(row.methods)
              this.select_papers.push(this.recommand_papers[i])
          }
        }
        console.log(this.select_papers)
      },
      handleUseCase(index, row){
        this.dialogVisibleUseCase = true;
        for (i = 0; i<this.recommand_papers.length; i++){
          if (row.methods == this.recommand_papers[i].method){
              console.log(this.recommand_papers[i].method)
              console.log(row.methods)
              this.select_usecases.push(this.recommand_papers[i])
          }
        }
      },
      handleGo(index, row) {
        
        if(row.methods =='風場模擬程式WFSim')
          window.location.href='http://140.112.26.237:8002/exe/?step=1&value=WFSim.exe&mode=exeExecution'

      },
      nextStep: function(){
        console.log(this.step);
        if(this.step == 1){
          this.step++;
          console.log(this.search_mode)
        }else if(this.step == 2){
          
          const _this=this
          this.step++;
          var input={
            "keyword":this.text
          }
          var device_name ={
            "device":this.device_name
          }
          if (this.scenery == 'device'){
            const loading = this.$loading({
                    lock: true,
                    text: '資料載入中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                    
                    });
            $.ajax({
                url: "http://140.112.26.237:8002/api/file/get_device_info/",
                type: "POST",
                dataType: "json",
                data:JSON.stringify(device_name),
                async:true,
                beforeSend: function(){
                    
                    
                },
                success: function (data) {
                   
                  for(i=0;i<data.length;i++){
                    
                    var paper={
                      'title':data[i][1],
                      'equiment':data[i][2],
                      'problem':data[i][3],
                      'algorithm':data[i][4],
                      'result':data[i][5],
                      'time':data[i][6],
                      
                    }
                   
                    _this.device_result.push(paper)
                  }
                  console.log(_this.device_result)
                
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                    loading.close();
                    console.log('Get all device paper!');
                  
                }
            });
            
          }
          if (this.scenery=='search'){
            const loading = this.$loading({
                    lock: true,
                    text: '資料載入中...',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                    
                    });
                if (_this.search_mode =='tableSearch'){
                    $.ajax({
                        url: "http://140.112.26.237:8002/api/file/read_paper/",
                        type: "POST",
                        dataType: "json",
                        data:JSON.stringify(input),
                        async:true,
                        beforeSend: function(){

                        },
                        success: function (data) {
                          
                          for(i=0;i<data.length;i++){
                            
                            var paper = {
                              'id':data[i][0],
                              'c_title':data[i][1],
                              'e_title':data[i][2],
                              'c_keyword':data[i][3],
                              'e_keyword':data[i][4],
                              'year':data[i][5],
                              'url':data[i][6],
                              'abstract':data[i][7],
                            }
                          
                            _this.search_result.push(paper)
                          }
                        
                        },
                        error: function(xhr, ajaxOptions, thrownError) {
                          console.log('error');
                          console.log(thrownError);
                        },
                        complete: function(){
                            loading.close();
                            console.log('Get all keywords!');
                            console.log(_this.search_result)
                          
                        }
                    });
                }
                else if(this.search_mode =='tableCreate'){
                    $.ajax({
                      url: "http://140.112.26.237:8002/api/file/google_search/",
                      type: "POST",
                      dataType: "json",
                      data:JSON.stringify(input),
                      async:true,
                      beforeSend: function(){
      
                      },
                      success: function (data) {
                        
                        for(i=0;i<data.length;i++){
                          
                          var paper = {
                            'c_title':data[i]['title'],
                            'url':data[i]['url'],
                            'abstract':data[i]['abstract'],
                          }
                        
                          _this.search_result.push(paper)
                        }
                      
                      },
                      error: function(xhr, ajaxOptions, thrownError) {
                        console.log('error');
                        console.log(thrownError);
                      },
                      complete: function(){
                          loading.close();
                          console.log('Get all keywords!');
                        
                      }
                  });
                }
          }
          else if(this.scenery=='knowlege-graph'){

            var keyword_input={
              "keyword":this.text,
              "topn":10
            }
            const loading = _this.$loading({
                      lock: false,
                      text: '資料載入中...',
                      spinner: 'el-icon-loading',
                      background: 'rgba(0, 0, 0, 0.7)',
                      
            });
          
            var Get_Keywords=$.ajax({
              url: "http://140.112.26.237:8002/api/file/get_keywords/",
              type: "POST",
              dataType: "json",
              data:JSON.stringify(keyword_input),
              async:true,
              beforeSend: function(){ 
                console.log("loading");
              },
              success: function (data) {
                _this.keywords = data.keywords;
                var pair = []
                _this.keywords.forEach(function(item){
                  pair.push([_this.text,item])
                });
                console.log( _this.keywords)
                Highcharts.addEvent(
                  Highcharts.seriesTypes.networkgraph,
                  'afterSetOptions',
                  function (e) {
                    var colors = Highcharts.getOptions().colors,
                      i = 0,
                      nodes = {};
                    e.options.data.forEach(function (link) {

                      if (link[0] === _this.text) {
                        nodes[_this.text] = {
                          id: _this.text,
                          marker: {
                            radius: 25
                          }
                        };
                        nodes[link[1]] = {
                          id: link[1],
                          marker: {
                            radius: 20
                          },
                          color: colors[i++]
                        };
                      } else if (nodes[link[0]] && nodes[link[0]].color) {
                        nodes[link[1]] = {
                          id: link[1],
                          color: nodes[link[0]].color
                        };
                      }
                    });

                    e.options.nodes = Object.keys(nodes).map(function (id) {
                      return nodes[id];
                    });
                  }
                );
                var temp = {
                  "chart": {
                    "type": 'networkgraph',
                    "height": '100%'
                  },
                  "title": {
                    "text": '知識圖譜'
                  },
                  "plotOptions": {
                    "networkgraph": {
                      "keys": ['from', 'to'],
                      "layoutAlgorithm": {
                        "enableSimulation": true,
                        "friction": -0.9
                      }
                    }
                  },
                  "series": [{
                    "dataLabels": {
                      "enabled": true,
                      "linkFormat": ''
                    },
                    "data": pair
                  }]
                }
                
                Highcharts.chart('container', temp );
           
              },
              error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
              },
              complete: function(){
                  console.log('Get all keywords!');
                  loading.close()

              }
            });
            $.when(Get_Keywords).done(function(){
              var input={
                        "keyword":_this.keywords
                        }
              $.ajax({
                    url: "http://140.112.26.237:8002/api/file/read_papers/",
                    // url:"http://140.112.26.237:8002/api/file/google_search_graph/",
                    type: "POST",
                    dataType: "json",
                    data:JSON.stringify(input),
                    async: false,
                    beforeSend: function(){
                      console.log("starting loading");
                    },
                    success: function (data) {
                      _this.keywords=[]
                      for(i = 0;i < input['keyword'].length;i++){
                        
                        // one_paper = data[input['keyword'][i]]
                        if (data[input['keyword'][i]].length!=0){
                          _this.keywords.push(input['keyword'][i])
                        }
                      }
                      console.log(data)
                      
                      for(i = 0; i < 5; i++){
                        one_paper=data[input['keyword'][i]]
                        var papers=[]
                        for(k = 0; k <one_paper.length; k++){
                             // handle url1 and url2
                    
                              var paper = {
                                'id':one_paper[k][0],
                                'c_title':one_paper[k][1],
                                'e_title':one_paper[k][2],
                                'c_keyword':one_paper[k][3],
                                'e_keyword':one_paper[k][4],
                                'year':one_paper[k][5],
                                'url':one_paper[k][6],
                                'abstract':one_paper[k][7],
                              }
                              papers.push(paper)
                              console.log(papers)
                      
                              
                              _this.fb_url1 = one_paper[k][6].substring(23,28)
                              _this.fb_url2 = one_paper[k][6].substring(29,35)
                              console.log(_this.fb_url1 )
                              console.log(_this.fb_url2 )
                              
                              _this.iframe_url = "https://www.facebook.com/plugins/like.php?href=https%3A%2F%2Fhdl.handle.net%2F"+_this.fb_url1+"%2F"/
                              +_this.fb_url2+"&width=450&layout=standard&action=like&size=small&show_faces=true&share=true&height=80&appId"
                              console.log(_this.iframe_url)
                        }
                        _this.tableData[input['keyword'][i]]=papers
                        // console.log(_this.tableData)
                        
                        }
                    },
                    error: function(xhr, ajaxOptions, thrownError) {
                    console.log('error');
                    console.log(thrownError);
                    },
                    complete: function(){
                        loading.close()
                        for(i = 0; i < 10; i++){
                          if (_this.tableData[input['keyword'][i]].length==0){
                            alert_message = true
                          }
                          else{
                            alert_message = false
                          }
                        }
                        if(alert_message == true){
                            alert("查無資料！");
                            window.location.reload();
                        }
                       
                        console.log('Get all Paper!');
                      
                      
                    }
                  });     
            }).fail(function(){
                  console.log("Error happening");
                  alert("Something go wrong! Email to r06525111@ntu.edu.tw")
              });
              console.log(this.value2)
          }
          else if(this.scenery == 'expert'){
            var input= {
              "sentences":this.textarea,
              "number":100,
              "mode":this.search_mode
            }
            _this.DialogVisibleMode = false
            var Find_Methods = $.ajax({
                url: "http://140.112.26.237:8002/api/batch/get_similarity/",
                type: "POST",
                dataType: "json",
                data:JSON.stringify(input),
                async:true,
                beforeSend: function(){
                  _this.loading = true;
                },
                success: function (data) {
                  console.log(data)
                  for(i = 0 ; i<data.methods.length ; i++){
                    _this.recommand_methods.push({"methods":data.methods[i].word,"wf":data.methods[i].wf})
                  }
                  // for(i = 0 ; i <data.pairs.length; i++){
                  //   _this.recommand_papers.push()
                  // }
                  _this.recommand_papers = data.pairs
                  console.log(_this.recommand_papers)
                },
                error: function(xhr, ajaxOptions, thrownError) {
                  console.log('error');
                  console.log(thrownError);
                },
                complete: function(){
                    console.log('Done!');
                    _this.loading = false;
                   
                  
                }
            });
           
          }
              
        }else if(this.step == 3){
          
          
        }
      }
      }
})


 function selectFanDialog(){
   $('#setFan').modal({
     keyboard: false
   });
 }

