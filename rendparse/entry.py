"""
Functions to parse command-line arguments and run the application.
"""

import os
import sys
import argparse

import parser as rfp

__author__ = "Ryan Tonini"


def parse_arguments(argv, prog=''):
    """
    Routine for parsing command-line arguments

    Input arguments
        - argv:   input command line arguments (as returned by sys.argv[1:])
        - prog:   name of the executable (as returned by sys.argv[0])
    Return values
        - a Namespace() object containing the user-specified arguments and
          any optional arguments that take default values
    """
    # Initialize the command-line parser
    parser = argparse.ArgumentParser(prog,
                                     description='Program for parsing csv files from a render farm.')

    #
    # Main input arguments
    #
    parser.add_argument('path',
                        nargs='?',
                        type=str,
                        help='Path to look for CSV files')
    parser.add_argument('-app', '--app',
                        type=str,
                        help='Application to filter renders on',
                        required=False)
    parser.add_argument('-renderer', '--renderer',
                        type=str,
                        help='Renderer to filter renders on',
                        required=False)
    parser.add_argument('-failed', '--failed',
                        action='store_true',
                        help='Include data from failed renders in the output',
                        required=False)
    #
    # Flags to change output (to be something other than number of renders)
    #
    flag_group = parser.add_mutually_exclusive_group(required=False)
    flag_group.add_argument('-avgtime', '--avgtime',
                            action='store_const',
                            dest='output_type',
                            const='avgtime',
                            help="Output the average render time in seconds")
    flag_group.add_argument('-avgcpu', '--avgcpu',
                            action='store_const',
                            dest='output_type',
                            const='avgcpu',
                            help="Output the average peak cpu")
    flag_group.add_argument('-avgram', '--avgram',
                            action='store_const',
                            dest='output_type',
                            const='avgram',
                            help="Output the average ram usage")
    flag_group.add_argument('-maxram', '--maxram',
                            action='store_const',
                            dest='output_type',
                            const='maxram',
                            help="Output the id for the render with the highest peak RAM")
    flag_group.add_argument('-maxcpu', '--maxcpu',
                            action='store_const',
                            dest='output_type',
                            const='maxcpu',
                            help="Output the id for the render with the highest peak CPU")
    flag_group.add_argument('-summary', '--summary',
                            action='store_const',
                            dest='output_type',
                            const='summary',
                            help="Output all of the above commands")
    parser.set_defaults(output_type='count')

    # Run the python argument-parsing routine, leaving any
    #  unrecognized arguments intact
    args, unprocessed_argv = parser.parse_known_args(argv)

    if args.path:
        # Check if given path is an invalid directory
        if not os.path.isdir(args.path):
            raise argparse.ArgumentTypeError("{0} is not a valid directory".format(args.path))
    else:
        # Set path to current working directory
         args.path = os.getcwd()

    return args


def main(argv, prog=''):
    """
    Top-level routine for CSVParser when running the code from the command line

    Input arguments
        - argv:   list of command-line arguments (as returned by sys.argv[1:])
        - prog:   name of the executable (as returned by sys.argv[0])
    """
    # Parse the command line arguments
    args = parse_arguments(argv, prog)

    # Create parser, run it and print stat
    render_parser = rfp.RenderFarmParser()
    render_parser.run_parser(args.path, args.app, args.renderer, args.failed)
    render_parser.show_stats(args.output_type)


# So we can run the script from the command line
if __name__ == '__main__':
    main(sys.argv[1:], sys.argv[0])




