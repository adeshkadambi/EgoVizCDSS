FROM continuumio/miniconda3
COPY . /app/
EXPOSE 5000
WORKDIR /app/

# Create a non-root user
# ARG username=egoviz
# ARG uid=1000
# ARG gid=100
# ENV USER $username
# ENV UID $uid
# ENV GID $gid
# ENV HOME /home/$USER
# RUN adduser --disabled-password \
#     --gecos "Non-root user" \
#     --uid $UID \
#     --gid $GID \
#     --home $HOME \
#     $USER

RUN conda env create -f environment_linux.yml 
# Change ownership of workdir
# RUN chown -R $UID:$GID /app/* && \
#  	chown $UID:$GID /opt/conda/envs/*

SHELL ["conda", "run", "-n", "handobj", "/bin/bash", "-c"]
WORKDIR /app/
RUN apt-get update && apt-get install -y libgl1-mesa-glx && \
cd detection_models/hand_obj/lib && python setup.py build develop 
WORKDIR /app/
# USER $USER
# CMD ["conda", "run", "--no-capture-output", "-n", "handobj", "python", "server_HOmodel.py"]
ENTRYPOINT ["./entrypoint.sh"]


