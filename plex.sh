docker run -d --name plex --network=host -v /home/pi/plex/database/:/var/lib/plexmediaserver -v /home/pi/plex/media/:/data jaymoulin/rpi-plex:latest
