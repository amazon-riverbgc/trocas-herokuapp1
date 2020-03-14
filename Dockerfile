# https://hub.docker.com/r/continuumio/miniconda3
FROM continuumio/miniconda3

# EM: Do I really need this? Try removing it
# to resolve the error: ImportError: libGL.so.1: cannot open shared object file: No such file or directory
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx

# update conda to latest version
# 3/13/2020: Changed from: RUN conda update conda
RUN conda update -n base -c defaults conda

# Grab conda environment file
# Conda channels are specified in this env file
ADD ./environment.yml /tmp/environment.yml

# Install Conda packages
# EM: Could hardwire a conda env name here
RUN conda env create -f /tmp/environment.yml

# EM: It's setting up a "default conda env"

# do some conda magic
ENV CONDA_DEFAULT_ENV holoviztrocas_panelapp
ENV PATH /opt/conda/envs/$CONDA_DEFAULT_ENV/bin:$PATH
ENV CONDA_PREFIX /opt/conda/envs/$CONDA_DEFAULT_ENV
RUN echo $PATH
# This is run just as a manual verification
RUN conda env list

# Add our code
ADD . /opt/apps
#ADD ./apps /opt/apps
WORKDIR /opt/apps

# Expose is NOT supported by Heroku
# EXPOSE 5006

# Run the image as a non-root user
RUN adduser --disabled-login myuser
USER myuser

# Note: to test locally at http://localhost:5006/webapp, we can either:
#
# option 1: build container and do a docker run (build it yourself locally):
# $ docker build -t bokeh-app-uk-road-accidents-viz .
# $ docker run -i -t -p 5006:5006 bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"
#
# option 2: use the one on dockerhub (built by github user: atlas7)
# $ docker run -i -t -p 5006:5006 atlas7/bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"
#
# option 3: use the one on Heroku Container Registry (built by github user: atlas7)
# $ docker run -i -t -p 5006:5006 registry.heroku.com/uk-road-accidents-viz/web "bokeh serve webapp --port=5006 --address=0.0.0.0"
#

# Heroku deployment
# Note: if you were to deploy this app yourself to say, Heroku, simply replace the host arguments with your Heroku app host name.
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD panel serve --port=${PORT} --address=0.0.0.0 trocas_pannelapp_1.ipynb --allow-websocket-origin=trocasdata-1.herokuapp.com
# EM: Original line, from the source
# CMD bokeh serve webapp --port=${PORT} --address=0.0.0.0 --host=trocasdata-1.herokuapp.com
