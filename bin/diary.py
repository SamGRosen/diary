#!/user/bin/env python

import sys, os, sqlite3

# Main function - passes commands into their own functions
def diary(args=sys.argv):
    if '-h' in args or '--help' in args:
        diary_help()
    elif 'generate' in args:
        generate(args)
    else:
        print("Diary couldn't parse that command.")
        diary_help()

# Help command
def diary_help():
    output = """
Usage:
  diary <command> [options]

Commands:
  generate sqlite [path]      Generates sqlite3 database for diary.py at path. Default path is log.sqlite3.

General Options:
  -h, --help                  Show help.
    """
    print(output)

# Generate command
def generate(args):
    # Make sure there was a subcommand passed
    if not args.index('generate') + 1 >= len(args):
        if args[args.index('generate') + 1] == 'sqlite':
            generate_sqlite(args)
        else:
            print('The only database currently supported for diary is sqlite3.')
            diary_help()
    else:
        print('You must pass a subcommand to the generate command.')
        diary_help()

# Generate subcommand for sqlite database
def generate_sqlite(args):
    if not args.index('sqlite') + 1 >= len(args):
        path = args[args.index('sqlite') + 1]
    else:
        path = 'log.sqlite3'
    cwd = os.getcwd()
    connection = sqlite3.connect(os.path.join(cwd, path))
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs
    (inputDT TIMESTAMP, level TEXT, log TEXT)
    ''')
    print('sqlite3 database generated at %s' % os.path.join(cwd, path))

if __name__ == '__main__':
    diary()
