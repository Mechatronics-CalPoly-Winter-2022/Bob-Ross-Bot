"""!
@file mainpage.py
@brief This file contains the mainpage for the project.

@author Kyle Jennings, Zarek Lazowski, William Dorosk
@date 2022-Feb-22
"""

##
# @mainpage
# @section description_main Bob Ross Bot
# This project modulates a robotic plotter that draws images
# 
# @section software_design Software Design
# The general design of our project is as follows:
# - The user selects a picture using the desktop interface
# - Some filters are run on the image to make it black and white
# - This black and white image is used to generate some plot paths
# - The plot paths are then sent to the Nucleo board
# - The Nucleo board draws the plot paths
# 
# @subsection software_design_sub_1 Desktop Interface
# The desktop interface is a CLI that allows the user to select a picture,
# Then it runs a sobel filter on the image, and then it inverts the image.
# This turns the image into a black and white image that is mainly lines.
# The desktop interface will then display the image before sending it to the
# Nucleo board.
# This example below is what it should look like when filtering the image. The
# result will be different when we implement it but it should look similar.
# \image html python_edge.jpg
# 
# @subsection software_design_sub_2 Task 1
# The first task controls the theta axis motor. This task will try to move the
# theta of the plotter to the desired angle.
#
# 
# @subsection software_design_sub_3 Task 2
# The second task controls the r axis motor. This task will try to move the
# radius of the plotter to the desired radius.
#
# For the two motors the FSM will be as follows:
# \image html motor_fsm.png
# 
# @subsection software_design_sub_4 Task 3
# The third task controls the z axis solenoid. This will move the pen up or down
# depending on whether it should be drawing or just moving.
# 
# @subsection software_design_sub_5 Limit Switches
# The limit switches are used to determine when the plotter has reached the
# end of the plot in either the theta or r axis.
# This should only be useful in calibration mode because the image will be
# inside the plotters range of motion. If the switch is pressed during operation
# it should skip the current point and move on to the next point.
# 
# @author Kyle Jennings, Zarek Lazowski, William Dorosk
# @date February 22, 2022


def main():
    ...


if __name__ == "__main__":
    main()