comment = 0
final_list = []
with open("testfile.c",mode = "r") as f:
	lines = [line.rstrip('\n') for line in f]

for line in lines:
	#print(line)
	if comment == 1:
		if "*/" in line:
			_index = line.index('*/')
			final_list.append(line[_index+2:])
			comment = 0
		continue

	if "//" in line:
		#single line comment
		_index = line.index('//')
		final_list.append(line[:_index])

	elif "/*" in line:
		if "*/" in line:
			#single line comment again
			s_index = line.index("/*")
			e_index = line.index("*/")
			final_list.append(line[:s_index] + line[e_index+2:])
		else:
			#multi line comment
			_index = line.index('/*')
			final_list.append(line[:_index])
			comment = 1
	else:
		final_list.append(line)

str1 = "\n".join(final_list)
print(str1)
