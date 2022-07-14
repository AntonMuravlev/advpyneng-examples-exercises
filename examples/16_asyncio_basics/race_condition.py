import random
import time
from concurrent.futures import ThreadPoolExecutor


def plus_1():
    global counter

    value = counter
    time.sleep(random.choice([0, 0.5]))
    counter = value + 1


def main():

    with ThreadPoolExecutor(20) as ex:
        futures = [ex.submit(plus_1) for _ in range(20)]
        [f.result() for f in futures]

    print(f"{counter=}")



if __name__ == "__main__":
    for _ in range(5):
        counter = 0
        main()
