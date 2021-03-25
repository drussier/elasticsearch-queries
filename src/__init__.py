# coding=utf-8
import os
import pwd
import socket
import pathlib

HOST = socket.gethostname()
USER = pwd.getpwuid(os.getuid())[0]

PROJ_DIR = str(pathlib.Path(__file__).parent.parent.absolute())
SRC_DIR = PROJ_DIR + "src"
TEST_DIR = SRC_DIR + "/test"

if __name__ == "__main__":
    print(f"host : {HOST}, user : {USER}, directory : {PROJ_DIR}")
