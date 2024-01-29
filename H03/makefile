copyfiles:
	cp $(filepath) .

compile-huffman:
	@echo 'Python solution. Nothing to compile.'

run-huffman:
	python3 huffman_encoder.py $(input)

check-huffman:
	python3 huffman_decoder.py $(input)
	python3 compression-info.py $(input)

list-huffman:
	ls huffman_encoder.py

show-huffman:
	@echo 'Showing python file huffman_encoder.py'
	cat huffman_encoder.py
