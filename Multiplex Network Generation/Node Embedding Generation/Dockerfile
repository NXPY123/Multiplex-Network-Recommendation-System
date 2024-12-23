# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

RUN pip install futures==2.1.6
RUN pip install six
RUN pip install --upgrade gensim
RUN pip install psutil
RUN pip install networkx

# Install the deepwalk package
RUN pip install deepwalk==1.0.3

# Copy the modified Python files to the container
COPY ./__main__.py /tmp/___main__.py
COPY ./weighted_random_walk.py /tmp/weighted_random_walk.py
COPY ./graph.py /tmp/graph.py
COPY ./volume/generate_embeddings.py /app/generate_embeddings.py

# Find the deepwalk library path and replace the files
RUN export LIB_PATH=$(python -c "import deepwalk, os; print(os.path.dirname(deepwalk.__file__))") && \
    mv /tmp/___main__.py $LIB_PATH/__main__.py && \
    mv /tmp/weighted_random_walk.py $LIB_PATH/weighted_random_walk.py

# Run the command to generate the embeddings
CMD ["python", "/app/generate_embeddings.py"]



