import os
import sys
import argparse

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from grammar import Grammar

def GenerateNewSample(http_grammar):
    """Generates a new HTTP request sample using the provided grammar"""
    return http_grammar.generate_symbol('http_fuzz')

def generate_samples(grammar_dir, outfiles):
    """Generates HTTP request samples using the grammar and writes them to files"""
    http_grammar = Grammar()
    err = http_grammar.parse_from_file(os.path.join(grammar_dir, 'http.txt'))
    if err > 0:
        print('There were errors parsing grammar')
        return
    
    for outfile in outfiles:
        result = GenerateNewSample(http_grammar)

        if result is not None:
            print('Writing a sample to ' + outfile)
            try:
                with open(outfile, 'w') as f:
                    f.write(result)
            except IOError:
                print('Error writing to output')

def main():
    """Main function - parses args and generates samples"""
    parser = argparse.ArgumentParser(description='Generate HTTP request samples')
    parser.add_argument(
        '--grammar_dir',
        default=os.path.dirname(__file__),
        help='Directory containing grammar files'
    )
    parser.add_argument(
        '--output_dir',
        default=os.path.join(os.path.dirname(__file__), 'output'),
        help='Directory to write samples to'
    )
    parser.add_argument(
        '--no_of_files',
        type=int,
        default=1,
        help='Number of files to generate'
    )
    
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Generate output file paths
    outfiles = []
    for i in range(args.no_of_files):
        outfiles.append(os.path.join(args.output_dir, 'fuzz-{}.txt'.format(i)))

    generate_samples(args.grammar_dir, outfiles)

if __name__ == '__main__':
    main()