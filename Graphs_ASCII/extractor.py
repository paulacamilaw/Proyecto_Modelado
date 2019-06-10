import sys
import numpy as np

filedata = open('1input_plots.par', 'r')
lines = filedata.readlines()
xmin = float(lines[1].split('=')[1])
xmax = float(lines[2].split('=')[1])
ymin = float(lines[3].split('=')[1])
ymax = float(lines[4].split('=')[1])
zmin = float(lines[5].split('=')[1])
zmax = float(lines[6].split('=')[1])
Nxx = int(lines[7].split('=')[1])
Nyy = int(lines[8].split('=')[1])
Nzz = int(lines[9].split('=')[1])
Ntt = int(lines[10].split('=')[1])
courant = float(lines[11].split('=')[1])
every3D = float(lines[14].split('=')[1])
filedata.close()

dx  = (xmax - xmin)/float(Nxx)
dy  = (ymax - ymin)/float(Nyy)
dz  = (zmax - zmin)/float(Nzz)
dt = courant * min(dx,dy,dz)

f = open('primitivas_1.xyzl', 'r') 

def extraer(parametro):
    variable = str(parametro.split('-')[0])
    bloque = format(int(parametro.split('-')[1]), '02')
    t = dt*float(bloque)*every3D
    print 'Extrayendo la variable',variable,'en el bloque',bloque,'en',t, 'segundos.'
    
    skip = int((((Nyy+2)*(Nxx+1)+1)*(Nzz+1)+4)*int(bloque))
    print 'Se saltan', skip, 'lineas.'
    for a in range (0,skip+3):
        f.readline()

    w = open('%s_b%s.3D'%(variable,bloque), 'wt')
    if ((variable == 'vectv') or (variable == 'vectB')):
        w.write('x y z valuex valuey valuez\n');
    elif ((variable != 'vectv') or (variable != 'vectB')):
        w.write('x y z value\n');
    
    for i in range (0,Nzz+1):
        f.readline() 
        for j in range (0,Nxx+1):
            f.readline()
            for k in range (0,Nyy+1):
                #print i, j, k
                z, x, y, rho, vx, vy, vz, press, Bx, By, Bz = f.readline().split()
                #print x, y, z, vx
                if (variable == 'v'):
                    v = np.sqrt(float(vx)**2+float(vy)**2+float(vz)**2)
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(v)))
                elif (variable == 'B'):
                    B = np.sqrt(float(Bx)**2+float(By)**2+float(Bz)**2)
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(B)))
                elif (variable == 'rho'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(rho)))
                elif (variable == 'vx'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(vx)))
                elif (variable == 'vy'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(vy)))
                elif (variable == 'vz'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(vz)))
                elif (variable == 'press'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(press)))
                elif (variable == 'Bx'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(Bx)))
                elif (variable == 'By'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(By)))
                elif (variable == 'Bz'):
                    w.write('%g %g %g %g\n' %(float(x),float(y),float(z),float(Bz)))
                elif (variable == 'vectv'):
                    w.write('%g %g %g %g %g %g\n' %(float(x),float(y),float(z),float(vx),float(vy),float(vz)))
                elif (variable == 'vectB'):
                    w.write('%g %g %g %g %g %g\n' %(float(x),float(y),float(z),float(Bx),float(By),float(Bz)))
                else: print 'Ingresa una variable valida entre rho, vx, vy, vz, press, Bx, By, Bz, v, B'
    w.close()
    f.close()
        
method_name = sys.argv[1]
parameter_name = sys.argv[2]
getattr(sys.modules[__name__], method_name)(parameter_name)

