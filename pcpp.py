#!/usr/bin/env python

"""
This is a preprocessor for cross-developing camera applications between
Mac OS and the Raspberry Pi.
"""

import argparse, time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# This declaration class holds the start and end line, as well as the platform target.
class Declaration:
    def __init__(self, start, platform):
        self.start = start
        self.end = 0
        self.platform = platform

class Handler(PatternMatchingEventHandler):
    patterns = ["*.py"]

    def process(self, event):
        preprocess(event.src_path)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def main():

    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True, help="source file / directory to preprocess")
    args = vars(ap.parse_args())

    # open source file (read-only)
    input = args["source"]

    observer = Observer()
    observer.schedule(Handler(), input)
    observer.start()

    print "Watching " + input
    print "To terminate, hit CTRL + C"

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


# Preprocesses an input file, and writes the result to an output file
def preprocess(inputPath):
    platform = ""
    index = 0
    currentDeclaration = None
    declarations = []

    inputFile = open(inputPath)

    # Identify preprocessor conditionals and defs
    for line in inputFile:
        if "#define mac" in line:
            # we're compiling for mac.
            platform = "mac"
            print "Recognised target platform: Mac"

        elif "#define pi" in line:
            # we're compiling for the pi.
            platform = "pi"
            print "Recognised target platform: Pi"

        elif "#ifdef mac" in line:
            # mac declaration
            currentDeclaration = Declaration(index, "mac")

        elif "#ifdef pi" in line:
            # pi declaration
            currentDeclaration = Declaration(index, "pi")

        elif "#endif" in line:
            # end of declaration
            currentDeclaration.end = index
            declarations.insert(0,currentDeclaration)
            print "Found conditional. Start line: " + `currentDeclaration.start` + " End line: " + `currentDeclaration.end`

        index = index+1

    if platform is "" and currentDeclaration is None:
        print "No platform declaration or conditionals. Will not preprocess file."
    elif platform is "" and currentDeclaration is not None:
        print "No platform declaration. However, conditionals were found. Will not preprocess file."
    elif platform is not "" and currentDeclaration is None:
        print "File preprocessed."
    else:
        print "Preprocessing file..."
        # create destination file
        outputFile = open(inputPath[:-3] + "-" + platform + ".py", "w")
        inputFile.seek(0, 0)
        lines = inputFile.readlines()

        for declaration in declarations:

            if platform is "mac":
                if declaration.platform is "mac":
                    # remove declarations, but keep code in between.
                    del lines[declaration.start]
                    del lines[declaration.end-1]

                elif declaration.platform is "pi":
                    # throw away declarations and code in between.
                    del lines[declaration.start:declaration.end+1]

            elif platform is "pi":
                if declaration.platform is "pi":
                    # remove declarations, but keep code in between.
                    del lines[declaration.start]
                    del lines[declaration.end-1]

                elif declaration.platform is "mac":
                    # throw away declarations and code in between.
                    del lines[declaration.start:declaration.end+1]

        for line in lines:
            outputFile.write(line)

        outputFile.close()
        inputFile.close()

if __name__ == '__main__':
    main()