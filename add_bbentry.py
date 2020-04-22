import sys

# filename = "log_with_bbentry.txt"
filename = "roughrough.txt"
with open(filename) as file:
	lines = [line.strip() for line in file]
i = 0
while(i < len(lines)):
	split_line = lines[i].split(" ")
	is_bbentry = split_line[0]
	i += 1
	if(is_bbentry == "BBEntry"):
		bb_entry = split_line[2]
		new_line = lines[i].split(" ")[0]
		while(new_line != "BBEntry" and i < len(lines)):
			lines[i] = lines[i] + " " + bb_entry
			i += 1
			print(i)
			if(i >= len(lines)):
				break
			else:
				new_line = lines[i].split(" ")[0]

with open('roughrough_new_trial.txt', 'w') as f:
    for item in lines:
    	if(item.split(" ")[0] != "BBEntry"):
        	f.write("%s\n" % item)