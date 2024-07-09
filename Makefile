.PHONY: test

gui:
	python gui.py

demo:
	python main.py bml_examples/Test1.txt

run:
	@echo "Test invocation without a program. Use make demo to run an example." && python main.py 

test:
	pytest
