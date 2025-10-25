# 修改字幕时间,SRT格式
import os
import datetime

lag = 75600 # 时间差,毫秒
zmfile = r'F:\Serial\House.of.Cards.2013.S01.1080p.BDRemux.Rus.Eng.HDCLUB\HOUSE_OF_CARDS_S01E13_BDREMUX_HDCLUB\BDMV\STREAM\00000.srt'

(filePath, ext) = os.path.splitext(zmfile)
debugFile = filePath + '_debug'+ext

text = ''


def getRightTime(xtime, lag):
    theTime = datetime.datetime.strptime(xtime, "%H:%M:%S,%f")
    return (theTime + datetime.timedelta(milliseconds=lag)).strftime("%H:%M:%S,%f")[:-3]


with open(zmfile, 'r', encoding='UTF-8') as f:
    for line in f.readlines():
        # print(line, end='')
        if '-->' in line:
            zmlist = line.split('-->')
            starttime = zmlist[0]
            endtime = zmlist[1]
            rightStart = getRightTime(starttime.strip(' '), lag) + ' '
            rightEnd = ' ' + getRightTime(endtime.strip(' ').rstrip('\n'), lag)+'\n'
            line = line.replace(starttime, rightStart)
            line = line.replace(endtime, rightEnd)
            text = text + line
            # print(line, end='')
        else:
            # print(line, end='')
            text = text + line


with open(debugFile, 'w', encoding='UTF-8') as f:
    f.write(text)

