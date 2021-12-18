<div class="select_area">
  <form method="GET" action="">
    <select class="post_sort_btn" name="sort" method="GET" onChange="submit(this.form)">
      <option>並び替え</option>
      <option value="date">投稿日（新しい）</option>
      <option value="inv_date">投稿日（古い）</option>             
      <option value="view">閲覧数（多い）</option>
      <option value="inv_view">閲覧数（少ない）</option>
      {% if user.is_authenticated %}
        {% if user.is_superuser %}
        <option value="all">すべて</option> 
        <option value="private">非公開</option>
        {% endif %}
      {% endif %}
    </select>
  </form>
</div>