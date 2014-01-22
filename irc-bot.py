#!/usr/bin/env python

import socket
import random

class Bot():
    
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONFIG = {
            'server': 'irc.freenode.net',
            'port': 6667,
            'channel': '#securitygeekguys',
            'nick': '_MastersBot_',
            'ident': random.randrange(1,100),
            'master': 'Xyndei'
    }
    
    
    
    def __init__(self):
        self.SERVER.connect((self.CONFIG['server'], self.CONFIG['port']))
        self.login(self.CONFIG)
        self.main()
    
    def send_data(self, msg):
        self.SERVER.send(msg)
    
    def login(self, config):
        self.send_data('NICK %s\r\n' % config['nick'])
        self.send_data('USER %i 8 * :%s\r\n' % (config['ident'], config['nick']))
        self.send_data('JOIN %s\r\n' % config['channel'])
        
    
    def pong(self, txt):
        self.send_data('PONG :%s' % txt)
        
    def op_user(self):
        self.send_data('/mode %s +o %s\r\n' % (self.CONFIG['channel'], self.CONFIG['master']))
    
    def main(self):
        while True:
            data = self.SERVER.recv(1024)
            tmp = data.split('\n')
            check = data.split(':')
            user = data.split(':')[1].split('!')[0]
            print check
            
            if data.find('PING') != -1:
                self.pong(check[1])
            elif data.find('JOIN') and user == 'Xyndei':
                self.op_user()
    
bot = Bot()