import argparse

parser = argparse.ArgumentParser(description='Dies ist die Bescheibung die bei -h kommt')

parser.add_argument('integers',
                    metavar='N',
                    type=int,
                    nargs='+',
                    help='an integer for the accumulator')

parser.add_argument('--sum',
                    dest='accumulate',
                    action='store_const',
                    const=sum,
                    default=max,
                    help='sum the integers (default: find the max)')

parser.add_argument('--end',
                    dest='end',
                    type=str,
                    default='',
                    help='String der zum dene des Progs gezeigt werden soll.')

parser.add_argument('-q',
                    dest='q',
                    action='store_const',
                    const='q',
                    default='',
                    help='Haengt ein Q an den Ausgabestring an.')

args = parser.parse_args()

file = open("testfile.py","w+")

file.write(str(args.accumulate(args.integers)) + '  ' + args.end + args.q)
file.close
