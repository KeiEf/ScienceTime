
  var str = document.getElementById("note_body" ).innerHTML;

  var or3 = "Planckの放射式"
  var or64 = "Hamilton-Jacobi方程式"
  var or66 = "Lorentz変換"
  var or68 = "連続の式"
  var or69 = "熱力学第一法則"
  var or72 = "有効放射温度"
  var or73 = "Stefan-Boltzmannの法則"
  var or74 = "双一次形式"
  var or75 = "温室効果"
  var or76 = "Russelのパラドックス"
  var or77 = "二項定理"

  for (var i = 0; i < 300; ++i) {
  var bf + i = "<" + or + i + ">"
  var replaced = str.replaceAll(bf + i, rp + i)
      };
  document.getElementById("note_body" ).innerHTML = replaced;