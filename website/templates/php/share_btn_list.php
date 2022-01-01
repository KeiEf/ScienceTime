
 {% load replace %}


<span>
      {% if post.title %}
      <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" data-via="sciencetime_jp" data-related="ST_phys_bot" class="twitter-share-button" data-show-count="false" data-hashtags="ScienceTime {% for tag in post.post_tags.all %},{{ tag.name|blank_remove }}{% endfor %}" data-lang="ja"></a>
      {% elif note.title %}
      <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" data-via="sciencetime_jp" data-related="ST_phys_bot" class="twitter-share-button" data-show-count="false" data-hashtags="ScienceTime {% for tag in note.note_tags.all %},{{ tag.name|blank_remove }}{% endfor %}" data-lang="ja"></a>
      {% elif product.name %}
      <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" data-via="sciencetime_jp" data-related="ST_phys_bot" class="twitter-share-button" data-show-count="false" data-hashtags="ScienceTime{% for tag in product.tags.all %},{{ tag.name|blank_remove }}{% endfor %}" data-lang="ja">Tweet</a>
      {% endif %}
</span>

<span>
  <script language="JavaScript">
  function line_button_tag(){
  var tag= "<div class='line-it-button' data-lang='ja' data-type='share-a' data-ver='2' data-url='{0}' style='display: none;'></div>";
  tag = tag.replace(/\{0\}/g, location.href);
  return tag;
  }
  </script>
  <script language="JavaScript">document.write(line_button_tag());</script>
  <script src="https://d.line-scdn.net/r/web/social-plugin/js/thirdparty/loader.min.js" async="async" defer="defer"></script>
</span>

