var app = angular.module("Dashboard", ["ngMaterial", "nvd3"]);

app.config(function($mdThemingProvider) {
  $mdThemingProvider.definePalette("ixnamiki", {
    "50": "e5e6e7",
    "100": "bdc1c3",
    "200": "92989b",
    "300": "666e72",
    "400": "454f54",
    "500": "243036",
    "600": "202b30",
    "700": "1b2429",
    "800": "161e22",
    "900": "0d1316",
    A100: "5ac8ff",
    A200: "27b7ff",
    A400: "00a2f3",
    A700: "0091da",
    contrastDefaultColor: "light",
    contrastDarkColors: ["50", "100", "200", "A100", "A200"],
    contrastLightColors: [
      "300",
      "400",
      "500",
      "600",
      "700",
      "800",
      "900",
      "A400",
      "A700"
    ]
  });

  $mdThemingProvider.definePalette("ixnamikiaccent", {
    "50": "e5e9ea",
    "100": "bfc9ca",
    "200": "95a5a6",
    "300": "6a8082",
    "400": "4a6568",
    "500": "2a4a4d",
    "600": "254346",
    "700": "1f3a3d",
    "800": "193234",
    "900": "0f2225",
    A100: "65edff",
    A200: "32e7ff",
    A400: "00e0fe",
    A700: "00cae5",
    contrastDefaultColor: "light",
    contrastDarkColors: ["50", "100", "200", "A100", "A200", "A400", "A700"],
    contrastLightColors: ["300", "400", "500", "600", "700", "800", "900"]
  });

  $mdThemingProvider
    .theme("default")
    .dark()
    .primaryPalette("ixnamiki")
    .accentPalette("ixnamikiaccent");
});

app.factory("updateService", function() {
  var updateService = {};

  updateService.data = {
    checkMode: {
      teleOpMode: true,
      autoMode: false,
      emergency: false,
      mode: "TeleOperated"
    },
    motors: {
      motorLeftSide: 0,
      motorRightSide: 0,
      motorLeftSide: 0,
      motorRightSide: 0,
      motorRFlippers: 0,
      motorBFlippers: 0,
      motorArm1: 0,
      motorArm2: 0,
      motorArm3: 0,
      motorArm4: 0,
      motorArm5: 0,
      motorClaw: 0,
      encoderLeftSide: 0,
      encoderRightSide: 0,
      encoderRFlippers: 0,
      encoderBFlippers: 0,
      encoderArm1: 0,
      encoderArm2: 0,
      encoderArm3: 0,
      encoderArm4: 0,
      encoderArm5: 0,
      encoderClaw: 0
    },
    power: {
      batteryVoltage: 10.8,
      totalPowerUse: 28.6,
      leftSide: 15.0,
      rightSide: 15.0,
      rearFlippers: 8.0,
      backFlippers: 8.0,
      Jetson: 10,
      Cpu: 86,
      Ram: 34
    },
    sensors: {
      gyroAngleX: 0,
      gyroAngleY: 0,
      CO: 0,
      accelerometer: 0
    },
    communication: {
      ip: "192.168.1.40",
      joysticks: 0,
      robot: 0
    },
    connected: 0,
    state: "disabled",
    datalog: {
      info: "ERROR 12 \n ERROR 56 \n"
    },
    joysticks: {
      stick: {
        1: { x: 0, y: 0 },
        2: { x: 0, y: 0 }
      },
      buttons: {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
        13: 0,
        14: 0,
        15: 0,
        16: 0,
        17: 0
      }
    }
  };

  updateService.sendValue = function(key, value) {};

  updateService.getValue = function(key) {};

  updateService.getProperty = function(o, s) {
    s = s.replace(/\[(\w+)\]/g, ".$1"); // convert indexes to properties
    s = s.replace(/^\./, ""); // strip a leading dot
    var a = s.split("/");
    for (var i = 0, n = a.length - 1; i < n; ++i) {
      var k = a[i];
      if (k in o) {
        o = o[k];
      } else {
        return;
      }
    }
    return o;
  };

  updateService.onValueChanged = function(key, value, isNew) {
    if (value == "true") {
      value = true;
    } else if (value == "false") {
      value = false;
    }

    var a = key.split("/");
    updateService.getProperty(updateService.data, key)[a[a.length - 1]] = value;
  };

  updateService.onConnection = function(connected) {
    updateService.data.connected = connected;
  };

  return updateService;
});

app.controller("uiCtrl", function($scope, updateService) {
  $scope.data = updateService.data;
  $scope.updateService = updateService;

  $scope.keydown = function(keyEvent) {
    var key = keyEvent.key.toLowerCase();
    var loggg = "";
    //console.log("Key: ", key);
    if (!$scope.data.checkMode.emergency) {
      //ws_sendData(key);
      switch (key) {
        case "a":
          updateService.onValueChanged("sensors/gyroAngleX", 0);
          loggg = "Value changed: gyro X to 0";
          break;
        case "b":
          break;
        case "c":
          break;
        case "d":
          break;
        case "e":
          break;
        case "f":
          break;
        case "g":
          break;
        case "h":
          break;
        case "i":
          break;
        case "j":
          break;
        case "k":
          break;
        case "l":
          break;
        case "m":
          updateService.onValueChanged(
            "checkMode/teleOpMode",
            !$scope.data.checkMode.teleOpMode
          );
          updateService.onValueChanged(
            "checkMode/autoMode",
            !$scope.data.checkMode.teleOpMode
          );
          if ($scope.data.checkMode.teleOpMode == true) {
            updateService.onValueChanged("checkMode/mode", "TeleOperated");
          }
          if ($scope.data.checkMode.autoMode == true) {
            updateService.onValueChanged("checkMode/mode", "Autonomous");
          }
          updateService.onValueChanged("state", "disabled");
          break;
        case "n":
          break;
        case "ñ":
          break;
        case "o":
          break;
        case "p":
          break;
        case "q":
          break;
        case "r":
          break;
        case "s":
          var posx = ($scope.data.sensors.gyroAngleX += 5);
          updateService.onValueChanged("sensors/gyroAngleX", posx);
          loggg = "Value changed: gyro X to " + posx;
          break;
        case "t":
          break;
        case "u":
          break;
        case "v":
          break;
        case "w":
          break;
        case "x":
          var posy = ($scope.data.sensors.gyroAngleY += 5);
          updateService.onValueChanged("sensors/gyroAngleY", posy);
          loggg = "Value changed: gyro X to " + posy;
          break;
        case "y":
          break;
        case "z":
          updateService.onValueChanged("sensors/gyroAngleY", 0);
          break;
        case "arrowup":
          updateService.onValueChanged(
            "motors/encoderLeftSide",
            ($scope.data.motors.encoderLeftSide += 1)
          );
          updateService.onValueChanged(
            "motors/encoderRightSide",
            ($scope.data.motors.encoderRightSide += 1)
          );
          break;
        case "arrowdown":
          updateService.onValueChanged(
            "motors/encoderLeftSide",
            ($scope.data.motors.encoderLeftSide -= 1)
          );
          updateService.onValueChanged(
            "motors/encoderRightSide",
            ($scope.data.motors.encoderRightSide -= 1)
          );
          break;
          case "arrowleft":
            break;
          case "arrowright":
            break;
        case "f1":
          ws_sendData($scope.data);
          //console.log(data);
          break;
        case "f2":
          clear_logg();
          break;
        case "f3":
          break;
        case "f4":
          break;
        case "f5":
          break;
        case "f6":
          break;
        case "f7":
          break;
        case "f8":
          break;
        case "f9":
          disconnectServer();
          break;
        case "f10":
          connectServer();
          break;
        case "f11": // button to full size DO NOT USE
          break;
        case "f12":
          break;
        case "1":
          break;
        case "2":
          break;
        case "3":
          break;
        case "4":
          break;
        case "5":
          break;
        case "6":
          break;
        case "7":
          break;
        case "8":
          break;
        case "9":
          break;
        case "0":
          break;
        case " ":
          updateService.onValueChanged("checkMode/emergency", true);
          updateService.onValueChanged("checkMode/mode", "Emergency");
          updateService.onValueChanged("state", "Stopped");
          loggg =  "\n\n\n \n\t\t\t\t\t*** EMERGENCY STOP *** \n\t\t\t\t\t\n \t\t\t\t\tRESET THE DASHBOARD\n\n\n";
          break;
      }

      updateService.onValueChanged("datalog/info", loggg + "\n");
      logg(loggg);
      ws_sendData($scope.data);
    }
    if ($scope.data.sensors.gyroAngleX >= 360) {
      updateService.onValueChanged("sensors/gyroAngle", 0);
    }
  };

  return $scope;
});

app.controller("clockCtrl", function($scope, updateService) {
  var data = updateService.data;
  $scope.data = data;

  $scope.getTime = function() {
    var minutes = data.match.time / 60;
    var seconds = data.match.time % 60;

    return (
      (minutes < 10 ? "0" : "") +
      minutes +
      ":" +
      (seconds < 10 ? "0" : "") +
      seconds
    );
  };
  $scope.getStatus = function() {
    if (data.connected) return "connected";
    else return "disconnected";
  };
});

app.controller("angleLockCtrl", function($scope, updateService) {
  $scope.info = {
    selected: "off"
  };

  $scope.select = function(name) {
    $scope.info.selected = name;
    updateService.sendValue("autoMode/selectedMode", name);
  };
});

app.controller("fieldOrientedCtrl", function($scope, updateService) {
  $scope.info = {
    fieldOriented: true
  };

  $scope.toggleFieldOriented = function() {
    $scope.info.fieldOriented = !$scope.info.fieldOriented;
  };
});

app.controller("autoCtrl", function($scope, updateService) {
  $scope.info = {
    selected: "forward"
  };

  $scope.select = function(name) {
    $scope.info.selected = name;
  };
});

app.controller("autoGearCtrl", function($scope, updateService) {
  $scope.info = {};
});

  app.controller("compassCtrl", function($scope, updateService) {
    var data = updateService.data;
    $scope.info = {
      value: (data.sensors.gyroAngleX * Math.PI) / 180
      //valueY: data.sensors.gyroAngleY * Math.PI / 180
    };
  });
