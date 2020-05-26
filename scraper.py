import pandas as pd
import re #regular expressions

season = 'fall' #choose this somehow later, spring, fall, or summer

table_df = pd.read_html("http://www.csueastbay.edu/students/academics-and-studying/finals/"+season+".html")[0]

#get clean dates from table...
clean_headers = ['Times']
for x in table_df.columns[1:]:
	date = x[:3]
	date += re.findall(', ...', x)[0]
	date += ' ' + re.findall('\d+', x)[0]
	if date[-2] in [' ', '2', '3'] and date[-1] in ['1','2','3']:
		if date[-1] == '1':
			date += 'st'
		elif date[-1] == '2':
			date += 'nd'
		else:
			date += 'rd'
	else:
		date += 'th'
	clean_headers.append(date)
print(clean_headers)
table_df.columns = clean_headers


#Storing the time ranges of the finals:
time_list = list(table_df['Times'])
classtimes_to_finalexamhour_dict={}

list_of_days=['MWF','MW','M','MF','TuTh','Tu','WF','W','Th','FS','F']

time_increments = []
for half_hour in range(6,23,.5):
	time_increments.append(half_hour)
	
df = pd.DataFrame(columns=list_of_days, index = time_increments)

class_to_final_dict = {}
for col in table_df.columns[1:]: #dates
    for x in range(0,6): #there are 6 possible final time intervals
        class_DTs = table_df.loc[x,col]
        lookup_set = re.findall("\w+ [0-9]+:?[0-9]*-[0-9]+:[0-9]+ [ap]m", class_DTs) #USES REGEX CONVERT TO LIST of str
        for y in lookup_set: #GETS EACH STR IN THE LIST JUST CREATED OUT OF TABLE ENTRY
            start_end_times = re.findall("[0-9]+:?[0-9]*",y) #start and end hours
            #print(start_end_times[0])
            #print(re.findall("\w+",y)[0]) #MWF/FS/etc
            #print(y[-2]) #am/pm
            #print(col + ', ' + time_list[x])
            days_class_meets = re.findall("\w+",y)[0]
            start_end_times[0] = (int(re.findall("[0-9]+",start_end_times[0])[0]))
            start_end_times[1] = (int(re.findall("[0-9]+",start_end_times[1])[0]))
            if y[-2] == 'p':
                if start_end_times[0] < 12:
                    start_end_times[0] += 12
                if start_end_times[1] < 12:
                    start_end_times[1] += 12
            for hour in range(start_end_times[0],start_end_times[1]+1):
                df.loc[hour,days_class_meets] = col + ', ' + time_list[x]
