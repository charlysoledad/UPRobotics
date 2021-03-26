function logg(text) {
  var val = $("#dataLog").val();
  if (val) {
   $("#dataLog").val(val + "\n" + text);
  } else {
   $("#dataLog").val(text);
  }
    $("#dataLog").scrollTop($("#dataLog")[0].scrollHeight);
}

function clear_logg(){
    $("#dataLog").val("");
}
