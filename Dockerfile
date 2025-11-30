FROM runpod/comfyui:latest

WORKDIR /workspace

COPY Shortie_Video_erstellung.json /workspace/Shortie_Video_erstellung.json
COPY main.py /workspace/main.py
COPY serverless_handler.py /workspace/serverless_handler.py
COPY requirements.txt /workspace/requirements.txt
COPY start.sh /workspace/start.sh

RUN chmod +x /workspace/start.sh

RUN pip install --upgrade pip && \
    pip install -r /workspace/requirements.txt

EXPOSE 8188

CMD ["/workspace/start.sh"]
