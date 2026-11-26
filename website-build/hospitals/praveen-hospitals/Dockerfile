FROM python:3.12-slim
WORKDIR /app
COPY server.py styles.css site.js index.html about.html services.html specialities.html patient-care.html empanelments.html gallery.html contact.html ./
ENV PYTHONUNBUFFERED=1
CMD ["python", "server.py"]
