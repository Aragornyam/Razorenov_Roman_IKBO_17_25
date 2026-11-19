PYTHON ?= python3
export PYTHONPATH := src
INPUT ?= examples/web_server.conf

.PHONY: install run test examples clean

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m confconv --input $(INPUT)

test:
	$(PYTHON) -m unittest discover -s tests -t . -v

examples:
	@for file in examples/*.conf; do \
		echo "== $$file"; \
		$(PYTHON) -m confconv --input $$file || exit 1; \
	done

clean:
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
