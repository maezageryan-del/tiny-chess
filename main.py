V=[0,100,320,330,500,900,0]
CM={4:12,7:14,0:13,60:3,63:11,56:7}
DR=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
KN=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
RY=[];NA=[];KA=[]
for q in range(64):
 f,r=q&7,q>>3
 RY.append([[q+(dr*8+df)*i for i in range(1,8)if 0<=f+df*i<8 and 0<=r+dr*i<8]for df,dr in DR])
 KA.append([z[0] for z in RY[q] if z])
 NA.append([(r+dy)*8+f+dx for dx,dy in KN if 0<=f+dx<8 and 0<=r+dy<8])
P=type('P',(),{})
def PS(pc,q):
 x=q&7;y=q>>3
 if pc<0:y=7-y
 w=min(x,7-x);c=w+min(y,7-y)
 return(0,y*y+w,7*c,5*c,w,c,-4*c)[abs(pc)]
def add(p,pc,q,g):
 p.ev+=(g if pc>0 else-g)*(V[abs(pc)]+PS(pc,q))
def fen(p):
 p.s=1;p.c=15;p.e=-1;p.ev=0;p.hs=[];p.kq=[4,60]
 p.b=[4,2,3,5,6,3,2,4]+[1]*8+[0]*32+[-1]*8+[-4,-2,-3,-5,-6,-3,-2,-4]
def atk(p,q,by):
 b=p.b;f=q&7;r=q>>3
 if 0<=r-by<8 and any(b[(r-by)*8+f+d]==by for d in(-1,1)if 0<=f+d<8):return 1
 if any(b[t]==pc*by for lst,pc in((NA,2),(KA,6))for t in lst[q]):return 1
 for d in range(8):
  pc=next((b[t]for t in RY[q][d]if b[t]),0)
  if pc and pc*by>0 and abs(pc)in((4,5)if d<4 else(3,5)):return 1
 return 0
def gen(p):
 b=p.b;s=p.s;mvs=[];ap=mvs.append
 for q in range(64):
  pc=b[q]
  if not pc or(pc>0)!=(s>0):continue
  t=abs(pc);f=q&7;r=q>>3
  def ap2(to):ap(q|to<<6|(5<<12 if to>>3 in(0,7)else 0))
  if t==1:
   d=8*s;one=q+d
   if not b[one]:
    ap2(one)
    if r==1+5*(s<0)and not b[q+2*d]:ap(q|(q+2*d)<<6)
   for df in(-1,1):
    to=one+df
    if 0<=f+df<8 and(b[to]*s<0 or to==p.e):ap2(to)
  elif t==2 or t==6:
   for to in(NA if t==2 else KA)[q]:
    vic=b[to]
    if not vic or(vic>0)!=(s>0):ap(q|to<<6)
   if t==6 and q==4+56*(s<0):
    for bit,dst,emp,tr in((1,2,(1,2),(0,1,2)),(2,-2,(-1,-2,-3),(0,-1,-2))):
     if p.c&(bit<<2*(s<0))and b[q+(3 if dst>0 else-4)]==4*s and all(not b[q+e]for e in emp)and all(not atk(p,q+u,-s)for u in tr):ap(q|(q+dst)<<6)
  else:
   for d in range(4*(t==3),4+(t!=4)*4):
    for to in RY[q][d]:
     vic=b[to]
     if vic:
      if(vic>0)!=(s>0):ap(q|to<<6)
      break
     ap(q|to<<6)
 return mvs
def make(p,m):
 b=p.b;f=m&63;t=m>>6&63;pc=b[f];s=p.s;cap=b[t]
 p.hs.append((b[:],p.c,p.e,p.ev,p.kq[:]))
 if abs(pc)==1 and t==p.e:cs=t-8*s;cap=b[cs];add(p,cap,cs,-1);b[cs]=0
 elif cap:add(p,cap,t,-1)
 add(p,pc,f,-1);b[f]=0
 npc=(m>>12)*s or pc
 if abs(pc)==6:p.kq[pc<0]=t
 b[t]=npc;add(p,npc,t,1)
 if abs(pc)==6 and abs(t-f)==2:
  rf,rt=(f+3,f+1)if t>f else(f-4,f-1);rk=b[rf];add(p,rk,rf,-1);add(p,rk,rt,1);b[rf]=0;b[rt]=rk
 p.e=f+8*s if abs(pc)==1 and t-f==16*s else-1
 p.c&=CM.get(f,15)&CM.get(t,15)
 p.s=-s
def unmake(p):
 p.b,p.c,p.e,p.ev,p.kq=p.hs.pop();p.s=-p.s
MATE=100000;INF=200000;BUD=80000
ND=[0];AB=[0];BM=[0]
def neg(p,d,alpha,beta,ply):
 ND[0]+=1
 if ND[0]>BUD:AB[0]=1;return 0
 ck=atk(p,p.kq[p.s<0],-p.s)
 if d<=0 and not ck:
  if d<-6:return p.ev*p.s
  st=p.ev*p.s
  if st>=beta:return st
  if st>alpha:alpha=st
 best=alpha if d<=0 and not ck else-INF
 for m in sorted(gen(p),key=lambda m:V[abs(p.b[m&63])]//40-V[abs(p.b[m>>6&63])]):
  if d<=0 and not ck and not p.b[m>>6&63]:continue
  make(p,m)
  if atk(p,p.kq[p.s>0],p.s):unmake(p);continue
  sc=-neg(p,d-1,-beta,-alpha,ply+1);unmake(p)
  if AB[0]:return 0
  if sc>best:best=alpha=sc;bm=m
  if alpha>=beta:break
 if best==-INF:return-MATE+ply if ck else 0
 if not ply:BM[0]=bm
 return best
def choose(p):
 ND[0]=0
 for d in range(1,64):
  AB[0]=0;neg(p,d,-INF,INF,0)
  if AB[0]:break
 return BM[0]
def uci(m):f=m&63;t=m>>6&63;return chr(97+(f&7))+chr(49+f//8)+chr(97+(t&7))+chr(49+t//8)+('nbrq'[m//4096-2]if m>>12 else'')
def parse(u):
 return ord(u[0])-97+(int(u[1])-1)*8|((ord(u[2])-97)+(int(u[3])-1)*8)<<6|(('nbrq'.index(u[4])+2 if len(u)>4 else 0))<<12
import os,json,urllib.request as RQ
url=os.environ['MAKEFUN_ENV_URL']
pos=P()
while True:
 g=json.loads(RQ.urlopen(url+'/game',b'{}').read())
 if g['status']=='done':break
 while g['status']=='your_move':
  fen(pos)
  for u in g['moves']:make(pos,parse(u))
  u=uci(choose(pos))
  if u not in g['legal_moves']:u=g['legal_moves'][0]
  g=json.loads(RQ.urlopen(url+'/move',json.dumps({'game':g['game'],'move':u}).encode()).read())
