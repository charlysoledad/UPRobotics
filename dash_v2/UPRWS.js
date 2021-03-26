var ws;
var $scope;
var ws_connected = false;

$(document).ready(function() {
  clear_logg();
  $scope = angular
    .element(document)
    .find("body")
    .scope();

    $("#disconnect").click(function(evt){
      evt.preventDefault();
      disconnectServer();
    });
  
    $("#connect").click(function(evt) {
    evt.preventDefault();
    connectServer()
    
  });
});

function ws_sendData(data) {
  if (ws_connected){
    let data_json = data;
    data_json = JSON.stringify(data_json);
    ws.send(data_json);
    //ws.json.send(data_json);
  }else {console.log("WebSocket disconnected"); logg("WebSocket disconnected");}

}

function disconnectServer(){
  ws.close();
}

function connectServer(){
  var host = $("#host").val();
    var port = $("#port").val();
    var uri = $("#uri").val();

    ws = new WebSocket("ws://" + host + ":" + port + uri);

    ws.onmessage = (evt) => {
      //invierte el contenido de la cadena
      //var str = evt.data.split("").reverse().join("");
      console.log(evt.data);
      logg(evt.data);

    };

    // Close Websocket callback
    ws.onclose = (evt) => {
      connectS(false);
      ws_connected = false;
    };

    // Open Websocket callback
    ws.onopen = (evt)  => {
      connectS(true);
      ws_connected = true;
    };

    function connectS(conected) {
      if (conected) {
        $scope.updateService.onValueChanged("communication/robot", 1);
        console.log("Connected to server");
        logg("Connected to server");
      } else {
        $scope.updateService.onValueChanged("communication/robot", 0);
        console.log("Disconnected to server");
        logg("Disonnected to server");
      }
      $scope.$apply();
    }
}
