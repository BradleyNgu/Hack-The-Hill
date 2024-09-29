# The Heart Stopper 💔


This Python/C++ project uses the MediaPipe library to capture and reconoze hand gesetures and sends the amount of fingers held up to an Arduino through serial communication. The project leverages computer vision to detect hand landmarks and identify how many fingers are extended using MediaPipe's hand tracking model. This information is then transmitted to the Arduino, where it turns a servo motar for a set ammount of time dependant on how many fingures are up.

## Inspiration
We love energy drinks -- who doesn’t? A quick pick-me-up can cure even the dreariest of moods. However, as we know, it is easy to go overboard unknowingly. Working on a late night project and - next thing you know - you've had several energy drinks within the span of a few short hours! If we could regulate our energy drinking habits all while sitting at the desk, we would be all the better off for it.

## What it does
The Heart Stopper is a machine that pours a designated amount of energy drink based on how many fingers you hold up to your webcam. Hold up one finger, you just need a slight pick-me-up. Hold up two, a little extra kick is all you need. Hold up 3 or 4, things are starting to get serious. Hold up 5, the situation is dire and you need to lock in.

## How we built it
The Heart Stopper uses Python's OpenCV library to access your webcam in conjunction with a Google API known as MediaPipe to gather visual data. MediaPipe can natively track hand movements, giving coordinates to certain points of the hand (i.e. each finger's key joints, such as the base, tip, et cetera); these points are known as landmarks. Identifying different gestures - such as how many fingers are extended - is as simple as comparing the coordinates of each landmark in relation to each other.

Using the the number of fingers extended as input, this data is sent to the Arduino board via Python's pySerial library. Written in C++, the Arduino code handles the data to control servo motors - used to pivot the cup holder - and LEDs, which turns the cup holder the optimal pouring angle (~67°) for a set duration of time, based on the number of fingers extended.

And of course, none of this functions without the best carpentry skills money can buy.

## Challenges we ran into
We had a few heart stopping moments throughout this entire process, to say the least. A few of our initial ideas were quickly rendered moot, such as gluing a can to the servo motor and using a pendulum with a counterweight to pour the liquid out of the can. However, our initial servo motor - a 9-gram servo mini - is not strong enough to hold or turn the weight of a full-sized can, hence why we opted for a much stronger model.

We also had trouble returning the Python data straight to the Arduino IDE, manipulating the data via C++. The solution? Serial ports. After much research and code revisions, we managed to implement the proper use of the serial port, connecting our hand-tracking script to the Arduino IDE.

## Accomplishments that we're proud of
3/4 of us on the team have never participated in a hackathon before. Because of this, we had to figure out how to not only start a project but also work together to build something that works. We're proud that given the time requirements, we managed to start from nothing to something in less than 48 hours. We're also proud that we were able to actually build a stable structure out of wood and have reliable code that will work when booted up.

## What we learned
We learned a ton from this project! First, working with MediaPipe was eye-opening because we didn’t realize how easy it could be to get hand-tracking up and running. It was super cool to see how well it detects the different parts of the hand in real time. We also learned a lot about OpenCV and how to process video frames. It was something that seemed a bit intimidating at first, but once we got into it, it made a lot of sense. On the hardware side, getting the Arduino to communicate with the Python script using serial communication taught us a lot about connecting software with physical devices. We realized it’s not just about writing code but it’s also about how you send and receive data reliably between two completely different systems. It felt great to see the Arduino reacting to our hand gestures in real time. Another big lesson was the importance of testing and debugging. We spent a lot of time tweaking things to get the gesture recognition just right and making sure the serial communication worked smoothly without lag. All in all, this project gave us hands-on experience with bridging software and hardware to create a working project.

## What's next for The Heart Stopper
We need to improve the accuracy of the gesture recognition function to prevent accidental input. Likewise, if no cup is in place, it should not pour regardless. We also want to take this further by adding more complex gestures. Imagine controlling multiple devices or even making this gesture recognition part of a bigger system, like having the option to have multiple drinks of your choosing. It could also be cool to make the Arduino communicate wirelessly, so instead of being tethered by a USB cable, you could use Bluetooth or Wi-Fi to send the gestures to a device across the room. For proper energy drink regulation, this machine would fulfill its role best if it were capable of data collection of how much drink has been poured. In the short-term, this can prevent you from drinking over the daily recommended. In the long-term, this can be used to find the optimal amount of drink for any designated individual.

