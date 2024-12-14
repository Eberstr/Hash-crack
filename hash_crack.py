#!/usr/bin/env python3

'''
TODO: Investigar sobre el uso de Queue o reemplazarlo por flags de true y false:

'''

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

def parse_wordlist(wordlist, block_size=1000):
    with open(wordlist, mode="r", encoding="utf-8") as file:
        lines = []
        for line in file:
            lines.append(line)
            if len(lines) == block_size:
                yield lines
                lines = []
        if lines:
            yield lines

def hash_check(lines, algorithm, hash_value, queue):
    for line in lines:
        h = hashlib.new(algorithm)
        h.update(line.strip().encode("utf8"))
        print(h.hexdigest())
        if h.hexdigest() == hash_value.lower():
            queue.put(line)
            return
        queue.put(None)

def main():
    args = get_arguments()

    processes = []
    threads = int(args.threads) if args.threads else multiprocessing.cpu_count()
    queue = multiprocessing.Queue()
    #hash_found = False

    for block in parse_wordlist(args.wordlist):
        print(block)
        process = multiprocessing.Process(target=hash_check, args=(block, args.algorithm, args.hash_value, queue))
        process.start()
        processes.append(process)

        if len(processes) >= threads:
            for p in processes:
                p.join()
            processes = []
            
        value = queue.get() # Si no esta esta linea el script falla
        while not queue.empty():
            result = queue.get()
            print(result)
            if result:
                print(f"Valor: {result}")

                for p in processes:
                    p.terminate()
                return

        for p in processes:
            p.join()
        
    #if not hash_found:
        print("No se encontro el hash en el diccionario")

if __name__ == '__main__':
    main()
