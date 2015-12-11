"""
This is a preprocessor for cross-developing camera applications between
Mac OS and the Raspberry Pi.
"""

import argparse

# This declaration class holds the start and end line, as well as the platform target.
class Declaration:
    def __init__(self, start, platform):
        self.start = start
        self.end = 0
        self.platform = platform

def main():
    # variables
    platform = ""
    index = 0
    declarationIterator = 0
    currentDeclaration = None
    declarations = []

    # parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--source", required=True, help="source file to preprocess")
    ap.add_argument("-d", "--dest", required=True, help="destination for the result")
    args = vars(ap.parse_args())

    # open source file (read-only)
    inputFile = open(args["source"])

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
            print "Found Mac declaration"

        elif "#ifdef pi" in line:
            # pi declaration
            currentDeclaration = Declaration(index, "pi")
            print "Found Pi declaration"

        elif "#endif" in line:
            # end of declaration
            currentDeclaration.end = index
            declarations.insert(0,currentDeclaration)
            print "Declaration closed. Start line: " + `currentDeclaration.start` + " End line: " + `currentDeclaration.end`

        index = index+1

    # create destination file
    outputFile = open(args["dest"], "w")
    inputFile.seek(0, 0)
    lines = inputFile.readlines()
    print lines
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

    print lines

    for line in lines:
        outputFile.write(line)

    outputFile.close()
    inputFile.close()

if __name__ == '__main__':
    main()