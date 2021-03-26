var hasGP = false;
var repGP;
var repS = true;

var $scope;

function getScope(ctrlName) {
  var sel = 'body[ng-controller="' + ctrlName + '"]';
  return angular.element(document).find(sel).scope;
}

var joystick = {
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
};

$(document).ready(function() {
  //console.log(canGame());
  $scope = angular
    .element(document)
    .find("body")
    .scope();

  if (canGame()) {
    $(window).on("gamepadconnected", function() {
      hasGP = true;
      console.log("connection event");
      //console.log(joystick);
      //console.log("GP: " + navigator.getGamepads()[0]);
      repGP = window.setInterval(reportOnGamepad, 100);
    });

    $(window).on("gamepaddisconnected", function() {
      console.log("disconnection event");
      //console.log("GP: " + navigator.getGamepads()[0]);
      hasGP = false;
      window.clearInterval(repGP);
    });

    //setup an interval for Chrome
    var checkGP = window.setInterval(function() {
      console.log("checkGP");
      //console.log("GP: " + navigator.getGamepads()[0]);
      if (navigator.getGamepads()[0]) {
        if (!hasGP) {
          $(window).trigger("gamepadconnected");
          logg("Gamepad: connected");
        }
        window.clearInterval(checkGP);
      }
    }, 500);
  }
});

function canGame() {
  return "getGamepads" in navigator;
}

function reportOnGamepad() {
  if (navigator.getGamepads()[0] != null) {
    var gp = navigator.getGamepads()[0];
    var id = "Xbox Controller";

    if (repS) {
      $("#GP_pmt").html(id);
      //$('.GP_buttons').empty();
      //$('.GP_axis').empty();

      for (var i = 0; i < gp.buttons.length; i++) {
        $(".GP_buttons").append(
          '<div class="GP_button btn_unpressed" id="btn_' +
            (i + 1) +
            '" value="' +
            pressed +
            '"><p>' +
            (i + 1) +
            "</p> </div>"
        );
        //joystick.buttons[i+1] = 1;
      }

      for (var i = 0; i < gp.axes.length; i += 2) {
        var stick = Math.ceil(i / 2) + 1;
        $(".gp" + stick).append(
          '<div class="GP_axis' +
            stick +
            ' grid">' +
            '<div class="gamepad-axis-pip' +
            stick +
            '" style="left: 50%; top: 50%;">' +
            '<div class="gamepad-axis-crosshair-v"></div>' +
            '<div class="gamepad-axis-crosshair-h"></div>' +
            "</div>"
        );
        $(".gp" + stick).append(
          '<div class="gamepad-axis-pair-value' + stick + '">0.00,0.00</div>'
        );
      }
      $scope.updateService.onValueChanged("communication/joysticks", 1);
      //console.log($scope.data.communication.joysticks);
      $scope.$apply();

      repS = false;
    }

    for (var i = 0; i < gp.buttons.length; i++) {
      var pressed = 0;
      if (gp.buttons[i].pressed) {
        pressed = 1;
        $("#btn_" + (i + 1)).removeClass("btn_unpressed");
        $("#btn_" + (i + 1)).addClass("btn_pressed");
        joystick.buttons[i + 1] = pressed;
        //$scope.updateService.onValueChanged("joysticks/buttons/"+(i+1), pressed);
        //append('<div class="GP_button btn_pressed" id="btn'+(i+1)+'" value="'+pressed+'">');
      } else {
        pressed = 0;
        $("#btn_" + (i + 1)).removeClass("btn_pressed");
        $("#btn_" + (i + 1)).addClass("btn_unpressed");
        joystick.buttons[i + 1] = pressed;
        //$scope.updateService.onValueChanged("joysticks/buttons/"+(i+1), pressed);
      }
    }

    for (var i = 0; i < gp.axes.length; i += 2) {
      var stick = Math.ceil(i / 2) + 1;
      var x = deadzone(gp.axes[i]);
      var y = deadzone(gp.axes[i + 1]);
      var ax = ((x + 1) / 2) * 100 + "%";
      var ay = ((y + 1) / 2) * 100 + "%";
      //console.log(x);
      $(".gamepad-axis-pip" + stick).css({ left: ax, top: ay });
      $(".gamepad-axis-pair-value" + stick).html(
        x.toFixed(2) + "," + y.toFixed(2)
      );
      // Complete axis value 
      //var axis_value = (x + y)
      $scope.updateService.onValueChanged("joysticks/stick/"+stick+"/x", x);
      $scope.updateService.onValueChanged("joysticks/stick/"+stick+"/y", y);
      joystick.stick[stick].x = x;
      joystick.stick[stick].y = y;
      //$('#axis_'+i).html("Axis "+i+":"+ ax.toFixed(2));
      //append('<div class="GP_ax" id="axis_'+i+'"> Axis '+i+': '+ ax.toFixed(2)+'</div>');
    }

    if (ws_connected)  ws_sendData($scope.updateService.data);
    updateRPM();
    updateGyro();
  } else {
    deleteGP();
    $scope.updateService.onValueChanged("communication/joysticks", 0);
    //console.log($scope.data.communication.joysticks);
    $scope.$apply();
    repS = true;
  }
  //console.log(joystick.stick[1]);
}

function updateGyro() {
  var angle_x = parseInt(joystick.stick[1].x * 10 * 1.5);
  var c_angleX = $scope.data.sensors.gyroAngleX;
  if (c_angleX > 361) {
    c_angleX = 0;
  } else if (c_angleX < -1) {
    c_angleX = 360;
  }

  $scope.updateService.onValueChanged(
    "sensors/gyroAngleX",
    (c_angleX += angle_x)
  );
  $scope.$apply();
}

function updateRPM() {
  var left_rpm = parseInt(-(joystick.stick[1].y - joystick.stick[1].x) * 25);
  var right_rpm = parseInt(-(joystick.stick[1].y + joystick.stick[1].x) * 25);

  $scope.updateService.onValueChanged("motors/encoderLeftSide", left_rpm);
  $scope.updateService.onValueChanged("motors/encoderRightSide", right_rpm);
  $scope.$apply();
}

function deadzone(v) {
  const DEADZONE = 0.2;

  if (Math.abs(v) < DEADZONE) {
    v = 0;
  } else {
    // Smooth
    v = v - Math.sign(v) * DEADZONE;
    v /= 1.0 - DEADZONE;
  }

  return v;
}

function deleteGP() {
  $("#GP_pmt").html("Connect a controller");
  $(".GP_buttons").empty();
  $(".gp1").empty();
  $(".gp2").empty();
}
