from django import template
import re

register = template.Library()

@register.filter
def blank_remove(value):
    return value.replace(" ","").replace("-","_")

@register.filter
def math_scroll(value):
    replaced = value.replace("\\begin{align}","</p><div class='eq'>\n\\begin{align}").replace("\\end{align}","\\end{align}</div><p>")
    replaced = replaced.replace("\\begin{equation}","</p><div class='eq'>\n\\begin{equation}").replace("\\end{equation}","\\end{equation}</div><p>")
    replaced = replaced.replace("\n\\{","\n</p>\n\\{").replace("\\}\n","\\}\n</p>\n")
    replaced = replaced.replace("\n<h4>","\n</p>\n<h4>").replace("\n<h5>","\n</p>\n<h5>").replace("\n<h6>","\n</p>\n<h6>")
    replaced = replaced.replace("</h4>\n","</h4>\n<p>\n").replace("</h5>\n","</h5>\n<p>\n").replace("</h6>\n","</h6>\n<p>\n")
    replaced = replaced.replace("\n<div>\n","\n</p>\n<div><p>").replace("\n</div>","\n</p>\n</div>\n<p>")
    replaced = replaced.replace("<p>\n<p>","<p>").replace("<p><p>","<p>").replace("</p>\n</p>","</p>").replace("</p></p>","</p>")
    replaced = re.sub(r'(\n\s*)+\n+', '</p><p>',replaced)
    replaced = replaced.replace("、","，")
    return replaced

@register.filter
def html_replace(value):
    replaced = value.replace("<li>","").replace("</li>","")
    replaced = replaced.replace("<ul>","").replace("</ul>","").replace("<ol>","").replace("</ol>","")
    replaced = replaced.replace("<b>","<span style='color:#191970;font-weight:bold;'>").replace("</b>","</span>")
    return replaced

@register.filter
def tex_additional(value):
    # screen
    replaced = value.replace("\\begin{screen}","</p><div class='tex_screen'>").replace("\\end{screen}","</div><p>")
    # quote
    replaced = replaced.replace("\\begin{quote}","</p><blockquote><p>").replace("\\end{quote}","</p></blockquote><p>")

    # dfn, thm, exm, exc, proof
    replaced = replaced.replace("\\begin{dfn}","</p><div class='dfn'>\n<p><b>定義</b>：").replace("\\end{dfn}","</p>\n</div><p>")
    replaced = replaced.replace("\\begin{thm}","</p><div class='thm'>\n<p><b>定理</b>：").replace("\\end{thm}","</p>\n</div><p>")
    replaced = replaced.replace("\\begin{exm}","</p><div class='exm'>\n<p><b>例</b>："  ).replace("\\end{exm}","</p>\n</div><p>")
    replaced = replaced.replace("\\begin{exc}","</p><div class='exm'>\n<p><b>例題</b>："  ).replace("\\end{exc}","</p>\n</div><p>")
    replaced = replaced.replace("\\begin{proof}","</p><div class='proof'>\n<p><i><b>proof</b></i></p><p>"  ).replace("\\end{proof}","</p>\n<div align='right'>□</div></div><p>")

    # itemize
    replaced = replaced.replace("\\begin{itemize}","</p><ul class='tex_itemize'>").replace("\\end{itemize}","</ul><p>")
    replaced = replaced.replace("\\begin{enumerate}","</p><ol class='tex_enumerate'>").replace("\\end{enumerate}","</ul><p>")


    # itembox
    reg_ibxl = r'(?<=\{itembox\}\[l\]\{).+?(?=\})' 
    reg_ibxc = r'(?<=\{itembox\}\[c\]\{).+?(?=\})'
    reg_ibxr = r'(?<=\{itembox\}\[r\]\{).+?(?=\})'    
    title_l = re.findall(reg_ibxl,replaced)
    title_c = re.findall(reg_ibxc,replaced)
    title_r = re.findall(reg_ibxr,replaced)

    # secs
    reg_sec = r'(?<=section\{).+?(?=\})'
    reg_subsec = r'(?<=subsection\{).+?(?=\})'
    reg_subsubsec = r'(?<=subsubsection\{).+?(?=\})'    
    title_sec = re.findall(reg_sec,replaced)
    title_subsec = re.findall(reg_subsec,replaced)
    title_subsubsec = re.findall(reg_subsubsec,replaced)

    # lists
    reg_itm = r'\\item(.*?)\n' #'(?<=item).+?(?=)'
    txt_itm = re.findall(reg_itm,replaced)

    # font
    reg_bf = r'(?<=textbf\{).+?(?=\})'
    reg_it = r'(?<=textit\{).+?(?=\})'     
    txt_bf = re.findall(reg_bf,replaced)
    txt_it = re.findall(reg_it,replaced)

    # mathjax design
    #reg_re= '(?<=\Re\{).+?(?=\})' 
    #txt_re = re.findall(reg_re,replaced)

    # itembox
    for i in title_l:
        item_1 ="\\begin{itembox}[l]{" + i + "}"
        item_2 ="</p><div class='tex_itembox'><span class='title_l'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div><p>")

    for i in title_c:
        item_1 ="\\begin{itembox}[c]{" + i + "}"
        item_2 ="</p><div class='tex_itembox'><span class='title_c'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div><p>")

    for i in title_r:
        item_1 ="\\begin{itembox}[r]{" + i + "}"
        item_2 ="</p><div class='tex_itembox'><span class='title_r'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div><p>")

    # sec
    for i in title_sec:
        sec_1 = "\\section{" + i + "}"
        sec_2 = "<h2>" + i + "</h2><p>"
        replaced = replaced.replace(sec_1,sec_2) 

    for i in title_subsec:
        sec_1 = "\\subsection{" + i + "}"
        sec_2 = "<h3>" + i + "</h3><p>"
        replaced = replaced.replace(sec_1,sec_2) 

    for i in title_subsubsec:
        sec_1 = "\\subsubsection{" + i + "}"
        sec_2 = "<h4>" + i + "</h4><p>"
        replaced = replaced.replace(sec_1,sec_2) 

    # font
    for i in txt_bf:
        txt_1 = "\\textbf{" + i + "}"
        txt_2 = "<b>" + i + "</b>"
        replaced = replaced.replace(txt_1,txt_2) 

    for i in txt_it:
        txt_1 = "\\textit{" + i + "}"
        txt_2 = "<i>" + i + "</i>"
        replaced = replaced.replace(txt_1,txt_2) 

#    for i in txt_re:
#        txt_1 = "\\Re{" + i + "}"
#        txt_2 = "\\mathrm\{Re\}\{" + i + "\}"
#        replaced = replaced.replace(txt_1,txt_2)     

    for i in txt_itm:
        txt_1 = "\\item" + i #+ "\n"
        txt_2 = "<li>" + i + "</li>"
        replaced = replaced.replace(txt_1,txt_2)    

    return replaced


