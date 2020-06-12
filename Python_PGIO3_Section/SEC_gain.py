__author__ = 'apa'

"""
    Function to compute SEC3 gain as a function of time

"""
import numpy as np

def SEC3(time_window, d_time, zero_time, frequency, velocity, alpha, G_floor,  G_max, G_type):


    times=np.arange(-zero_time, time_window-zero_time, d_time)

    Gain=np.ndarray((len(times)),dtype=np.float32)

    #print Gain.shape

    time_norm = 4000. / (2. * frequency)
    depth_norm = velocity * time_norm / 2.

    A = 1.4142 * np.pi * frequency * np.exp(-0.5) / 1000.
    B = pow(1.4142 * np.pi * frequency / 1000., 2)
    Coef = [1, A, B]


    gain_plane_norm = depth_norm*depth_norm*depth_norm*8. / (Coef[0] + Coef[1] * depth_norm * 2.0 / velocity +
                                                Coef[2] * depth_norm* depth_norm*4./ velocity* velocity  )
    gain_point_norm = depth_norm*depth_norm*depth_norm / (Coef[0] + Coef[1] * depth_norm / velocity +
                                            Coef[2] * depth_norm*depth_norm*4. / velocity* velocity)
    a = np.exp(2. * alpha * depth_norm / 8.69)

    gain_plane_norm = gain_plane_norm * a
    gain_point_norm = gain_point_norm*gain_point_norm * a

    for i in range(0, len(times)):

        if times[i] <0:
            Gain[i]=G_floor
        else:

            depths = velocity * times[i] / 2.

            #print i, depths, times[i]

            if G_type=='planar':
                gain_plane = depths * depths * depths *8. / (Coef[0] +
                                            Coef[1] * depths * 2.0 / velocity + Coef[2] * depths * depths
                                             * 4.0 / velocity * velocity)
                a = np.exp(2. * alpha * depths / 8.69)
                gain_plane = G_floor + gain_plane * a / gain_plane_norm

                if gain_plane > G_max:
                    Gain[i] = G_max
                else:
                    Gain[i] = gain_plane

            if G_type == 'point':
                gain_point= depths * depths * depths / (Coef[0] + Coef[1] * depths / velocity +
                                                               Coef[2] * depths * depths / velocity * velocity)
                gain_point = gain_point*gain_point

                a = np.exp(2. * alpha * depths / 8.69)
                gain_point = G_floor + gain_point* a / gain_point_norm

                if gain_point > G_max:
                    Gain[i]=G_max
                else:
                    Gain[i] = gain_point

    return Gain


def  dewow(trace, npts, width):

    """

   carry out the standard dewow  subtracts average over window width about each point

    """

    if width%2 == 0:  width=width+1

    wind2= int((width-.1)/2)


    out_trace=np.ndarray(npts,np.float32)

    for i in range(0,npts):

        count=0
        sum=0.
        for j in range(i-wind2, i+wind2+1):
            if j > -1 and j <npts:

                count=count+1
                sum=sum+trace[j]
        sum=sum/count
        out_trace[i]=trace[i]- sum

    return out_trace