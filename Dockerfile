# My Django Project
# Version: 1.0

# FROM - Image to start building on.
FROM python


# PROJECT SETUP
# ----------------

# sets the working directory
WORKDIR /eclinic

# copy these two files from <src> to <dest>
# <src> = current directory on host machine
# <dest> = filesystem of the container
COPY Pipfile Pipfile.lock /eclinic/

# install pipenv on the container
RUN pip install -U pipenv

# install project dependencies
RUN pipenv install --system

# copy all files and directories from <src> to <dest>
COPY . /eclinic
EXPOSE 8000