# ScaredyBot

*A robot vacuum that runs away from people, built using an iRobot `Create2` and a `Raspberry Pi`*

###### By N. Escobar / nickesc

###### COMP 349: Robotics

###### [Code](https://github.com/nickesc/scaredyBot) / [Videos](https://drive.google.com/drive/folders/1hUl7qcqlOvjXQzaLcYq3QibzHZxcoDM1?usp=sharing)

![scaredyBot](img/handsomeBoy.png)

## 1. Abstract

In this report, we go through the process of building ScaredyBot. It will start with a detailed description of the project as it stands and describe what was accomplished and why, as well as a brief discussion of the goals of the project and how they changed significantly when I abandoned the idea of using an `Arduino` in favor of a `Raspberry Pi` and changed my strategy for sensing people near ScaredyBot. Next we go through the components and a detailed process of actually building, wiring, and coding ScaredyBot, from testing sensors to deployment. Then, we'll discuss the many challenges and setbacks faced during the process, most notably frying many of the sensors I'd hoped to use. Finally, we'll finish with a wrap up and conclusion reflecting on the experience

## 2. Overview

In this project, we build a robot that runs away from you when you get too close. It uses a PIR motion sensor to tell when you've approached it, and then chooses a semi-random direction and runs away from you. He avoids obstacles and walls, rotating away from them to keep running. He has two main states, _`searching` and _`running`.

I wanted to make this project because I really enjoyed the `Create2` robots, but they were incredibly limiting. 

## 3. Objectives

The top-level objective for this project was to create a robot that ran away from people when it was approached. Below this, I wanted to use a microcontroller to interface with an iRobot `Create2` and extend its functionality. 

> To do this, I would, initially, use an Arduino to extend the sensing capabilities of a `Create2` with things like a vibration sensor to detect when there was a person nearby by sensing the vibration in the ground from their footfalls. This quickly pivoted when both the controller and sensors proved to be unsuitable for the task.
>
> Still using the `Create2`, I would use a Raspberry Pi as the controller to handle sensor input and robot behaviour instead, and I would replace the vibration sensor with other, more appropriate sensors like a PIR motion sensor.

## 4. Methods

### Components:

> ![components](img/components.png)
> ***img 4.1*** | ScaredyBot components, from top to bottom, left to right:
1. `Raspberry Pi 3 Model B+`
2. GPIO extension board
3. PIR motion sensor
4. motion sensor header
5. breadboard
6. various jumper cables
7. button
8. RGB LED
9. 1x 10kΩ resistor
10. 3x 220Ω resitor
11. GPIO ribbon cable
12. 2x ultrasonic sensor modules (dead)
13. obstacle avoidance sensor module (dead)

### 4.2

*a note on this section: the methods describe don't quite line up to the prelab. We'll be discussing everything that happened after prelab testing*

1. in class on the first day of the lab, I begin to test the piezo's vibration sensing capabilities, which I'd been hoping to use, and they are extremely limited. The piezo *does not* pick up footfalls, so I need to pivot fairly significantly
   1. I choose to rely on a PIR motion sensor. This sensor detects movement using IR, and when a warm body passes through the sensor, it outputs `True`. I also grab an ultrasonic distance sensor, thinking I can use this to sense where walls and obstacles are better than the `Create2` already does
   2. at the same time, I relaize this is going to be a significant change, and while I'm already there decide to swap from an `Arduino` to a `Raspberry Pi`. This opens up a lot of possibilites, and untethers me from my laptop, as the Arduino needed to use the laptop's serial connection to control the `Create2`.
2. after pivoting the approach, I start by figuring out how to actually use the GPIO of the Raspberry Pi. While a lot of the work I did in the prelab for the Arduiono went to waste, getting comfortable wiring and workign with GPIO and on a breadboard was helpful. However, I'm working with GPIO in Python rather than C-like, so there's some adjustment.
3. Once I have a handle on the system and how to work with it, I start to test my new sensors and figure out how they work.
   1. I've also purchased one of the [Raspberry Pi Starter Kits](https://www.amazon.com/gp/product/B09BMVT4CB/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1), which comes with a number of new sensors.
      1. from this pack, I take everything in the project but one distance sensor and the Raspberry Pi. 
      2. I also swap out my PIR sensor, as the one from class is soldered into the `Non-Retriggering` mode, and I want the opposite. 
         1. note about these
   2. a lot of trial and error goes into this.
      1. first we write generic tests to see the output of the sensors individually, then bring them together and to see all outputs. 
      2. I also experiment with adding a gyroscope at this point, but quickly realize it's unnecessary and drop it.
      3. once we are sure all sensors are reading (*note: one distance sensor was dead-on-arrival, so would not read and had to be dropped*), we write a method for the robot to access them, [`sensors.py`](https://github.com/nickesc/scaredyBotPrelab/blob/main/sensors.py), and create an initial `scaredyBot.py` file that just imported it and read the sensors.
4. at this point we hit catastrophic failure. While cleaning up the wiring, I accidentally fry a number of components, including three of my sensors and spend the night scrambling to figure it out.
   1. I'm left with my PIR motion sensor, thankfully. This becomes our only external sensor. Read *section 5. Challenges* for more information on this.
   2. at the end of the night though, we have mostly finished with our sensors and are ready to move onto the robot.
      1. [Video of this stage](https://drive.google.com/file/d/10asBjgjwoHYMwey8_Bq01dDAC0ZplnpV/view?usp=sharing)
5. with the ScaredyBot's code, I decide the best method to handle his behaviour is with a finite-state-machine `ScaredyBot` of this form:
```python
class ScaredyBot():
     def __init__(bot):
        bot.scaredyBot = ScaredyBot()

    def loop(bot):
        while True:
            bot.state.execute()
            time.sleep(.01)

    def destroy(_state):
        quit()

class _state():
    def __init__(_state, scaredyBot):
        _state.scaredyBot = scaredyBot

    def getName(_state):
        return "stateName"

    def enter(_state):
        print('entering', _state.scaredyBot.getState())

    def execute(_state):
        pass

    def exit(_state):
        print('exiting', _state.scaredyBot.getState())
```
6. from here, I start constructing methods for getting sensors with the robot, creating a `PIR` class to handle the motion sensor in `Motion.py`
   1. I also realize that an indicator of ScaredyBot's state would be helpful, and add an RGB light with the `Light` class inside the `PIR` class
      1. off in `_start`, the setup state, 
      2. green in `_searching`, when it's looking for motion and 
      3. red in `_running`, when it's running from detected motion.
   2. I also realize a power button would be incredibly helpful, and add one that triggers the beginning of the loop and kills the program, with the `Power` class in `button.py`
   3. Now, we're finally ready to add movement. 
      1. We start by writing methods to make it search and rotate to a random direction behind it when motion is triggered
      2. then, I realize that another state-machine is appropriate, and in `_running` we add a less complex state machine to handle the different phases
         1. `rotating` - when the roomba is turning around
         2. `running` - when the roomba is actually running away
         3. `waiting` - the cooldown time for the motion sensor (about 6 seconds) where the roomba needs to be stationary to reset.
      3. from here, we have a robot that will run until it hits a wall or for a few seconds anytime it detects motion.
         1. [Video of this stage](https://drive.google.com/file/d/1-UBnOioYR3tijqwtAUgPi-zkTxlGM-rA/view?usp=sharing)
      4. here, the rest is pretty simple:
         1. we remove the wall end condition and make it always run for a certain amount of time, rotating and running away from obstacles when it reaches them, and spend a good deal of time debugging this
         2. we also tell ScaredyBot to back up a little if it senses a bump while `waiting` and turn around. This makes him less idle and just waiting, and like he's still trying to avoid you when you walk up to him
      5. The project is basically finished, when ScaredyBot runs over a metal bump on the floor and screws up his motion sensor. I spend hours debugging, but am not able to fully fix it. ScaredyBot is, unfortunately, never the same. Read *section 5. Challenges* for more information on this.
         1. But he still works! It just took a few tries.
         2. [Video one of the final stage](https://drive.google.com/file/d/1lP1P-42ooJOhF5uGC8GoanMYOg7aiPAC/view?usp=sharing)
         3. [Video two of the final stage](https://drive.google.com/file/d/15bHUwT_oJJtBaSlm4elB4OfEUVbIKJoP/view?usp=sharing)
## Challenges

This project was *full* of challenges. At nearly every turn, things either went differently than expected or completely
broke, which forced me to change tact a number of times.
> The first challenge I ran into was in the communication between the `Arduino` I'd initially planned to use and the `Create2`. While it was possible, it was *incredibly* inelegant. I found the `Create2` wouldn't be able to be controlled from the `Arduino` using the `pyCreate2` library because it could not execute `Python` code, and that I would need to pass the sensor readings from it to another controller using serial (or, more specifically, `pyFirmata`). It forced me to use three devices, all of which needed to be wired to each other: the Arduino, the Create2 and my laptop. The Arduino handled some sensor readings, the Create2 handled movement and the others, and the laptop acted as the controller, with serial in and out from the other two.
>
> The solution was to drop the `Arduino`, and instead use a Raspberry Pi as the controller. This opened up a new world of possibilities, because the Pi could not only natively run the Python code and interface with the `Create2` using its included USB cable, but it could be used to program on. This made my workflow significantly faster, as I could just run a `git pull` and edit whatever small things I needed to on the machine without having to reset entirely. It also let me connect and execute the code over SSH, which became integral once ScaredyBot was mobile; I couldn't plug an HDMI or Ethernet cable into the Pi, and plugging it in to test every time would have been a huge hassle and waste of time.

> At the same time, I realized the piezo wasn't going to be sensitive enough to read vibrations in the ground from footfalls. This meant I'd need new sensors. In class, I'd eyed the PIR motion sensor, but the starter kit I got gave me access to more hardware and sensors. From there, I had to learn how to read the new sensors, which took a good amount of trial and error, messing with sensitivities and sensing-modes and reading hundreds of line sof output.
>
> With the new motion sensor, I also had to figure out a way to keep it upright and still on the breadboard, as its pins wouldn't reach beyond the components on its board. As a workaround, I removed the connectors from an extra USB-to-serial cable and added headers to the pins.

The biggest problem came when I, stupidly, plugged a ribbon cable into a GPIO extension board the wrong way. While rewiring the breadboard after testing and refining *all* the sensors I was using, I folded the cable over and lost track of the initial direction. Not thinking, I plugged it in the wrong way, and instantly fried three-out-of-four of the sensors. I had lost my ultrasonic and obstacle avoidance sensors, as well as the extension board and possibly the breadboard. It took a while to figure out what I'd done, but when I realized, I saw that I would need to pivot significantly. Thankfully, the PIR motion sensor wasn't touched, which would have killed the project. 

From here, a significant amount of the project was changed. The scope would become smaller, and the only sensor used to detect someone would be the motion sensor. It was not, however the end of the world, because the motion sensor ended up being all I strictly *needed* to make it work. Thankfully I hadn't programmed robot behaviour based on those sensors, but I had to scrap a huge amount of work on sensors that I'd done in order to accommodate the mistake. At the end of the night, I was, however, ready to move onto programming motion. 

> The next challenge also came when I had to drop off the `Create2`. I had to stop working with it, but needed to keep working, I had things to code and test. My workaround was to create a dummy `Create2` and `PIR` class, which would feed mostly-random sensor readings from all the sensors I was using and give me dummy methods for the `Create2`. While the motion sensor wasn't completely necessary, it allowed me to code and test on my laptop in PyCharm without being connected to the Pi at all. This sped up workflow yet again, and let me keep working without either device. The important thing to mimic accurately was the motion sensor, and a good amount of time went into making the dummy classes work properly. Probably more than was necessary. While the dummy classed sped up workflow, the amount I worked on them was also a waste of time. 

> I also realized I would need a way to reliably stop a robot that was going to be running away from me for mine and ScaredyBot's safety. I decided to add a stop/start button to the breadboard, that acted as the trigger for entering the `_searching` state for the first time, and as an emergency stop that would actually shut down the GPIO and `Create2`, instead of a `keyboardInterrupt` with `ctrl + C`.

From here, coding the movement actually went pretty smoothly, comparatively. And once ScaredyBot was moving, I only really had two challenges; one was significantly greater than the other, however.

> The first, I realized that my motion sensor was tilted so that it was facing slightly backwards (see **img 4.1**). This meant it was much more likely to detect movement behind than in front, and had a much larger range backwards. I was confused why anytime I walked behind the roomba, regardless of distance, it would activate and run; once I realized what was wrong, I used a jumper cable on the breadboard to hold up the sensor and keep it pointed directly upwards (see **img 4.2**). This worked perfectly, and it's activation radius became the same on all sides.

> The last and most frustrating challenge came at the *very* end. As I was testing the nearly-final build, the `Create2` ran over a bump in the floor. This dislodged the motion sensor from the headers, and somehow irreversibly damaged it. After this, the sensor would throw random false positives in an empty room, I spent the last few hours with ScaredyBot trying to debug the sensor. I found that as the sensor was on longer, it would throw more false positives, but that once it hit its third time in the `_running` state, it would almost always be throwing consistent false positives. Getting the final video showing the roomba working correctly took *many* tries. Consistent behaviour of the sensor, however, can be seen in the progress video.

## Future Work

If I were to continue this project, there are a lot of ways that I could see myself expanding it. My first thought is to
use the sensors I'd initially been hoping to.

> I'd wanted to use the ultrasonic sensor to determine if the roomba was going to hit a wall before it actually hit it and create a turning radius to avoid the wall. It would basically function like a more advanced version of the `light_bump` sensor on the `Create2`, but with it's own drawbacks, like only having one. When I had all my hardware at first, I'd planned to use two ultrasonic sensors to combat this, but the second sensor was dead-on-arrival. I'd also wanted to use the obstacle avoidance sensor (essentially what the `light_bump` is) to sense backwards, and see if there was anything directly behind the roomba at all times, which would let it run from people approaching the back in the `_running` state's `waiting` phase.

I also think it would be interesting to do this project without motion sensing at all, and to instead rely on cameras.
This, however, was outside the scope of what I felt capable of, so I did not attempt image processing.

Using any manner of other sensors to get a more accurate picture of the space immediately around the roomba would be a
fun expansion, things like sound, light or vibration (like the prelab planned to use) can all be used to detect
movement, and all together can create a clearer picture and help to combat false positives from the motion sensor.

## Conclusion

----------

### References:

https://docs.sunfounder.com/projects/raphael-kit/en/latest/2.1.1_button_python.html

https://docs.sunfounder.com/projects/raphael-kit/en/latest/1.1.2_rgb_led_python.html

https://docs.sunfounder.com/projects/raphael-kit/en/latest/2.2.5_ir_obstacle_avoidance_sensor_python.html

https://docs.sunfounder.com/projects/raphael-kit/en/latest/2.2.7_pir_python.html

https://docs.sunfounder.com/projects/raphael-kit/en/latest/2.2.8_ultrasonic_sensor_module_python.html

https://docs.sunfounder.com/projects/raphael-kit/en/latest/2.2.9_mpu6050_module_python.html

https://github.com/MomsFriendlyRobotCompany/pycreate2

https://lastminuteengineers.com/pir-sensor-arduino-tutorial/