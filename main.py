import cv2
import numpy as np
from PIL import Image
import pyautogui
import os
import mss
import discord
from discord.ext import commands, tasks
import asyncio
import pygetwindow as gw
import psutil as ps
import requests
from selenium import webdriver
import time

client = commands.Bot(command_prefix=">", intents=discord.Intents.all())

def check_live():
    channelName = 'vedal987'
    contents = requests.get('https://www.twitch.tv/' +channelName).content.decode('utf-8')
    if 'isLiveBroadcast' in contents:
        return True
    else:
        print(requests.get('https://www.twitch.tv/' +channelName))
        return False

isLoopActive = False
@client.event
async def on_ready():
    print('Hello World!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
    await daloop.start()
def check_roles(ctx):
    role = discord.utils.get(ctx.guild.roles, id=574931772781887488)
    if role in ctx.author.roles:
        return True
    else:
        role = discord.utils.get(ctx.guild.roles, id=574720716025626654)
        if role in ctx.author.roles:
            return True
        else: 
            role = discord.utils.get(ctx.guild.roles, id=574724513376370691)
            if role in ctx.author.roles:
                return True
            else:
                if ctx.author.id == 452436342841016341:
                    return True
                else: 
                    return False
@client.command()
async def start(ctx):
    if check_roles(ctx):
        global isLoopActive, stop
        if isLoopActive:
            await ctx.reply('Im already capturing neuro quotes!')
        elif isLoopActive  == False and check_live():
            await ctx.reply('Now capturing neuro quotes.')
            function = 'nl'
            isLoopActive = True
        elif isLoopActive == False and check_live() == False:
            await ctx.reply('Cannot start capturing if there isnt any livestream going on.')
@client.command()
async def stop(ctx):
    if check_roles(ctx):
        global isLoopActive, stop
        if isLoopActive == False:
            await ctx.reply('Im not capturing any neuro quotes yet!')
        elif isLoopActive and check_live():
            await ctx.reply('No longer capturing neuro quotes.')
            stop = True
            isLoopActive = False
        elif isLoopActive and check_live() == False:
            await ctx.reply('Cannot stop capturing if there isnt any livestream going on. Also, this error shouldnt exist as if there is no livestream, it automaticly stops capturing <@!452436342841016341>')
@client.command()
async def collab(ctx):
    global function
    if check_roles(ctx):
        if function == 'cl':
            await ctx.reply('Already on collab template.')
        else:
            function = 'cl'
            await ctx.reply('Setting to collab template.')
@client.command()
async def normal(ctx):
    global function
    if check_roles(ctx):
        if function == 'nl':
            await ctx.reply('Already on normal template.')
        else:
            function = 'nl'
            await ctx.reply('Setting to normal template.')


def mse(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse


for file in os.listdir(r'C:\Users\TC\Desktop\NeuroClipper'): 
        if file.startswith('result'):
            os.remove(r'C:\Users\TC\Desktop\NeuroClipper\\' + file )

def preprocessing(image):
    image = cv2.imread(image)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 0])
    mask = cv2.inRange(hsv, lower, upper)
    result = 255 - mask
    cv2.imwrite('output.png', result)
    image = cv2.imread('output.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    return image

collab_template = cv2.imread('collab_template.png')
collab_template = cv2.cvtColor(collab_template, cv2.COLOR_BGR2GRAY)  
async def collab_loop():
    channel = client.get_channel(1067638175478071307)
    global counter, array, recentImage
    pyautogui.screenshot('input.png', (950, 940, 450, 80))
    output = preprocessing('input.png')
    rating = mse(collab_template, output)
    if rating == 0:
        x = 1
        for input in array:
            image = input
            mss.tools.to_png(input.rgb, input.size, level=9, output='checking.png')
            image = Image.open('checking.png')
            image = image.crop((950, 940, 1400, 1020))
            image.save('checking.png')
            image = preprocessing('checking.png')
            rating = mse(image, collab_template)
            if recentImage == False:
                if rating == 0:
                    mss.tools.to_png(input.rgb, input.size, level=9, output='result_' + str(counter) + '.png')
                    file = discord.File('result_' + str(counter) + '.png')
                    print('Got a result. Saving and sending to discord...')
                    await channel.send(file=file)
                    recentImage = True
                    counter = counter + 1
                    array = []
                    break
                elif x == len(array):
                    print('Could not find an image!')
            x = x + 1
    else:
        with mss.mss() as sct:
            mon = sct.monitors[1]
            mon = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"], "mon": 1}
            placeholder = sct.grab(monitor=mon)
            array.append(placeholder)
        recentImage = False
    if len(array) >= 15:
        array = []

normal_template = cv2.imread('normal_template.png')
normal_template = cv2.cvtColor(normal_template, cv2.COLOR_BGR2GRAY)     
async def normal_loop():
    channel = client.get_channel(1067638175478071307)
    global counter, array, recentImage
    image = pyautogui.screenshot('input.png', (790, 900, 350, 100))
    input = preprocessing('input.png')
    rating = mse(normal_template, input)
    if rating == 0:
        x = 1
        for input in array:
            image = input
            mss.tools.to_png(input.rgb, input.size, level=9, output='checking.png')
            image = Image.open('checking.png')
            image = image.crop((790, 900, 1140, 1000))
            image.save('checking.png')
            image = preprocessing('checking.png')
            rating = mse(image, normal_template)
            print(rating)
            if recentImage == False:
                if rating == 0:
                    mss.tools.to_png(input.rgb, input.size, level=9, output='result_' + str(counter) + '.png')
                    file = discord.File('result_' + str(counter) + '.png')
                    print('Got a result. Saving and sending to discord...')
                    await channel.send(file=file)
                    recentImage = True
                    counter = counter + 1
                    array = []
                    break
                elif x == len(array):
                    print('Could not find an image!')
            x = x + 1
    elif rating > 0:
        with mss.mss() as sct:
            mon = sct.monitors[1]
            mon = {"top": mon["top"], "left": mon["left"], "width": mon["width"], "height": mon["height"], "mon": 1}
            placeholder = sct.grab(monitor=mon)
            array.append(placeholder)
        recentImage = False
    if len(array) >= 15:
        array = []

function = 'nl'
counter = 0
array = []
stop = False
recentImage = False
isLoopActive = False
@tasks.loop(seconds=0.1)
async def daloop():
    global isLoopActive, browser, stop
    channel = client.get_channel(1059569601144442911)
    if check_live() and isLoopActive == False and stop == False:
        general = client.get_channel(1059569601144442911)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="neuro-sama"))
        isLoopActive = True
        await general.send('Neuro is live! <#1059569601144442911>')
        browser = webdriver.Firefox()
        browser.get('https://www.twitch.tv/vedal987')
        browser.fullscreen_window()
        time.sleep(5)
        pyautogui.press('f')
        pyautogui.press('r')
        pyautogui.press('s')
        pyautogui.click(1862, 1054)
        time.sleep(0.2)
        pyautogui.click(1716, 833)
        time.sleep(0.2)
        pyautogui.click(1599, 888)
        time.sleep(0.2)
        pyautogui.click(918, 800)
        pyautogui.press('b')
    elif check_live() == False and isLoopActive == True:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="out for neuro-sama's livestream"))
        browser.quit()
        await general.send('Neuro is no longer live :(')
        stop = False
        isLoopActive = False
    if isLoopActive:
        if function == 'nl':
            await normal_loop()
        elif function == 'cl':
            await collab_loob()
      

client.run("Your code format irritates me!")
