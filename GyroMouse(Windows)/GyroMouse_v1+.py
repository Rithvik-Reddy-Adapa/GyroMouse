'''
    GyroMouse - A simple scientific calculator using python3.
    Copyright (C) Year: 2020,  Author: Rithvik Reddy Adapa
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

'''
GyroMouse
Made on 21/05/2020
'''

#** For better understanding of comments set your text editor font to monospace **#

import tkinter as tk # Use tkinter module to create GUI 
import serial        # Use serial module to connect to serial connection
import serial.tools.list_ports

# pynput module is used to implement mouse and keyboard operations
from pynput.mouse import Button,Controller
m=Controller() # Mouse Controller
from pynput.keyboard import Key,Controller
k=Controller() # Keyboard Controller

global values,running,a
values=[5,1,4.5,2,20,-6,-3,-2,1,-2,1] # values variable contains predefined default values for [COM port, serial number, mouse movement sensitivity, scroll sensitivity, volume contol sensitivity, minimum error of gyro about x-axis, maximum error of gyro about x-axis, minimum error of gyro about y-axis, maximum error of gyro about y-axis, minimum error of gyro about z-axis, maximum error of gyro about z-axis]
running=True

def run_GUI(): # Function defining Graphical User Interface
    global values

    def read_default_values(): # Reads default values from a text file saved as "default.txt" it contains the data of "values" variable. If the "default.txt" file does not exist data from "values" variable is taken.
        global values
        try: # If "default.txt" file exists
            with open("default.txt","r") as f:
                values=f.readlines()              # Reading data from "default.txt" file to values variable
                values=[float(i) for i in values] # Converting data from string to float
                com_port.set(int(values[0]))      # Assigning COM port
                ser_num.set(int(values[1]))       # Assigning serial number
                mouse_s.set(values[2])            # Assigning mouse movement sensitivity
                scroll_s.set(values[3])           # Assigning scroll sensitivity
                vol_s.set(values[4])              # Assigning volume contol sensitivity
                values[5]=values[5]   # ---
                values[6]=values[6]   #    |
                values[7]=values[7]   #    | Assigning error
                values[8]=values[8]   #    | values of gyroscope
                values[9]=values[9]   #    |
                values[10]=values[10] # ---
        except: # If "default.txt" file does not exist
            values=[5,1,4.5,2,20,-6,-3,-2,1,-2,1]
            com_port.set(int(values[0]))   # Assigning COM port
            ser_num.set(int(values[1]))    # Assigning serial number
            mouse_s.set(float(values[2]))  # Assigning mouse movement sensitivity
            scroll_s.set(float(values[3])) # Assigning scroll sensitivity
            vol_s.set(float(values[4]))    # Assigning volume sensitivity

    def print_values(): # Function to start using the mouse
        global values
        a=int(com_port.get())
        if(a<0): com_port.set(0)       # | Restricting COM port value entered  
        elif(a>255): com_port.set(255) # | within the range 0 t0 255
        del a
        values[0]=int(com_port.get())
        values[1]=int(ser_num.get())
        values[2]=float(mouse_s.get())
        values[3]=float(scroll_s.get())
        values[4]=float(vol_s.get())
        
        window.destroy()
    
    def calibrate(): # Function to detect errors of gyroscope and accelerometer
        global values
        def get_data(s): # Function to read data from serial port and to find error
            global values
            min_gx=10000
            max_gx=-10000
            min_gy=10000
            max_gy=-10000
            min_gz=10000
            max_gz=-10000
            count=0
            for i in range(40): # Error is found by averaging over 40 values
                data=s.readline() # Reading data from serial port
                if data==b'': # If nothing is received from serial port ( b in b'' indicates binary format i.e. data is coming in binary format )
                    count=count+1 # If nothing is received increment count
                if count==3: # If nothing is received for 3 times
                    #Button "Calibrate"
                    tk.Button(window,text="Calibrate",font=("Helvetica",20,"bold"),fg="Black",activebackground="SlateBlue2",bg="IndianRed2",bd=0,width=13,command=calibrate).grid(row=5,column=0) # Change "Clibrate" button appearence indicating failed to find errors
                    break
                if(data!=b'-1\r\n'): # If "-1" is received ( this indicates the start of data transmission from serial port )
                    continue
                try:
                    gx=float(s.readline()) # Reading gyro x-axis data
                    gy=float(s.readline()) # Reading gyro y-axis data
                    gz=float(s.readline()) # Reading gyro z-axis data
                    ax=float(s.readline()) # Reading accel x-axis data
                    ay=float(s.readline()) # Reading accel y-axis data
                    az=float(s.readline()) # Reading accel z-axis data
                    lb=int(s.readline())   # Reading left mouse button  |
                    rb=int(s.readline())   # Reading rignt mouse button | ( whether button is pressed or not )
                    sb=int(s.readline())   # Reading scroll button      |
                    mb=int(s.readline())   # Reading movement button    |
                    if gx>max_gx: max_gx=gx #   |
                    if gx<min_gx: min_gx=gx #   |
                    if gy>max_gy: max_gy=gy #   | Getting minimum and maximum values
                    if gy<min_gy: min_gy=gy #   | of gyroscope about x, y and z axes
                    if gz>max_gz: max_gz=gz #   |
                    if gz<min_gz: min_gz=gz #   |
                except: pass
            if min_gx<9000: values[5]=min_gx
            if max_gx>-9000: values[6]=max_gx
            if min_gy<9000: values[7]=min_gy
            if max_gy>-9000: values[8]=max_gy
            if min_gz<9000: values[9]=min_gz
            if max_gz>-9000:
                values[10]=max_gz
                #Button "Calibrate"
                tk.Button(window,text="Calibrate",font=("Helvetica",20,"bold"),fg="Black",activebackground="SlateBlue2",bg="SpringGreen2",bd=0,width=13,command=calibrate).grid(row=5,column=0) # Change "Clibrate" button appearence indicating successfully found errors

        
        try:
            try: # Try to connect to serial device using known serial number of the device
                values[1]=ser_num.get()
                device_serial_number=values[1]
                ports = list(serial.tools.list_ports.comports()) # Getting list of connected serial devices
                for p in ports:
                    if int(p.serial_number)==device_serial_number:
                        device_serial_port=p.device # If serial number matches ( If required serial device is connected ) then save it's COM port value
                        break
                s=serial.Serial(device_serial_port,baudrate=115200,timeout=1) # Open the COM port
                values[0]=int(device_serial_port[3:]) # Save COM port number to "values" variable
                com_port.set(values[0])
                get_data(s)
                
                #Entry  "COM"
                # Change COM port Spinbox appearence indicating successfully connected to required serial device
                com_value=tk.Spinbox(window,from_=0,to=256,font=("Helvetica", 30, "bold"),fg="SteelBlue4",bg="SpringGreen2",bd=0,width=9,textvariable=com_port)
                com_value.grid(row=0,column=2)
                com_port.set(values[0])
                
                #Entry "Serial number"
                # Change Serial number Entry appearence indicating successfully connected to required serial device
                tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="SpringGreen2",bd=3,textvariable=ser_num).grid(row=1,column=2,sticky="W")
                ser_num.set(values[1])
                
            except: # Try to connect to serial device using known COM port of the device
                values[0]=com_port.get()
                if values[0]<0: values[0]=0;com_port.set(0)       # | Restricting COM port
                if values[0]>255: values[0]=255;com_port.set(255) # | number within 0 and 255
                device_serial_port="COM"+str(int(values[0]))
                s=serial.Serial(device_serial_port,baudrate=115200,timeout=1) # Open the COM port
                try:
                    for p in ports: # "ports" variable is defined in above try block
                        if p.device==device_serial_port:
                            device_serial_number=int(p.serial_number) # If COM port number matches ( If required serial device is connected ) then save it's serial number
                            break
                    values[1]=device_serial_number
                    ser_num.set(values[1])
                    
                    #Entry "Serial number"
                    # Change Serial number Entry appearence indicating invalid serial number
                    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="SpringGreen2",bd=3,textvariable=ser_num).grid(row=1,column=2,sticky="W")
                    ser_num.set(values[1])
                except:
                    #Entry "Serial number"
                    # Change Serial number Entry appearence indicating invalid serial number
                    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="IndianRed2",bd=3,textvariable=ser_num).grid(row=1,column=2,sticky="W")
                    ser_num.set(values[1])
                get_data(s)
                #Entry  "COM"
                # Change COM port Spinbox appearence indicating successfully connected to required serial device
                com_value=tk.Spinbox(window,from_=0,to=256,font=("Helvetica", 30, "bold"),fg="SteelBlue4",bg="SpringGreen2",bd=0,width=9,textvariable=com_port)
                com_value.grid(row=0,column=2)
                com_port.set(values[0])
        except:
            #Entry  "COM"
            # Change COM port Spinbox appearence indicating unable to connect to required serial device
            com_value=tk.Spinbox(window,from_=0,to=256,font=("Helvetica", 30, "bold"),fg="SteelBlue4",bg="IndianRed2",bd=0,width=9,textvariable=com_port)
            com_value.grid(row=0,column=2)
            com_port.set(values[0])

            #Entry "Serial number"
            # Change Serial number Entry appearence indicating unable to connect to required serial device
            tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="IndianRed2",bd=3,textvariable=ser_num).grid(row=1,column=2,sticky="W")
            ser_num.set(values[1])

            #Button "Calibrate"
            # Change Calibrate Button appearence indicating unable to connect to required serial device
            tk.Button(window,text="Calibrate",font=("Helvetica",20,"bold"),fg="Black",activebackground="SlateBlue2",bg="IndianRed2",bd=0,width=13,command=calibrate).grid(row=5,column=0)

    def end(): # Close GUI window
        global running,a
        window.destroy()
        a=True
        running=False

    window=tk.Tk()
    window.title("GYRO MOUSE") # GUI window title
    window.configure(bg="white smoke")
    try: window.iconphoto(False,tk.PhotoImage(file='pointer.png')) # Set image beside title of window ( image name is "pointer.png" )
    except: pass
    

    ser_num=tk.IntVar()     # tkinter variable for serial number
    com_port=tk.IntVar()    # tkinter variable for COM port number
    mouse_s=tk.DoubleVar()  # tkinter variable for mouse movement sensitivity
    scroll_s=tk.DoubleVar() # tkinter variable for scroll sensitivity
    vol_s=tk.DoubleVar()    # tkinter variable for volume contol sensitivity

    read_default_values() # Default values are read from "default.txt" file, if any error from reading this file then predefined default values are assigned
    

    #Label  "COM"
    com=tk.Label(window,text="Select COM port number",font=("Helvetica", 30, "bold"),fg="Blue",bg="white smoke")
    com.grid(row=0,column=0,columnspan=2)

    #Entry  "COM"
    com_value=tk.Spinbox(window,from_=0,to=256,font=("Helvetica", 30, "bold"),fg="SteelBlue4",bg="white smoke",bd=0,width=9,textvariable=com_port)
    com_value.grid(row=0,column=2)

    #Label "Serial number"
    tk.Label(window,text="Serial Number  ",font=("Helvetica",30,"bold"),fg="Blue",bg="white smoke").grid(row=1,column=0,sticky="W",columnspan=2)

    #Entry "Serial number"
    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="white smoke",bd=3,textvariable=ser_num).grid(row=1,column=2,sticky="W")

    #Label  "Mouse sensitivity"
    tk.Label(window,text="Mouse sensitivity  ",font=("Helvetica",30,"bold"),fg="Blue",bg="white smoke").grid(row=2,column=0,sticky="W",columnspan=2)

    #Entry "Mouse sensitivity"
    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="white smoke",bd=3,textvariable=mouse_s).grid(row=2,column=2,sticky="W")

    #Label  "Scroll sensitivity"
    tk.Label(window,text="Scroll sensitivity  ",font=("Helvetica",30,"bold"),fg="Blue",bg="white smoke").grid(row=3,column=0,sticky="W",columnspan=2)

    #Entry  "Scroll sensitivity"
    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="white smoke",bd=3,textvariable=scroll_s).grid(row=3,column=2,sticky="W")

    #Label  "Volume sensitivity"
    tk.Label(window,text="Volume sensitivity  ",font=("Helvetica",30,"bold"),fg="Blue",bg="white smoke").grid(row=4,column=0,sticky="W",columnspan=2)

    #Entry  "Volume sensitivity"
    tk.Entry(window,width=10,font=("Helvetica",30,"bold"),fg="SteelBlue4",bg="white smoke",bd=3,textvariable=vol_s).grid(row=4,column=2,sticky="W")

    #Button  "Run"
    tk.Button(window,text="Run",font=("Helvetica",20,"bold"),fg="Black",activebackground="green2",bg="white smoke",bd=0,width=14,command=print_values).grid(row=5,column=1)

    #Button  "Cancel"
    tk.Button(window,text="Cancel",font=("Helvetica",20,"bold"),fg="Black",activebackground="red",bg="white smoke",bd=0,width=13,command=end).grid(row=5,column=2)

    #Button "Calibrate"
    tk.Button(window,text="Calibrate",font=("Helvetica",20,"bold"),fg="Black",activebackground="SlateBlue2",bg="white smoke",bd=0,width=13,command=calibrate).grid(row=5,column=0)

    window.mainloop()


a=False
run_GUI()
while a==False:
    try:
        try: # Try to connect to serial device using known serial number of the device
            device_serial_number=values[1]
            ports = list(serial.tools.list_ports.comports())
            for p in ports:
                if int(p.serial_number)==device_serial_number:
                    device_serial_port=p.device
                    break
            s=serial.Serial(device_serial_port,baudrate=115200,timeout=1)
            values[0]=int(device_serial_port[3:])
            a=True
        except: # Try to connect to serial device using known COM port of the device
            device_serial_port="COM"+str(int(values[0]))
            s=serial.Serial(device_serial_port,baudrate=115200,timeout=1)
            try:
                for p in ports:
                    if p.device==device_serial_port:
                        device_serial_number=int(p.serial_number)
                        break
                values[1]=device_serial_number
            except: pass
            a=True
    except:
        run_GUI()
del a
if running:
    del running

    with open("default.txt","w") as f: # Since everything works well, save all the data i.e. [COM port, serial number, mouse movement sensitivity, scroll sensitivity, volume contol sensitivity, minimum error of gyro about x-axis, maximum error of gyro about x-axis, minimum error of gyro about y-axis, maximum error of gyro about y-axis, minimum error of gyro about z-axis, maximum error of gyro about z-axis] into "default.txt" file for future use
        f.write(str(values[0]))
        f.write("\n"+str(values[1]))
        f.write("\n"+str(values[2]))
        f.write("\n"+str(values[3]))
        f.write("\n"+str(values[4]))
        f.write("\n"+str(values[5]))
        f.write("\n"+str(values[6]))
        f.write("\n"+str(values[7]))
        f.write("\n"+str(values[8]))
        f.write("\n"+str(values[9]))
        f.write("\n"+str(values[10]))



    sensitivity=float(values[2])        # Mouse movement sensitivity
    scroll_sensitivity=float(values[3]) # Scroll sensitivity
    volume_sensitivity=float(values[4]) # Volume sensitivity

    # Initially all buttons status is set to 1, if button is pressed then status changes to 0 and button is released status changes to 1
    lb=1 # Left Button
    rb=1 # Right Button
    sb=1 # Scroll Button
    mb=1 # Movement Button

    lbc=0 # Left Button Count
    rbc=0 # Right Button Count
    sbc=0 # Scroll Button Count
    mbc=0 # Movement Button Count

    vc=0 # Volume count

    nsbc=0 # Number of Scroll Button Clicks

    cd=30 # Click Duration ( It defines number of iterations to wait to differentiate between Single Click and Long Press ) ( So, if button is pressed for 30 iterations it is considered as long press )

    print('running') # Optional

    while True:
        data=s.readline()
        if data==b'': # If nothing is received from serial port, continue the current iteration
            continue
        if(data!=b'-1\r\n'): # "-1" is the indication of start of data transfer, so until "-1" is not received continue the iterations, if "-1" is received proceed in the current iteration
            continue
        try:
            plb=lb # plb => Previous Left Button,     lb => Left Button
            prb=rb # prb => Previous Right Button,    rb => Right Button
            psb=sb # psb => Previous Scroll Button,   sb => Scroll Button
            pmb=mb # pmb => Previous Movement Button, mb => Movement Button

            gx=float(s.readline()) # gx => Gyro value about x-axis
            gy=float(s.readline()) # gy => Gyro value about y-axis
            gz=float(s.readline()) # gz => Gyro value about z-axis
            ax=float(s.readline()) # ax => Accel value along x-axis
            ay=float(s.readline()) # ay => Accel value along y-axis
            az=float(s.readline()) # az => Accel value along z-axis
            lb=int(s.readline())  # Status of Left Button      |
            rb=int(s.readline())  # Status of Right Button     |   Status is 0 when button is pressed &
            sb=int(s.readline())  # Status of Scroll Button    |   Status is 1 when button is released
            mb=int(s.readline())  # Status of Movement Button  |
        except:
            continue
        
        gx=gx-((values[5]+values[6])/2)  # | Adjusting the obtained
        gy=gy-((values[7]+values[8])/2)  # | gyro values to eliminate
        gz=gz-((values[9]+values[10])/2) # | error by subtracting error
        
        
        # Setting Upper and Lower limits till when the values should be '0'
        if(gx<=(values[6]-((values[5]+values[6])/2)) and gx>=(values[5]-((values[5]+values[6])/2))):
            gx=0
        if(gy<=(values[8]-((values[7]+values[8])/2)) and gy>=(values[7]-((values[7]+values[8])/2))):
            gy=0
        if(gz<=(values[10]-((values[9]+values[10])/2)) and gz>=(values[9]-((values[9]+values[10])/2))):
            gz=0

        # "xmove" variables stores/tells how much the mouse cursor should move horizontally ( in x - direction ) on the screen
        # "ymove" variables stores/tells how much the mouse cursor should move vertically ( in y - direction ) on the screen
        # Based on the orientation of my sensor, rotation about negative z-axis moves the cursor in positive x-direction and rotation about negative x-axis moves the cursor in positive y-direction on the screen.   ( So adjust these based upon the orientation of your sensor )
        xmove=-gz/sensitivity # | Dividing by "sensitivity"
        ymove=-gx/sensitivity # | So more is the "sensitivity" less is the movement speed and vice-versa
        
        move=0 # "move" variable stores/tells whether to move or not ( if greater than or equal to '1', move the cursor, else if less than '1', don't move the cursor )

        
        
        # Movement Button Operations
        # 1 -> Long press ( more than "cd" iterations ) movement button to move the cursor, press and hold to move cursor and release to stop moving
        # 2 -> Click ( i.e. to release before "cd" iterations ) the movement button and tilt the mouse towards left side to change to previous track or tilt the mouse towards right side to change to next track while playing media
        if(mb==0):
            mbc=mbc+1
            if(mbc>=cd):
                move=1
        elif(pmb==0 and mb==1):
            if(mbc<=cd):
                if(gy>20): # Click and tilt towards right side
                    k.press(Key.media_next)
                    k.release(Key.media_next)
                if(gy<-20): # Click and tilt towards left side
                    k.press(Key.media_previous)
                    k.release(Key.media_previous)
            mbc=0
        
        
        # Left Button Operations
        # 1 -> Press for more than "cd" iterations to act as Long Press and release to stop long press
        # 2 -> Press and release within "cd" iterations to act as Single Click
        if(lb==0):
            lbc=lbc+1
            if(lbc==cd):
                m.press(Button.left)
            move=lbc//cd # "move" variable is set to '1'
        elif(plb==0 and lb==1):
            if(lbc<=cd):
                m.click(Button.left)
            else:
                m.release(Button.left)
            lbc=0



        
        
        # Right Button Operations
        # 1 -> Press for more than "cd" iterations to act as Long Press and release to stop long press
        # 2 -> Press and release within "cd" iterations to act as Single Click
        if(rb==0):
            rbc=rbc+1
            if(rbc==cd):
                m.press(Button.right)
            move=rbc//cd # "move" variable is set to '1'
        elif(prb==0 and rb==1):
            if(rbc<=cd):
                m.click(Button.right)
            else:
                m.release(Button.right)
            rbc=0



        
        
        
        # Scroll Button Operations
        # 1 -> Single click => no operation
        # 2 -> Double click => play / pause media
        # 3 -> Single Long Press and rotating the mouse up and down => Scroll up and down respectively
        # 4 -> Single Click and then Long Press and rotating the mouse up and down => Volume increase and decrease respectively
        if(sb==0):
            sbc=sbc+1
            if(sbc>=cd and nsbc==0): # Single Long Press
                m.scroll(0,gx/scroll_sensitivity)
            if(sbc>=cd and nsbc==1): # Single Click and then Long Press
                vc=vc+1
                ymove=gx//volume_sensitivity
                if(ymove>1 and vc%2==0):
                    k.press(Key.media_volume_up)
                    k.release(Key.media_volume_up)
                if(ymove<-1 and vc%2==0):
                    k.press(Key.media_volume_down)
                    k.release(Key.media_volume_down)
        elif(psb==0 and sb==1):
            if(sbc<=cd and nsbc==0): # Single Click
                nsbc=1
            elif(sbc<=2*cd and nsbc==1): # Double Click
                k.press(Key.media_play_pause)
                k.release(Key.media_play_pause)
            if(sbc>=cd and nsbc==0):
                sbc=0
                nsbc=0
            if(sbc>=cd and nsbc==1):
                sbc=0
                nsbc=0
                vc=0
        elif(sb==1 and nsbc==1 and sbc>=2*cd): # If Scroll Button is clicked once and is not pressed second time then it resets
            nsbc=0
            sbc=0
        
        if(sb==1 and nsbc==1):
            sbc=sbc+1
            
        # Move the cursor if "move" variable is greater than or equal to '1' and don't move cursor if "move" variable is less than '1'
        if(move>=1):
            m.move(xmove,ymove)
