import sys
import numpy as np

# Se importa el archivo con los datos correspondientes a las dimensiones y tiempos de las corridas
filedata = open('1input_plots.par', 'r')

lines = filedata.readlines()
# Se asignan la variables del archivo filedata en las variables correspondientes
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

# Se cierra el archivo
filedata.close()

# Se calculan los pasos espaciales y temporales
dx  = (xmax - xmin)/float(Nxx)
dy  = (ymax - ymin)/float(Nyy)
dz  = (zmax - zmin)/float(Nzz)
dt = courant * min(dx,dy,dz)

# Se importa el archivo con los datos de las corridas correspondientes a las variables
# densidad, velocidad en x, y, z, presion y campo magnetico en x, y, z
f = open('primitivas_1.xyzl', 'r') 

# Se crea la funcion 'extraer' para tomar determinado tiempo y variable del archivo f
def extraer(parametro):
    
    # Se leen las entradas para reconocer la variable y tiempo a extraer
    variable = str(parametro.split('-')[0])
    bloque = format(int(parametro.split('-')[1]), '02')
    
    # Se calcula el tiempo real que se esta extrayendo
    t = dt*float(bloque)*every3D
    
    # Se valida la infomacion acerca de la variable, el bloque de tiempo y el tiempo
    # real que se esta extrayendo
    print 'Extrayendo la variable',variable,'en el bloque',bloque,'en',t, 'segundos.'
    
    # Se saltan las lineas correspondientes a los tiempos anteriores al que se requiere
    skip = int((((Nyy+2)*(Nxx+1)+1)*(Nzz+1)+4)*int(bloque))
    print 'Se saltan', skip, 'lineas.'
    for a in range (0,skip+3):
        f.readline()
    
    # Se crea un archivo nuevo llamado por el nombre de la variable y el bloque a extraer
    w = open('%s_b%s.3D'%(variable,bloque), 'wt')
    # Se escribe el encabezado necesario para que VisIt pueda leer los archivos ASCII
    w.write('x y z %s\n'%variable);
    
    # Se leen las lineas de la misma manera como fueron salvadas y se reescriben
    # los datos requeridos en el archivo w
    for i in range (0,Nzz+1):
        f.readline() 
        for j in range (0,Nxx+1):
            f.readline()
            for k in range (0,Nyy+1):
                z, x, y, rho, vx, vy, vz, press, Bx, By, Bz = f.readline().split()
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
                
    # Se cierran ambos archivos
    w.close()
    f.close()
        
# Se utilizan estas 3 lineas para llamar la funcion e ingresar la variable y bloque a salvar desde la terminal
method_name = sys.argv[1]
parameter_name = sys.argv[2]
getattr(sys.modules[__name__], method_name)(parameter_name)
