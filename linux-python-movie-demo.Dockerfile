# This FILE SHOULD BE RENAMED TO Dockerfile

#####################################################################
#
# Purpose:
# * download a movie without sound, and a sound file, then... 
#   use the amazing moviepy library to smash them together as
#   a video with an audio track.
# * output is an mp4
# 
# For more info;
# * moviepy: http://zulko.github.io/moviepy/ 
# * the image on which this is based: https://hub.docker.com/r/dkarchmervue/moviepy/
#
#####################################################################

FROM dkarchmervue/moviepy
MAINTAINER Bill Wilder <@codingoutloud>

WORKDIR /work
#RUN ["curl", "-s", \
     #"https://raw.githubusercontent.com/codingoutloud/bolly/master/makebolly.py", \
     #"-o", "/work/makebolly.py"]

ENV SECRET "open sesame" # can be used by CMD

# default action (if not supplied by 'docker run') when a container based on this image starts
# be sure this PATH IS MAPPED by 'docker run' (/media) so 
# the container can find source files and write its result
#CMD ["/builder/makebolly.sh"] # be sure foo.sh has execute permission and shebang
#CMD ["/media/dostuff.sh"] # be sure foo.sh has execute permission and shebang
WORKDIR /work
COPY ./movie-smasher.py /work
RUN pip install --upgrade pip
RUN pip install azure
CMD ["python", "movie-smasher.py"]



