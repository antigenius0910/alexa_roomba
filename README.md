## alexa_echo
For controlling Roomba with the Amazon Echo.

After you tell Alexa "turn on startdust destroyer" Roomba will start singing "The imperial march" and start to clean.

For Alexa function see [here](https://github.com/antigenius0910/alexa_roomba/blob/master/fauxmo.py#L315)

For singing Roomba function see [here](https://github.com/antigenius0910/alexa_roomba/blob/master/create.py#L1474)

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
