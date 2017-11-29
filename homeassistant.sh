docker run -d --net=host -v /home/pi/homeassistant/:/config  -v /etc/localtime:/etc/localtime:ro --name="home-assistant" homeassistant/raspberrypi3-homeassistant:latest
#--net=host
