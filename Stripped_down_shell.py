#importing the libraries to be used
import os
import sys
import signal
from multiprocessing import Process
import subprocess
from subprocess import check_output


#***************************************************************************
#**********************GENERAL PURPOSE FUNCTIONS****************************
#***************************************************************************

#function to handle command line input from user
def get_cmd():
	cmd = input("\nInput your command in the following format: CMD ARG ARG ARG ....., all arguments should be seperated with a space: \n\n")
	cmd_args = cmd.split()
	return cmd_args

#function to execute the function related to input command
def exec_cmd(cmd_args):
	func = switcher.get(cmd_args[0], "Invalid command") #finding the function corresponding to the command
	func(cmd_args) #executing the function


#***************************************************************************
#**********************FUNCTIONS TO HANDLE COMMANDS*************************
#***************************************************************************
	
#Function to handle dir command. dir is the windows equivalent of ls in Unix
def dir_info(cmd_args):
	print(check_output("dir", shell=True))

#Function to handle make directory command
def make_dir(cmd_args):
	arg = "mkdir " + cmd_args[1]
	print(check_output(arg, shell=True))

#Function to handle remove directory command
def remove_dir(cmd_args):
	arg = "rmdir " + cmd_args[1]
	print(check_output(arg, shell=True))

#Function to handle change directory command
def chg_dir(cmd_args):
	try:
		os.chdir(os.path.abspath(cmd_args[1]))
		print("Directory has been changed to: ", os.getcwd())
	except Exception:
		print("cd: no such file or directory: {}".format(cmd_args[1]))

#simple function to demonstrate opening and closing of a text file
def open_file(cmd_args):
	f = open('test.txt')
	print(f.readlines())
	f.close()

#***************************************************************************
#****************************THE MAIN FUNCTION******************************
#***************************************************************************

def main():
	while True:
		cmd_args = get_cmd() #calling get_cmd() to get user input command from terminal

		#handling the exit command
		if cmd_args[0] == 'exit':
			sys.exit("Thank you for using the stripped down shell simulation!!!!!")

		#code to execute the command with pipes
		command = cmd_args
		if "|" in command:
    		# save for restoring later on
			s_in, s_out = (0, 0)
			s_in = os.dup(0)
			s_out = os.dup(1)

    		# first command takes commandut from stdin
			fdin = os.dup(s_in)

    		# iterate over all the commands that are piped
			for cmd in command.split("|"):
        		# fdin will be stdin if it's the first iteration
        		# and the readable end of the pipe if not.
				os.dup2(fdin, 0)
				os.close(fdin)

        		# restore stdout if this is the last command
				if cmd == command.split("|")[-1]:
					fdout = os.dup(s_out)
				else:
					fdin, fdout = os.pipe()

        		# redirect stdout to pipe
				os.dup2(fdout, 1)
				os.close(fdout)

				try:
					subprocess.run(cmd.strip().split())
				except Exception:
					print("psh: command not found: {}".format(cmd.strip()))

        	# restore stdout and stdin
			os.dup2(s_in, 0)
			os.dup2(s_out, 1)
			os.close(s_in)
			os.close(s_out)
		else:
			#checking command for being invalid based to below 2 conditions
			#1. If the command is not defined in this program
			#2. If the syntax of the command is not correct
			if_err = switcher.get(cmd_args[0], "Invalid command")
			if if_err == 'Invalid command':
				print("This command is not recognized as an internal or external command,operable program or batch file.!!!!!")
				continue

			true_args = switcher1.get(cmd_args[0], "Invalid command")
			cmd_args_len = len(cmd_args)
			if true_args != cmd_args_len:
				print("You have entered invalid command. Please check your command and start the shell again!!!!!")
				continue


			#creating a child process to execute the command
			proc = Process(target=exec_cmd, args=(cmd_args,)) 
			proc.start()
			print(proc)
			proc.join()
			print(proc)

#***************************************************************************
#*******************************SWITCHERS***********************************
#***************************************************************************

#switcher to choose function to execute
switcher = {
        'dir' : dir_info,
        'mkdir' : make_dir,
        'rmdir' : remove_dir,
        'cd' : chg_dir,
        'fopen' : open_file
    }

#switcher to find what are the correct number of command line args for a particular command
switcher1 = {
        'dir' : 1,
        'mkdir' : 2,
        'rmdir' : 2,
        'cd' : 2,
        'fopen' : 3
    }
		
#***************************************************************************
#****************************DRIVER CODE************************************
#***************************************************************************

if __name__ == '__main__':
	main()  # calling main function
	