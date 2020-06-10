FROM centos:7.2.1511

RUN yum install -y \
     vim\
     python-pip\
     wget

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    echo "export PATH=/opt/conda/bin:$PATH" >> ~/.bashrc

ENV PATH /opt/conda/bin:$PATH
ARG ENVFILE=environment.yml
COPY $ENVFILE /app/environment.yml
WORKDIR /app

# Create the environment:
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
RUN conda config --set show_channel_urls yes
RUN conda env create -f environment.yml

COPY . /app

# Make RUN commands use the new environment:
# SHELL ["conda", "run", "-n", "kddcup", "/bin/bash", "-c"]
RUN echo "source activate kddcup" >> ~/.bashrc
CMD ["/app/entrypoint.sh"]
