import schedule
import requests


def test ():
    s = 'compeate'
    print(s)
    
def main():
    schedule.every(4).seconds.do(test)
    
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    main()