# backend/Dockerfile

# Use the official AWS Lambda base image for Python 3.10
FROM public.ecr.aws/lambda/python:3.10

# Copy your backend code into the image's working directory
COPY . ${LAMBDA_TASK_ROOT}

# Install the uv tool
RUN pip install uv

# Use uv to install the project and its dependencies INTO THE SYSTEM
RUN uv pip install --system .

# Set the command to run when the Lambda is invoked
CMD [ "lambda_processor.lambda_handler" ]