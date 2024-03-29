<div class="paginating">

    <nav aria-label="">
      <ul class="pagination">
        {% if pages.has_previous %}
        <li class="page-item"><a class="page-link"  href="?page={{pages.previous_page_number}}{% if sort %}&sort={{ sort }}{% endif %}" tabindex="-1" aria-disabled="true">Prev</a></li>
        {% else %}
        <li class="page-item disabled"><a class="page-link"  href="#" tabindex="-1" aria-disabled="true">Prev</a></li>        
        {% endif %}
        {% for page_num in pages.paginator.page_range %}
          {% if page_num %}
            {% if page_num == pages.number %}
            <li class="page-item disabled"><a class="page-link" href="#">{{page_num}}</a></li>
            {% else %}
              <li class="page-item"><a class="page-link"  href="?page={{page_num }}{% if sort %}&sort={{ sort }}{% endif %}">{{page_num}}</a></li>
            {% endif %}
          {% else %}
          <li class="page-item"><a class="page-link"  href="#">...</a></li>
          {% endif %}
        {% endfor %}

        {% if pages.has_next %}
        <li class="page-item">
          <a class="page-link" href="?page={{pages.next_page_number}}{% if sort %}&sort={{ sort }}{% endif %}">Next</a>
        </li>
        {% else %}
        <li class="page-item disabled">
          <a class="page-link" href="#" >Next</a>
        </li>        
        {% endif %}

      </ul>
    </nav>

</div>

<!--{% if pages.has_other_pages %}-->
<!--{% endif %}-->
