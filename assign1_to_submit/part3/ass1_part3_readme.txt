Assignment 1

Part 3-1

Files: 			assign1-3_1.py
Image file:		image.data
python assign1-3_2_1.py image.data 

The program applies the perception algorithm upon the table from assignment1 part 3.1.
Simple call:
                           python assign1-3_1.py image.data

The data -  image.data set. Number of iterations is 20 by default. Number of features is 50 by default. Learning rate is = 0.1 by default
Weights initially set as 0s lists by default. It is not printing_images by default.Not printing rates or weights by default.

 To change the paramenters use the following command python. Order of parameters should be the same.
 ____________________________________________________________________________________________________________________________________________________
 python assign1-3_2_1.py image.data <your number of iterations> <your number of features><your learning rate> f/anything else p/enything else wout/rout
 ______________________________________________________________________________________________________________________________________________________

                Examples:
                        python assign1-3_1.py image.data 10 60 0.01 f p rout
			python assign1-3_1.py image.data 15 50 0.1 t f wout
			python assign1-3_1.py image.data 30 50 0.1 f p
			python assign1-3_1.py image.data 30 40


Part 3-2

Files:
Script:			assign1-3_2.py
Main data:		ass1_3_2.data
Additional data:	iris_test.txt

The python program uses perception algorythm, compares perception value with real class ,uses learning algorythm to change.
Call it like "python assign1-3_2.py ass1_3_2.data"
The iteration number is 20 by default. Bios =1. Learning rate =0.1 If no "f" in the end of the command initial weights will be given as list of 0s.
To modify parameters use this command:
	python assign1-3_2.py assign1_3_2.data <your number of iterations> <your learning rate> <your bios> f
Example:
	python assign1-3_2.py ass1_3_2.data 3 0.01 -0.5 f

The program outputs the number of correct guesses and weights after each iteration.

Main data is taken from table in assignment 1 part 3

   InstanceN  Feature1  Feature2  Feature3  Class
0          1         0         0         1      0
1          2         0         1         0      1
2          3         1         0         1      1
3          4         1         1         0      0
4          5         1         1         1      0
5          6         1         0         0      1
6          7         0         1         1      1
7          8         0         0         0      0
Additional data - modified iris set.