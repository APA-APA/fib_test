__author__ = 'apa'

"""  This program tests out using GPR_Tools to read data and process some traces """


import PY_PGIO3
import numpy as np
import matplotlib.pyplot as plt
#import copy_header as ch
import os

import sys


#  "The following code is part of testing set up of a GPR_Tools module. Since cannot use C:\... in import need to define the path
#  Used the append path system call so can use the local file name.
# various options see  https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
#  Currently only the spatial box filter is tested in this program.  More to come.



sys.path.append("C:\\Users\\apa\\PycharmProjects\\")


print sys.path

import GPR_Tools as G_T


G_T.Spacer.Space_tools()
G_T.Timer.Time_tools()



a = G_T.PGIO.Header('XL0040.hd')

a.readheader()


z=G_T.PGIO.dt1('XL0040.dt1', a.ntraces, a.npts_trace,a.data_type)



# Next 2 lines are for test purposed only

if os.access('Copy1.hd', os.F_OK)==True:  os.remove('Copy1.hd')

if os.access('Copy1.dt1', os.F_OK)==True:    os.remove('Copy1.dt1')


"""
m = PY_PGIO3.Header('Copy1.hd')

ch.copy_hd(a,m)
m.writeheader()

w=PY_PGIO3.dt1('Copy1.dt1', m.ntraces, m.npts_trace,m.data_type)
m.writeheader()


num=5

for i in range(0,m.ntraces):

    qqq=z.read_trc_hd(i)
    data=z.read_trace(i)

    if i< num:
        print 'trc_num  ', qqq.trc_num, '  position  ', qqq.position,'  pts_trc  ', qqq.pts_trc, '  topo  ',  qqq.topo,'  five  ', qqq.five
        print  '  byte_pt  ', qqq.byte_pnt, '  window  ',qqq.time_window, '  stacks  ', qqq.stacks,' GPS  ', qqq.GPS_X,  qqq.GPS_Y, qqq.GPS_Z
        print  '  Rx xyz  ',qqq.rx_x,  qqq.rx_y,  qqq.rx_z
        print   '  Tx xyz  ', qqq.tx_x,  qqq.tx_y,  qqq.tx_z
        print  '  Zero adj  ', qqq.zero_adj, '  zeroflag  ', qqq.zero_flag,'  chan_no  ', qqq.chn_no,'  time  ', qqq.time_midnight,
        print '  flag  ',  qqq.flag,  '  Comment  ', qqq.flg_comment


    w.write_trc_hd(i,qqq)
    w.write_trace(i,data)

    #print ' Trace number in main  ', qqq.trc_num
    #print ' Time after midnight   ', qqq.time_midnight
"""


tr_hed=[]

data=[]


tr_hed, data = z.read_section()


for i in range(0,20):
    print 'Trace_number = ', tr_hed[0,i], '   Position=  ', tr_hed[1,i], '  Time=  ',tr_hed[23,i]-tr_hed[23,0]

vel=[]
for i in range(0,a.ntraces):
    if i==0:
        dtime=10.
        d_x=0.
    else:
        dtime=tr_hed[23,i]-tr_hed[23,i-1]
        d_x = tr_hed[1, i] - tr_hed[1, i - 1]

    vel.append(d_x/dtime)


m = G_T.PGIO.Header('Copy1.hd')

G_T.PGIO.copy_hd(a,m)
m.writeheader()

w=G_T.PGIO.dt1('Copy1.dt1', m.ntraces, m.npts_trace,m.data_type)
w.write_section(tr_hed, data)


print 'Data files written'


print "Number of pts per trace  ", a.npts_trace
times = np.array(np.arange(a.npts_trace), float)

pulse_width =  int(3000. / (2. * a.frequency * a.sampling/1000.))
dew=G_T.Timer.dewow(data[0:a.npts_trace,10], a.npts_trace,pulse_width )

#for jj in range(0,b.npts_trace-1):
#    times[jj]= jj*b.sampling/1000.

plt.figure(1)
plt.plot(times, data[0:a.npts_trace, 10],label='Raw')
plt.plot(times, dew[0:a.npts_trace], label="After dewow")
plt.title(a.filename)
plt.xlabel('Time (ns)')
plt.ylabel('Amplitude')
plt.legend(loc='lower right')
#plt.show()
#plt.axis([0,max(times),-50,50])

plt.figure(2)
plt.plot(tr_hed[0, 0:a.ntraces], vel[0:a.ntraces])
plt.title('Velocity')
plt.xlabel('Trace Number')
plt.ylabel('Velocity (m/s)')

#G_T.Timer()
#help(G_T.PGIO.PY_PGIO3)


smooth=G_T.Spacer.box_filter(data[int(a.timezero)+50,0:a.ntraces],a.ntraces, 20)

plt.figure(3)

plt.plot(tr_hed[1, 0:a.ntraces],data[int(a.timezero)+50,0:a.ntraces],label = 'Raw')
plt.plot(tr_hed[1, 0:a.ntraces],smooth[0:a.ntraces],label="After 20 point smoothing" )
plt.xlabel('Position (m)')
plt.ylabel('Amplitude (A/D units)')
plt.legend(loc='lower right')

plt.show()
