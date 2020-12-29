from pathlib import Path
import glob
import os
from PyPDF2 import PdfFileWriter, PdfFileReader
# b = glob.glob('./*.txt')
from operator import itemgetter


# p = Path(mypath)

# pattern1 =  ".*/.*js"
# # list1 = [x for x in p.iterdir() if x.is_dir()]

# # print (list1)


# generator_obj_1 = p.glob(".*")
# print (list(generator_obj_1))

# b = glob.glob('/Users/panos/GitBox/gatsby-playground/.*')
# print (b)

html_template = """
<!DOCTYPE html>
<html>
<head>
<style type="text/css">
@media print {
	.blank_page {
	   page-break-after: always;

	}
	.number {
	background:#ccc;
	border-radius: 5px;
	padding:2px;

	}
    xmp {
        white-space: pre-wrap;
        font-family: "Monaco"; 
        font-size:14px;
    }
}

h2 {
font-family: Arial, Helvetica, sans-serif;
    text-align:center;

}
</style>
</head>
<body>
<div class="blank_page"></div>
<h2>[%s] %s</h2>
<xmp>%s</xmp>

</body>
</html>
"""

def printlist(l):
	for index,item in enumerate(l):
		print(index+1, "\t", item[2])

def myfunc(path_open, file_extentions):
	final = []
	for root, dirs, files in os.walk(path_open):
		for file_name in files:

			if file_name.endswith(file_extentions):
				full_path = os.path.join(root, file_name)
				# print (file_name)
				# print (full_path)
				final.append(full_path)
	return final

def transformation(x, path_open):
	#EXAMPLE OF χ
	# '/Users/panos/GitBox/gatsby-playground/gatsby-book-club/src/pages/index.js', 

	# print (x)
	root = "/root"
	removed_init_path = x.replace(path_open, "")
	final_path_original = root + removed_init_path.replace("/", "__")
	final_path_html = path_save_pdf + final_path_original.split(".", -1)[0] + ".html"

	# x_html = x.split(".", -1)[0] + ".html"
	return [x, final_path_html, final_path_original]

def delete_fist_pdf_page(pdf_path_str):
	pages_to_delete = [0] # page numbering starts from 0
	infile = PdfFileReader(pdf_path_str, 'rb')
	output = PdfFileWriter()

	for i in range(infile.getNumPages()):
		if i not in pages_to_delete:
			p = infile.getPage(i)
			output.addPage(p)


	safe_path_str = pdf_path_str
	with open(safe_path_str, 'wb') as f:
		output.write(f)


def main(path_open, path_save_pdf):
	f = myfunc(path_open, filter_ext)
	e = [x for x in f if "/node_modules/" not in x]
	g = [x for x in e if "/.cache/" not in x]
	final_path_list = g

	h = [transformation(x, path_open) for x in g]
	print (h)
	h.sort(key=lambda x: x[2])
	printlist(h)

	# sorted_h = sorted(h, key=itemgetter(2))


	for index,path_list in enumerate(h):
		safe_pdf(index, path_list)

def add_prefix_number(prefix, mypath):
	print ("Mypath", mypath)
	first_part = mypath.rsplit("/", 1)[0]
	print ("first_part", first_part)
	second_part = mypath.rsplit("/", 1)[1]
	final = first_part + "/" + prefix + "_" + second_part
	print ("FINAL", final)
	return final



def safe_pdf(index, path_list):
	file_num = index+1

	file_num_prefix = str(file_num)
	file_num_prefix = file_num_prefix.zfill(3) 

	# EXAMPLE OF PATH_LIST
	# ['/Users/panos/GitBox/gatsby-playground/gatsby-book-club/src/pages/404.js', 
	# '/Users/panos/GitBox/gatsby-playground/gatsby-pdfs/root__src__pages__404.html']

	p_input_str = path_list[0]
	p_output_str = path_list[1]
	# example 
	# p_output_str /Users/panos/GitBox/gatsby-playground/gatsby-book-club-master-pdfs/root__src__pages__add-book.html
	p_output_original = path_list[2]

	p_output_str = add_prefix_number(file_num_prefix, p_output_str)

	# print ('p_input_str', p_input_str)
	print ('p_output_str', p_output_str)
	# print ('p_output_original', p_output_original)

	h2_title = p_output_original.split("/")[-1].replace("__", " / ")

	p_input = Path(p_input_str)
	p_output = Path(p_output_str).touch()

	mycode = p_input.read_text()

	myhtml = html_template % (file_num, h2_title, mycode)
	# print(myhtml)
	p_save = Path(p_output_str)
	p_save.write_text(myhtml)



	# princexml creates pdf
	cmd = "prince {}".format(p_save)
	os.system(cmd)
	p_save.unlink()


	pdf_output_str = p_output_str.split(".", -1)[0] + ".pdf"

	# print (pdf_output_str)

	delete_fist_pdf_page(pdf_output_str)



if __name__ == '__main__':
	# IMPORTANT NOTE!!!
	# PATHS SHOULD NOT END WITH "/"!!!!

	parent_path = ""

	filter_ext = (".txt", ".js", ".md", ".json", ".scss")

	path_open =     "/folder/input"
	path_save_pdf = "/folde/output"

	main(path_open, path_save_pdf)




