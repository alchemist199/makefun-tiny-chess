import json,os,urllib.request as R
U=os.getenv('MAKEFUN_ENV_URL')
V=(0,100,320,330,500,900,0)
P={1:'dddd}}}}iinsffipdddnfa_dfiiZdddd'}
J=(33,31,-31,-33,18,14,-14,-18);I=(15,17,-15,-17);H=(1,-1,16,-16);G=H+I
D=(J,I,H,G,G)
S=[i for i in range(128)if i%16<8]
CK={4:12,7:14,0:13,116:3,119:11,112:7}
L=20e4;TT={};Y=(0,0,8,8,3,3,-8)
def q(p,b):
 return json.load(R.urlopen(U+p,json.dumps(b).encode()))
def pf(f):
 global B,T,C,E,W,K
 a=f.split();B=[0]*128
 for i,r in enumerate(a[0].split('/')):
  z=(7-i)*16
  for c in r:
   if c.isdigit():z+=int(c)
   else:
    v='PNBRQK'.index(c.upper())+1
    if c.islower():v=-v
    B[z]=v
    if v==6:W=z
    if v==-6:K=z
    z+=1
 T=2*(a[1]=='w')-1;C=sum(1<<'KQkq'.index(c)for c in a[2]if c in'KQkq')
 E=ord(a[3][0])-97+(int(a[3][1])-1)*16 if a[3]!='-'else-1
def at(s,y):
 for O,p in(((-15*y,-17*y),y),(J,2*y),(G,6*y)):
  for o in O:
   z=s+o
   if z&136<1 and B[z]==p:return 1
 for O,ps in((I,(3*y,5*y)),(H,(4*y,5*y))):
  for o in O:
   z=s+o
   while z&136<1 and not B[z]:z+=o
   if z&136<1 and B[z]in ps:return 1
 return 0
def lg():return at((W,K)[T>0],T)
def gn(cp=0):
 m=[];a=m.append
 for s in S:
  p=B[s]
  if p*T<1:continue
  t=abs(p)
  if t==1:
   d=16*T
   for o in(0,-1,1):
    z=s+d+o
    if z&136:continue
    if o:
     if z!=E and B[z]*T>=0:continue
    elif B[z]:continue
    if z>>4 in(0,7):
     for v in(5,4,3,2):a(s|z<<7|v<<14)
    elif o or not cp:a(s|z<<7)
   if not cp and s>>4==1+5*(T<0)and not(B[s+d]or B[s+2*d]):a(s|(s+2*d)<<7)
  else:
   for o in D[t-2]:
    z=s+o
    while z&136<1:
     if B[z]*T<0:a(s|z<<7);break
     if B[z]:break
     if not cp:a(s|z<<7)
     if t%4==2:break
     z+=o
  if t==6 and s==60-56*T:
   for d,r in((1,3),(-1,-4)):
    if C>>(1-T+(d<0))&1 and B[s+r]==4*T and all(not B[z]for z in range(s+d,s+r,d))and not(at(s,-T)or at(s+d,-T))and not cp:a(s|(s+2*d)<<7)
 return m
def mk(x):
 global T,C,E,W,K
 f=x&127;t=x>>7&127;z=x>>14;c=B[f];v=B[t];e=-1
 if abs(c)==1 and t==E and not v:e=t-16*T;v=B[e];B[e]=0
 u=(v,e,C,E,W,K);B[t]=z*c//abs(c)if z else c;B[f]=0
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
 B[f]=c//abs(c)if z else c;B[t]=0
 if e>=0:B[e]=v
 elif v:B[t]=v
def ev():
 s=0
 for z in S:
  p=B[z]
  if p:
   t=abs(p);f=z&7;f=min(f,7-f);r=z>>4
   v=V[t]+(ord(P.get(t,'d'*32)[(r^(7*(p>0)))*4+f])-100)*2+Y[t]*(f+min(r,7-r))
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
 if N>L:1/0
 if d<=0:return qs(a,b)
 k=(tuple(B),T,C,E);e=TT.get(k)
 if e and e[0]>=d and(e[2]==0 or e[1]>=b if e[2]<2 else e[1]<=a):return e[1]
 ms=gn();ms.sort(key=lambda x:(x!=(e and e[3]))*1e4-cv(x))
 bs=-1e4;bm=0;fl=2
 for x in ms:
  u=mk(x)
  if lg():un(x,u);continue
  s=-sr(d-1,-b,-a);un(x,u)
  if s>bs:bs=s;bm=x
  if s>a:a=s;fl=0
  if a>=b:fl=1;break
 if bs==-1e4:return-9990+d if at((W,K)[T<0],-T)else 0
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
  pf(g['fen']);m=rt();g=q('/move',{'game':g['game'],'move':uc(m)})
