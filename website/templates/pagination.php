    <!--pagination -->
    <div class="d-flex justify-content-center">
        <ul class="pagination">
          <!-- 前へ  -->
          {% if page_obj.has_previous %}
          <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.previous_page_number }}">
              <span aria-hidden="true">&laquo;</span>
            </a>
          </li>
          {% endif %}
     
          <!-- ページ番号 -->
          {% for num in page_obj.paginator.page_range %}
          {% if page_obj.number == num %}
          <li class="page-item active"><a class="page-link" href="#!">{{ num }}</a></li>
          {% else %}
          <li class="page-item"><a class="page-link" href="?page={{ num }}">{{ num }}</a></li>
          {% endif %}
          {% endfor %}
     
          <!-- 次へ -->
          {% if page_obj.has_next %}
          <li class="page-item">
            <a class="page-link" href="?page={{ page_obj.next_page_number }}">
              <span aria-hidden="true">&raquo;</span>
            </a>
          </li>
          {% endif %}
        </ul>
      </div>
      <br>