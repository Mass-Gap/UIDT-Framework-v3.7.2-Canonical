# UIDT Framework v3.9 Audit Toolchain
# Exact software stack for reproduction of feature/audit-toolchain-v1
# Build:  docker build -t uidt-audit .
# Run:    docker run --rm uidt-audit bash tools/repro_verification.sh

FROM python:3.11.9-slim-bookworm

LABEL maintainer="P. Rietz" \
      version="audit-toolchain-v1" \
      doi="10.5281/zenodo.17835200"

WORKDIR /repo

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies — pinned exact versions
RUN pip install --no-cache-dir \
    mpmath==1.3.0 \
    sympy==1.13.3

# Copy repository (in CI: mount as volume instead)
COPY . /repo

# Pre-create output directory
RUN mkdir -p verification/data/visualizations

# Default command: run full verification
CMD ["bash", "tools/repro_verification.sh"]
