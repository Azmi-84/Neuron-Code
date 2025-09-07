import CoolProp
import CoolProp.CoolProp as CP
print('CoolProp version:', CoolProp.__version__)
from CoolProp.CoolProp import PropsSI
#Power Need to generate
#Given 250 MVA electrical generator supplying electricity to the regional grid
# Considering Power factor 0.9
# Combined Cycle
# GAS CYCLE PART( Brayton Cycle)
## State 5
p5=100*10**3
t5=300
h5=(PropsSI('H','P', p5,'T',t5,'Air'))
print('h5=',h5/1000,'KJ/kg')

s5 = PropsSI('S','P', p5,'T',t5,'Air')
print('s5=',s5/1000,'KJ/kg')
#State 6
#Considering compressor efficiency of the steam 84%
#Calculated the compressor output temperature t6=610k
t6=678 #k
p6=1200*10**3
h6=(PropsSI('H','P', p6,'T',t6,'Air'))
s6 = PropsSI('S','P', p6,'T',t6,'Air')
print('h6=',h6/1000,'KJ/kg')
print('s6=',s6/1000,'KJ/kg')
##state 7
p7=1200*10**3
t7=1400 #k
h7=(PropsSI('H','P', p7,'T',t7,'Air'))
print('h7=',h7/1000,'KJ/kg')
s7 = PropsSI('S','P', p7,'T',t7,'Air')
print('s7=',s7/1000,'KJ/kg')
#State 8
#Gas turbine efficiency 88%
#Calculated the turbine output temperature t6=778 k
t8=778.68341 #k
p8=p5
h8=(PropsSI('H','P', p5,'T',t8,'Air'))
print('h8=',h8/1000,'KJ/kg')
s8 = PropsSI('S','P', p8,'T',t8,'Air')
print('s8=',s8/1000,'KJ/kg')
#State 9
t9=400 #k
p9=p5
h9=(PropsSI('H','P', p5,'T',t9,'Air'))
print('h9=',h9/1000,'KJ/kg')
s9 = PropsSI('S','P', p5,'T',t9,'Air')
print('s9=',s9/1000,'KJ/kg')
## FOR STEAM PORTION
##Turbine and pump Efficicency 90% and 80%
#State 1
p1=8000 #pa
q1=0
h1=(PropsSI('H','P', p1,'Q',q1,'water'))
print('h1=',h1/1000,'KJ/kg')

x=h1/1000
s1 = PropsSI('S','P', p1,'Q',q1,'water')
print('s1=',s1/1000,'KJ/kg')
#State 2
p2=8*10**6
Wpump=10.05993 #kJ/kg (work done by pump when efficiency is 80%)
h2= x+Wpump
print('h2=', x + Wpump,'KJ/kg')
s2 = PropsSI('S','H', h2*1000,'P',p2,'water')
print('s2=',s2/1000,'KJ/kg')
#State 3
p3=8*10**6
t3=673 #k
h3=(PropsSI('H','P', p3,'T',t3,'water'))
print('h3=',h3/1000,'KJ/kg')
s3 = PropsSI('S','T',t3,'P',p3,'water')
print('s3=',s3/1000,'KJ/kg')
#State 4
p4=p1
q4=0.8077 #Considering Turbine efficiency 90%
h4=(PropsSI('H','P', p4,'Q',q4,'water'))
print('h4=',h4/1000,'KJ/kg')
s4 = PropsSI('S','P',p4,'Q',q4,'water')
print('s4=',s4/1000,'KJ/kg')
## THERMAL EFFICIENCY
#ENERGY BALANCE IN THE HRSG
#Mg*Cp(t8-t9)=Ms(h3-h2)
#Ms/Mg=0.128
#WE GET Mg=100 kg/s & Ms=12.8369 Kg/s
Mg=100 #kg/s
Ms=12.8369 #kg/s
Qin=(Mg*(h7-h6))/10**6 # KJ/Kg
print('Qin=',(Mg*(h7-h6))/10**6,'MW')
#1st Law efficiency
Wnet=Mg*(h7-h8)+Ms*(h3-h4)-Mg*(h6-h5)-Ms*(h2*10**3-h1)
print('Wnet=',Wnet/10**6,'MW')
print('Eta=',((Wnet/10**6)/Qin)*100,'%')
# ||EXERGY ANALYSIS||
## T0= 300k and p0=100kpa

import math
T0=300
p0=100*10**3
#1. GAS Turbine
Xdest78 = Mg*T0*(s8/10**3-s7/10**3-0.287*(math.log((p8/p7),2.718)))
print('Xdest78=',Xdest78/10**3,'MW')
#2. Compressor
Xdest56 = Mg*T0*(s6/10**3-s5/10**3-0.287*(math.log((p6/p7),2.718)))
print('Xdest56=',Xdest56/10**3,'MW')
# 3. Steam Turbine
Xdest34 = Ms*T0*(s4/10**3-s3/10**3)
print('Xdest34=',Xdest34/10**3,'MW')
#4.Pump
Xdest12 = Ms*T0*(s2/10**3-s1/10**3)
print('Xdest12=',Xdest12/10**3,'MW')
#5.HRSH
Xdest=Ms*T0*(s3/10**3-s2/10**3)+Mg*T0*(s9/10**3-s8/10**3)
print('Xdest=',Xdest/10**3,'MW')
# State 6-7
qin67=(h7-h6)/10**3
print('qin67',qin67,'KJ/Kg')
Tin=1600 #k
Xdest67 = Mg*T0*(s7/10**3-s6/10**3-qin67/Tin)
print('Xdest67=',Xdest67/10**3,'MW')
#Condenser State 4-1
qout41=(h4-h1)/10**3
print('qout41',qout41,'KJ/Kg')
Tout=300 #k
Xdest41 = Ms*T0*(s1/10**3-s4/10**3+qout41/Tout)
print('Xdest41=',Xdest41/10**3,'MW')
# Total Exergy Destruction
XdestTotal=(Xdest78+Xdest56+Xdest34+Xdest12+Xdest+Xdest67+Xdest41)/10**3
print('XdestTotal=',XdestTotal,'MW')
#NOW Exergy expanded
Xdestin=(1-T0/Tin)*Qin
print('Xdestin=',Xdestin,'MW')
Xwpump=Ms*(h2-h1/10**3)/10**3
print('Xwpump=',Xwpump,'MW')

Xwcomp=Mg*(h6-h5)/10**6
print('Xwcomp=',Xwcomp,'MW')
Xexpanded=(Xdestin+Xwpump+Xwcomp)
print('Xexpanded=',Xexpanded,'MW')
## Second Law Efficiency
Eta2=(1-XdestTotal/Xexpanded)
print('Eta2=',Eta2*100,'%')
#Gas Turbine Outpu
WTurbineOut=(Mg*(h7/10**3-h8/10**3)+Ms*(h3/10**3-h4/10**3))/10**3
print('WTurbineOut=',WTurbineOut,'MW')