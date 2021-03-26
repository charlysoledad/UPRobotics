function getData1(){
    var python = require("python-shell")
    var path = require("path")

    var options = {
        scriptPath: path.join(__dirname, '../../engine/')
    }

    var dataOut = new python('main.py', options);

    dataOut.end(function(message){
        document.getElementById('data').innerHTML = message
    })
}