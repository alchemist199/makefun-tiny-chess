import json,os,urllib.request as R
U=os.getenv('MAKEFUN_ENV_URL')
V=(0,100,320,330,500,900,0)
P={1:'dddd}}}}iinsffipdddnfa_dfiiZdddd'}
KN=(33,31,-31,-33,18,14,-14,-18);BI=(15,17,-15,-17);RO=(1,-1,16,-16);KI=RO+BI
D=(KN,BI,RO,KI,KI)
S=[i for i in range(128)if not i&136]
CK={4:12,7:14,0:13,116:3,119:11,112:7}
B=[0]*128;T=1;C=15;E=-1;W=4;K=116;N=0;L=15e4;TT={}
def q(p,b):
 return json.load(R.urlopen(U+p,json.dumps(b).encode()))
def pf(f):
 global B,T,C,E,W,K
 a=f.split();B=[0]*128
 for i,r in enumerate(a[0].split('/')):
  y=7-i;x=0
  for c in r:
   if c.isdigit():x+=int(c)
   else:
    v='PNBRQK'.index(c.upper())+1
    if c.islower():v=-v
    B[y*16+x]=v
    if v==6:W=y*16+x
    if v==-6:K=y*16+x
    x+=1
 T=2*(a[1]=='w')-1;C=sum(1<<'KQkq'.index(c)for c in a[2]if c in'KQkq')
 E=ord(a[3][0])-97+(int(a[3][1])-1)*16 if a[3]!='-'else-1
def at(s,y):
 for O,p in(((-15*y,-17*y),y),(KN,2*y),(KI,6*y)):
  for o in O:
   z=s+o
   if not z&136 and B[z]==p:return 1
 for O,ps in((BI,(3*y,5*y)),(RO,(4*y,5*y))):
  for o in O:
   z=s+o
   while not z&136 and not B[z]:z+=o
   if not z&136 and B[z]in ps:return 1
 return 0
def lg():return at(W if T<0 else K,T)
def gn(cp=0):
 m=[]
 for s in S:
  p=B[s]
  if not p or p*T<0:continue
  t=abs(p)
  if t==1:
   d=16*T
   for o in(0,-1,1):
    z=s+d+o
    if z&136:continue
    if o:
     if z!=E and(not B[z]or B[z]*T>0):continue
    elif B[z]:continue
    if z>>4 in(0,7):
     for v in(5,4,3,2):m.append(s|z<<7|v<<14)
    elif o or not cp:m.append(s|z<<7)
   if not cp and s>>4==1+5*(T<0)and not(B[s+d]or B[s+2*d]):m.append(s|(s+2*d)<<7)
  else:
   for o in D[t-2]:
    z=s+o
    while not z&136:
     if B[z]:
      if B[z]*T<0:m.append(s|z<<7)
      break
     if not cp:m.append(s|z<<7)
     if t%4==2:break
     z+=o
  if t==6 and s==60-56*T:
   for d,r in((1,3),(-1,-4)):
    if C&((1+(d<0))*2**(1-T))and B[s+r]==4*T and all(not B[z]for z in range(s+d,s+r,d))and not(at(s,-T)or at(s+d,-T))and not cp:m.append(s|(s+2*d)<<7)
 return m
def mk(x):
 global T,C,E,W,K
 f=x&127;t=x>>7&127;z=x>>14;c=B[f];v=B[t];e=-1
 if abs(c)==1 and t==E and not v:e=t-16*T;v=B[e];B[e]=0
 u=(v,e,C,E,W,K);B[t]=(z if c>0 else-z)if z else c;B[f]=0
 if c==6:W=t
 if c==-6:K=t
 if c*c==36 and abs(t-f)==2:
  a,b=(f+3,f+1)if t>f else(f-4,f-1);B[b]=B[a];B[a]=0
 C&=CK.get(f,15)&CK.get(t,15);E=(f+t)//2 if abs(c)==1 and abs(t-f)==32 else-1;T=-T
 return u
def un(x,u):
 global T,C,E,W,K
 f=x&127;t=x>>7&127;z=x>>14;v,e,C,E,W,K=u;c=B[t];T=-T
 if c*c==36 and abs(t-f)==2:
  a,b=(f+3,f+1)if t>f else(f-4,f-1);B[a]=B[b];B[b]=0
 B[f]=c if not z else c//abs(c);B[t]=0
 if e>=0:B[e]=v
 elif v:B[t]=v
def ev():
 s=0
 for z in S:
  p=B[z]
  if p:
   t=abs(p);f=z&7;f=min(f,7-f);r=z>>4
   v=V[t]+(ord(P.get(t,'d'*32)[(r if p<0 else 7-r)*4+f])-100)*2
   s+=v*p//abs(p)
 return s*T
def cv(x):
 t=B[x>>7&127]
 return V[abs(t)]*10 if t else 900 if x>>14 else 0
def qs(a,b):
 global N
 N+=1
 s=ev()
 if s>=b:return b
 if s>a:a=s
 ms=gn(1);ms.sort(key=cv,reverse=1)
 for x in ms:
  u=mk(x)
  if lg():un(x,u);continue
  s=-qs(-b,-a);un(x,u)
  if s>=b:return b
  if s>a:a=s
 return a
def sr(d,a,b):
 global N
 N+=1
 if N>L:raise Exception
 if d<=0:return qs(a,b)
 k=(tuple(B),T,C,E);e=TT.get(k)
 if e and e[0]>=d and(e[2]==0 or(e[1]>=b if e[2]==1 else e[1]<=a)):return e[1]
 ms=gn();ms.sort(key=lambda x:-1e4 if x==(e and e[3])else-cv(x))
 bs=-1e4;bm=0;fl=2
 for x in ms:
  u=mk(x)
  if lg():un(x,u);continue
  s=-sr(d-1,-b,-a);un(x,u)
  if s>bs:bs=s;bm=x
  if s>a:a=s;fl=0
  if a>=b:fl=1;break
 if bs==-1e4:return-9990 if at(W if T>0 else K,-T)else 0
 TT[k]=(d,bs,fl,bm)
 return bs
def rt():
 global N
 bs=0;N=0
 for d in range(29):
  try:
   ms=gn();v=-1e4;w=0
   for x in ms:
    u=mk(x)
    if lg():un(x,u);continue
    s=-sr(d,-1e4,1e4);un(x,u)
    if s>v:v=s;w=x
   bs=w
  except:break
 return bs
def uc(x):
 f=x&127;t=x>>7&127;z=x>>14
 return chr(97+f%8)+str(f//16+1)+chr(97+t%8)+str(t//16+1)+('nbrq'[z-2]if z else'')
while 1:
 g=q('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  pf(g['fen']);m=rt()
  g=q('/move',{'game':g['game'],'move':uc(m)})
