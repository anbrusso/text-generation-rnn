FROM tensorflow/tensorflow:latest-gpu-jupyter
ENV HOME /tf/
RUN rm -rf /tf/tensorflow-tutorials
WORKDIR $HOME
COPY notebooks/. $HOME
Run pip install sklearn