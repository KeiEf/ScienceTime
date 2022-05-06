{% load static %}
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="{% static 'website/js/side_menu.js' %}"></script>
   <!-- MathJax -->
   <script>
    MathJax = {
    tex: {
    tags: 'ams',
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    processEscapes: true,
    macros: { pd: "{\\partial}",
              ep: "{\\epsilon}",
              varep: "{\\varepsilon}",
              bm: ["{\\boldsymbol{#1}}",1],
              sD: ["{\\mathcal{D}}"],
              sG: ["{\\mathcal{G}}"],
              sJ: ["{\\mathcal{J}}"],             
              sL: ["{\\mathcal{L}}"],
              sN: ["{\\mathcal{N}}"],
              sO: ["{\\mathcal{O}}"],
              sS: ["{\\mathcal{S}}"],
              sT: ["{\\mathcal{T}}"],
              sU: ["{\\mathcal{U}}"],
              frg: ["{\\mathfrak{g}}"],
              frh: ["{\\mathfrak{h}}"],
              frgl: ["{\\mathfrak{gl}}"],  
              frsu: ["{\\mathfrak{su}}"],
              ad: ["{\\text{ad}}"],
              tr: ["{\\text{tr}}"],
            }
    }     
    };
 </script>



 <script type="text/javascript" id="MathJax-script" async
 src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
 </script>