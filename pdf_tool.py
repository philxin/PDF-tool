import PyPDF2
import logging
from shutil import copyfile
import os

logging.basicConfig(level=logging.INFO)
#logging.basicConfig(level=logging.DEBUG)

# insert function: insert a range of pages from pdf1 into a specific position of pdf2
# 	copy those pages from pdf1 as part_1, copy the former pages of the position in pdf2 as part_2,
# 	copy the latter pages of the position in pdf2 as part_3.
# 	merge part_2, part_1, part_3 in order as a new file. DONE.

# copy function: copy a range of pages from an existed pdf file

# merge function: just put two PDF files together




#return type: PdfFileWriter
def copyPages(pdfFile_reader, pdf_writer, range_start, range_end):		# range starts from 1
	for pageNum in range(range_start - 1, range_end):
		pageObj = pdfFile_reader.getPage(pageNum)
		pdf_writer.addPage(pageObj)
	return pdf_writer


def copyPDF(fileToCopy, copyRange, newFile):

	pdfFile = open(fileToCopy, "rb")
	pdf_reader = PyPDF2.PdfFileReader(pdfFile)

	range_list = copyRange.split()
	pdf_writer = PyPDF2.PdfFileWriter()

	for rg in range_list:
		logging.info("rg == " + rg)
		if "-" in rg:
			rgs = rg.split('-')
			logging.info("rgs[0] == " + rgs[0])
			logging.info("rgs[1] == " + rgs[1])
			if len(rgs) == 2:
				pdf_writer = copyPages(pdf_reader, pdf_writer, int(rgs[0]), int(rgs[1]))
			else:
				logging.debug('Wrong input range with -!!')
		else:
			pdf_writer = copyPages(pdf_reader, pdf_writer, int(rg), int(rg))

	pdfOutputFile = open(newFile + ".pdf", 'wb')
	pdf_writer.write(pdfOutputFile)

	pdfOutputFile.close()
	pdfFile.close()


def merge2Files(pdf1, pdf2, newPDF):
	pdf1File = open(pdf1 + ".pdf", "rb")
	pdf2File = open(pdf2 + ".pdf", "rb")
	pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
	pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

	pdfWriter = PyPDF2.PdfFileWriter()

	pdfWriter = copyPages(pdf1Reader, pdfWriter, 1, pdf1Reader.numPages)
	pdfWriter = copyPages(pdf2Reader, pdfWriter, 1, pdf2Reader.numPages)

	pdfOutputFile = open(newPDF + ".pdf", "wb")
	pdfWriter.write(pdfOutputFile)

	pdfOutputFile.close()
	pdf1File.close()
	pdf2File.close()




# insert: insert a range of pages from pdf1 into a specific position of pdf2
# copy those pages from pdf1 as part_1, copy the former pages of the position in pdf2 as part_2,
# copy the latter pages of the position in pdf2 as part_3.
# merge part_2, part_1, part_3 in order as a new file.
def insertPDF(fileToCopy, copyRange, fileToInsert, ins_pos, newFile):
	pdf2 = open(fileToInsert, "rb")
	pdf_reader = PyPDF2.PdfFileReader(pdf2)

	copyPDF(fileToCopy, copyRange, "part_1")
	copyPDF(fileToInsert, "1-" + str(int(ins_pos)-1), "part_2")
	copyPDF(fileToInsert, ins_pos + "-" + str(pdf_reader.numPages), "part_3")

	merge2Files("part_2", "part_1", "temp")
	merge2Files("temp", "part_3", newFile)

	os.remove("temp.pdf")
	os.remove("part_1.pdf")
	os.remove("part_2.pdf")
	os.remove("part_3.pdf")
	pdf2.close()





function = input("What do you want to do with pdf files? (copy, insert, merge)\n")
if function == "copy":
	#Copy function: copy a range of pages from an existed pdf file
	pdfFile_o = str(input("Name of the pdf file you want to copy (without .pdf): ")) + '.pdf' # original file name
	range_str = str(input("Range of the pages IN THE ORDER you want to copy (e.g. 1-4 7-10 6): \n"))
	pdfFile_n = str(input("Name of the pdf file of the copied pages (without .pdf): ")) # new file

	copyPDF(pdfFile_o, range_str, pdfFile_n)

elif function == "insert":
	pdfToCopy = str(input("Name of the pdf file you want to copy (without .pdf): ")) + '.pdf' 
	range_str = str(input("Range of the pages IN THE ORDER you want to copy (e.g. 1-4 7-10 6): \n"))
	pdfToInsert = str(input("Name of the pdf file you want to insert copied pages (without .pdf): ")) + '.pdf'
	posToInsert = str(input("Position in the file you want to insert pages: "))
	newFile = str(input("New PDF file name (without .pdf): "))

	insertPDF(pdfToCopy, range_str, pdfToInsert, posToInsert, newFile)
'''
elif function == 'merge':
	filesToMerge = str(input("PDF files you want to merge (seperated by spcae, without .pdf): \n"))
	files = filesToMerge.split()
	temp = files[0]
	for i in range(1, len(files)):
		merge(temp, files[i], "temp_new")
		temp = temp_new

'''
