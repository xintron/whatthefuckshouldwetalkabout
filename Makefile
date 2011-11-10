BOOTSTRAP = ./html/bootstrap.css
MAIN_CSS = ./html/style.css
BOOTSTRAP_LESS = ./bootstrap/lib/bootstrap.less
LESS_COMPRESSOR ?= `which lessc`

.PHONY: build

build:
	@@if test ! -z ${LESS_COMPRESSOR}; then \
		cat ${BOOTSTRAP_LESS} > ${BOOTSTRAP_LESS}.tmp; \
		echo '@import "../../flaskr/css/custom.less";' >> ${BOOTSTRAP_LESS}.tmp; \
		lessc ${BOOTSTRAP_LESS}.tmp > ${MAIN_CSS} --compress; \
		rm -f ${BOOTSTRAP_LESS}.tmp; \
		echo "Bootstrap successfully built!"; \
	else \
		echo "You must have the LESS compiler installed in order to build Bootstrap."; \
		echo "You can install it by running: npm install less -g"; \
	fi
