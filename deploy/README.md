# docker-ssh
A container from Ubuntu 12.04 with openssh-server preinstalled to be used as a base image. Inspired by docker-wordpress-nginx container by Eugene Ware.

# Installation

$ git clone https://github.com/sullof/docker-sshd.git
$ cd docker-sshd
Substitute the current authorized_keys file with your public key. If not, potentially, I could access your container : ) If you prefer to use a password, comment the keys block

Usage

# Build the container:

$ sudo docker build -t sullof/sshd .
It's better if you change the tag using your Docker username.

To spawn a new instance and see the IP:

$ CONTAINER_ID=$(sudo docker run -d docker-ssh)
$ sudo docker inspect $CONTAINER_ID | grep IPAddress | awk '{ print $2 }' | tr -d ',"'
You will have a result like this:

172.17.0.74
And, finally, you should connect to the container with

$ ssh root@172.17.0.74
What after?

You can create new images starting your Dockerfile with something like

FROM sullof/sshd
and modify appropriately the supervisord.conf file without overwriting the previous one. For example, in your derivated images, you could use the following approach appending a new file:

$ ADD ./supervisord.conf.append /etc/supervisord.conf.append
$ RUN cat /etc/supervisord.conf.append >> /etc/supervisord.conf &&\
      rm /etc/supervisord.conf.append
There is an example at docker-wpngx.

License

(The MIT License)

Copyright (c) 2013 Francesco Sullo sullof@sullof.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.