<img src="https://github.com/marcgarrofe/RLP-PLAB/blob/main/luci_logo.png" align="right" width="300" alt="header pic"/>

# Luci
Human seeker robot in hostile environments.


# Table of Contents
   * [What is this?](#what-is-this)
   * [Requirements](#requirements)
   * [How to use](#how-to-use)
   * [Controller panel](#controller-panel)
   * [Driving](#driving-modes)
   * [Speach to text](#speach-to-text)
   * [Image processing](#image-processing)
   * [License](#license)
   * [Contribution](#contribution)
   * [Authors](#authors)


# What is this?

Luci is a human detector robot designed to locate people inside hostile enviroments such as gas, smoke or fire. 

![alt text](https://github.com/marcgarrofe/RLP-PLAB/blob/main/img/luci.png)

Features:

1. Easy to controll and operate.

2. Widely range of sensor and cameras.

3. Small and fast.


# Requirements

For running each sample code:

- [Python 3.10.x](https://www.python.org/)

- [C++]

- [Flask/socket.io](https://socket.io/)

- [PySerial](https://pypi.org/project/pyserial/)

- [OpenCV](https://opencv.org/)

- [VidGear](https://abhitronix.github.io/vidgear/v0.2.5-stable/)

- [Google Cloud Speach](https://cloud.google.com/speech-to-text)

- [PyAudio](https://pypi.org/project/PyAudio/)

- [Adafruit](https://www.adafruit.com/)

- [NumPy](https://numpy.org/)
 

# How to use

- Step 1:
`cd code`

- Step 2:
`pip install -r requirements.txt` 

- Step 3:
`python main.py`

- Step 4:
Isn't it beautiful?


# Controller panel

Luci has a build-in controller panel web server. Her user-friendly interface allows the operator to see through Luci's eyes and sensors can drive where none can arrive.

Luci's has a wide range of sensors such as: gas sensor, distance, temperature, humidity, microphone and two cameras. You can see all the sensors displaying below:

![alt text](https://github.com/marcgarrofe/RLP-PLAB/blob/main/img/website.png)

# Driving modes

In order to perform more accurate driving experience, Luci is controlled with a gamepad. This cool feature allows the operator to control each wheal movement and speed separately in order to get a better accuracy movement.

# Speach to text

Luci's microphone can recognize voice and convert it to text. This feature is founded on the controller panel and allows the operator to read the live transcription of the room's voice.

# Image processing

The robot's eyes are formed of a wide-range camera and a thermal camera that combined using image processing provides an RGB realtime image with temperature coloring.

Finally, in order to drive and have a real time image from Luci, she has a build in video stabilization developed with software that uses a wide range of image stabilization such as: KeyPoint matching, Fourier image superposition and Optical Flow. Each age can be called by the operator in order to find the implementation that works best for each situation.


# License 

MIT

# Contribution

Any contribution is welcome!! 

# Authors
 * [Marti Caixal](https://github.com/marti1999)
 * [Hernan Capilla](https://github.com/hcapilla)
 * [Marc Garrofe](https://github.com/marcgarrofe)
 * [Ricard Lopez](https://github.com/Ricardlol)
 * [Bruno Moya](https://github.com/elblogbruno)
