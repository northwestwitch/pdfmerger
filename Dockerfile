FROM python:3.8-slim

LABEL base_image="python/3.8-slim"
LABEL about.license="MIT License (MIT)"
LABEL about.home="https://github.com/northwestwitch/pdfmerger"
LABEL about.documentation="https://github.com/northwestwitch/pdfmerger"
LABEL about.tags="pdf,merge,bookmark,PyPDF2,reportlab,click,orientation,watermark"

RUN useradd --create-home --shell /bin/bash worker
WORKDIR /home/pdfmerger/app
COPY . /home/pdfmerger/app

# Install requirements
RUN pip install -r requirements.txt

# Install the software
RUN pip install -e .

# Run commands as non-root user
RUN chown worker:worker -R /home/worker
RUN mkdir /home/pdfmerger/data
USER worker
ENTRYPOINT ["pdfmerger"]
CMD ["$@"]
