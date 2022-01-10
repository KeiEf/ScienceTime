for (var i = 0; i < 3; ++i) {
  var str = document.getElementById("note_id-" + i ).innerHTML;

  var or3 = "Planckの放射式"
  var rp3 = "<a href='https://www.sciencetime.jp/note/66' target='_blank'>" + or3 +"<\/a>"

  var or64 = "Hamilton-Jacobi方程式"
  var rp64 = "<a href='https://www.sciencetime.jp/note/66' target='_blank'>" + or64 +"<\/a>"

  var or66 = "Lorentz変換"
  var rp66 = "<a href='https://www.sciencetime.jp/note/66' target='_blank'>" + or66 +"<\/a>"

  var or68 = "連続の式"
  var rp68 = "<a href='https://www.sciencetime.jp/note/68' target='_blank'>" + or68 +"<\/a>"

  var or69 = "熱力学第一法則"
  var rp69 = "<a href='https://www.sciencetime.jp/note/69' target='_blank'>" + or69 +"<\/a>"

  var or72 = "有効放射温度"
  var rp72 = "<a href='https://www.sciencetime.jp/note/72' target='_blank'>" + or72 +"<\/a>"

  var or73 = "Stefan-Boltzmannの法則"
  var rp73 = "<a href='https://www.sciencetime.jp/note/72' target='_blank'>" + or73 +"<\/a>"

  var replaced = str.replaceAll(or3, rp3).replaceAll(or64, rp64).replaceAll(or66, rp66).replaceAll(or68,rp68).replaceAll(or69, rp69).replaceAll(or72,rp72).replaceAll(or73, rp73); 
//document.getElementsByTagName("p").innerHTML = replaced;
  document.getElementById("note_id-" + i).innerHTML = replaced;
}