FROM python:3.12-slim

# a container process should not be root
RUN useradd --create-home --uid 10001 appuser
WORKDIR /srv

# the code goes last, because it is what changes most often
COPY app.py .

USER appuser
EXPOSE 8000
CMD ["python", "app.py"]
