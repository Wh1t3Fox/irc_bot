#!/usr/bin/env python

import socket
import urllib2
import random
import threading

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
    COLORS = {
            'white': '\x030',
            'black': '\x031',
            'navy': '\x032',
            'green': '\x033',
            'red': '\x034',
            'maroon': '\x035',
            'purple': '\x036',
            'olive': '\x037',
            'yellow': '\x038',
            'lime': '\x039',
            'teal': '\x0310',
            'cyan': '\x0311',
            'blue': '\x0312',
            'pink': '\x0313',
            'grey': '\x0314',
            'silver': '\x0315'
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
    
        
    def op_user(self, user):
        self.send_data('MODE %s +o %s\r\n' % (self.CONFIG['channel'], user))
    
    
    def deop_user(self, user):
        self.send_data('MODE %s -o %s\r\n' % (self.CONFIG['channel'], user))
    
    
    def is_up(self, site):
        response = urllib2.urlopen('http://www.isup.me/'+site)
        if response.read().find("It's just you.") != -1:
            self.send_data("PRIVMSG %s :\x0312[+]%s IS UP\r\n" % (self.CONFIG['channel'], site))
        else:
            self.send_data("PRIVMSG %s :\x034[+]%s IS DOWN\r\n" % (self.CONFIG['channel'], site))
        response.close()
    
    
    def auto_message(self):
        threading.Timer(300, self.auto_message).start()
        self.send_data("PRIVMSG %s :\x039[+]Type !commands to view the options\r\n" % self.CONFIG['channel'])
    
    
    def commands(self):
        self.send_data("PRIVMSG %s :\x037[+]All commands start with '!'\r\n" % self.CONFIG['channel'])
        self.send_data("PRIVMSG %s :\x037[+]isup to view a website status\r\n" % self.CONFIG['channel'])
    
    
    def main(self):
        self.auto_message()
        while True:
            try:
                data = self.SERVER.recv(1024)
                check = data.split(':')
                user = check[1].split('!')[0]
                print check
            
            
                if check[0].find('PING') != -1:
                    self.pong(check[1])
                elif check[1].find('JOIN') != -1 and user == self.CONFIG['master']:
                    self.op_user(self.CONFIG['master'])
                elif check[2].find('!isup') != -1:
                    self.is_up(check[2][6:-2])
                elif check[2].find('!commands') != -1:
                    self.commands()
            except Exception, e:
                print e
            
            
bot = Bot()