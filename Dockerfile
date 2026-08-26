FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 8501

# Default command runs the API; docker-compose overrides this
# for the streamlit service.
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]