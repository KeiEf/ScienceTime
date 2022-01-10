for (var i = 0; i < 3; ++i) {
  var str = document.getElementById("note_id-" + i ).innerHTML;

  var or66 = "Lorentz変換"
  var rp66 = "<a href='https://www.sciencetime.jp/note/66' target='_blank'>" + or66 +"<\/a>"

  var or68 = "連続の式"
  var rp68 = "<a href='https://www.sciencetime.jp/note/68' target='_blank'>" + or68 +"<\/a>"

  var or69 = "熱力学第一法則"
  var rp69 = "<a href='https://www.sciencetime.jp/note/69' target='_blank'>" + or69 +"<\/a>"

  var or72 = "有効放射温度"
  var rp72 = "<a href='https://www.sciencetime.jp/note/72' target='_blank'>" + or72 +"<\/a>"




  var replaced = str.replaceAll(or66, rp66).replaceAll(or68,rp68).replaceAll(or69, rp69).replaceAll(or72,rp72); 
//document.getElementsByTagName("p").innerHTML = replaced;
  document.getElementById("note_id-" + i).innerHTML = replaced;
}