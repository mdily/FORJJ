import codecs
import re
import xlwt
import csv
import datetime

def get_file_name():
	now = datetime.datetime.now()
	year = now.year
	month = now.month
	day = now.day
	file_name = "%d-%d-%d.txt" % (year, month, day)
	return file_name


def read_txt_data(encoding="utf_8_sig"):
	file_name = get_file_name()
	try:
		with codecs.open(file_name, 'r', encoding='utf_8_sig', errors="ignore") as fp:
			rows = fp.readlines()
	except IOError as e:
		raise IOError("请将txt文件放在与本脚本相同的文件夹之下，并将文件名称改成 %s" % file_name)
	return rows


def txt_to_excel_data(txt_data):
	excel_data = []
	for row in txt_data:
		item = row.split('\t')
		excel_data.append(item)
	return excel_data


def write_into_excel(excel_data):
	re_obj = re.compile(r'^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})')
	fp = xlwt.Workbook(encoding="utf_8_sig")
	sheet = fp.add_sheet('sheet1')
	for row_index, row_data in enumerate(excel_data):
	    for column_index, cell_data in enumerate(row_data):
	    	cell_data = cell_data.replace('\x00', '')
	    	match_data = re_obj.match(cell_data)
	    	if match_data:
	    		date = match_data.group(1)
	    		time = match_data.group(2)
	    		cell_data = "%s %s" % (date, time)
	    	sheet.write(row_index, column_index, cell_data)
	file_name = get_file_name().replace('txt', 'xls')
	fp.save(file_name)


def wirter_into_csv(excel_data):
	file_name = get_file_name().replace('txt', 'csv')
	re_obj = re.compile(r'^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})')
	with codecs.open(file_name, 'w', 'utf_8_sig') as fp:
		csv_writer = csv.writer(fp)
		for row_data in excel_data:
			for index, cell_data in enumerate(row_data):
				cell_data = cell_data.replace('\x00', '')
				match_data = re_obj.match(cell_data)
				if match_data:
					date = match_data.group(1)
					time = match_data.group(2)
					cell_data = "%s %s" % (date, time)
				else:
					try:
						if cell_data.startswith('0'):
							int(cell_data)
                            # 为了csv用excel打开时显示首位0
							cell_data = '="%s"' % cell_data
					except Exception as e:
						pass
				row_data[index] = cell_data
			csv_writer.writerow(row_data)

def export_excel_csv_data():
	try:
		txt_data = read_txt_data()
	except UnicodeError:  
		txt_data = read_txt_data('utf-8')
	txt_data = [i for i in txt_data if i.strip() and i.strip() != '\x00']
	excel_data = txt_to_excel_data(txt_data)
	write_into_excel(excel_data)
	print("导出excel文件成功")
	wirter_into_csv(excel_data)
	print("导出csv文件成功")


def main():
	try:
		export_excel_csv_data()
	except Exception as e:
		print("导出失败：", e)


if __name__ == "__main__":
	main()
	

