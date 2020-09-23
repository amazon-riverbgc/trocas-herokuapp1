# 9/23, 3/21/2020. Emilio Mayorga, https://github.com/emiliom
# For strategies to make the docker image / heroku slug size smaller,
# refer to https://github.com/amazon-riverbgc/trocas-herokuapp1/issues/2

FROM continuumio/miniconda3

COPY environment.yml environment.yml

RUN /opt/conda/bin/conda env update --name base --file environment.yml \
&& rm environment.yml \
&& conda clean --all --force-pkgs-dirs --yes \
&& find /opt/conda/ -follow -type f -name '*.a' -delete \
&& find /opt/conda/ -follow -type f -name '*.pyc' -delete \
&& find /opt/conda/ -follow -type f -name '*.js.map' -delete \
&& find /opt/conda/lib/python*/site-packages/bokeh/server/static -follow -type f -name '*.js' ! -name '*.min.js' -delete

# Add our code
ADD . /opt/apps
WORKDIR /opt/apps

# Expose is NOT supported by Heroku
# EXPOSE 5006

# Run the image as a non-root user
RUN adduser --disabled-login myuser
USER myuser

# To test locally at http://localhost:5006/webapp, build container and do a docker run:
# $ docker build -t bokeh-app-uk-road-accidents-viz .
# $ docker run -i -t -p 5006:5006 bokeh-app-uk-road-accidents-viz "bokeh serve webapp --port=5006 --address=0.0.0.0"

# Heroku deployment
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD panel serve --port=${PORT} --address=0.0.0.0 trocas_pannelapp_1.ipynb --allow-websocket-origin=trocasdata-1.herokuapp.com
# Note: if you were to deploy this app yourself to say, Heroku, simply replace the host arguments with your Heroku app host name.
# EM: Original statement, from the source
# CMD bokeh serve webapp --port=${PORT} --address=0.0.0.0 --host=trocasdata-1.herokuapp.com
