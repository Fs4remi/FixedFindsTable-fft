import pandas as pd
import re #regular expressions
import sys #to get access to command line args :D
import datetime

def scrape(season):
	"""returns a length 2 tuple.
Index zero is the dataframe that is the lookup table, with indicies being the time in half-hour increments written as an integer that combines the hour and minutes from a 24 hour clock (1234 would refer to 12:34 pm).
Index one contains a datetime object referring to the Saturday after the Friday in the aforementioned dataframe."""
	table_df = pd.read_html("http://www.csueastbay.edu/students/academics-and-studying/finals/"+season+".html")[0]

	#get clean dates from table...
	clean_headers = ['Times']
	for x in table_df.columns[1:]:
		date = re.findall('\w+, \w+ \d+', x)[0]
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
	saturday_after_finals = re.findall("\w+ \d+, \d+",table_df.columns[-1])[0]
	saturday_after_finals = datetime.datetime.strptime(saturday_after_finals, "%B %d, %Y")
	saturday_after_finals += datetime.timedelta(days=1)
	table_df.columns = clean_headers


	#Storing the time ranges of the finals:
	time_list = list(table_df['Times'])
	num_season_time_slots = len(time_list)
	classtimes_to_finalexamhour_dict={}

	list_of_days=['MWF','MW','M','MF','TuTh','Tu','WF','W','Th','FS','F']

	time_increments = []
	for hour in range(600,2300,100):
		time_increments.append(hour)
		time_increments.append(hour+30) #add half hours too

	df = pd.DataFrame(columns=list_of_days, index = time_increments)

	class_to_final_dict = {}
	for col in table_df.columns[1:]: #dates
		for x in range(0,num_season_time_slots):
			class_DTs = table_df.loc[x,col]
			lookup_set = re.findall("\w+ [0-9]+:?[0-9]*-[0-9]+:[0-9]+ [ap]m", class_DTs) #turn the box of time ranges from the CSUEB finals table into a list of strings
			for y in lookup_set: #GETS EACH STR IN THE LIST JUST CREATED OUT OF TABLE ENTRY
				start_end_times = re.findall("[0-9]+:?[0-9]*",y) #start and end time ranges
				days_class_meets = re.findall("\w+",y)[0] #first 1-3 letters
				start_hours_minutes = re.findall("[0-9]+",start_end_times[0]) #length 1 or 2 list of the hour and optional minute of the start of the time range, index 1 is the minutes (if present)
				end_hours_minutes = re.findall("[0-9]+",start_end_times[1]) #as above, but for the end of the time range, and the minutes are always present as far as I can tell
				#turn the start time into an integer number
				start_time =  int(start_hours_minutes[0]) * 100
				if len(start_hours_minutes) > 1:
					start_time += int(start_hours_minutes[1])
				end_time   =  int(  end_hours_minutes[0]) * 100
				if len(end_hours_minutes) > 1: #probably unnecessary if statement...
					end_time   += int(  end_hours_minutes[1])
				#shift am/pm clock into a 24 hour clock:
				# need if statements because noon stays at 1200 hours
				# we're ignoring 12am since there are no classes that start in the range of 12am to 1am
				if y[-2] == 'p':
					if start_time < 1200:
						start_time += 1200
					if end_time < 1200:
						end_time += 1200
				#finally, store these values in a huge lookup table that doesn't suck!
				for hour in range(start_time, end_time,100):
					#col is the date, e.g. Tue, Dec 12th
					#time_list contains the 2 hour time block of the final
					#days_class_meets is e.g. MWF or TuTh
					df.loc[hour,days_class_meets] = col + ', ' + time_list[x]
					if (hour+30) < end_time: #add half-hours too
						if hour % 100 == 30:
							df.loc[hour+70,days_class_meets] = col + ', ' + time_list[x]
						else:
							df.loc[hour+30,days_class_meets] = col + ', ' + time_list[x]
	return (df, saturday_after_finals.date())

def scrape_to_file(a_valid_semester):
	df, date = scrape(a_valid_semester)
	df.to_csv("./lookup_table.csv")
	print('"lookup_table.csv" has been created!')
	print('It will be useful until',date)

def ask_for_scraper_input(valid_semesters):
	for idx, val in enumerate(valid_semesters):
		print(str(idx) + ") " + val)
	index = -1
	while index >= len(valid_semesters) or index < 0:
		index = int(input("Please enter an integer from the list above (0 to "+str(len(valid_semesters)-1)+", inclusive): "))
	scrape_to_file(valid_semesters[index])

if __name__ == "__main__":
	#if they have a winter semester again, we'll need to add that here
	valid_semesters = ["spring", "summer", "fall"]
	if len(sys.argv) > 1:
		semester = sys.argv[1]
		if semester in valid_semesters:
			scrape_to_file(semester)
		else:
			print("The following are valid inputs:")
			print("\n".join(valid_semesters),end="\n\n")
			print(semester + " is invalid.", end="\n\n")
			ask_for_scraper_input(valid_semesters)
	else:
		print("Valid semesters:")
		ask_for_scraper_input(valid_semesters)
