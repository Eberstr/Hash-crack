#!/usr/bin/env python3

import hashlib
import argparse
import multiprocessing

def get_arguments():
    parser = argparse.ArgumentParser(description="Hash cracker")
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='Ruta del archivo wordlist', required=True)
    parser.add_argument('-H', dest='hash_value', help='Hash to break', required=True)
    parser.add_argument('-a', dest='algorithm', help='Algoritmo de hasheo', required=True)
    parser.add_argument('-t', dest='threads', help='Number of threads to use')

    return parser.parse_args()

# Eliminar esta funcion?????
def count_lines():
    count=0
    with open(wordlist, errors="ignore") as file:
        lines = file.readlines()
        for line in lines:
            lines_number += 1
        return lines_number

def parse_wordlist(wordlist):
    lines_number = count_lines()
	    block = 1000
	    with open(wordlist, block) as file:
		    lines = []
            for line in file:
                lines.append(line)
                if len(lines) == block:
                   yield lines
                   lines = []
                if lines:
                    yield lines
                
def hash_chek(lines, algorithm, hash_value):
    for line in lines:
        h = hashlib.new(hash_value)
        h.update(line.strip().encode("utf8"))
        if h.hexdigest() == hash_value.lower():
            return line
            break
    
    return none

def main():
    args = get_arguments()

    processes = []
    threads = int(args.threads) if args.threads else: multiprocessing.cpu_count()

    for block in parse_wordlist(args.wordlist):
        process = multiprocessing.Process(target=hash_check, block)
        process.start()
        processes.appen(process)

        if len(processes) >= threads:
            for p in processes:
                p.join()
            processes = []

    for p in processes:
        p.join()

if __name__ == '__main__':
    main()
