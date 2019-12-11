FROM onion/omega2-source
RUN apt-get update
RUN apt-get install -y git curl build-essential python3 python3-pip python3-wheel nano unzip zip patch xsltproc gcc python3-dev python3-setuptools
RUN pip3 install cython
RUN make