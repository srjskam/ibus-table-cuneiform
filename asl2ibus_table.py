#!/usr/bin/env python
# coding: utf-8

# In[105]:


from xml.dom import minidom

with open('ogsl.asl', 'r') as infile:
    asl = infile.read()


# In[106]:


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
['ū','uu'],
    ['×','x'],
    ['°','0'],
    ['·','.'],
    ['⁺','+'],
    ['⁻','-'],
    ['𒑱',':'],
]

def to_ascii(s):
    for fro, to in reps:
        s=s.replace(fro, to)
    return s
    


# In[107]:


def unistr2unicode(x):
    x=x.replace('X', "x58") # replace X with unicode X
    x=x.replace('None', "x58") # replace None with unicode X (|UD.MA₂.AB×(U.U.U).ŠIR|)
    return ''.join(chr(int(y[1:], base=16)) for y in x.split('.'))
print(unistr2unicode("x12000.x12094.x1223E"))
print(unistr2unicode("x12000"))


# In[108]:


def maybeadd(reading,unic,sign=''):
    reading=to_ascii(reading).strip('|')
    sign=to_ascii(sign).strip('|')
    if reading not in mapping:
        mapping[reading]={(unic,sign)}
    else:
        mapping[reading].add((unic,sign))


# In[109]:


mapping = {}

funic = None
unic = None
form = False
for line in asl.splitlines():
    if line =="":
        continue
    if line.startswith("@sign"):
        #print(line)
        sign = line.split()[1]
    if line=="@end sign":
        if sign and unic and not form:
            maybeadd(sign, unic)
        if sign and funic and form: # end sign also ends last form
            maybeadd(sign, funic)
        form = False
        unic = None
        funic = None
        sign = None
        
    if line.startswith("@v"):
        reading = line.split()[1]
        if sign and unic and not form:
            maybeadd(reading, unic, sign)
        if sign and funic and  form:
            maybeadd(reading, funic, sign)
        
    if line.startswith("@ucode"):
        if form:
            funic = unistr2unicode(line.split()[1])
        else:
            unic = unistr2unicode(line.split()[1])
    #if line.startswith("@uname"):
    #    uname = unistr2unicode(line.split(maxsplit=1))[1]
        
    if line.startswith("@form"):
        form = True
        foo, formcode, sign, *foo = line.split()
    if line=="@end form":
        form = False
        if sign and funic:
            maybeadd(sign, funic)
        funic = None
        sign = None
    if line.startswith("@form"):
        pass
mapping['darengal']


# In[110]:


valid_chars = ''.join(sorted(list(set(''.join(k for k in mapping.keys())))))
#''.join(k for k in mapping.keys())
valid_chars


# In[111]:


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

