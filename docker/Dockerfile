FROM python:alpine
WORKDIR /app

ARG cmd
ARG wheel_name

RUN : "${cmd:?'cmd' build-arg is required}"
RUN : "${wheel_name:?'wheel_name' build-arg is required}"

COPY dist/${wheel_name} .

RUN pip install -qq ${wheel_name}

RUN rm -f ${wheel_name}

ENV COMMAND ${cmd}
CMD ${COMMAND}