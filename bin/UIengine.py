# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 23:01:04 2020

@author: user
"""

from flask import Flask, render_template

App_engine=Flask(__name__)

@App_engine.route('/')


def UIhomepage():
    home='FlaskHome.html'
    return render_template(home)



if __name__ =="__main__":
    App_engine.run(host='127.0.0.1',port=8342)