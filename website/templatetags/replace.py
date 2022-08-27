from django import template
import re

register = template.Library()

@register.filter
def blank_remove(value):
    return value.replace(" ","").replace("-","_")

@register.filter
def math_scroll(value):   
    return value.replace("\\begin{align}","<div class='eq'>\n\\begin{align}").replace("\\end{align}","\\end{align}</div>").replace("\\begin{equation}","<div class='eq'>\n\\begin{equation}").replace("\\end{equation}","\\end{equation}</div>").replace("<b>","<span style='color:#191970;font-weight:bold;'>").replace("</b>","</span>")

@register.filter
def html_replace(value):
    return value.replace("<li>","").replace("</li>","").replace("<ul>","").replace("</ul>","").replace("<ol>","").replace("</ol>","")

@register.filter
def tex_additional(value):
    # screen
    replaced = value.replace("\\begin{screen}","<div class='tex_screen'>").replace("\\end{screen}","</div>")
    # quote
    replaced = replaced.replace("\\begin{quote}","<blockquote>").replace("\\end{quote}","</blockquote>")

    # itembox
    reg_ibxl = '(?<=\{itembox\}\[l\]\{).+?(?=\})'
    reg_ibxc = '(?<=\{itembox\}\[c\]\{).+?(?=\})'
    reg_ibxr = '(?<=\{itembox\}\[r\]\{).+?(?=\})'    
    title_l = re.findall(reg_ibxl,replaced)
    title_c = re.findall(reg_ibxc,replaced)
    title_r = re.findall(reg_ibxr,replaced)

    # secs
    reg_sec = '(?<=section\{).+?(?=\})'
    reg_subsec = '(?<=subsection\{).+?(?=\})'
    reg_subsubsec = '(?<=subsubsection\{).+?(?=\})'    
    title_sec = re.findall(reg_sec,replaced)
    title_subsec = re.findall(reg_subsec,replaced)
    title_subsubsec = re.findall(reg_subsubsec,replaced)

    # font
    reg_bf = '(?<=textbf\{).+?(?=\})'
    reg_it = '(?<=textit\{).+?(?=\})'   
    txt_bf = re.findall(reg_bf,replaced)
    txt_it = re.findall(reg_it,replaced)


    # itembox
    for i in title_l:
        item_1 ="\\begin{itembox}[l]{" + i + "}"
        item_2 ="<div class='tex_itembox'><span class='title_l'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div>")

    for i in title_c:
        item_1 ="\\begin{itembox}[c]{" + i + "}"
        item_2 ="<div class='tex_itembox'><span class='title_c'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div>")

    for i in title_r:
        item_1 ="\\begin{itembox}[r]{" + i + "}"
        item_2 ="<div class='tex_itembox'><span class='title_r'>" + i + "</span>"
        replaced = replaced.replace(item_1,item_2).replace("\\end{itembox}","</div>")

    # sec
    for i in title_sec:
        sec_1 = "\\section{" + i + "}"
        sec_2 = "<h4>" + i + "</h4>"
        replaced = replaced.replace(sec_1,sec_2) 

    for i in title_subsec:
        sec_1 = "\\subsection{" + i + "}"
        sec_2 = "<h5>" + i + "</h5>"
        replaced = replaced.replace(sec_1,sec_2) 

    for i in title_subsubsec:
        sec_1 = "\\subsubsection{" + i + "}"
        sec_2 = "<h6>" + i + "</h6>"
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

    return replaced