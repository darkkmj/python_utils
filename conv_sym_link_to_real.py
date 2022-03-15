import os
import sys
import shutil

'''
This class finds symbolic link files in target_folder recursively.
And it changes symbolic link file to real file using os.replace
'''
class conv_sym_link_to_real:
    def __init__(self, target_folder):
        self.target_folder = target_folder
        self.sym_file_list = []

    def find_sym_link(self):
        for root, dirs, files in os.walk(self.target_folder):
            for file in files:
                f = root + "/" + file
                if (os.path.islink(f)) and (os.path.exists(f)) and ("xenomai" in os.readlink(f)):
                    print("sym file: {0}\t-> {1}".format(os.path.abspath(f), os.readlink(f)))
                    self.sym_file_list.append(f)
    
    def replace_sym_link_to_real(self):
        count = 0
        for f in self.sym_file_list:
            src = os.readlink(f)
            dst = os.path.abspath(f)
            os.unlink(f)
            try:
                count += 1
                shutil.copyfile(src, dst)
            except PermissionError:
                print("Operation is not permitted")
            except OSError as error:
                print(error.strerror)
        print("Complete to change symbolic link: {0}".format(count))

if __name__ == "__main__":
    argument = sys.argv
    del argument[0]     # first argument is a name of script
    conv_sym = conv_sym_link_to_real(argument[0])
    conv_sym.find_sym_link()
    flag = input("Start to change symbolic link(y or n):")
    if flag == "y" or flag == 'Y':
        conv_sym.replace_sym_link_to_real()
