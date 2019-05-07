

f = open("D:\\pythonGames\\WorkGUI\\idc5\\up_fw\\rbComponent\\src\\rbComponent.cpp",'r',)
string = f.read()

broken = string.split("\"")

headers = []
for each in broken:
	if ".h" in each and ("<" not in each or ">" not in each):
		headers.append(each)
print(headers)


