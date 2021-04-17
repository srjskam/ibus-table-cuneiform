#!/usr/bin/env python
# coding: utf-8

# In[1]:


from xml.dom import minidom

x = minidom.parse('ogsl-sl.xml')


# In[2]:


reps = [
['š','sz'],
['Š','SZ'],
['ṣ','s,'],
['Ṣ','S,'],
['ṭ','t,'],
['Ṭ','T,'],
['ś',"s'"],
['Ś',"S'"],
['ʾ',"'"],
['₀','0'],
['₁','1'],
['₂','2'],
['₃','3'],
['₄','4'],
['₅','5'],
['₆','6'],
['₇','7'],
['₈','8'],
['₉','9'],
['ₓ','x'],
['ḫ','h,'],
['Ḫ','H,'],
['ŋ','j'],
['Ŋ','J'],
['û','u'],
['ā','aa'],
['ē','ee'],
['ī','ii'],
['ū','uu']
]

def normalize(s):
    for fro, to in reps:
        s=s.replace(fro, to)
    return s
    


# In[46]:





# In[70]:


def maybeadd(reading,unic,name=''):
    reading=normalize(reading)
    name=normalize(name)
    if reading not in mapping:
        mapping[reading]={(unic,name)}
    else:
        mapping[reading].add((unic,name))


# In[71]:


mapping = {}

for sign in x.getElementsByTagName('sign'):
    name = sign.attributes['n'].value.strip('|')
    unicodestr=''
    for child in sign.childNodes:
        if child.tagName == 'utf8':
            unicodestr = (child.childNodes[0].nodeValue)
        if child.tagName == 'v':
            reading = child.attributes['n'].value
            maybeadd(reading, unicodestr, name)
    if unicodestr!= '':
        maybeadd(name, unicodestr)
    for form in sign.getElementsByTagName('form'):
        name = form.attributes['n'].value.strip('|')
        #print(name)
        maybec = form.getElementsByTagName('g:c')
        unicodestr=''
        try:
            if len(maybec)>0 :
                unicodestr = maybec[0].attributes['g:utf8'].value
            else:
                unicodestr = form.getElementsByTagName('g:s')[0].attributes['g:utf8'].value
        except :
            pass
        for reading in form.getElementsByTagName('v'):
            if unicodestr != '':
                maybeadd(reading.attributes['n'].value, unicodestr, name)
        if unicodestr!= '':
            maybeadd(name, unicodestr)

mapping['darengal']


# In[72]:


valid_chars = ''.join(sorted(list(set(''.join(k for k in mapping.keys())))))
#''.join(k for k in mapping.keys())
valid_chars


# In[73]:


inf = ""
with open("ibus-tables-cuneiform_pre.txt",'r') as infile:
    inf = infile.read()
    inf = inf.replace('{VALID_INPUTS}', valid_chars)
with open("ibus-tables-cuneiform.txt",'w') as outfile:
    outfile.write(inf)
    for reading, vals in mapping.items():
        if len(vals)>1:
            for unic,name in vals:
                outfile.write(f"{reading}({name})\t{unic}\t0\t### {name}\n")
        else:
            unic,name = vals.pop()
            outfile.write(f"{reading}\t{unic}\t0\t### {name}\n")
    outfile.write("END_TABLE")

