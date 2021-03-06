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
Made on 30/03/2020
'''

import serial   '''Import "PySerial" module'''
from pynput.mouse import Button,Controller   '''Import "Buttons" and "Mouse Controller" from 'pynput' module'''
m=Controller()   '''Set 'Mouse Controller' to 'm' variable'''
from pynput.keyboard import Key,Controller   '''Import "Keys" and "Mouse Controller" from 'pynput' module'''
k=Controller()   '''Set 'Keyboard Controller' to 'k' variable'''
s=serial.Serial('com5',baudrate=115200,timeout=1)   '''Set COM port, baudrate and timeout i.e. for how much time to check in serial buffer for data in seconds'''

sensitivity=4.5
scroll_sensitivity=3
volume_sensitivity=20

lb=1   '''Present left mouse button state, initially set to one'''
rb=1   '''Present right mouse button state, initially set to one'''
sb=1   '''Present scroll mouse button state, initially set to one'''
mb=1   '''Present movement mouse button state, initially set to one'''

lbc=0   '''Left mouse button iteration count, initially set to zero'''
rbc=0   '''Right mouse button iteration count, initially set to zero'''
sbc=0   '''Scroll mouse button iteration count, initially set to zero'''
mbc=0   '''Movement mouse button iteration count, initially set to zero'''

vc=0   '''Volume iteration count, initially set to zero'''

nsbc=0   '''Number of scroll button clicks, initially set to zero'''
nmbc=0   '''Number of movement button clicks, initially set to zero'''

cd=30   '''Click Duration, initially set to 30'''

print('running')

while True:
    if(s.readline()!=b'-1\r\n'):
        continue
    try:
        plb=lb   '''plb => Previous left mouse button state'''
        prb=rb   '''prb => Previous right mouse button state'''
        psb=sb   '''psb => Previous scroll mouse button state'''
        pmb=mb   '''pmb => Previous movement mouse button state'''

        gx=float(s.readline())   '''Reading current gyroscope value about x-axis'''
        gy=float(s.readline())   '''Reading current gyroscope value about y-axis'''
        gz=float(s.readline())   '''Reading current gyroscope value about z-axis'''
        ax=float(s.readline())   '''Reading current accelerometer value along x-axis'''
        ay=float(s.readline())   '''Reading current accelerometer value along y-axis'''
        az=float(s.readline())   '''Reading current accelerometer value along z-axis'''
        lb=int(s.readline())       '''Reading current left mouse button state'''
        rb=int(s.readline())       '''Reading current right mouse button state'''
        sb=int(s.readline())       '''Reading current scroll mouse button state'''
        mb=int(s.readline())       '''Reading current movement mouse button state'''
    except:
        continue

    gx=gx+4.5   '''Making initial offset error to zero'''
    gy=gy+0.5   '''Making initial offset error to zero'''
    gz=gz+0.5   '''Making initial offset error to zero'''
    
    if(gx<=1.5 and gx>=-1.5):   '''Making initial offset error to zero'''
        gx=0
    if(gy<=1.5 and gy>=-1.5):   '''Making initial offset error to zero'''
        gy=0
    if(gz<=1.5 and gz>=-1.5):   '''Making initial offset error to zero'''
        gz=0

    xmove=-gz/sensitivity   '''Intensity of cursor movement along horizontal axis'''
    ymove=-gx/sensitivity   '''Intensity of cursor movement along vertical axis'''
    move=0   '''If move>=1 then cursor moves else cusor doesn't move, initially set to 0'''


    if(mb==0):   '''If movement mouse button is pressed'''
        mbc=mbc+1
        if(mbc>=cd):   '''If movement mouse button is pressed for more than 'click duration' iterations then move'''
            move=1
    elif(pmb==0 and mb==1):   '''If movement mouse button is released'''
        if(mbc<=cd):   '''If movement mouse button is pressed for less than 'click duration' iterations'''
            if(gy>20):   '''If mouse is tilted right side then next track'''
                k.press(Key.media_next)
            if(gy<-20):   '''If mouse is tilted left side then previous track'''
                k.press(Key.media_previous)
        mbc=0   '''Movement mouse button iteration count is reset to zero'''


    if(lb==0):   '''If left mouse button is pressed'''
        lbc=lbc+1
        if(lbc==cd):   '''If left mouse button is pressed for 'click duration' iterations then it's button press'''
            m.press(Button.left)
        move=lbc//cd   '''move is set to 1'''
    elif(plb==0 and lb==1):   '''If left mouse button is released'''
        if(lbc<=cd):   '''If left mouse button is pressed for less than 'click duration' then it's button click'''
            m.click(Button.left)
        else:   '''If left mouse button is pressed for more than or equal to 'click duration' iterations now release button press'''
            m.release(Button.left)
        lbc=0   '''Left mouse button iteration count is reset to zero'''



    if(rb==0):   '''If right mouse button is pressed'''
        rbc=rbc+1
        if(rbc==cd):   '''If right mouse button is pressed for 'click duration' iterations then it's button press'''
            m.press(Button.right)
        move=rbc//cd   '''move is set to 1'''
    elif(prb==0 and rb==1):   '''If right mouse button is released'''
        if(rbc<=cd):   '''If right mouse button is pressed for less than 'click duration' then it's button click''' '''If right mouse button is clicked'''
            m.click(Button.right)
        else:   '''If right mouse button is pressed for more than or equal to 'click duration' iterations now release button press'''   '''If right mouse button is pressed and released now'''
            m.release(Button.right)
        rbc=0   '''Right mouse button iteration count is reset to zero'''



    if(sb==0):   '''If scroll mouse button is pressed'''
        sbc=sbc+1
        if(sbc>=cd and nsbc==0):   '''If scroll mouse button is pressed for more than 'click duration' iterations and if number of scroll button clicks is zero then scroll along vertical axis'''  '''If scroll mouse button is pressed'''
            m.scroll(0,gx/scroll_sensitivity)
        if(sbc>=cd and nsbc==1):   '''If scroll mouse button is pressed for more than 'click duration' iterations and if number of scroll button clicks is one then change volume'''    '''If scroll mouse button is pressed after one click'''
            vc=vc+1   '''Increment volume count'''
            ymove=gx//volume_sensitivity
            if(ymove>1 and vc%2==0):   '''If mouse is tilted upward then increase volume'''
                k.press(Key.media_volume_up)
            if(ymove<-1 and vc%2==0):   '''If mouse is tilted downward then decrease volume'''
                k.press(Key.media_volume_down)
    elif(psb==0 and sb==1):   '''If scroll mouse button is released'''
        if(sbc<=cd and nsbc==0):   '''If scroll mouse button is pressed for less than 'click duration' iterations and number of scroll mouse button clicks is zero i.e. when scroll mouse button is clicked once then increment to one (no operation)'''
            nsbc=1
        elif(sbc<=2*cd and nsbc==1):   '''If scroll mouse button is pressed for less than 2*'click duration' iterations and number of scroll mouse button clicks is one i.e. when scroll mouse button is clicked twice then play/pause media'''
            k.press(Key.media_play_pause)
        if(sbc>=cd and nsbc==0):    '''If scroll mouse button is pressed and released with zero clicks'''
            sbc=0
            nsbc=0
        if(sbc>=cd and nsbc==1):    '''If scroll mouse button is pressed and released after one click'''
            sbc=0
            nsbc=0
            vc=0
    elif(sb==1 and nsbc==1 and sbc>=2*cd):   '''If scroll mouse button is clicked once and left for more than 2*'click duration' iterations then reset all required parameters'''
        nsbc=0
        sbc=0

    if(sb==1 and nsbc==1):   '''Increment scroll mouse button iteration count when scroll mouse button is not pressed and number of scroll mouse button clicks is one'''
        sbc=sbc+1



    if(move>=1):   '''If move>=1 then cursor moves else cusor doesn't move'''
        m.move(xmove,ymove)
