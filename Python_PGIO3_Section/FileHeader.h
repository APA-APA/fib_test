#if !defined(FILEHEADER_H__B78D5B81_4B14_11D3_A563_444553540000__INCLUDED_)
#define FILEHEADER_H__B78D5B81_4B14_11D3_A563_444553540000__INCLUDED_

#pragma pack(push, ssihdr) //store current byte boundaries
#pragma pack(1) //use 1 byte boundary for file header

typedef struct SHeaderFile 
      {
	   char job[10];         // job number or id 
       char  title1[71];     // line 1 of title 
       char  title2[71];     // line 2 of title 
       char  date[20];       // date data collected 
       int   ntraces;        // number of traces in profile 
       short   nauxtrc;        // number of auxillary traces 
       short   npts_trace;     // number of poshorts per trace 
       float   timezero;       // timezero in poshorts 
       float   time_window;    // total time window in ns 
       short   nstacks;        // number of stacks 
       float sampling;       // time between samples 
       float strt_pos;       // starting position 
       float end_pos;        // ending position 
       float stepsize;       // step size used 
       float frequency;      // antenna frequency 
       float ant_sep;        // antenna separation 
       short   pulservolts;    // pulser voltage 
       char  units[10];      // position units 
       char  survmode[20];   // survey mode 
       char  dewow_done;     // Y/N whether dewow done 
       char  elev_done;      // Y/N whether elevation done 
       float max_elev;       // max. elevation value 
       float min_elev;       // min. elevation value 
       float data_min;       // min. data value 
       float data_max;       // max. data value 
       char data_type[4]; 
	   int	missing_traces;	  // Find number of missing traces in the header file
	   char * sComments;	  // It contains an arrays  of comments 
	   int numComments;		  // number of comments in the header file
}; 

#pragma pack(pop, ssihdr) //restore current byte boundaries

#endif // !defined(FILEHEADER_H__B78D5B81_4B14_11D3_A563_444553540000__INCLUDED_) 