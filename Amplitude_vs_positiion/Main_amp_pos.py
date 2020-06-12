__author__ = 'apa'



"""    Program to normalize a file based on RMS of data amplitudes and write as I*2 output using GPR_Tools module """



import numpy as np
import matplotlib.pyplot as plt
import os
import sys


sys.path.append("C:\\Users\\apa\\PycharmProjects")


print sys.path

import GPR_Tools as G_T


from optparse import OptionParser


#file_in= "XL0040"
#file_in="borpipes"
file_in="Line01-Spin_2_2"

start_time=13
end_time=16.4

start_time = 13.7
end_time= 16.6


#file_in='C:\Temp\AAAA- Near surface target enhancement\Data Examples\StaceySidewalk\Nov_17_2017\Noggin_500_Sidewalk-2'
#file_out='C:\Temp\AAAA- Near surface target enhancement\Data Examples\StaceySidewalk\Nov_17_2017\Noggin_500_Sidewalk-2-SEC3a'

#file_in='C:\Temp\AAAA- Near surface target enhancement\Data Examples\StaceySidewalk\Jan_6_2017a\Noggin_250_North_Sidewalk'
#file_out='C:\Temp\AAAA- Near surface target enhancement\Data Examples\StaceySidewalk\Jan_6_2017a\Noggin_250_North_Sidewalk-SEC3a'


www=[]
data=[]

amp=[]
angle=[]

in_hd= file_in+'.hd'
in_dt1= file_in+'.dt1'

#print in_hd,  in_dt1


a = G_T.PGIO.Header(in_hd)
a.readheader()
print  a.data_type[0:3]



#exit(200)



# Open the input and output .dt1 files

aa = G_T.PGIO.dt1(in_dt1, a.ntraces, a.npts_trace, a.data_type)


# read in the whole input file
in_thd = []
in_dat = []

#Read the input file

in_thd, in_dat = aa.read_section()


#Dewow the input data and make floating point

dat = np.ndarray(shape=(a.npts_trace, a.ntraces), dtype=np.float32)

pulse_width =  int(3000. / (2. * a.frequency * a.sampling/1000.))  # width in sample points


#gain = GGG.GFG(a.time_window, a.sampling/1000., a.timezero*a.sampling/1000., a.frequency, 0.0, 0.0, velocity, alpha, G_scale,  G_floor,  G_max, 'planar')

perfect=[]
phase=-40 # Spin 1
phase=-52   # spin 2

start_point= int(a.timezero+1000.*start_time/a.sampling)
end_point  = int(a.timezero+1000.*end_time/a.sampling)

print "Start and end points", start_point, end_point

print "Number of traces:  ", a.ntraces

for i in range(0, a.ntraces):

    dat[0:a.npts_trace, i] = G_T.Timer.dewow(in_dat[0:a.npts_trace, i], a.npts_trace, pulse_width)

    angle.append(360.*float(i)/float(a.ntraces))

    xxxx=8.*pow(np.cos(2. * np.pi * (angle[i] + phase) / 360.), 2)
    perfect.append(xxxx)

    summer = 0.
    for k in range(start_point,end_point):
        summer += pow(dat[k, i],2)

    amp.append(np.sqrt(summer/(float(end_point-start_point+1))))

print "Starting plot process"
plt.figure(1)

plt.plot(angle, amp, angle, in_thd[24, 0:a.ntraces], angle, perfect)
plt.xlabel("Rotation angle (degrees)")
plt.ylabel("Reflection RMS amplitude (mV)")
plt.title(file_in)

plt.show()



exit(1234)


    # Test of using EKKO_View to plot processed data
import subprocess

program = 'C:\\EKKO_PETER\\ekkocode\\EKKO_View12\\EKKO_View12.exe'

args = (program, file_out)

popen = subprocess.Popen(args, stdout=subprocess.PIPE)

output = popen.communicate()

for i in range(len(output)):
    print output[i]
