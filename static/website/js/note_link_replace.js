for (var i = 0; i < 3; ++i) {
  var str = document.getElementById("note_id-" + i ).innerHTML;

  var or1 = "連続の式"
  var rp1 = "<a href='https://www.sciencetime.jp/note/68' target='_blank'>" + or1 +"<\/a>"
  var or2 = "Lorentz変換"
  var rp2 = "<a href='https://www.sciencetime.jp/note/66' target='_blank'>" + or2 +"<\/a>"


  var replaced = str.replaceAll(or1, rp1).replaceAll(or2,rp2); 
//document.getElementsByTagName("p").innerHTML = replaced;
  document.getElementById("note_id-" + i).innerHTML = replaced;
}