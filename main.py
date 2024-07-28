# External module imports
import RPi.GPIO as GPIO
#import pigpio
import time
#------------
from dc_motors import *
from matplot import *
from ir_sense import *
from pid_c import PID
#from test import *
#from encoder import Encoder
#------------
from multiprocessing import Process, Lock, Pool
import multiprocessing as mp
#------------
import pigpio
from rotary_encoder import decoder
import rotary_encoder
#------------
import numpy as np
#from simple_pid import PID
#------------
pos_L = 0
pos_R = 0
#------------
way_L = 0
way_R = 0

wcurr_L = 0
output_L = 0
wcurr_R = 0
output_R = 0

# Setting general parameters
tstop = 2  # Execution duration (s)
tsample = 0.01  # Sampling period (s)
wsp = 20  # Motor speed set point (rad/s)
#tau = 0.1  # Speed low-pass filter response time (s)
taupid = 0.1

j = 0

def callback_L(way_L):
	global pos_L
	pos_L += way_L
	#print("L={}".format(pos_L))

def callback_R(way_R):
	global pos_R
	pos_R += way_R
	#print("R={}".format(pos_R))
  
#-----------------------------------------------------------------  

def runR(j,pid_L,pid_R,pwm0,pwm1,pwm2,pwm3):

	
	# Initializing previous and current values
	#ucurr = 0  # x[n] (step input)
	wfprev_L = 0  # y[n-1]
	wfcurr_L = 0  # y[n]
	wfprev_R = 0  # y[n-1]
	wfcurr_R = 0  # y[n]
	
	# Initializing variables and starting clock
	thetaprev_L = 0
	thetaprev_R = 0
	tprev = 0
	tcurr = 0
	
	tstart = time.perf_counter()

	DC0 = 0
	DC1 = 0
	DC2 = 0
	DC3 = 0
	
	DEF1=30
	DEF2=-30
	
	#Factor = 4
	i = 0
	
	# num = mp.cpu_count()
	# pool = mp.Pool(num)
	while True:
		i = i+1
		j = j+1
		
		# -------------
		runM(pwm0,pwm1,pwm2,pwm3,DC0,DC1,DC2,DC3)
		
		L, R = motor_speed(L_dir,R_dir)
		
		# pid_L = PID(P, I, D, setpoint=L*50*Factor)
		# pid_R = PID(P, I, D, setpoint=-R*50*Factor)
		
		# -------------
		# Pausing for `tsample` to give CPU time to process encoder signal
		time.sleep(tsample)
		
		# Getting current time (s)
		tcurr = time.perf_counter() - tstart
		
		# Getting motor shaft angular position: I/O (data in)
		thetacurr_L = pos_L
		thetacurr_R = pos_R
		
		# Calculating motor speed (rad/s)
		wcurr_L = np.pi/180 * (thetacurr_L-thetaprev_L)/(tcurr-tprev) * 10
		wcurr_R = np.pi/180 * (thetacurr_R-thetaprev_R)/(tcurr-tprev) * 10
		
		# Filtering motor speed signal
		#wfcurr_L = tau/(tau+tsample)*wfprev_L + tsample/(tau+tsample)*wcurr_L
		#wfcurr_R = tau/(tau+tsample)*wfprev_R + tsample/(tau+tsample)*wcurr_R
		
		# wfprev_L = wfcurr_L
		# wfprev_R = wfcurr_R
		
		# Updating previous values
		tprev = tcurr
		thetaprev_L = thetacurr_L
		thetaprev_R = thetacurr_R
		# -------------
		
		print("L={}".format(wcurr_L))
		print("R={}".format(wcurr_R))
		
		#------------
		# # Calculating closed-loop output
		# output_L = pid_L(wcurr_L-L*DEF1)		
		# output_R = pid_R(wcurr_R-R*DEF2)
		#------------
		output_L = pid_L.control(0,wcurr_L-L*DEF1)		
		output_R = pid_R.control(0,wcurr_R-R*DEF2)
		#------------
		

		if (output_L > 0):
			#output_L = pid_L.update(control_L)
			DC0 = 0
			DC1 = output_L
		if (output_R < 0):
			#output_R = pid_L.update(control_R)
			DC2 = -output_R
			DC3 = 0
			
		if (output_L < 0):
			#output_L = pid_L.update(control_L)
			DC0 = -output_L
			DC1 = 0
			
		if (output_R > 0):
			#output_R = pid_L.update(control_R)
			DC2 = 0
			DC3 = output_R
			
		if (output_L == 0):
			#output_L = pid_L.update(control_L)
			DC0 = 0
			DC1 = 0
		if (output_R == 0):
			#output_R = pid_L.update(control_R)
			DC2 = 0
			DC3 = 0
		
		# Assigning motor output: I/O (data out)
		
		# m1 = mp.Process(target=runM, args = (pwm0,pwm1,pwm2,pwm3,DC0,DC1,DC2,DC3))
		# m2 = mp.Process(target=anim_plot, args = (j, wcurr_L, output_L, wcurr_R, output_R))
		
		# m1.start()
		# m2.start()
		
		# m1.join()
		# m2.join()
		
		# if (i == 1):
		#anim_plot(j, wcurr_L, output_L, wcurr_R, output_R)
			# i = 0
		# fig.canvas.draw()
		# fig.canvas.flush_events()
		#time.sleep(1)
		#pass
		



def main():
	
	P = 1.0
	I = 1.0
	D = 0	#0.001
	
	R = 0
	L = 0
	
	try:
		pi = pigpio.pi()

		pwm0,pwm1,pwm2,pwm3 = setup()
		
# #------------------------		
		# pid_L = PID(P, I, D, setpoint=0)
		# #pid_L.SetPoint=0.0
		# pid_L.output_limits = (-100, 100)
		# #pid_L.setSampleTime(tsample)
		
		# pid_R = PID(P, I, D, setpoint=0)
		# #pid_R.SetPoint=0.0
		# pid_R.output_limits = (-100, 100)
		# #pid_R.setSampleTime(tsample)
# #------------------------		

		pid_R = PID(tsample, P, I, D, 100, -100, tau=taupid)
		pid_L = PID(tsample, P, I, D, 100, -100, tau=taupid)
		
		# calling the animation function
		#anim = animation.FuncAnimation(fig, animate, init_func = init, frames = None, interval = 20, blit = True)
		#plt.show()
		#anim.save('Rand.mp4', writer = 'ffmpeg', fps = 30) 
#------------------------

		decoder_R = rotary_encoder.decoder(pi, 5, 6, callback_R)
		decoder_L = rotary_encoder.decoder(pi, 12, 13, callback_L)
		
		runR(j,pid_L,pid_R,pwm0,pwm1,pwm2,pwm3)

#------------------------		
		# # # # # #time.sleep(1)
		# num = mp.cpu_count()
		# pool = mp.Pool(num)
		
		# # # m4 = mp.Process(target=rotary_encoder.decoder, args = (pi, 5, 6, callback_L))
		# # # m3 = mp.Process(target=rotary_encoder.decoder, args = (pi, 12, 13, callback_R))
		# # # # m1 = mp.Process(target=callback_L, args = (way_L))
		# # # # m2 = mp.Process(target=callback_R, args = (way_R))
		# m1 = mp.Process(target=runR, args = (j,pid_L,pid_R,pwm0,pwm1,pwm2,pwm3))
		# # #m2 = mp.Process(target=anim_plot, args = (j, wcurr_L, output_L, wcurr_R, output_R))
		
		# # # m4.start()
		# # # m3.start()
		# # #m2.start()
		# m1.start()
		
		# # # # # #runR(pid_L,pid_R,pos_L,pos_R,pwm0,pwm1,pwm2,pwm3)
		
		# # # m4.join()
		# # # m3.join()
		# # #m2.join()
		# m1.join()
		
		# # # # # #runR(pid_L,pid_R,pos_L,pos_R,pwm0,pwm1,pwm2,pwm3)
#-------------------------

	#except Exception:
		#pass

	except KeyboardInterrupt:
		#print("Keyboard Interrupt")
		#pid_L = PID(0, 0, 0, setpoint=0)
		#pid_R = PID(0, 0, 0, setpoint=0)
		#plt.ioff()
		#runM(pwm0,pwm1,pwm2,pwm3,0,0,0,0)
		
		stopM(pwm0,pwm1,pwm2,pwm3)
		
		decoder_L.cancel()
		decoder_R.cancel()
		
		pi.stop()
		
		GPIO.cleanup()
	finally:
		#runM(pwm0,pwm1,pwm2,pwm3,DC0,DC1,DC2,DC3)
		stopM(pwm0,pwm1,pwm2,pwm3)
		decoder_L.cancel()
		decoder_R.cancel()
		pi.stop()
		#GPIO.cleanup()

#### Main ####
if __name__ == "__main__":
	main()
  
