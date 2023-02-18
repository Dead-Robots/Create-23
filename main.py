#!/usr/local/bin/python3.10 -u
from createserial.connection import CreateConnection
from kipr import *
from createserial.commands import open_create, close_create, reset_create, create_dd
from createserial.serial import open_serial, close_serial

from createserial.shutdown import shutdown_create_in


def init():
    print("resetting create...")
    open_serial()  # Open a serial port connection to the Create
    reset_create()
    print("initializing...")
    open_create()  # Initialize the Create
    # shutdown_create_in(119)


def shutdown():
    close_create()
    close_serial()


def main():
    gotToFirstBlock()
    gotToAnalysisLab1()
    gotToSecondBlock()
    gotToAnalysisLab2()
    gotTothirdblock()
    gotToAnalysisLab3()
    gotTofourthblock()

def drive(lm, rm, time):
    create_dd(-5*lm, -5*rm)
    msleep(time)
    create_dd(0, 0)

def gotToFirstBlock():
    print('firstblock')
    #turning
    drive(0, 20, 400)
    drive(80, 80, 3000)
    msleep(2000)

def gotToAnalysisLab1():
    print('analysislab1')
    #backing up
    drive(-20, -20, 1000)
    #turning
    drive(-40, 40, 1500)
    #going straight
    drive(40, 40, 2000)
    msleep(2000)

def gotToSecondBlock():
    print('secondblock')
    #backup
    drive(-40, -40, 500)
    #turning
    drive(30, -30, 790)
    create_dd(-200, -200)
    msleep(850)
    #turning
    drive(80, 0, 950)
    drive(40, 40, 1500)
    msleep(2000)

def gotToAnalysisLab2():
    print('analysislab2')
    #backingup
    drive(-40, -40, 500)
    #turning
    drive(50, -50, 1500)
    #going straight
    drive(40, 40, 1500)
    msleep(2000)

def gotTothirdblock():
    print('thirdblock')
    #backup
    drive(-40, -40, 500)
    #turning
    drive(50, -50, 780)
    #drivestraight
    drive(70, 70, 2200)
    #turning again
    drive(50, 0, 1300)
    #go straight again
    drive(40, 40, 2000)
    msleep(5000)

def gotToAnalysisLab3():
    print("analysislab3")
    #backing up
    drive(-40, -40, 1000)
    #turning
    drive(40, -40, 1000)
    #go straight
    drive(60, 60, 2500)
    #turn again
    drive(40, -40, 600)
    #go straight
    drive(40, 40, 900)
    msleep(2000)

def gotTofourthblock():
    #backup
    drive(-40, -40, 500)


if __name__ == '__main__':
    with CreateConnection():
        main()
