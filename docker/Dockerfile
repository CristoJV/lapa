# Dockerfile with support for GPU
# author: CristoJV
# date: 2025-01-23

# -------------------------------------------------------------------- #
# Base Image
# -------------------------------------------------------------------- #

FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

LABEL maintainer="cristojv" \
    version="1.0" \
    description="Docker to work with Python and Pytorch"

ENV SHELL /bin/bash
SHELL ["/bin/bash", "-c"]

# -------------------------------------------------------------------- #
# Preconfigure the timezone
# -------------------------------------------------------------------- #
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq tzdata \
    && ln -fs /usr/share/zoneinfo/Europe/Madrid /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------- #
# Install dependencies
# -------------------------------------------------------------------- #
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    git-lfs \
    curl \
    ca-certificates \
    libgl1-mesa-glx \
    libglib2.0-0 \
    v4l-utils \
    software-properties-common \
    screen \
    openssh-client \
    ffmpeg \
    unzip \
    unrar \
    portaudio19-dev \
    can-utils \
    x11-apps \
    xauth \
    htop \
    gnupg \
    && git lfs install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG HISTFILE
# Configure Bash history
ENV HISTFILE="${HISTFILE}" \
    HISTSIZE=1000 \
    HISTFILESIZE=2000 \
    HISTCONTROL=ignoredups:erasedups \
    PROMPT_COMMAND="history -a; history -c; history -r"

RUN mkdir -p $(dirname ${HISTFILE}) && \
    touch ${HISTFILE} && \
    chmod 600 ${HISTFILE}

# -------------------------------------------------------------------- #
# Install Python
# -------------------------------------------------------------------- #
ARG PYTHON_VERSION
ARG PYTHON_VENV_DIR
ENV PYTHON_VERSION=${PYTHON_VERSION} \
    PYTHON_VENV_DIR=${PYTHON_VENV_DIR}

RUN add-apt-repository -y ppa:deadsnakes/ppa \
    && apt update \
    && apt install --no-install-recommends -y \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-venv \
    tk-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------- #
# Setup Python and install Python packages
# -------------------------------------------------------------------- #
RUN python${PYTHON_VERSION} -m ensurepip --upgrade \
    && python${PYTHON_VERSION} -m pip install --no-cache-dir \
    --upgrade pip setuptools wheel

RUN python${PYTHON_VERSION} -m venv ${PYTHON_VENV_DIR} \
    && ${PYTHON_VENV_DIR}/bin/pip install --no-cache-dir \
    numpy \
    && ${PYTHON_VENV_DIR}/bin/pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio --index-url https://download.pytorch.org/whl/cu118

COPY requirements.txt requirements-dev.txt /tmp/

RUN ${PYTHON_VENV_DIR}/bin/pip install --no-cache-dir \
    -r /tmp/requirements.txt \
    && ${PYTHON_VENV_DIR}/bin/pip install --no-cache-dir \
    -r /tmp/requirements-dev.txt

# -------------------------------------------------------------------- #
# FUTURE
# -------------------------------------------------------------------- #
# In the future, these instructions can be split into a base image and a
# user-specific image to allow other users to utilize the same base image
# from the Docker Hub Registry.

# -------------------------------------------------------------------- #
# Setup working directory
# -------------------------------------------------------------------- #

ARG WORKDIR=/app
WORKDIR ${WORKDIR}

# -------------------------------------------------------------------- #
# Create Non-Root User
# By default, the container runs as the root user. If user-specific
# variables are provided (which is recommended), a non-root user will
# be created and the container will run under that user.
# -------------------------------------------------------------------- #

ARG USER_NAME=root
ARG USER_ID=0
ARG GROUP_ID=0
ARG SHARED_GROUP_ID

RUN set -eux; \
    if [ "${USER_ID}" -ne 0 ] && [ "${GROUP_ID}" -ne 0 ]; then \
    if ! getent group "${GROUP_ID}" > /dev/null; then \
    groupadd -g "${GROUP_ID}" "${USER_NAME}"; \
    fi; \
    if ! id -u "${USER_NAME}" > /dev/null 2>&1; then \
    useradd -l -u "${USER_ID}" -g "${GROUP_ID}" "${USER_NAME}"; \
    fi; \
    # Ensure home directory permissions
    install -d -m 0754 -o "${USER_NAME}" -g "${GROUP_ID}" \
    "/home/${USER_NAME}"; \
    chown -R "${USER_NAME}:${GROUP_ID}" "${WORKDIR}"; \
    chown -R "${USER_NAME}:${GROUP_ID}" "${PYTHON_VENV_DIR}"; \
    fi

# -------------------------------------------------------------------- #
# Adjust ownership of the working directory and
# add user to shared_group, audio and video groups
# -------------------------------------------------------------------- #

RUN set -eux; \
    if [ "${SHARED_GROUP_ID}" -ne 0 ] && ! getent group \
    "${SHARED_GROUP_ID}" > /dev/null; then \
    groupadd -g "${SHARED_GROUP_ID}" shared; \
    usermod -aG shared "${USER_NAME}"; \
    fi && \
    usermod -aG audio,video "${USER_NAME}"

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER ${USER_NAME}
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
