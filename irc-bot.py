#!/usr/bin/env python

import socket
import urllib2
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
        self.send_data('MODE %s +o %s\r\n' % (self.CONFIG['channel'], self.CONFIG['master']))
    
    
    def is_up(self, site):
        response = urllib2.urlopen('http://www.isup.me/'+site)
        if response.read().find("It's just you."):
            self.send_data("PRIVMSG %s :%s is UP\r\n" % (self.CONFIG['channel'], site))
        else:
            self.send_data("PRIVMSG %s :%s is DOWN\r\n" % (self.CONFIG['channel'], site))
    
    
    def commands(self):
        pass
    
    
    def main(self):
        while True:
            data = self.SERVER.recv(1024)
            check = data.split(':')
            user = check[1].split('!')[0]
            print check
            
            try:
                if check[0].find('PING') != -1:
                    self.pong(check[1])
                elif check[1].find('JOIN') != -1 and user == self.CONFIG['master']:
                    self.op_user()
                elif check[2].find('!isup') != -1:
                    self.is_up(check[2][5:])
            except Exception, e:
                print e
            
            
bot = Bot()