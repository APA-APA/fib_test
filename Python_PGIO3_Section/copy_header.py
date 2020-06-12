__author__ = 'apa'

__author__ = 'apa'

"""
    Function to copy .hd attributes from one object to another
"""


def copy_hd(a,b):

        b.job = a.job
        b.title1 = a.title1
        b.title2 = a.title2
        b.date = a.date
        b.ntraces = a.ntraces
        b.nauxtrc = a.nauxtrc
        b.npts_trace = a.npts_trace
        b.timezero = a.timezero
        b.time_window = a.time_window
        b.nstacks = a.nstacks
        b.sampling = a.sampling
        b.strt_pos = a.strt_pos
        b.end_pos = a.end_pos
        b.stepsize = a.stepsize
        b.frequency = a.frequency
        b.ant_sep = a.ant_sep
        b.pulservolts = a.pulservolts
        b.units = a.units
        b.survmode = a.survmode
        b.dewow_done = a.dewow_done
        b.elev_done = a.elev_done
        b.max_elev = a.max_elev
        b.min_elev = a.min_elev
        b.data_max = a.data_max
        b.data_min = a.data_min
        b.data_type = a.data_type
        b.stack_type = a.stack_type
        b.trig_mode = a.trig_mode
        #b.trace_head_26 = a.trace_head_26   #Note a header variable needs special treatment so is a comment
        b.tx_serial = a.tx_serial
        b.rx_serial = a.rx_serial
        b.missing_traces = a.missing_traces
        b.comments = a.comments
        b.numComments = a.numComments
