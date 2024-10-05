#!/usr/bin/env python3

import hashlib
import argparse

def get_arguments():
    parser = argparse.ArgumentParser(description="Hash cracker")
    parser.add_argument('-w', '--wordlist', dest='wordlist', help='Ruta del archivo wordlist', required=True)
    parser.add_argument('--hash', dest='hash', help='Hash to break', required=True)
    parser.add_argument('-a', dest='algorithm', help='Algoritmo de hasheo', required=True)
    parser.add_argument('-t', dest='threads', help='Number of threads to use')

    return parser.parse_args()

def count_lines():
    count=0
    with open(wordlist, errors="ignore") as file:
        lines = file.readlines()
        for line in lines:
            count += 1
        return count

def parse_wordlist():
    lines = count_lines()
    files = []
    if lines >= 1000:
        for i in range(1, lines+1):
            with open(f'file_{1}.txt', 'x') as f:
                


def hash_chek(wordlist, algorithm, hash):
    with open(wordlist) as wl:
        for word in wl:
            h = hashlib.new(algorithm)
            h.update(word.strip().encode('utf-8'))
            if h.hexdigest() == hash.lower():
                break
    return word

def main():
    args = get_arguments()

    password = hash_chek(args.wordlist, args.algorithm, args.hash)
    print(password)

if __name__ == '__main__':
    main()
