# Dependencies

The only dependency for this program is the python programming langauage

# Directions

To use this program, simply download main.py and protocolNums.py and place them in the directory with the desired log file and lookup csv.  Then run:

`python main.py [lookup file] [log file]`

The output will be written to a file called output.csv in the same directory

# Assumptions

1. All logs will be in the format defined [here](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html), with the destination port in the 7th spot and the protocol number in the 8th spot
2. All logs will be valid and contain the same number of entries
3. No deprecated protocol numbers will be logged, neither will unassigned protocols or protocols used for testing like 253/254
4. All protocol port lookup combos will be valid and well defined, although some error handling is still implemented for this
5. The lookup file will not exceed 10,000 mappings, therefore it can fit in a python dictionary without any issues
   
# Notes

1. My main focus when writing this was to have reusable code, hence the handling of each step in a seperate function
2. I used minimal comments because I find them unnecessary, especially in a simple program like this.  If company style prefferred more comments, such as comments explaining each function at an abstract level, I would be happy to implement this, but currently the low number of comments is intentional.
