from abstraction_support_functions import *


def main():
    '''
    Desc.   runnable function from the command line
    Used    abstractions.py is executed
    Input   N/A
    Output  N/A
    '''
    parser = argparse.ArgumentParser(
        description='''To transform the logs with the pattern.
                        The --path and --pattern are mandatory.'''
        )

    # definition of --path argument
    parser.add_argument(
        '--path',
        required=True,
        type=argparse.FileType('r'),
        metavar='xes_file_name',
        help='specify the path of xes file. e.g. test.xes'
    )
    # definition of --pattern argument
    parser.add_argument(
        '--pattern',
        type=str,
        required=True,
        metavar='pattern_ID',
        nargs='+',
        help='''Referring to the xes_file_name.pattern,
                specify the sequence of the pattern
                in order which you want to make abstractions with.
                e.g. 1 2 3 1 '''
        )

    # Hideen parameter for pattern file. Not requiring user's input
    parser.add_argument(
        '-filename',
        type=check_if_xes,
        default=parser.parse_args().path.name,
        metavar='filename',
        help=argparse.SUPPRESS
    )

    # getting the arguments by parse_args
    args = parser.parse_args()

    # required arguments for perform_pattern_abstraction
    ext = "_patterns.json"
    logfilename = args.path.name
    file = logfilename.replace(".xes", ext).replace(".XES", ext).replace(".csv", ext).replace(".CSV", ext)
    patterns = args.pattern

    if logfilename.endswith('.xes') or logfilename.endswith('.XES'):
        log = utils.import_log_XES(args.path.name)
    elif logfilename.endswith('.csv') or logfilename.endswith('.CSV'):
        log = utils.import_csv(args.path.name)

    # pattern files in dictionary format
    pattern_dic = read_pattern_file(file)

    # if erorr occur in reading the pattern file
    if not pattern_dic:
        return

    # if the pattern is not matched with the input of user
    if not check_pattern(patterns, pattern_dic):
        return

    # read the activities and timestamps from the given log
    con_traces, con_timestamps = read_log(log)

    # print the original traces / timestamps
    print_traces_stamps(con_traces, con_timestamps, "original traces")

	# The validation for this file is already
    # checked at line 75 with pattern_dic variable that
    # includes IDs in string format
    # To prevent from exceptions, we need to get pattern_dict having same data but IDs in integers.
    # Hence calling with same file doing some type conversion
    pattern_dic = utils.import_pattern_json(file)

    # abstractions are performed
    abs_traces, abs_timestamps = perform_abstractions(
        patterns, pattern_dic, con_traces, con_timestamps
    )

    # print the abstracted traces / timestamps
    print_traces_stamps(abs_traces, abs_timestamps, "abstracted traces")

# When abstraction.py runs, it call main()
if __name__ == '__main__':
    main()
