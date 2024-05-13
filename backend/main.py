from websocket import init_server
from asyncio import run

def main():
    run(init_server())

if __name__=="__main__": 
    main() 