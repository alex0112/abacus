.PHONY: test

demo:
	python3 main.py bml_examples/Test1.txt

run:
	echo "Test invocation without a program. Use make demo to run an example." && \
	python3 main.py 
test:
	pytest 
