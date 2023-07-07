FROM base:0.3

# https://github.com/rrwick/Porechop
ARG PORECHOP_VERSION="0.2.4"
# https://github.com/marbl/canu
ARG CANU_VERSION="2.2"
# https://github.com/lh3/minimap2
ARG MINIMAP2_VERSION="2.26"

# porechop
RUN wget -q https://github.com/rrwick/Porechop/archive/refs/tags/v${PORECHOP_VERSION}.tar.gz \
  && tar -xzf v${PORECHOP_VERSION}.tar.gz && rm v${PORECHOP_VERSION}.tar.gz \
  && cd Porechop-${PORECHOP_VERSION} && python3 setup.py build && python3.11 setup.py install && cd .. \
  && rm -r Porechop-${PORECHOP_VERSION}

# canu
RUN wget -q https://github.com/marbl/canu/releases/download/v${CANU_VERSION}/canu-${CANU_VERSION}.tar.xz \
  && tar -xJf canu-${CANU_VERSION}.tar.xz && rm canu-${CANU_VERSION}.tar.xz \
  && cd canu-${CANU_VERSION}/src && make && cd ../.. \
  && mkdir /opt/canu && cp -r canu-${CANU_VERSION}/build/* /opt/canu/ \
  && ln -sf /opt/canu/bin/canu /usr/local/bin/canu \
  && rm -r canu-${CANU_VERSION}

# minimap2 (картировщик)
RUN wget -q https://github.com/lh3/minimap2/archive/refs/tags/v${MINIMAP2_VERSION}.tar.gz \
  && tar -xzf v${MINIMAP2_VERSION}.tar.gz && rm v${MINIMAP2_VERSION}.tar.gz \
  && cd minimap2-${MINIMAP2_VERSION} && make && cd .. \
  && cp minimap2-${MINIMAP2_VERSION}/minimap2 /usr/local/bin/ \
  && rm -r minimap2-${MINIMAP2_VERSION}
