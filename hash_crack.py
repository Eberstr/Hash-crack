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

def parse_wordlist(wordlist):
    block = 1000
    with open(wordlist, mode="r", encoding="utf-8") as file:
        lines = []
        for line in file:
            lines.append(line)
            if len(lines) == block:
                yield lines
                lines = []
        if lines:
            yield lines
                
def hash_check(lines, algorithm, hash_value, queue):
    for line in lines:
        h = hashlib.new(algorithm)
        h.update(line.strip().encode("utf8"))
        if h.hexdigest() == hash_value.lower():
            queue.put(line.strip())
            break
        else:
            queue.put("Debug desde check")

def main():
    args = get_arguments()

    processes = []
    threads = int(args.threads) if args.threads else multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    
    for block in parse_wordlist(args.wordlist):
        
        process = multiprocessing.Process(target=hash_check, args=(block, args.algorithm, args.hash_value,queue))
        process.start()
        processes.append(process)

        if len(processes) >= threads:
            for p in processes:
                p.close()
                p.join()
            processes = []
              
        if not queue.empty():
            found = queue.get()
            print(f"Valor: {found}")
            break
        else:
            print("Debug ")

    for p in processes:
        p.terminate()
        p.join()

if __name__ == '__main__':
    main()
