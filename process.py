import os
import re


def clen(text):
    return len(text.encode('gb18030'))

def tp(text, l):
    return text + ' ' * (l - len(text))

def ctp(text, l):
    return text + ' ' * (l - clen(text))

pinyinToneMarks = {
    u'a': u'āáǎà', u'e': u'ēéěè', u'i': u'īíǐì',
    u'o': u'ōóǒò', u'u': u'ūúǔù', u'ü': u'ǖǘǚǜ',
    u'A': u'ĀÁǍÀ', u'E': u'ĒÉĚÈ', u'I': u'ĪÍǏÌ',
    u'O': u'ŌÓǑÒ', u'U': u'ŪÚǓÙ', u'Ü': u'ǕǗǙǛ'
}

def convertPinyinCallback(m):
    tone=int(m.group(3))%5
    r=m.group(1).replace(u'v', u'ü').replace(u'V', u'Ü')
    # for multple vowels, use first one if it is a/e/o, otherwise use second one
    pos=0
    if len(r)>1 and not r[0] in 'aeoAEO':
        pos=1
    if tone != 0:
        r=r[0:pos]+pinyinToneMarks[r[pos]][tone-1]+r[pos+1:]
    return r+m.group(2)

def convertPinyin(s):
    return re.sub('([aeiouüvÜ]{1,3})(n?g?r?)([012345])', convertPinyinCallback, s, flags=re.IGNORECASE)

BEGIN_DOCUMENT = '''
\\documentclass{article}
\\usepackage[T1,T2A]{fontenc}
\\usepackage[utf8]{inputenc}
\\usepackage[russian, english]{babel}
\\usepackage{CJKutf8}
\\begin{document}
'''

END_DOCUMENT="\\end{document}"

def generate_tex(table):
    tex = ''
    tex += '\\begin{tabular}{lll}\n'
    for c, p, r in table:
        tex += " \\begin{CJK}{UTF8}{gbsn} %s \\end{CJK} & \\begin{CJK}{UTF8}{gbsn} %s \\end{CJK}  & %s \\\\\n" % (c,p,r)
    tex += '\\end{tabular}'
    return tex

def generate_tex_ch(table):
    tex = ''
    tex += '\\begin{tabular}{lll}\n'
    for c, p, r in table:
        tex += " \\begin{CJK}{UTF8}{gbsn} %s \\end{CJK}  \\\\\n" % (c)
    tex += '\\end{tabular}'
    return tex

def generate_tex_pinyin(table):
    tex = ''
    tex += '\\begin{tabular}{lll}\n'
    for c, p, r in table:
        tex += " \\begin{CJK}{UTF8}{gbsn} %s \\end{CJK}  \\\\\n" % (p)
    tex += '\\end{tabular}'
    return tex

def generate_tex_rus(table):
    tex = ''
    tex += '\\begin{tabular}{lll}\n'
    for c, p, r in table:
        tex += " \\begin{CJK}{UTF8}{gbsn} %s \\end{CJK}  \\\\\n" % (r)
    tex += '\\end{tabular}'
    return tex

def parse_table(fname):
    table = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            c, p, r = line.split('\t')
            c = c.strip()
            p = convertPinyin(p.strip())
            r = r.strip()
            table.append((c, p, r))
    return table

def main():
    output_tex = 'chinese.tex'
    output_tex_c = 'chinese-ch.tex'
    output_tex_p = 'chinese-pinyin.tex'
    output_tex_r = 'chinese-rus.tex'

    tex = BEGIN_DOCUMENT
    tex_c = BEGIN_DOCUMENT
    tex_p = BEGIN_DOCUMENT
    tex_r = BEGIN_DOCUMENT
    fnames = [x for x in os.listdir('.') if x.endswith('.txt')]
    for fname in fnames:
        lesson_num = fname.replace('.txt', '').replace('lesson', '')
        table = parse_table(fname)
        tex += '\\section{Lesson %s}\n' % lesson_num
        tex += generate_tex(table) + "\n\n"
        tex += "\\newpage"

        tex_c += '\\section{Lesson %s}\n' % lesson_num
        tex_c += generate_tex_ch(table) + "\n\n"
        tex_c += "\\newpage"

        tex_p += '\\section{Lesson %s}\n' % lesson_num
        tex_p += generate_tex_pinyin(table) + "\n\n"
        tex_p += "\\newpage"

        tex_r += '\\section{Lesson %s}\n' % lesson_num
        tex_r += generate_tex_rus(table) + "\n\n"
        tex_r += "\\newpage"
    tex += END_DOCUMENT + '\n'
    tex_c += END_DOCUMENT + '\n'
    tex_p += END_DOCUMENT + '\n'
    tex_r += END_DOCUMENT + '\n'

    with open(output_tex, 'w') as f:
        f.write(tex)
    os.system('pdflatex %s' % output_tex)

    with open(output_tex_c, 'w') as f:
        f.write(tex_c)
    os.system('pdflatex %s' % output_tex_c)
    with open(output_tex_p, 'w') as f:
        f.write(tex_p)
    os.system('pdflatex %s' % output_tex_p)
    with open(output_tex_r, 'w') as f:
        f.write(tex_r)
    os.system('pdflatex %s' % output_tex_r)


if __name__ == "__main__":
    main()







