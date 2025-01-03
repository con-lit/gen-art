FROM python:3.12

# Set work directory
WORKDIR /code

# Copy requirements.txt
COPY requirements.txt /code/
COPY setup.sh /code/

# Copy project code
COPY ./pattern_generator /code/pattern_generator 
COPY ./app /code/app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r --root-user-action /code/requirements.txt

# Install local package
# RUN pip install -e ./stolpersteine_data_import

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1