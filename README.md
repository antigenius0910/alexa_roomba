## alexa_echo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Controlling Roomba with the Amazon Echo.

After you tell Alexa "turn on startdust destroyer" Roomba will start singing "The imperial march" and start to clean.

See it in action 

https://user-images.githubusercontent.com/5915590/138384009-169e9dc4-5142-4027-aa18-df4c367915f5.mp4

For Alexa function see [here](https://github.com/antigenius0910/alexa_roomba/blob/master/fauxmo.py#L315)

For singing Roomba function see [here](https://github.com/antigenius0910/alexa_roomba/blob/master/create.py#L1474)

### Hardware Setup

**📋 [Complete Hardware Setup Guide →](HARDWARE_SETUP.md)**

This project requires hardware assembly inside your Roomba. The setup guide includes:
- ✅ Detailed component list with specifications
- ✅ **Step-by-step battery tap instructions with photos**
- ✅ Wiring diagrams and connection points
- ✅ DC-DC converter setup and voltage testing
- ✅ Raspberry Pi mounting and serial cable connection
- ✅ Troubleshooting guide

**Quick Hardware Summary:**
- iRobot Roomba (500/600/700/800 series)
- Raspberry Pi Zero W
- DC-DC Converter (14.4V → 5V)
- USB-to-Serial cable
- Amazon Echo device

### Quick Start

    1. Create a [Python Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
    2. git clone *this_repo*
    3. cd *this_repo*
    4. pip install -r requirements.txt
    4. python example-minimal.py
    6. Tell Echo, "discover my devices"
    7. Use Echo's "turn on startdust destroyer" and "turn off startdust destroyer" to see script output


### Use as library

The main class is create.py which contains everything to talk to the Roomba. To use it write sth like:

    import create
    import time
    robot = create.Create(ROOMBA_PORT)
    robot.printSensors() # debug output
    wall_fun = robot.senseFunc(create.WALL_SIGNAL) # get a callback for a sensor.
    print (wall_fun()) # print a sensor value.
    robot.toSafeMode()
    robot.go(0,100) # spin
    time.sleep(2.0)
    robot.close()
    
Instructions for installation and usage [available on Instructables here](http://www.instructables.com/id/Hacking-the-Amazon-Echo/), brought by [FabricateIO](http://fabricate.io)


### Create a on boot deamon

     pi@stardust_destroyer:~/echo $ cat /etc/systemd/system/roomba.service

     [Unit]
     Description=Roomba keepalive daemon
     ## make sure we only start the service after network is up
     Wants=network-online.target
     After=network.target

     [Service]
     ## use 'Type=forking' if the service backgrounds itself
     ## other values are Type=simple (default) and Type=oneshot
     Type=forking
     ## here we can set custom environment variables
     ExecStart=/home/pi/alexa_roomba/roomba-start.sh 
     #ExecStop=/usr/bin/killall -9 python
     ### NOTE: you can have multiple `ExecStop` lines
     # don't use 'nobody' if your script needs to access user files
     # (if User is not set the service will run as root)
     #User=nobody

     # Useful during debugging; remove it once the service is working
     StandardOutput=console

     [Install]
     WantedBy=multi-user.target

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This means you are free to use, modify, and distribute this project for any purpose, including commercial use, as long as you include the original copyright notice.
