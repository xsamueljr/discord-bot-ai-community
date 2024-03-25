FROM python:3.9

RUN useradd -ms /bin/bash user

USER user

ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/code

COPY ./requirements.txt $HOME/code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r $HOME/code/requirements.txt

COPY --chown=user . $HOME/code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]