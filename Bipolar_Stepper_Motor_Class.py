import RPi.GPIO as GPIO
import time

#sequence for a1, b2, a2, b1
#phase_seq=[[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]];
#full step sequence. maximum torque
phase_seq=[[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
#half-step sequence. double resolution. But the torque of the stepper motor is not constant 
num_phase=len(phase_seq);

class Bipolar_Stepper_Motor:
    
    phase=0;
    dirction=0;
    position=0;
    
    a1=0;#pin numbers
    a2=0;
    b1=0;
    b2=0;
    def __init__(self,a1,a2,b1,b2):
    #initial a Bipolar_Stepper_Moter objects by assigning the pins
    
        GPIO.setmode(GPIO.BOARD);
        
        self.a1=a1;
        self.a2=a2;
        self.b1=b1;
        self.b2=b2;
        
        GPIO.setup(self.a1,GPIO.OUT);
        GPIO.setup(self.a2,GPIO.OUT);
        GPIO.setup(self.b1,GPIO.OUT);
        GPIO.setup(self.b2,GPIO.OUT);
        print "Stepper Configured"
        self.phase=0;
        self.dirction=0;        
        self.position=0;
        
    def move(self, dirction, steps, delay=0.2):
        for _ in range(steps):
            next_phase=(self.phase+dirction) % num_phase;
            
            GPIO.output(self.a1,phase_seq[next_phase][0]);
            GPIO.output(self.b2,phase_seq[next_phase][1]);
            GPIO.output(self.a2,phase_seq[next_phase][2]);
            GPIO.output(self.b1,phase_seq[next_phase][3]);
            
            self.phase=next_phase;
            self.dirction=dirction;
            self.position+=dirction;
            
            time.sleep(delay);

    def unhold(self):
        GPIO.output(self.a1,0);
        GPIO.output(self.a2,0);
        GPIO.output(self.b1,0);
        GPIO.output(self.b2,0);
        
