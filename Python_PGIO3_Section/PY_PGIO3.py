__author__ = 'apa'

"""
    The following creates classes for Sensors & Software GPR dta files.

    ***********************************************************************************
    The class Header contains the information in a .hd file.  Attributes or parameters
    include the file name plus the standard structure elements used in c with PGIO DLL.

    Operations include readheader and writeheader.

    Adding comments just requires appending to self.comments and incrementing the
    numComments field and then calling the writeheader operation.

    Declaring a header objects uses the call

        a = PY_PGIO3.Header('header file name.hd')

        a.readheader()   - reads in the specified .hd file and sets header values

        a.writeheader()  - writes/creates the specified .hd file

    Note that the .hd file is an ASCII file

    ***********************************************************************************

    The class dt1 access the binary .dt1 and allow for reading and writing the trace header
    and the trace data.  The trace header is a 128 byte block that contains trace specific
    information ( see the EKKO_Project and various other product user manuals or read code below).

    The GPR data are stored as either I*2 or F*4 values in binary form.  The number of traces
    and points per trace as well as storage type are needed to operate i/o so the declaration
    of a dt1 object requires these values as inputs as well as the file name.

    Operations include read an arbitrary trace header and trace data. Reading any trace in
    essential random access operation is supported.

    Write operations of writing a trace header and a data trace must be done in sequential
    mode since random access writes do not seem supported in vanilla python. As a result
    traces must be written in sequence and cannot be overwritten tha random access would permit.

    Reading traces and trace headers are accomplished by the following

        z=PY_PGIO3.dt1('filename.dt1', a.ntraces, a.npts_trace,a.data_type)


        qqq=z.read_trc_hd(i)

        data=z.read_trace(i)

    where is a class trc_hd object and data is a list object that is filled with the trace data.

    Obviously the .dt1 file msut exist to allw data to be read.

    Writing trace headers and traces is as follows.  In order to create the full file all
    trace headers and trace data must be written in sequence.

        w=PY_PGIO3.dt1('filename.dt1', a.ntraces, a.npts_trace,a.data_type)


        num=a.ntraces



        for i in range(0,num):

            w.write_trc_hd(i,qqq)
            w.write_trace(i,data)


    Note that I*2 data types files are in A/D units (1 A/D unit ~ 1.52 uV)

    Note that F*4 data types files are in IEEE 32 bit floating point in units of mV

    The current codoe expects the user to handle the transformation to appropriate units
    after calling the read functions and prior to calling the write functions.

    The file is closed after each trace header and trace write.  A more flexible operation could
    be developed if the .dt1 file was opened at the start and a close operation was added.
    This modification will be explored in the future.

    ***********************************************************************************


    Class trc_hd() is used to define the internal structure of the trace header and
    allow access to elements

    For example

        qqq.flg_comment  defines a trace flag descriptor

        qqq.flag   = 0/1 indicates if a flag is attached to the trace.

    ***********************************************************************************


"""
import string

import numpy as np

class Header:

    def __init__(self,  filename):


        self.filename = filename

        self.job ='                      '
        self.title1 = '                  '
        self.title2 = '                  '
        self.date='01/01/1971            '
        self.ntraces = 0
        self.nauxtrc = 0
        self.npts_trace = 1
        self.timezero = 0.0
        self.time_window = 100.
        self.nstacks = 1
        self.sampling = 800.0
        self.strt_pos = 0.0
        self.end_pos = 1.0
        self.stepsize = 1.0
        self.frequency = 100.0
        self.ant_sep = 1.0
        self.pulservolts = 1000.0
        self.units = 'm'
        self.survmode = 'Reflection'
        self.dewow_done = 'Y'
        self.elev_done = 'N'
        self.max_elev = 0.0
        self.min_elev = 0.0
        self.data_max = 32767.
        self.data_min = -32768.
        self.data_type = 'I*2'
        self.stack_type = 'Unknown '
        self.trig_mode = 'Unknown'
        #self.trace_head_26 = 'Unknown '
        self.tx_serial = '0000'
        self.rx_serial = '0000'
        self.missing_traces = 0
        self.comments = []
        self.numComments = 0


    def readheader(self):

        f = open(self.filename, 'r')

        #  Note that string attribute reads include the line feed so use len()-1
        #  when capturing string attributes (except pure text like job, title1,  title2 and date)

        i=0
        flg = 1
        for line in f:
            i=i+1
            flg = 1
            if i==1:
                self.job = line[0:len(line) - 1]
                flg = 0
            if i==2:
                self.title1 = line[0:len(line) - 1]
                flg = 0
            if i==3:
                #if len(line) == 0:
                #print 'Title2  ', len(line)
                self.title2= line[0:len(line) - 1]
                flg = 0
            if i==4:
                if line[0:16] == 'NUMBER OF TRACES':  #Trap if only 1 title line not 2
                    self.date=self.title2
                    self.title2 = '                    '
                else:
                    line[0:len(line) - 1]
                flg = 0
            if line[0:16] == 'NUMBER OF TRACES':
                self.ntraces = string.atoi(line[21:len(line)])
                flg = 0
            if line[0:17] == 'NUMBER OF PTS/TRC':
                self.npts_trace = string.atoi(line[21:len(line)])
                flg = 0
            if line[0:17] == 'TIMEZERO AT POINT':
                self.timezero = string.atof(line[21:len(line)])
                flg = 0
            if line[0:17] == 'TOTAL TIME WINDOW':
                self.time_window = string.atof(line[21:len(line)])
                flg = 0
            if line[0:17] == 'STARTING POSITION':
                self.strt_pos = string.atof(line[21:len(line)])
                flg = 0
            if line[0:14] == 'FINAL POSITION':
                self.end_pos = string.atof(line[21:len(line)])
                flg = 0
            if line[0:14] == 'STEP SIZE USED':
                self.stepsize = string.atof(line[21:len(line)])
                flg = 0
            if line[0:14] == 'POSITION UNITS':
                self.units = line[21:len(line)-1]
                flg = 0
            if line[0:17] == 'NOMINAL FREQUENCY':
                self.frequency = string.atof(line[21:len(line)])
                flg = 0
            if line[0:18] == 'ANTENNA SEPARATION':
                self.ant_sep = string.atof(line[21:len(line)])
                flg = 0
            if line[0:18] == 'PULSER VOLTAGE (V)':
                self.pulservolts = string.atof(line[21:len(line)])
                flg = 0
            if line[0:16] == 'NUMBER OF STACKS':
                self.nstacks = string.atoi(line[21:len(line)])
                flg = 0
            if line[0:11] == 'SURVEY MODE':
                self.survmode = line[21:len(line)-1]
                flg = 0
            if line[0:9] == 'DATA TYPE':
                #print len(line)
                self.data_type = line[21:len(line)-1]
                flg = 0
            if line[0:13] == 'STACKING TYPE':
                self.stack_type = line[21:len(line)-1]
                flg = 0
            if line[0:12] == 'TRIGGER MODE':
                self.trig_mode = line[21:len(line)-1]
                flg = 0
            #if line[0:15] == 'TRACEHEADERDEF_':      # Change so this goes as a comment Needs special handling
                #self.trace_head_26 = line[21:len(line)-2]
                #flg = 0
            if line[0:11] == 'TX SERIAL #':
                self.tx_serial = line[21:len(line)-1]
                flg = 0
            if line[0:11] == 'RX SERIAL #':
                self.rx_serial = line[21:len(line)-1]
                flg = 0
            if flg == 1:
                self.comments.append(line[0:len(line)-1])
                self.numComments=self.numComments+1
                flg = 0

            #print "Number of comment lines", self.numComments
            #print self.comments

                        #print line

        self.sampling = 1000.0*self.time_window/self.npts_trace  # Get dT in ps

        f.close()

    def writeheader(self):
        f = open(self.filename, 'w+')


        f.write( '{:s}\n'.format(self.job))
        f.write( '{:s}\n'.format(self.title1))
        f.write( '{:s}\n'.format(self.title2))
        f.write( '{:s}\n'.format(self.date))
        f.write('NUMBER OF TRACES   = {:d}\n'.format(self.ntraces))
        f.write('NUMBER OF PTS/TRC  = {:d}\n'.format(self.npts_trace) )
        f.write('TIMEZERO AT POINT  = {:.3f}\n'.format( self.timezero))
        f.write('TOTAL TIME WINDOW  = {:.3f}\n'.format(self.time_window))
        f.write('STARTING POSITION  = {:.4f}\n'.format(self.strt_pos))
        f.write('FINAL POSITION     = {:.4f}\n'.format(self.end_pos))
        f.write('STEP SIZE USED     = {:.4f}\n'.format(self.stepsize))
        f.write('POSITION UNITS     = {:s}\n'.format(self.units))
        f.write('NOMINAL FREQUENCY  = {:.2f}\n'.format(self.frequency))
        f.write('ANTENNA SEPARATION = {:.4f}\n'.format(self.ant_sep))
        f.write('PULSER VOLTAGE (V) = {:.2f}\n'.format(self.pulservolts))
        f.write('NUMBER OF STACKS   = {:d}\n'.format(self.nstacks))
        f.write('SURVEY MODE        = {:s}\n'.format(self.survmode))
        f.write('DATA TYPE          = {:s}\n'.format(self.data_type))
        f.write('STACKING TYPE      = {:s}\n'.format(self.stack_type))
        f.write('TRIGGER MODE       = {:s}\n'.format(self.trig_mode))
        #f.write('TRACEHEADERDEF_26  = {:s}\n'.format(self.trace_head_26))   # Special mode, treat as comment
        f.write('TX SERIAL #        = {:s}\n'.format(self.tx_serial))
        f.write('RX SERIAL #        = {:s}\n'.format(self.rx_serial))

        #print "Number of comment lines", self.numComments
        #print self.comments

        for i in range(0,self.numComments):
            #f.write(self.comments[i])
            f.write('{:s}\n'.format(self.comments[i]))

        f.close()



class trc_hd():

    def __init__(self):


        self.trc_num = 1.0
        self.position = 0.0
        self.pts_trc = 1
        self.topo = 0.
        self.five = 0
        self.byte_pnt = 2
        self.time_window = 1.
        self.stacks =1
        self.GPS_X = 0.00   # 9 & 10
        self.GPS_Y = 0.00   #11 & 12
        self.GPS_Z = 0.00   #12 & 14
        self.rx_x = 0.00
        self.rx_y = 0.00
        self.rx_z = 0.00
        self.tx_x = 0.00
        self.tx_y = 0.00
        self.tx_z = 0.00
        self.zero_adj = 0.0
        self.zero_flag = 0
        self.chn_no = 1
        self.time_midnight = 0
        self.flag = 0
        self.flg_comment = []   # np.array([0,0,0,0,0,0,0], dtype=np.int32)



class dt1():

    def __init__(self, filename, ntrace, npts, data_type):

        self.filename = filename
        self. ntrace  = ntrace
        self.npts  =  npts
        self.data_type = data_type

        if self.data_type[0:3] == 'I*2':
            self.bytes_trace = 128 + 2 * self.npts

        if self.data_type[0:3] == 'F*4':
            self.bytes_trace = 128 + 4 * self.npts

    def read_trc_hd(self,trc):

        self.trc=trc

        a=trc_hd()

        offset = self.trc*self.bytes_trace

        f = open(self.filename,'rb')

        f.seek(offset)

        s = f.read(4)
        tt  =  np.frombuffer( s, dtype=np.float32, count=-1, offset=0)
        a.trc_num = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.position = tt[0]


        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.pts_trc = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.topo = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.five = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.byte_pnt = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.time_window = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.stacks = tt[0]

        s = f.read(8)
        tt = np.frombuffer(s, dtype=np.float64, count=-1, offset=0)
        a.GPS_X = tt[0]

        s = f.read(8)
        tt = np.frombuffer(s, dtype=np.float64, count=-1, offset=0)
        a.GPS_Y = tt[0]

        s = f.read(8)
        tt = np.frombuffer(s, dtype=np.float64, count=-1, offset=0)
        a.GPS_Z = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.rx_x = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.rx_y = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.rx_z = tt[0]


        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.tx_x = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.tx_y = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.tx_z = tt[0]


        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.zero_adj = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.zero_flg = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.chn_no = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.time_midnight = tt[0]

        s = f.read(4)
        tt = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
        a.flag = tt[0]

        s=f.read(28)
        tt = np.frombuffer(s, dtype=np.int32, count=-1, offset=0)
        a.flg_comment = tt[0:7]

        f.close()

        return a




    def read_trace(self, trc):
        self.trc = trc

        tt = []

        offset = self.trc * self.bytes_trace +128

        f = open(self.filename, 'rb')

        f.seek(offset)

        s = f.read(self.bytes_trace-128)
        if self.data_type[0:3] == 'F*4':
            tt = np.frombuffer(s, dtype=np.float32)


        if self.data_type[0:3] == 'I*2':
            tt = np.frombuffer(s, dtype=np.int16)

        f.close()

        return tt



    def read_section(self):

        thd=np.ndarray(shape=(32,self.ntrace),dtype=np.float32)

        if self.data_type[0:3] == "F*4":
            s = np.array(tt, dtype=np.float32)
            dat = np.ndarray(shape=(self.npts,self.ntrace),dtype=np.float32)

        if self.data_type[0:3] == "I*2":
            dat = np.ndarray(shape=(self.npts, self.ntrace), dtype=np.int16)

        f = open(self.filename, 'rb')


        for i in range(0,self.ntrace):
            s = f.read(128)
            thd[0:32, i] = np.frombuffer(s, dtype=np.float32, count=-1, offset=0)

            s=f.read(self.bytes_trace-128)
            if self.data_type[0:3] == "F*4":
                dat[0:self.npts,i]=np.frombuffer(s, dtype=np.float32, count=-1, offset=0)
            if self.data_type[0:3] == "I*2":
                dat[0:self.npts, i] = np.frombuffer(s, dtype=np.int16, count=-1, offset=0)

        f.close()

        return thd, dat



    def write_trc_hd(self, trc, aa):

        #aa=trc_hd()

        self.trc=trc

        offset = self.trc * self.bytes_trace

        #  Note need to use ab which is append binary to make writing work
        #  Use of wb with open and close casues file to be overwritten
        #  Note that the file has to be written sequentially - not random access

        f = open(self.filename, 'ab')

        #f.seek(offset,0)

        s = np.array(aa.trc_num, dtype=np.float32)
        #print s
        f.write(s)

        s = np.array(aa.position, dtype=np.float32)
        f.write(s)

        s = np.array(aa.pts_trc, dtype=np.float32)
        f.write(s)


        s = np.array(aa.topo, dtype=np.float32)
        f.write(s)

        s = np.array(aa.five, dtype=np.float32)
        f.write(s)

        s = np.array(aa.byte_pnt, dtype=np.float32)
        f.write(s)

        s = np.array(aa.time_window, dtype=np.float32)
        f.write(s)

        s = np.array(aa.stacks, dtype=np.float32)
        f.write(s)

        s = np.array([aa.GPS_X,aa.GPS_Y,aa.GPS_Z], dtype=np.float64)
        f.write(s)

        s = np.array([aa.rx_x, aa.rx_y, aa.rx_z], dtype=np.float32)
        f.write(s)

        s = np.array([aa.tx_x, aa.tx_y, aa.tx_z], dtype=np.float32)
        f.write(s)

        s = np.array(aa.zero_adj, dtype=np.float32)
        f.write(s)

        s = np.array(aa.zero_flg, dtype=np.float32)
        f.write(s)

        s = np.array(aa.chn_no, dtype=np.float32)
        f.write(s)

        s = np.array(aa.time_midnight, dtype=np.float32)
        f.write(s)

        s = np.array(aa.flag, dtype=np.float32)
        f.write(s)

        s = np.array(aa.flg_comment[0:7], dtype=np.int32)
        f.write(s)

        f.close()

        return


    def write_trace(self,trc,tt):

        self.trc=trc

        offset = self.trc * self.bytes_trace + 128

        #  Note need to use ab which is append binary to make writing work
        #  Use of wb with open and close causes file to be overwritten
        #  Note that the file has to be written sequentially - not random access

        f = open(self.filename, 'ab')

        #f.seek(offset,0)

        #print 'data type = ', self.data_type

        if self.data_type[0:3] =="F*4":
            s = np.array(tt, dtype=np.float32)
            f.write(s)

        if self.data_type[0:3] =="I*2":
            s = np.array(tt, dtype=np.int16)
        #print 'Inside write trace  ', tt[0:10]
        #s = np.array(tt[0:5], dtype=np.float32)

        #print s

            f.write(s)

        f.close()

        return


    def write_section(self, thd, dat):


        f = open(self.filename, 'ab')

        for i in range(0, self.ntrace):


            s = np.array(dat[0:32, i], dtype=np.float32)
            #print s
            f.write(s)

            if self.data_type[0:3] == "F*4":
                s = np.array(dat[0:self.npts,i], dtype=np.float32)
                f.write(s)

            if self.data_type[0:3] == "I*2":
                s = np.array(dat[0:self.npts,i], dtype=np.int16)
                f.write(s)


        f.close()

        return



