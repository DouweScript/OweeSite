#!/usr/bin/env python
""" A script to generate block schematic images of the De Bolk's OWee schedule for the OWee website, along with the HTML for the image map and descriptions."""
# I recomend not forgetting to install this
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import codecs

__author__ = "Matthijs Amesz"
__email__ = "matthijsamesz@hotmail.com"
__copyright__ = "Copyright 2015, D.S.V. Nieuwe Delft"


# ################################################################################
# ############################  START READING HERE      ##############################
# ################################################################################

# These are the variables that you can change the script to your preferences

# Relative locations of the input file and the desired output folder. Change as desired.
# Currently assumes the script resides in <OWeeCom Main Folder>\Website\Schedule_Drawer
# Currently assumes the input resides in  <OWeeCom Main Folder>\Activiteiten
schedule_location = "C:\Users\Connor\Google Drive\Bolk\OWeeCom\OweeCom 2017\OWee Site 2017\Probeersel\input_blokkenschema.txt"
#Vul tussen de aanhalingstekens de map waarin het tekstbestand van het blokkenschema staat in, en eindig met "\input_blokkenschema.txt"
output_folder = "C:\Users\Connor\Google Drive\Bolk\OWeeCom\OweeCom 2017\\Probeersel\OWee Site 2017"  # Make sure to end this string with an escaped backslash
#Hetzelfde als bij schedule_location, maar dan zonder "\input_blokkenschema"
# The width of the images that are created for each day. Image height is calculated based on requirements. Default is 1000.
image_width = 1000


class Drawer:  # Don't touch this, and make sure all variables below have exactly 1 tab in front of them

        # Here you can set the RGB color values for the image. The fill color should be the year's primary color, and the line color your secondary color.
        # This tool was made and first used in 2015. 2014 and 2013's color schemes are noted below for reference. Feel free to play around with different coloring schemes.
        # Please append your year's colors, and leave those of previous years for future generations to look back upon.

	line_col = (0, 0, 0) # 2017:Black with blue
	fill_col = (0, 0, 0)
	text_col = (0, 215, 255) #Changes the color of the text, since for this year, the color was black, and black text would not work.
        

        #fill_col = (254, 80, 0)  # 2016: Orange with black
        #line_col = (0, 0, 0)

        # fill_col = (160, 255, 0)  # 2015: Green with black
        # line_col = (0, 0, 0)

        # fill_col = (87, 0, 117)  # 2014: Purple with blue
        # line_col = (90, 200, 204)

        # fill_col = (0, 180, 255)  # 2013: Blue with white
        # line_col = (255, 255, 255)

        # The fonts used to write the text in the images. These should reside in the same folder as the script.
        font_day = "Montserrat-Bold.ttf"  # Font used for the day heading. Hint: make this a bold font type.
        font_timeline = "Montserrat-Regular.ttf"  # Font used for the timeline.
        font_activity = "Montserrat-Regular.ttf"  # Font used for the activity names inside the rectangles.

        # These values impact the size of various parts, and bu extension the height of each image.
        day_font_size = 32  # Font size for the day heading. Increase or decrease as desired. Default is 32.
        time_font_size = 20  # Font size for the timeline. Large fonts risk overlapping. Default is 20.
        offset = 5  # Offset between all elements, e.g. the whitespace between the image edge and the rectangles, between the rectangles themselves, etc. Default is 5.
        row_height = 20  # Height of each row of rectangles in the image. Note that activities are meant to span 2, 3 or 6 rows. Default is 20.
        max_rows = 6  # Total number of rows for activities. Default is 6, so single activities can span 6 rows, double activities both get 3 and triples get 2 each.

        # Use these values to tweak the appearance of the rounded rectangles
        cur_corner_size = 8  # The inner radius of the circles used to round the rectangles with.
        cur_line_width = 3  # The width of the borders drawn around the rectangles. Line width expands inward, meaning the outside size of a rectangle is constant.

# ################################################################################
# ###########################   STOP READING HERE       ##############################
# ################################################################################

        quarter_width = 5  # initial value, overridden by calculation later.
        handled_activities = []

	def __init__(self, width):
		self.image_width = width
                # Calculate the required height. Day title, timeline, the number of rows, and offsets between each of them
		self.image_height = self.offset*(3+self.max_rows) + self.row_height*self.max_rows + self.time_font_size + self.day_font_size
		self.image = Image.new("RGB", (self.image_width, self.image_height), (255, 255, 255))
		self.draw = ImageDraw.Draw(self.image)

		self.image_map = []
		self.activity_list = []

	def draw_rounded_rectangle(self, x, y, width, height, corner_size=cur_corner_size, line_color=line_col, fill=fill_col, line_width=cur_line_width):
                """Draw a rounded rectangle.

                Draws a rounded rectangle on the image with (x,y) as the top left coordinates.

                :param x: leftmost coordinate
                :param y: top coordinate
                :param width: width of the rectangle including borders
                :param height: height of the rectangle including borders
                :param corner_size: inner radius of the rounded corner (excluding line width)
                :param line_width: width of the border lines in pixels
                :param fill: (R, G, B) tuple for the fill color of the rectangle
                :param line_color: (R, G, B) tuple for the color of the border lines

                :return: void
                """
		right = x + width-1
		bottom = y + height-1

		x1 = x + (line_width-1)/2
		y1 = y + (line_width-1)/2
		x2 = right - line_width/2
		y2 = bottom - line_width/2

		# print "Drawing the corners"
		draw_circle(self.draw, x+line_width+corner_size, y+line_width+corner_size, line_width+corner_size, line_color)
		draw_circle(self.draw, right-line_width-corner_size, y+line_width+corner_size, line_width+corner_size, line_color)
		draw_circle(self.draw, right-line_width-corner_size, bottom-line_width-corner_size, line_width+corner_size, line_color)
		draw_circle(self.draw, x+line_width+corner_size, bottom-line_width-corner_size, line_width+corner_size, line_color)

		draw_circle(self.draw, x+line_width+corner_size, y+line_width+corner_size, corner_size, fill)
		draw_circle(self.draw, right-line_width-corner_size, y+line_width+corner_size, corner_size, fill)
		draw_circle(self.draw, right-line_width-corner_size, bottom-line_width-corner_size, corner_size, fill)
		draw_circle(self.draw, x+line_width+corner_size, bottom-line_width-corner_size, corner_size, fill)

		lines = [
			(x1+corner_size, y1, x2-corner_size, y1),
			(x2, y1+corner_size, x2, y2-corner_size),
			(x1+corner_size, y2, x2-corner_size, y2),
			(x1, y1+corner_size, x1, y2-corner_size)]
		# print "Drawing the lines"
		for line in lines:
			self.draw.line(line, line_color, line_width)

		# print "Drawing fillers"
		filler1 = (x1+corner_size, y1+1+line_width/2, x2-corner_size, y1+corner_size)
		self.draw.rectangle(filler1, fill, fill)
		filler2 = (x1+1+line_width/2, y1+corner_size, x2-1-(line_width-1)/2, y2-corner_size)
		self.draw.rectangle(filler2, fill, fill)
		filler3 = (x1+corner_size, y2-corner_size, x2-corner_size, y2-1-(line_width-1)/2)
		self.draw.rectangle(filler3, fill, fill)

	def draw_schedule_item(self, name, start_time, end_time, row=1, height=1, actual_name ="Name", description="No Description"):
                """Draw a single activity on the canvas

                Draws an activity on the canvas, with the formatted name inside the rounded rectangle.
                The font size is maximized based on the rectangle size and the activity name.
                Also generated HTML for the image map and activity list

                :param name: An array containing each line of the formatted name as entry, or a String if the entire name goes onto a single line.
                :param start_time: Start time of the activity in quarters of an hour since the start of this day's schedule
                :param end_time: End time of the activity in quarters of an hour since the start of this day's schedule
                :param row: Start row for this activity
                :param height: Number of rows this activity spans
                :param actual_name: Unformatted name of the activity for the HTML page
                :param description: Description of the activity for the HTML page
                :return: void
                """

                # Calculate the x, y, width and height of the activity's rectangle
                x = self.offset + start_time*self.quarter_width
                # Offset to the day title, day title hiehght, between day and timeline, timeline hieght, between timeline and first row, and previous row heights and their offsets (if any)
                y = 3*self.offset + self.time_font_size + self.day_font_size + row*(self.row_height + self.offset)
                width = (end_time-start_time)*self.quarter_width-self.offset
                height = height*self.row_height + (height-1)*self.offset

                # Draw the rectangle
		if type(name) is str:
			name = [name]
		print "Drawing activity:", " ".join(name), x, y, width, height
		self.draw_rounded_rectangle(x, y, width, height)

		# Find maximum font size
		text_offset = self.cur_corner_size + self.cur_line_width
		if len(name[0]) == 1: # If the activity name is vertical, the rectangle is very narrow and we need less offset
			text_offset /= 2
		max_height = height - 2*text_offset
		max_width = width - 2*text_offset
		size = 5
		font = None
		dim = (0, 0)
                # increase font size until the text no longer fits inside the rectangle
		while dim[0] < max_width and dim[1] < max_height:
			size += 1
			font = ImageFont.truetype("Montserrat-Regular.ttf", size)
			dim_x = 0
			dim_y = 0
			for text in name:
				text_dim = self.draw.textsize(text, font)
				dim_y += size
				dim_x = max(dim_x, text_dim[0])
			dim = (dim_x, dim_y)

		# Draw Text
		text_y = y+text_offset + (max_height - dim[1])/2.0 - 2
		for i, text in enumerate(name):
			text_dim = self.draw.textsize(text, font)
			self.draw.text((x+text_offset+(max_width - text_dim[0])/2.0, text_y), text, self.text_col, font)  # y+text_offset+(max_height - dim[1])/2.0 + i*text_dim[1]
			text_y += size

		# Create HTML
		anchor_name = "".join(name)
		anchor_name = anchor_name.replace(" ", "")
                # Allow for multiple activities with the same name, like "eettafel"
		if anchor_name in self.handled_activities:
			i = 2
			while anchor_name+str(i) in self.handled_activities:
				i += 1
			anchor_name += str(i)

		self.image_map.append('\t<area shape="rect" coords="%d,%d,%d,%d" href="#%s" alt="%s">' % (x, y, x+width, y+height, anchor_name, actual_name))

		self.activity_list.append(
			"""\t<li class="activiteit" id="%s">
		<a href="javascript:void(0)" class="act-header">
			<img src="img/plus.png" class="collapsed">
			<img src="img/min.png" class="expanded">
			%s
		</a>
		<p class="expanded">
			%s
		</p>
	</li>\n""" % (anchor_name, actual_name, description))
		self.handled_activities.append(anchor_name)

	def make_day_schedule(self, day, schedule):
                """Create the schedule image and HTML for an entire day

                Fills the entire current image with the schedule for the given day, using the activities in the provided dict.
                The schedule param should contain the start and end time of the day in quarters of an hour since midnight in "start" and "end"
                "act" should contain a list of activities. An activity is a list with the following structure:
                [int: start time in quarters, int: end time in quarters, string or list: formatted name, int: row number, int: number of rows spanned,
                        string: unformatted name, string: description of the activity]

                :param day: name of the day
                :param schedule: Dict containing the start and end time of the day's schedule, and a list of all activities
                :return: void
                """
		start = schedule["start"]
		end = schedule["end"]
		day_length = (end-start)

		# Prepare HTML
		self.image_map.append('<map name="map_%s">' % day)
		self.activity_list.append('<h1 id="activiteiten-%s">%s</h1><ul>\n' % (day, day))

		# Draw the day heading
		font = ImageFont.truetype("Montserrat-Bold.ttf", self.day_font_size)
		dim = self.draw.textsize(day, font)
		text_x = (self.image_width-dim[0])/2
		self.draw.text((text_x, self.offset), day, self.line_col, font)
		self.image_map.append('\t<area shape="rect" coords="%d,%d,%d,%d" href="#activiteiten-%s" alt="%s">' % (text_x, self.offset, text_x+dim[0], self.offset+dim[1], day, day))

		self.quarter_width = (self.image_width-self.offset)/float(day_length)

		# Draw the timeline
		font = ImageFont.truetype("Montserrat-Regular.ttf", self.time_font_size)
		for i in range(int(start/4), int(end/4)+1):
			self.draw.text((self.offset + (i-int(start/4))*self.quarter_width*4, 2*self.offset + self.day_font_size), "|" + str(i%24) + ":00", self.line_col, font)

		# Draw activities
		print start, end, self.quarter_width
		for activity in schedule["act"]:
			self.draw_schedule_item(activity[2], activity[0]-start, activity[1]-start, activity[3], activity[4], activity[5], activity[6])

		# End HTML
		self.image_map.append('</map>\n')
		self.activity_list.append('</ul>\n')

	def save_image(self, filename="schedule.png"):
		self.image.save(filename)
		if self.draw is not None:
			del self.draw
		self.draw = None

	def pop_image_map(self):
		image_map = "\n".join(self.image_map)
		self.image_map = []
		return image_map

	def pop_activity_list(self):
		activity_list_str = ""
		for activity in self.activity_list:
			activity_list_str += activity
		self.activity_list = []
		return activity_list_str


def read_schedule(filename):
        """ Read the schedule from the given .csv file

        Opens the given file assuming it is an .csv file containing the schedule in the proper format.
        See external documentation for the appropriate csv format.

        :param filename: path to the .csv file containing the schedule
        :return: Dict containing the schedule per day
        """
        # prepare the schedule dict
        schedule = {"Maandag": {}, "Dinsdag": {}, "Woensdag": {}, "Donderdag": {}}
        for day in schedule:
                schedule[day]["act"] = []
                schedule[day]["start"] = 48*4  # Will be min()ed, so set to highest value (midnight of next day)
                schedule[day]["end"] = 0  # Will be max()ed, so set to lowest value (midnight at start of day)
        working_day = None
        with codecs.open(filename, 'r', 'cp1252') as f:
                for line in f:
                        line = line[:-1]  # remove the \n
                        if line[:line.index("\t")] in schedule:  # If this line is the heading for a new day
                                working_day = line[:line.index("\t")]
                                continue
                        if line[0] == "\t" or line[:5] == "Begin":  # If this line is a blank line or the line with column names
                                continue
                        # first 5 characters are start time followed by a tab
                        start_time = time_to_double(line[0:5])
                        # after that, 5 characters for the end time
                        end_time = time_to_double(line[6:11])
                        # then come the row and the height
                        row = int(line[12])
                        height = int(line[14])
                        # and finally the name with the description
                        tab_id = line[16:].index('\t')
                        name = line[16:16+tab_id].split("#")
                        last_tab = 17 + tab_id
                        tab_id = line[last_tab:].index('\t')
                        actual_name = line[last_tab:last_tab+tab_id]
                        print "name", name
                        descr = line[last_tab+tab_id+1:]
                        schedule[working_day]["act"] += [(start_time, end_time, name, row, height, actual_name, descr)]
                        schedule[working_day]["start"] = min(schedule[working_day]["start"], start_time)
                        schedule[working_day]["end"] = max(schedule[working_day]["end"], end_time)
        # print "Schedule:"
        # for day in schedule:
        #       print day, ":"
        #       print schedule[day]
        return schedule


def draw_circle(draw, x, y, r, color):
	draw.ellipse((x-r, y-r, x+r, y+r), color, color)


def time_to_double(time):
	hour = int(time[0:2])
	if hour < 10:
		hour += 24
	minutes = int(time[3:5])/15
	return 4*hour + minutes


def main():
	week_schedule = read_schedule("input_blokkenschema.txt")
	indent = 2
	image_map_html = ""
	activity_list_html = ""
	expand_all = """\t\t\t<ul style="overflow:hidden;">
				<li class="activiteit">
					<a href="javascript:void(0)" class="act-all">
						<img src="img/plus.png" class="collapsed">
						<img src="img/min.png" class="expanded">
						Alles in/uitklappen
					</a>
					<p class="expanded"></p>
				</li>
			</ul>"""
	days = ["Maandag", "Dinsdag", "Woensdag", "Donderdag"]
	for day in days:
		drawer = Drawer(image_width)
		drawer.make_day_schedule(day, week_schedule[day])
		drawer.save_image("Site\\img\\" + day + ".png")
		drawer.save_image(day + ".png")
		image_map_html += drawer.pop_image_map()
		activity_list_html += drawer.pop_activity_list()

	indent = 3
	# Output HTML Image Map
	image_map_html = "\t"*indent + image_map_html.replace("\n", str("\n"+indent*"\t"))
	image_map_html = "" + (indent-1)*"\t" + '<span id="image_map">\n' + image_map_html + "\n" + (indent-1)*"\t" + "</span>\n"
	with codecs.open("image_map.html", 'w', 'cp1252') as f:
		f.write(image_map_html)
	# Output HTML Activity List
	activity_list_html = "\t"*indent + activity_list_html.replace("\n", str("\n"+indent*"\t"))
	activity_list_html = "" + (indent-1)*"\t" + '<div id="activity_list">\n' + expand_all + '\n' + activity_list_html + "\n" + (indent-1)*"\t" + "</div>\n"
        with codecs.open("activity_list.html", 'w', 'cp1252') as f:
                f.write(activity_list_html)

	print "Finished!"

main()
