<button id="copy_btn" onclick="copy_text(name)" name="{{ file.id}}">
  コピーする
</button>

<script>
function copy_text(id) {
var text = document.getElementById(id).value;
var area = document.getElementById(id);
area.select();
navigator.clipboard.writeText(text).then(e => {
       alert('コピーしました。');
       });
      }
</script>