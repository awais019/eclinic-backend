FROM python:3

ENV PYTHONUNBUFFERED=1
WORKDIR /eclinic

# Install pipenv
RUN pip install --upgrade pip 
RUN pip install pipenv

# Install application dependencies
COPY Pipfile Pipfile.lock /eclinic/
# We use the --system flag so packages are installed into the system python
# and not into a virtualenv. Docker containers don't need virtual environments. 
RUN pipenv install --system --dev

# Copy the application files into the image
COPY . /eclinic/

# Expose port 8000 on the container
EXPOSE 8000 8001