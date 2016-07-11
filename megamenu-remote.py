#!/usr/bin/python
#encoding=utf-8

import traceback, os, re, time, sys, paramiko
from snack import * #导入图形界面


class ProWin:
#进度条
  def __init__(self, screen, title, text):
    self.screen = screen
    self.g = GridForm(self.screen, title, 1, 2)
    self.s = Scale(60, 100)
    self.g.add(Textbox(60, 2, text), 0, 0)
    self.g.add(self.s, 0, 1)

  def show(self):
    self.g.draw()
    self.screen.refresh()

  def update(self, progress):
    self.s.set(progress)
    self.g.draw()
    self.screen.refresh()

  def close(self):
    self.update(70)
    time.sleep(1)
    self.update(98)
    time.sleep(1)
    self.update(100)
    time.sleep(1)
    self.screen.popWindow()

class GetVDInfo:
  def __init__(self, n):
    self.num = n

  def vdnum(self):
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + self.num + " -nolog | grep 'DISK GROUP:' -n | awk -F ':' '{print $1}'")
    i = t.readlines()
    return i

  def vdtotalnum(self):
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + self.num + " -nolog | grep 'DISK GROUP:' -n | wc -l")
    i = t.read()
    return i

  def vdhsp(self):
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + self.num + " -nolog | grep 'Number of dedicated Hotspares: ' | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

  def vdshow(self):
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + self.num + " -nolog | grep 'DISK GROUP:'")
    i = t.readlines()
    return i

  def vdsize(self):
    r, t, y = client.exec_command(megacli + " -ldinfo -lall -a" + self.num + " -nolog | grep 'Size                :' | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

  def vdstate(self):
    r, t, y = client.exec_command(megacli + " -ldinfo -lall -a" + self.num + " -nolog | grep State | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

  def delvdnum(self):
    r, t, y = client.exec_command(megacli + " -ldinfo -lall -a" + self.num + " -nolog | grep 'Virtual Drive:' | awk -F ' ' '{print$3}'")
    i = t.readlines()
    return i

  def raidstate(self):
    r, t, y = client.exec_command(megacli + " -ShowSummary -a" + self.num + " -nolog | grep 'RAID Level' | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

class GetPDInfo:
  def __init__(self, n):
    self.num = n

  def pdisknum(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Enclosure Device ID' -n | awk -F ':' '{print $1}'")
    i = t.readlines()
    return i

  def pdiskrnum(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Enclosure Device ID' | awk -F ': ' '{print $2}'")
    i = t.readlines()
    return i

  def pdtotalnum(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Enclosure Device ID' -n | wc -l")
    i = t.read()
    return i

  def pdshow(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Slot Number:'")
    i = t.readlines()
    return i

  def pdsize(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Raw Size' | awk -F ' ' '{print$3$4}'")
    i = t.readlines()
    return i

  def pdstate(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Firmware state' | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

  def pdstate2(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Firmware state' | awk -F ': ' '{print$2}'")
    i = t.read()
    return i

  def pdedid(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Enclosure Device ID' | awk -F ': ' '{print $2}'")
    i = t.readlines()
    return i
    
  def pdslnum(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Slot Number:' | awk -F ': ' '{print$2}'")
    i = t.readlines()
    return i

  def pdforeign(self):
    r, t, y = client.exec_command(megacli + " -pdlist -a" + self.num + " -nolog | grep 'Foreign State:'")
    i = t.readlines()
    return i

def warwindows(screen, title, text, help = None):
#警告窗口
  btn = Button("确定")
  war = GridForm(screen, title, 1, 15)
  war.add(Label(text),0,1)
  war.add(Label(""),0,2)
  war.add(btn, 0, 3)
  war.runOnce(35,10)

def conformwindows(screen, text, help = None):
#确认窗口
  btns = ("是", "否")
  le = len(text) + 3
  bb = ButtonBar(screen, btns, compact = 1)
  g = GridForm(screen, text, 20, 16)
  g.add(Label(text),0,2)
  g.add(bb,0,3,(10,0,10,0), growx = 1)
  re = g.runOnce(30, 8)
  return (bb.buttonPressed(re), re)

def sc():
#刷新屏幕
  global screen
  screen = SnackScreen()
  screen.finish()
  screen = SnackScreen()
  screen.setColor("ROOT", "white", "blue")
  screen.setColor("ENTRY","white","blue")
  screen.setColor("LABEL","black","white")
  screen.setColor("HELPLINE","white","blue")
  screen.setColor("TEXTBOX","black","yellow")

def QUIT():
#调用退出到命令行，输入exit返回
    global out
    buttons = ("是", "否")
    bb = ButtonBar(screen, buttons)
    g = GridForm(screen, "返回登陆界面？" , 20,16)
    g.add(bb,1,3,(10,0,10,0), growx = 1)
    rq = g.runOnce(32,8)
    screen.popWindow()
    if rq == "ESC" or bb.buttonPressed(rq) == "否":
      screen.finish()
      return mainform()
    else:
      screen.finish()
      out = 1
      return

def details1(num):
  re = []
  n = 0
  li = Listbox(height = 8, width = 24, returnExit = 1, showCursor = 0)
  li.append("a)物理磁盘信息", 1)
  li.append("b)虚拟磁盘组信息", 2)
  li.append("c)磁盘组对应关系列表",3)
  li.append("d)RAID卡及磁盘信息摘要",4)
  li.append("e)RAID卡详细信息",5)
  li.append("f)磁盘组初始化进度",6)
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep Product")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep Disks")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep 'Critical Disks  :'")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep 'Failed Disks    :'")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep Virtual")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep 'Offline         :'")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep Degraded")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep JBOD")
  re.append(t.readline())
  r, t, y = client.exec_command(megacli + " -pdlist -a" + num + " -nolog | grep 'Foreign State: Foreign' -c")
  foreign = t.read()
  r, t, y = client.exec_command(megacli + " -pdlist -a" + num + " -nolog | grep 'Firmware state: Hotspare' -c")
  hsp = t.read()
  r, t, y = client.exec_command(megacli + " -pdlist -a" + num + " -nolog | grep JBOD -c")
  JBOD = t.read()
  h = GridForm(screen, "概览", 1, 18)
  r, t, y = client.exec_command(megacli + " -adpbootdrive -get -a" + num + " -nolog | grep Virtual | awk -F ' ' '{print$7}'")
  bootdrv = t.read().replace('#','').strip('/n')
  for i in re:
    n = n + 1
    h.add(TextboxReflowed(40, str(i).replace('Product Name','RAID卡名称').replace('Failed Disks    :','失效磁盘:').replace('Critical Disks  :','高危磁盘:').replace('Disks','物理磁盘数量').replace('Virtual Drives','已创建磁盘组').replace('Enable JBOD','开启JBOD模式').replace(' ','').replace('Offline:','下线磁盘组:').replace('Degraded:','降级磁盘组:').strip("\n"), flexDown = 5, flexUp = 10, maxHeight = -1), 0, n)
  h.add(TextboxReflowed(40, "JBOD模式磁盘数量:%s" %JBOD, flexDown = 5, flexUp = 10, maxHeight = -1), 0, n + 1)
  h.add(TextboxReflowed(40, "外来磁盘数量: " + str(foreign).strip('\n'), flexDown = 5, flexUp = 10, maxHeight = -1), 0, n + 2)
  h.add(TextboxReflowed(40, "热备磁盘数量: " + str(hsp).strip('\n'), flexDown = 5, flexUp = 10, maxHeight = -1), 0, n + 3)
  try:
    int(bootdrv)
    h.add(TextboxReflowed(40, "BOOT磁盘组: DG-" + str(bootdrv).strip('\n'), flexDown = 5, flexUp = 10, maxHeight = -1), 0, n + 4)
  except:
    h.add(TextboxReflowed(40, "BOOT磁盘组: 还未设定", flexDown = 5, flexUp = 10, maxHeight = -1), 0, n + 4)
  h.add(li, 0, n + 5)
  bb = CompactButton('返回') 
  h.add(bb, 0, 14)
  rc = h.runOnce(44,3)
  if rc == "ESC" or "snack.CompactButton" in str(rc):
    return ADPSelect()
  elif li.current() == 1:
    pdinfo(num)
  elif li.current() == 2:
    vdinfo(num)
  elif li.current() == 3:
    vdpdinfo(num)
  elif li.current() == 4:
    infosum(num)
  elif li.current() == 5:
    moredetails(num)
  elif li.current() == 6:
    diskinit(num)
  elif li.current() == 7:
    dgrebulid(num)

def diskinit(num):
  r, t, y = client.exec_command(megacli + " -ldbi -showprog -lall -a" + str(num).strip('\n') + " -nolog")
  info = t.read()
  h = GridForm(screen, "磁盘组初始化进度", 1, 5)
  h.add(Textbox(90, 15, info, scroll = 1, wrap = 1), 0, 1)
  bb = CompactButton('返回')
  h.add(bb, 0, 2)
  rc = h.runOnce(2,3)
  return details1(num)

def infosum(num):
  r, t, y = client.exec_command(megacli + " -ShowSummary -a" + str(num) + " -nolog".strip('\n'))
  info = t.read()
  h = GridForm(screen, "RAID卡及磁盘信息摘要", 1, 5)
  h.add(Textbox(90, 15, info, scroll = 1, wrap = 1), 0, 1)
  bb = CompactButton('返回')
  h.add(bb, 0, 2)
  rc = h.runOnce(2,3)
  return details1(num)

def vdpdinfo(num):
  more = ''
  r, t, y = client.exec_command(megacli + " -cfgdsply –a" + str(num).strip('\n') + " -nolog | grep -E 'DISK\\ GROUP|Slot\\ Number|RAID\\ Level|Target'")
  more1 = t.readlines()
  for i in more1:
    if 'DISK GROUP:' in i:
      more = more + "----------------------------------\n|----" + (str(i)).strip('\n') + '----|\n' + "----------------------------------\n"
    else:
      more = more + (str(i))
  h = GridForm(screen, "磁盘对应关系列表", 1, 5)
  h.add(Textbox(80, 15, more, scroll = 1, wrap = 1), 0, 1)
  bb = CompactButton('返回')
  h.add(bb, 0, 2)
  rc = h.runOnce(2,3)
  return details1(num)

def moredetails(num):
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog")
  more = t.read()
  h = GridForm(screen, "RAID卡详细信息", 1, 10)
  h.add(Textbox(55, 15, more, scroll = 1, wrap = 1), 0, 1)
  bb = CompactButton('返回')
  h.add(bb, 0, 2)
  rc = h.runOnce(25,3)
  return details1(num)

def pdinfo(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  pdforeign = p.pdforeign()
  pdiskrnum = p.pdiskrnum()
  pdslnum = p.pdslnum()
  n = 0
  li = Listbox(height = 20, width = 100, returnExit = 1, showCursor = 0, scroll = 1)
  try:
    if pdisknum != []:
      for i in pdshow:
        if 'None' in pdforeign[n]:
          li.append(str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "\t状态: " + str(pdstate[n]).strip('\n').replace(' ',''), n + 1)
        else:
          li.append(str(i).strip('\n').replace('Slot Number','<Foreign>槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "\t\t状态: " + str(pdstate[n]).strip('\n').replace(' ',''), n + 1)
        n = n + 1
      g = GridForm(screen, "物理磁盘信息", 1, 10)
      g.add(li, 0, 1)
      bb = CompactButton('返回')
      g.add(bb, 0, 2)
      rc = g.runOnce(2,3)
      if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
        return details1(num)
      else:
        selectPD = int(li.current() - 1)
        li2 = Listbox(height = 5, width = 33, returnExit = 1, showCursor = 0, scroll = 1)
        li2.append("查看槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘详细信息", 1)
        li2.append("查看槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘重建信息", 2)
        if 'Unconfigured(good)' in str(pdstate[selectPD]) :
          li2.append("将槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘作为全局热备盘", 3)
        if 'Hotspare' in str(pdstate[selectPD]) :
          li2.append("槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘不再作为热备盘", 4)
        f = GridForm(screen, "请选择", 1, 5)
        f.add(li2, 0, 1)
        bb2 = CompactButton('返回')
        f.add(bb2, 0, 2)
        rf = f.runOnce(44,3)
        if rf == 'ESC' or 'snack.CompactButton' in str(rf) :
          return pdinfo(num)
        elif li2.current() == 1:
          return pdinfo2(num,pdisknum,pdtotalnum,selectPD)
        elif li2.current() == 2:
          r, t, y = client.exec_command(megacli + " -pdrbld -ShowProg -physdrv [" + str(pdiskrnum[selectPD]).strip('\n') + ":" + str(pdslnum[selectPD]).strip('\n') + "] -a" + str(num) + " -nolog")
          diskrebuild = t.read()
          d = GridForm(screen, "磁盘详细信息", 1, 5)
          d.add(Textbox(65, 5, str(diskrebuild), scroll = 1, wrap = 1), 0, 1)
          bb3 = CompactButton('返回')
          d.add(bb3, 0, 2)
          rd = d.runOnce(15,3)
          if rd == 'ESC' or 'snack.CompactButton' in str(rd) :
            return pdinfo(num)
        elif li2.current() == 3:
          rx = conformwindows(screen, "确定将槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘作为全局热备盘？")
          if rx[0] == "否" or rx[1] == "ESC":
            return pdinfo(num)
          r, t, y = client.exec_command(megacli + " -pdhsp -set -physdrv[" + str(pdiskrnum[selectPD]).strip('\n') + ":" + str(pdslnum[selectPD]).strip('\n') + "] -a" + str(num) + " -nolog")
          ghsp = t.read()
          if 'Success' in ghsp:
            warwindows(screen, "完成", "成功设置全局热备盘")
            return pdinfo(num)
          warwindows(screen, "警告", "设置全局热备盘失败")
          return pdinfo(num)
        elif li2.current() == 4:
          rx = conformwindows(screen, "确定取消槽位" + str(pdslnum[selectPD]).strip('\n') + "的磁盘为热备盘？")
          if rx[0] == "否" or rx[1] == "ESC":
            return pdinfo(num)
          r, t, y = client.exec_command(megacli + " -pdhsp -rmv -physdrv[" + str(pdiskrnum[selectPD]).strip('\n') + ":" + str(pdslnum[selectPD]).strip('\n') + "] -a" + str(num) + " -nolog")
          nohsp = t.read()
          if 'Success' in nohsp:
            warwindows(screen, "完成", "已为磁盘取消热备盘")
            return pdinfo(num)
          warwindows(screen, "警告", "取消热备盘失败")
          return pdinfo(num)
    else:
      warwindows(screen, "警告", "未能找到磁盘")
      return details1(num)
  except:
    warwindows(screen, "警告", "MegaCLI运行错误，请手动检查")
    return details1(num)

def pdinfo2(num,pdisknum,pdtotalnum,selectPD):
  if int(selectPD) + 1 != int(pdtotalnum) :
    r, t, y = client.exec_command(megacli + " -pdlist -a" + num + " -nolog | sed -n '" + str(pdisknum[int(str(selectPD).strip('\n'))]).strip('\n') + "," + str(int(str(pdisknum[int(str(selectPD).strip('\n')) + 1]).strip('\n')) - 3).strip('\n') + "p'")
    pd = t.read()
    #pdnum = str(selectDG) + "  " + str(vdtotalnum)
  else:
    r, t, y = client.exec_command(megacli + " -pdlist -a" + num + " -nolog | sed -n '" + str(pdisknum[int(str(selectPD).strip('\n'))]).strip('\n') + ",999999p'")
    pd = t.read()
    #pdnum = str(selectDG) + "  " + str(vdtotalnum)
  h = GridForm(screen, "磁盘详细信息", 20, 20)
  h.add(Textbox(95, 15, pd, scroll = 1, wrap = 1), 0, 1)
  bb = CompactButton('返回')
  h.add(bb, 0, 2)
  rc = h.runOnce(2,3)
  return pdinfo(num)

def vdinfo(num):
  p = GetVDInfo(num)
  vdnum = p.vdnum()
  vdtotalnum = p.vdtotalnum()
  vdshow = p.vdshow()
  vdsize = p.vdsize()
  vdstate = p.vdstate()
  raidstate = p.raidstate()
  vdhsp = p.vdhsp()
  li = Listbox(height = 20, width = 100, returnExit = 1, showCursor = 0, scroll = 1)
  n = 0
  disknum = 0
  try:
    if vdnum != []: 
      for i in vdnum:
        if n != int(vdtotalnum):
          if n != int(vdtotalnum) - 1:
            r, t, y = client.exec_command(megacli +" -cfgdsply -a" + num + " -nolog | sed -n '" + str(i).strip('\n') + "," + str(vdnum[n+1]).strip('\n') + "p' | grep 'Number of PDs:' | awk -F ': ' '{print$2}'")
            pdnum = t.readlines()
            for k in pdnum:
              disknum = disknum + int(k.strip('\n'))
            li.append(str(vdshow[n].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + "\t磁盘数量:" + str(disknum).strip('\n') + "\tRAID后大小:" + str(vdsize[n]).strip('\n') + "\t状态:" + str(vdstate[n]).strip('\n') + "\tRAID级别:" + str(raidstate[n]), n + 1)
            disknum = 0
            n = n + 1
          else:
            r, t, y = client.exec_command(megacli +" -cfgdsply -a" + num + " -nolog | sed -n '" + str(i).strip('\n') + ",999999p' | grep 'Number of PDs:' | awk -F ': ' '{print$2}'")
            pdnum = t.readlines()
            for k in pdnum:
              disknum = disknum + int(k.strip('\n'))
            li.append(str(vdshow[n].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + "\t磁盘数量:" + str(disknum).strip('\n') + "\tRAID后大小:" + str(vdsize[n]).strip('\n') + "\t状态:" + str(vdstate[n]).strip('\n') + "\tRAID级别:" + str(raidstate[n]), n + 1)
            disknum = 0
            n = n + 1
      g = GridForm(screen, "DG&VG 信息", 1, 10)
      g.add(li, 0, 1)
      bb = CompactButton('返回')
      g.add(bb, 0, 2)
      rc = g.runOnce(2,3)
      if rc == 'ESC' or 'snack.CompactButton' in str(rc):
        return details1(num)
      else:
        selectDG = int(li.current() - 1)
        li2 = Listbox(height = 7, width = 43, returnExit = 1, showCursor = 0, scroll = 1)
        li2.append("查看" + str(vdshow[selectDG].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + " 的详细信息", 1)
        li2.append("指定" + str(vdshow[selectDG].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + " 的热备盘", 2)
        if int(vdhsp[selectDG]) != 0:
          li2.append("查看" + str(vdshow[selectDG].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + " 的热备盘", 3)
        li2.append("指定" + str(vdshow[selectDG].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + " 为BOOT磁盘组", 4)
        f = GridForm(screen, "请选择", 1, 10)
        f.add(li2, 0, 1)
        bb2 = CompactButton('返回')
        f.add(bb2, 0, 2)
        rf = f.runOnce(44,3)
        if rf == 'ESC' or 'snack.CompactButton' in str(rf) :
          return vdinfo(num)
        elif li2.current() == 1:
          return vdinfo2(num,vdnum,vdtotalnum,selectDG)
        elif li2.current() == 2:
          p = GetPDInfo(num)
          pdisknum = p.pdisknum()
          pdtotalnum = p.pdtotalnum()
          pdshow = p.pdshow()
          pdedid = p.pdedid()
          pdslnum = p.pdslnum()
          pdsize = p.pdsize()
          pdstate = p.pdstate()
          pdstate2 = p.pdstate2()
          ct = CheckboxTree(height = 8, scroll = 1)
          n = 0
          pdedid2 = []
          pdslnum2 = []
          pdshow2 = []
          pdsize2 = []
          ok = False
          li3 = Listbox(height = 15, width = 75, returnExit = 1, showCursor = 0, scroll = 1)
          if pdisknum != []:
              if "Unconfigured(good)" not in pdstate2 and "Hotspare" not in pdstate2:
                warwindows(screen, "警告", "没有合适的磁盘")
                return vdinfo(num)
          n2 = 0
          for i in pdshow:
            if "Unconfigured(good)" in str(pdstate[n]).strip('\n') or "Hotspare" in str(pdstate[n]).strip('\n'):
              li3.append(str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "\t状态：" + str(pdstate[n].strip('\n')), n2)
              pdedid2.append(str(pdedid[n]))
              pdslnum2.append(str(pdslnum[n]))
              n2 = n2 + 1
            n = n + 1
          bb = ButtonBar(screen, (("确定", "ok"), ("取消", "cancel")))
          j = GridForm(screen, "选择热备磁盘", 1, 3)
          j.add(li3, 0, 1)
          j.add(bb, 0 ,2)
          rq = j.runOnce(25, 3)
          if rq == 'ESC' or str(bb.buttonPressed(rq)) == "cancel" :
            return vdinfo(num)
          hsp = megacli + " -PDHSP -set -dedicated -array " + str(selectDG) + " -physdrv[" + pdedid2[li3.current()].strip('\n') + ":" + pdslnum2[li3.current()].strip('\n') + "] -a" + str(num) + " -nolog"
          r, t, y = client.exec_command(hsp)
          hsp = t.read()
          if 'Success' in hsp:
            warwindows(screen, "完成", "已为DG" + str(selectDG) + " 设置热备盘")
            return vdinfo(num)
          warwindows(screen, "警告", "热备盘设置失败")
          return vdinfo(num)
        elif li2.current() == 3:
          r, t, y = client.exec_command(megacli + " -ldinfo -l" + str(selectDG) +" -a" + num + " -nolog | egrep 'Number of Dedicated Hot Spares|EnclId'")
          gethsp = t.read()
          h = GridForm(screen, "热备盘信息", 1, 5)
          bb = CompactButton('返回')
          h.add(Textbox(55, 15, gethsp, scroll = 1, wrap = 1), 0, 1)
          h.add(bb, 0, 2)
          rq = h.runOnce(44,3)
          return vdinfo(num)
        elif li2.current() == 4:
          r, t, y = client.exec_command(megacli + " -adpbootdrive -set -l" + str(selectDG) + " -a" + num + " -nolog")
          setbootdrv = t.read()
          if 'is set to' in setbootdrv:
            warwindows(screen, "完成", "BOOT磁盘组设置成功")
            return vdinfo(num)
          warwindows(screen, "警告", "BOOT磁盘组设置失败")
          return vdinfo(num)
    else:
      warwindows(screen, "警告", "还未创建磁盘组")
      return details1(num)
  except:
    warwindows(screen, "警告", "MegaCLI运行错误，请手动检查")
    return details1(num)

def vdinfo2(num,vdnum,vdtotalnum,selectDG):
  if int(selectDG) + 1 != int(vdtotalnum) :
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + num + " -nolog | sed -n '" + str(vdnum[int(str(selectDG).strip('\n'))]).strip('\n') + "," + str(int(str(vdnum[int(str(selectDG).strip('\n')) + 1]).strip('\n')) - 3).strip('\n') + "p'")
    vd = t.read()
    #pdnum = str(selectDG) + "  " + str(vdtotalnum)
  else:
    r, t, y = client.exec_command(megacli + " -cfgdsply -a" + num + " -nolog | sed -n '" + str(vdnum[int(str(selectDG).strip('\n'))]).strip('\n') + ",999999p'")
    vd = t.read()
    #pdnum = str(selectDG) + "  " + str(vdtotalnum)
  h = GridForm(screen, "磁盘组详细信息", 20, 20)
  bb = CompactButton('返回')
  h.add(Textbox(55, 15, vd, scroll = 1, wrap = 1), 0, 1)
  h.add(bb, 0, 2)
  rc = h.runOnce(25,3)
  return vdinfo(num)

def CommandList(num):
  li = Listbox(height = 12, width = 20, returnExit = 1, showCursor = 0, scroll = 1)
  li.append("a)增加磁盘组", 1)
  li.append("b)增加组合磁盘组", 2)
  li.append("c)删除磁盘组", 3)
  li.append("d)外来磁盘操作", 4)
  li.append("e)标记磁盘状态", 5)
  li.append("f)BBU配置", 6)
  bb = CompactButton('返回')
  g = GridForm(screen, "命令清单", 1, 10)
  g.add(li, 0, 1)
  g.add(bb, 0, 2)
  rc = g.runOnce(44, 3)
  if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
    return ADPSelect()
  elif li.current() == 1:
    return AddDG(num)
  elif li.current() == 2:
    return AddSDG(num)
  elif li.current() == 3:
    return DelDG(num)
  elif li.current() == 4:
    return ConfigFD(num)
  elif li.current() == 5:
    return ConfigPD(num)
  elif li.current() == 6:
    return ConfigBBU(num)

def AddSDG(num):
  #选择raid级别
  p = GetPDInfo(num)
  pdshow = p.pdshow()
  pdstate = p.pdstate()
  pdforeign = p.pdforeign()
  n = 0
  diskcount = 0
  for i in pdshow:
    if "Unconfigured(good)" in str(pdstate[n]).strip('\n') and "None" in str(pdforeign[n]).strip('\n'):
      diskcount = diskcount + 1
    n = n + 1
  li = Listbox(height = 5, width = 15, returnExit = 1, showCursor = 0)
  li.append("\tRaid-10", 1)
  li.append("\tRaid-50", 2)
  li.append("\tRaid-60", 3)
  li.append("\t 返回", 4)
  g = GridForm(screen, "选择RAID级别", 1, 10)
  g.add(li, 0, 1)
  rc = g.runOnce(44,3)
  SelectRaidLevel = li.current()
  if li.current() == 4 or rc == 'ESC':
    return CommandList(num)
  if li.current() == 1:
    if diskcount < 4 :
      warwindows(screen, "警告", "剩余磁盘不足以构建RAID-10")
      return AddSDG(num)
    else:
      return AddSDGR10(num)
  if li.current() == 2:
    if diskcount < 6 :
      warwindows(screen, "警告", "剩余磁盘不足以构建RAID-50")
      return AddSDG(num)
    else:
      return AddSDGR50(num)
  if li.current() == 3:
    if diskcount < 8 :
      warwindows(screen, "警告", "剩余磁盘不足以构建RAID-60")
      return AddSDG(num)
    else:
      return AddSDGR60(num)

def AddSDGR10(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdedid = p.pdedid()
  pdslnum = p.pdslnum()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  pdforeign = p.pdforeign()
  spannum = 1
  j = []
  while True:
    arraydisknum = []
    ct = CheckboxTree(height = 8, scroll = 1)
    n = 0
    unconfigdiskcount = 0
    unconfigdiskcount2 = 0
    pdedid2 = []
    pdslnum2 = []
    pdshow2 = []
    pdsize2 = []
    unconfigreok = False
    bb = ButtonBar(screen, (("下一组", "next"), ("完成", "finish")))
    if pdisknum != []:
      for i in pdstate:
        if "Unconfigured(good)" in str(i):
          if pdforeign != []:
            if "None" in str(pdforeign[unconfigdiskcount]).strip('\n') :
              unconfigreok = True
              unconfigdiskcount2 = unconfigdiskcount2 + 1
        if "choose" in str(i):
          unconfigdiskcount2 = unconfigdiskcount2 - 1
        unconfigdiskcount = unconfigdiskcount + 1
      if unconfigreok == True and unconfigdiskcount2 >= 2:
        for i in pdshow:
          if "Unconfigured(good)" in str(pdstate[n]).strip('\n') and "None" in str(pdforeign[n]).strip('\n'):
            if "choose" not in str(pdstate[n]).strip('\n'):
              ct.append("槽位:" + str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "     ")
              pdshow2.append(str(pdshow[n]))
              pdedid2.append(str(pdedid[n]))
              pdslnum2.append(str(pdslnum[n]))
              pdsize2.append(str(pdsize[n].replace('TB','')))
          n = n + 1
        g = GridForm(screen, "选择第" + str(spannum) + "组磁盘", 3, 10)
        g.add(Label("选择磁盘"), 0, 1)
        g.add(ct, 0, 2)
        g.add(Label("  "), 1, 2)
        g.add(bb, 0, 3, growx = 1)
        rc = g.runOnce(44,3)
      else:
        warwindows(screen, "警告", "剩余磁盘不足")
        return CommandList(num)
      if rc == 'ESC' or str(bb.buttonPressed(rc)) == "finish" :
        rx = conformwindows(screen, "磁盘组已经配置完毕？")
        if rx[0] == "否" or rx[1] == "ESC":
          rxx = conformwindows(screen, "要继续配置吗？")
          if rxx[0] == "否" or rxx[1] == "ESC":
            return CommandList(num)
          else:
            continue
        else:
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          n = 0
          DiskSelection = ct.getSelection()
          DiskSelection2 = []
          for i in DiskSelection:
            n = n + 1
          if n == 0:
            warwindows(screen, "警告", "至少选择一块磁盘")
            continue
          elif n != 2 :
            warwindows(screen, "警告", "只能选择两块磁盘")
            continue
          size = str(pdsize2[0]).strip('\n')
          for i in pdsize2:
            if size != str(i).strip('\n'):
              warwindows(screen, "警告", "请选择大小相同的磁盘")
              continue
          if spannum > 1:
            if groupdiskcount != n:
              warwindows(screen, "警告", "每组磁盘数量必须相同")
              continue
          groupdiskcount = n
          j.append(' -array' + str(spannum - 1) + '[')
          for i in DiskSelection:
            n = 0
            for k in pdshow2:
              if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
                DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
                DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
                arraydisknum.append(str(pdslnum2[n]).strip('\n'))
              n = n + 1
          n = 0
          pdstatebackup = pdstate
          for i in arraydisknum:
            n = 0
            for k in pdslnum:
              if int(i) == int(k):
                pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
              n = n + 1
          n = 0
          for i in pdstate:
            if " choose" in str(i):
              if size not in str(pdsize[n].replace(' TB','')):
                warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
                pdstate = pdstatebackup
                continue
            n = n + 1
          for i in DiskSelection2:
            j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
          j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
          break
      else:
        n = 0
        DiskSelection = ct.getSelection()
        DiskSelection2 = []
        for i in DiskSelection:
          n = n + 1
        if n == 0:
          warwindows(screen, "警告", "至少选择一块磁盘")
          continue
        elif n != 2:
          warwindows(screen, "警告", "只能选择两块磁盘")
          continue
        size = str(pdsize2[0]).strip('\n')
        for i in pdsize2:
          if size != str(i).strip('\n'):
            warwindows(screen, "警告", "请选择大小相同的磁盘")
            continue
        if spannum > 1:
          if groupdiskcount != n:
            warwindows(screen, "警告", "每组磁盘数量必须相同")
            continue
        groupdiskcount = n
        j.append(' -array' + str(spannum - 1) + '[')
        for i in DiskSelection:
          n = 0
          for k in pdshow2:
            if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
              DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
              DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
              arraydisknum.append(str(pdslnum2[n]).strip('\n'))
            n = n + 1
        n = 0
        pdstatebackup = pdstate
        for i in arraydisknum:
          n = 0
          for k in pdslnum:
            if int(i) == int(k):
              pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
            n = n + 1
        n = 0
        for i in pdstate:
          if " choose" in str(i):
            if size not in str(pdsize[n].replace(' TB','')):
              warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
              pdstate = pdstatebackup
              continue
          n = n + 1
        for i in DiskSelection2:
          j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
        j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
        rx = conformwindows(screen, "要配置下一组磁盘吗")
        if rx[0] == "否" or rx[1] == "ESC":
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          break
        else:
          spannum = spannum + 1
    else:
      warwindows(screen, "警告", "未能找到磁盘")
      return CommandList(num)
  CachePolicyRB = RadioBar(screen, (("打开", " -wt", 1), ("关闭", " -wb", 0)))
  RAPolicyRB = RadioBar(screen, (("打开", " -ra", 1), ("关闭", " -nora", 0), ("自适应", " -adra", 0)))
  DiskCachePolicyRB = RadioBar(screen, (("关闭", "off", 1), ("打开", "on", 0)))
  BBUPolicyRB = RadioBar(screen, (("否", " -nocachedbadbbu", 1), ("是", " -cachedbadbbu", 0)))
  StripSizeRB = RadioBar(screen, (("128KB", " -strpsz128", 1), ("256KB", " -strpsz256", 0), ("1024KB", " -strpsz1024", 0)))
  bb = ButtonBar(screen, (("确定", "ok"), ("取消", "cancel")))
  g = GridForm(screen, "配置DG选项", 4, 10)
  g.add(TextboxReflowed(10, "条带大小", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 1)
  g.add(StripSizeRB, 0, 2)
  g.add(TextboxReflowed(10, "预读选项", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 3)
  g.add(RAPolicyRB, 0, 4)
  g.add(TextboxReflowed(10, "磁盘缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 1)
  g.add(DiskCachePolicyRB, 1, 2)
  g.add(TextboxReflowed(10, "无BBU也缓存", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 1)
  g.add(BBUPolicyRB, 2, 2)
  g.add(TextboxReflowed(10, "RAID卡缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 3)
  g.add(CachePolicyRB, 1, 4)
  g.add(bb, 3, 2, growx = 1)
  rc = g.runOnce(25,3)
  arraygroup = ''
  for i in j:
    arraygroup = arraygroup + str(i).strip('\n')
  CachePolicy = CachePolicyRB.getSelection()
  RAPolicy = RAPolicyRB.getSelection()
  DiskCachePolicy = DiskCachePolicyRB.getSelection()
  BBUPolicy = BBUPolicyRB.getSelection()
  StripSize = StripSizeRB.getSelection()
  k = megacli + " -cfgspanadd -r10" + arraygroup + str(RAPolicy).strip('\n') + " -cached" + str(BBUPolicy).strip('\n') + str(StripSize).strip('\n') + " -a" + str(num).strip('\n') + " -nolog | grep VD | awk -F ' ' '{print$5}'"
  if str(DiskCachePolicy).strip('\n') != "on":
    ss = ProWin(screen, "请等待", "创建磁盘组中")
    ss.show()
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    ss.update(40)
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + " -ldsetprop -disdskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)
  else:
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + "  -ldsetprop -endskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)

def AddSDGR50(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdedid = p.pdedid()
  pdslnum = p.pdslnum()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  pdforeign = p.pdforeign()
  groupdiskcount = 0
  spannum = 1
  j = []
  while True:
    arraydisknum = []
    ct = CheckboxTree(height = 8, scroll = 1)
    n = 0
    unconfigdiskcount = 0
    unconfigdiskcount2 = 0
    pdedid2 = []
    pdslnum2 = []
    pdshow2 = []
    pdsize2 = []
    unconfigreok = False
    bb = ButtonBar(screen, (("下一组", "next"), ("完成", "finish")))
    if pdisknum != []:
      for i in pdstate:
        if "Unconfigured(good)" in str(i):
          if pdforeign != []:
            if "None" in str(pdforeign[unconfigdiskcount]).strip('\n') :
              unconfigreok = True
              unconfigdiskcount2 = unconfigdiskcount2 + 1
        if "choose" in str(i):
          unconfigdiskcount2 = unconfigdiskcount2 - 1
        unconfigdiskcount = unconfigdiskcount + 1
      if unconfigreok == True and unconfigdiskcount2 >= 2:
        for i in pdshow:
          if "Unconfigured(good)" in str(pdstate[n]).strip('\n') and "None" in str(pdforeign[n]).strip('\n'):
            if "choose" not in str(pdstate[n]).strip('\n'):
              ct.append("槽位:" + str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "     ")
              pdshow2.append(str(pdshow[n]))
              pdedid2.append(str(pdedid[n]))
              pdslnum2.append(str(pdslnum[n]))
              pdsize2.append(str(pdsize[n].replace('TB','')))
          n = n + 1
        g = GridForm(screen, "选择第" + str(spannum) + "组磁盘", 3, 10)
        g.add(Label("选择磁盘"), 0, 1)
        g.add(ct, 0, 2)
        g.add(Label("  "), 1, 2)
        g.add(bb, 0, 3, growx = 1)
        rc = g.runOnce(35,3)
      else:
        warwindows(screen, "警告", "剩余磁盘不足")
        return CommandList(num)
      if rc == 'ESC' or str(bb.buttonPressed(rc)) == "finish" :
        rx = conformwindows(screen, "磁盘组已经配置完毕？")
        if rx[0] == "否" or rx[1] == "ESC":
          rxx = conformwindows(screen, "要继续配置吗？")
          if rxx[0] == "否" or rxx[1] == "ESC":
            return CommandList(num)
          else:
            continue
        else:
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          n = 0
          DiskSelection = ct.getSelection()
          DiskSelection2 = []
          for i in DiskSelection:
            n = n + 1
          if n == 0:
            warwindows(screen, "警告", "至少选择一块磁盘")
            continue
          elif n < 3 :
            warwindows(screen, "警告", "每个磁盘组至少需要3块磁盘")
            continue
          size = str(pdsize2[0]).strip('\n')
          for i in pdsize2:
            if size != str(i).strip('\n'):
              warwindows(screen, "警告", "请选择大小相同的磁盘")
              continue
          if spannum > 1:
            if groupdiskcount != n:
              warwindows(screen, "警告", "每组磁盘数量必须相同")
              continue
          groupdiskcount = n
          j.append(' -array' + str(spannum - 1) + '[')
          for i in DiskSelection:
            n = 0
            for k in pdshow2:
              if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
                DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
                DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
                arraydisknum.append(str(pdslnum2[n]).strip('\n'))
              n = n + 1
          n = 0
          pdstatebackup = pdstate
          for i in arraydisknum:
            n = 0
            for k in pdslnum:
              if int(i) == int(k):
                pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
              n = n + 1
          n = 0
          for i in pdstate:
            if " choose" in str(i):
              if size not in str(pdsize[n].replace(' TB','')):
                warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
                pdstate = pdstatebackup
                continue
            n = n + 1
          for i in DiskSelection2:
            j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
          j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
          break
      else:
        n = 0
        DiskSelection = ct.getSelection()
        DiskSelection2 = []
        for i in DiskSelection:
          n = n + 1
        if n == 0:
          warwindows(screen, "警告", "至少选择一块磁盘")
          continue
        elif n < 3 :
          warwindows(screen, "警告", "每个磁盘组至少需要3块磁盘")
          continue
        size = str(pdsize2[0]).strip('\n')
        for i in pdsize2:
          if size != str(i).strip('\n'):
            warwindows(screen, "警告", "请选择大小相同的磁盘")
            continue
        if spannum > 1:
          if groupdiskcount != n:
            warwindows(screen, "警告", "每组磁盘数量必须相同")
            continue
        groupdiskcount = n
        j.append(' -array' + str(spannum - 1) + '[')
        for i in DiskSelection:
          n = 0
          for k in pdshow2:
            if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
              DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
              DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
              arraydisknum.append(str(pdslnum2[n]).strip('\n'))
            n = n + 1
        n = 0
        pdstatebackup = pdstate
        for i in arraydisknum:
          n = 0
          for k in pdslnum:
            if int(i) == int(k):
              pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
            n = n + 1
        n = 0
        for i in pdstate:
          if " choose" in str(i):
            if size not in str(pdsize[n].replace(' TB','')):
              warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
              pdstate = pdstatebackup
              continue
          n = n + 1
        for i in DiskSelection2:
          j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
        j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
        rx = conformwindows(screen, "要配置下一组磁盘吗")
        if rx[0] == "否" or rx[1] == "ESC":
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          break
        else:
          spannum = spannum + 1
    else:
      warwindows(screen, "警告", "未能找到磁盘")
      return CommandList(num)
  CachePolicyRB = RadioBar(screen, (("打开", " -wt", 1), ("关闭", " -wb", 0)))
  RAPolicyRB = RadioBar(screen, (("打开", " -ra", 1), ("关闭", " -nora", 0), ("自适应", " -adra", 0)))
  DiskCachePolicyRB = RadioBar(screen, (("关闭", "off", 1), ("打开", "on", 0)))
  BBUPolicyRB = RadioBar(screen, (("否", " -nocachedbadbbu", 1), ("是", " -cachedbadbbu", 0)))
  StripSizeRB = RadioBar(screen, (("128KB", " -strpsz128", 1), ("256KB", " -strpsz256", 0), ("1024KB", " -strpsz1024", 0)))
  bb = ButtonBar(screen, (("确定", "ok"), ("取消", "cancel")))
  g = GridForm(screen, "配置DG选项", 4, 10)
  g.add(TextboxReflowed(10, "条带大小", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 1)
  g.add(StripSizeRB, 0, 2)
  g.add(TextboxReflowed(10, "预读选项", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 3)
  g.add(RAPolicyRB, 0, 4)
  g.add(TextboxReflowed(10, "磁盘缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 1)
  g.add(DiskCachePolicyRB, 1, 2)
  g.add(TextboxReflowed(10, "无BBU也缓存", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 1)
  g.add(BBUPolicyRB, 2, 2)
  g.add(TextboxReflowed(10, "RAID卡缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 3)
  g.add(CachePolicyRB, 1, 4)
  g.add(bb, 3, 2, growx = 1)
  rc = g.runOnce(25,3)
  arraygroup = ''
  for i in j:
    arraygroup = arraygroup + str(i).strip('\n')
  CachePolicy = CachePolicyRB.getSelection()
  RAPolicy = RAPolicyRB.getSelection()
  DiskCachePolicy = DiskCachePolicyRB.getSelection()
  BBUPolicy = BBUPolicyRB.getSelection()
  StripSize = StripSizeRB.getSelection()
  k = megacli + " -cfgspanadd -r50" + arraygroup + str(RAPolicy).strip('\n') + " -cached" + str(BBUPolicy).strip('\n') + str(StripSize).strip('\n') + " -a" + str(num).strip('\n') + " -nolog | grep VD | awk -F ' ' '{print$5}'"
  if str(DiskCachePolicy).strip('\n') != "on":
    ss = ProWin(screen, "请等待", "创建磁盘组中")
    ss.show()
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    ss.update(40)
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + " -ldsetprop -disdskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)
  else:
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + "  -ldsetprop -endskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)

def AddSDGR60(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdedid = p.pdedid()
  pdslnum = p.pdslnum()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  pdforeign = p.pdforeign()
  groupdiskcount = 0
  spannum = 1
  j = []
  while True:
    arraydisknum = []
    ct = CheckboxTree(height = 8, scroll = 1)
    n = 0
    unconfigdiskcount = 0
    unconfigdiskcount2 = 0
    pdedid2 = []
    pdslnum2 = []
    pdshow2 = []
    pdsize2 = []
    unconfigreok = False
    bb = ButtonBar(screen, (("下一组", "next"), ("完成", "finish")))
    if pdisknum != []:
      for i in pdstate:
        if "Unconfigured(good)" in str(i):
          if pdforeign != []:
            if "None" in str(pdforeign[unconfigdiskcount]).strip('\n') :
              unconfigreok = True
              unconfigdiskcount2 = unconfigdiskcount2 + 1
        if "choose" in str(i):
          unconfigdiskcount2 = unconfigdiskcount2 - 1
        unconfigdiskcount = unconfigdiskcount + 1
      if unconfigreok == True and unconfigdiskcount2 >= 2:
        for i in pdshow:
          if "Unconfigured(good)" in str(pdstate[n]).strip('\n') and "None" in str(pdforeign[n]).strip('\n'):
            if "choose" not in str(pdstate[n]).strip('\n'):
              ct.append("槽位:" + str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "     ")
              pdshow2.append(str(pdshow[n]))
              pdedid2.append(str(pdedid[n]))
              pdslnum2.append(str(pdslnum[n]))
              pdsize2.append(str(pdsize[n].replace('TB','')))
          n = n + 1
        g = GridForm(screen, "选择第" + str(spannum) + "组磁盘", 3, 10)
        g.add(Label("选择磁盘"), 0, 1)
        g.add(ct, 0, 2)
        g.add(Label("  "), 1, 2)
        g.add(bb, 0, 3, growx = 1)
        rc = g.runOnce(35,3)
      else:
        warwindows(screen, "警告", "剩余磁盘不足")
        return CommandList(num)
      if rc == 'ESC' or str(bb.buttonPressed(rc)) == "finish" :
        rx = conformwindows(screen, "磁盘组已经配置完毕？")
        if rx[0] == "否" or rx[1] == "ESC":
          rxx = conformwindows(screen, "要继续配置吗？")
          if rxx[0] == "否" or rxx[1] == "ESC":
            return CommandList(num)
          else:
            continue
        else:
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          n = 0
          DiskSelection = ct.getSelection()
          DiskSelection2 = []
          for i in DiskSelection:
            n = n + 1
          if n == 0:
            warwindows(screen, "警告", "至少选择一块磁盘")
            continue
          elif n < 4 :
            warwindows(screen, "警告", "每个磁盘组至少需要4块磁盘")
            continue
          size = str(pdsize2[0]).strip('\n')
          for i in pdsize2:
            if size != str(i).strip('\n'):
              warwindows(screen, "警告", "请选择大小相同的磁盘")
              continue
          if spannum > 1:
            if groupdiskcount != n:
              warwindows(screen, "警告", "每组磁盘数量必须相同")
              continue
          groupdiskcount = n
          j.append(' -array' + str(spannum - 1) + '[')
          for i in DiskSelection:
            n = 0
            for k in pdshow2:
              if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
                DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
                DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
                arraydisknum.append(str(pdslnum2[n]).strip('\n'))
              n = n + 1
          n = 0
          pdstatebackup = pdstate
          for i in arraydisknum:
            n = 0
            for k in pdslnum:
              if int(i) == int(k):
                pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
              n = n + 1
          n = 0
          for i in pdstate:
            if " choose" in str(i):
              if size not in str(pdsize[n].replace(' TB','')):
                warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
                pdstate = pdstatebackup
                continue
            n = n + 1
          for i in DiskSelection2:
            j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
          j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
          break
      else:
        n = 0
        DiskSelection = ct.getSelection()
        DiskSelection2 = []
        for i in DiskSelection:
          n = n + 1
        if n == 0:
          warwindows(screen, "警告", "至少选择一块磁盘")
          continue
        elif n < 4 :
          warwindows(screen, "警告", "每个磁盘组至少需要4块磁盘")
          continue
        size = str(pdsize2[0]).strip('\n')
        for i in pdsize2:
          if size != str(i).strip('\n'):
            warwindows(screen, "警告", "请选择大小相同的磁盘")
            continue
        if spannum > 1:
          if groupdiskcount != n:
            warwindows(screen, "警告", "每组磁盘数量必须相同")
            continue
        groupdiskcount = n
        j.append(' -array' + str(spannum - 1) + '[')
        for i in DiskSelection:
          n = 0
          for k in pdshow2:
            if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
              DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
              DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
              arraydisknum.append(str(pdslnum2[n]).strip('\n'))
            n = n + 1
        n = 0
        pdstatebackup = pdstate
        for i in arraydisknum:
          n = 0
          for k in pdslnum:
            if int(i) == int(k):
              pdstate[n] = str(pdstate[n]).strip('\n') + " choose"
            n = n + 1
        n = 0
        for i in pdstate:
          if " choose" in str(i):
            if size not in str(pdsize[n].replace(' TB','')):
              warwindows(screen, "警告" ,"每个磁盘组内的磁盘大小必须相同")
              pdstate = pdstatebackup
              continue
          n = n + 1
        for i in DiskSelection2:
          j[spannum - 1] = str(j[spannum -1]).strip('\n') + str(i).strip('\n')
        j[spannum - 1] = str(j[spannum -1]).strip('\n').rstrip(',') + "]"
        rx = conformwindows(screen, "要配置下一组磁盘吗")
        if rx[0] == "否" or rx[1] == "ESC":
          if spannum < 2:
            warwindows(screen, "警告", "至少配置两组磁盘")
            continue
          break
        else:
          spannum = spannum + 1
    else:
      warwindows(screen, "警告", "未能找到磁盘")
      return CommandList(num)
  CachePolicyRB = RadioBar(screen, (("打开", " -wt", 1), ("关闭", " -wb", 0)))
  RAPolicyRB = RadioBar(screen, (("打开", " -ra", 1), ("关闭", " -nora", 0), ("自适应", " -adra", 0)))
  DiskCachePolicyRB = RadioBar(screen, (("关闭", "off", 1), ("打开", "on", 0)))
  BBUPolicyRB = RadioBar(screen, (("否", " -nocachedbadbbu", 1), ("是", " -cachedbadbbu", 0)))
  StripSizeRB = RadioBar(screen, (("128KB", " -strpsz128", 1), ("256KB", " -strpsz256", 0), ("1024KB", " -strpsz1024", 0)))
  bb = ButtonBar(screen, (("确定", "ok"), ("取消", "cancel")))
  g = GridForm(screen, "配置DG选项", 4, 10)
  g.add(TextboxReflowed(10, "条带大小", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 1)
  g.add(StripSizeRB, 0, 2)
  g.add(TextboxReflowed(10, "预读选项", flexDown = 5, flexUp = 10, maxHeight = -1), 0, 3)
  g.add(RAPolicyRB, 0, 4)
  g.add(TextboxReflowed(10, "磁盘缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 1)
  g.add(DiskCachePolicyRB, 1, 2)
  g.add(TextboxReflowed(10, "无BBU也缓存", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 1)
  g.add(BBUPolicyRB, 2, 2)
  g.add(TextboxReflowed(10, "RAID卡缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 3)
  g.add(CachePolicyRB, 1, 4)
  g.add(bb, 3, 2, growx = 1)
  rc = g.runOnce(25,3)
  arraygroup = ''
  for i in j:
    arraygroup = arraygroup + str(i).strip('\n')
  CachePolicy = CachePolicyRB.getSelection()
  RAPolicy = RAPolicyRB.getSelection()
  DiskCachePolicy = DiskCachePolicyRB.getSelection()
  BBUPolicy = BBUPolicyRB.getSelection()
  StripSize = StripSizeRB.getSelection()
  k = megacli + " -cfgspanadd -r60" + arraygroup + str(RAPolicy).strip('\n') + " -cached" + str(BBUPolicy).strip('\n') + str(StripSize).strip('\n') + " -a" + str(num).strip('\n') + " -nolog | grep VD | awk -F ' ' '{print$5}'"
  if str(DiskCachePolicy).strip('\n') != "on":
    ss = ProWin(screen, "请等待", "创建磁盘组中")
    ss.show()
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    ss.update(40)
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + " -ldsetprop -disdskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)
  else:
    r, t, y = client.exec_command(k)
    getre = t.readlines()
    if getre == []:
      ss.close()
      warwindows(screen, "警告", "创建磁盘组失败")
      return AddSDG(num)
    else:
      l = megacli + "  -ldsetprop -endskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
      ss.update(60)
      r, t, y = client.exec_command(l)
      ss.close()
      warwindows(screen, "已完成", "创建磁盘组成功")
      return CommandList(num)

def ConfigFD(num):
  warwindows(screen, "抱歉", "研发中...")
  return CommandList(num)

def ConfigPD(num):
  warwindows(screen, "抱歉", "研发中...")
  return CommandList(num)

def ConfigBBU(num):
  warwindows(screen, "抱歉", "研发中...")
  return CommandList(num)

def DelDG(num):
  p = GetVDInfo(num)
  vdnum = p.vdnum()
  vdtotalnum = p.vdtotalnum()
  vdshow = p.vdshow()
  vdsize = p.vdsize()
  vdstate = p.vdstate()
  delvdnum = p.delvdnum()
  raidstate = p.raidstate()
  li = Listbox(height = 20, width = 100, returnExit = 1, showCursor = 0, scroll = 1)
  n = 0
  disknum = 0
  try:
    if vdnum != []: 
      for i in vdnum:
        if n != int(vdtotalnum):
          if n != int(vdtotalnum) - 1:
            r, t, y = client.exec_command(megacli +" -cfgdsply -a" + num + " -nolog | sed -n '" + str(i).strip('\n') + "," + str(vdnum[n+1]).strip('\n') + "p' | grep 'Number of PDs:' | awk -F ': ' '{print$2}'")
            pdnum = t.readlines()
            for k in pdnum:
              disknum = disknum + int(k.strip('\n'))
            li.append(str(vdshow[n].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + "\t磁盘数量:" + str(disknum).strip('\n') + "\tRAID后大小:" + str(vdsize[n]).strip('\n') + "\t状态:" + str(vdstate[n]).strip('\n') + "\tRAID级别:" + str(raidstate[n]), n + 1)
            disknum = 0
            n = n + 1
          else:
            r, t, y = client.exec_command(megacli +" -cfgdsply -a" + num + " -nolog | sed -n '" + str(i).strip('\n') + ",999999p' | grep 'Number of PDs:' | awk -F ': ' '{print$2}'")
            pdnum = t.readlines()
            for k in pdnum:
              disknum = disknum + int(k.strip('\n'))
            li.append(str(vdshow[n].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n') + "\t磁盘数量:" + str(disknum).strip('\n') + "\tRAID后大小:" + str(vdsize[n]).strip('\n') + "\t状态:" + str(vdstate[n]).strip('\n') + "\tRAID级别:" + str(raidstate[n]), n + 1)
            disknum = 0
            n = n + 1
      g = GridForm(screen, "DG 信息", 1, 10)
      g.add(li, 0, 1)
      bb = CompactButton('返回')
      g.add(bb, 0, 2)
      rc = g.runOnce(2,3)
      if rc == 'ESC' or 'snack.CompactButton' in str(rc):
        return CommandList(num)
      else:
        selectDG = int(li.current() - 1)
        rx = conformwindows(screen, "确认操作:删除DG-" + str(vdshow[selectDG].replace('SPANNED DISK GROUP','组合磁盘组').replace('DISK GROUP','普通磁盘组')).strip('\n'))
        if rx[0] == "否" or rx[1] == "ESC":
          return DelDG(num)
        r, t, y = client.exec_command(megacli + " -cfglddel -l" + str(delvdnum[selectDG]).strip('\n') + " -a" + num + " -nolog")
        k = t.read()
        if "Deleted Virtual Drive-" in k:
          warwindows(screen, "完成", "已删除所选DG")
          return DelDG(num)
        else:
          warwindows(screen, "警告", "删除DG失败")
          return DelDG(num)
    else:
      warwindows(screen, "警告", "还未创建DG")
      return CommandList(num)
  except:
    warwindows(screen, "警告", "MegaCLI运行错误，请手动检查")
    return CommandList(num)

def AddDG(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdedid = p.pdedid()
  pdslnum = p.pdslnum()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  ct = CheckboxTree(height = 8, scroll = 1)
  n = 0
  pdedid2 = []
  pdslnum2 = []
  pdshow2 = []
  pdsize2 = []
  ok = False
  li = Listbox(height = 20, width = 100, returnExit = 1, showCursor = 0, scroll = 1)
  if pdisknum != []:
    for i in pdstate:
      if "Unconfigured(good)" in str(i):
        ok = True
    if ok == True:
      for i in pdshow:
        if "Unconfigured(good)" in str(pdstate[n]).strip('\n'):
          ct.append("槽位:" + str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "     ")
          pdshow2.append(str(pdshow[n]))
          pdedid2.append(str(pdedid[n]))
          pdslnum2.append(str(pdslnum[n]))
          pdsize2.append(str(pdsize[n].replace('TB','')))
        n = n + 1
      RAIDLevelRB = RadioBar(screen, (("RAID-0", " -r0", 1), ("RAID-1", " -r1", 0), ("RAID-5", " -r5", 0)))
      CachePolicyRB = RadioBar(screen, (("打开", " -wt", 1), ("关闭", " -wb", 0)))
      RAPolicyRB = RadioBar(screen, (("打开", " -ra", 1), ("关闭", " -nora", 0), ("自适应", " -adra", 0)))
      DiskCachePolicyRB = RadioBar(screen, (("关闭", "off", 1), ("打开", "on", 0)))
      BBUPolicyRB = RadioBar(screen, (("否", " -nocachedbadbbu", 1), ("是", " -cachedbadbbu", 0)))
      StripSizeRB = RadioBar(screen, (("128KB", " -strpsz128", 1), ("256KB", " -strpsz256", 0), ("1024KB", " -strpsz1024", 0)))
      bb = ButtonBar(screen, (("确定", "ok"), ("取消", "cancel")))
      g = GridForm(screen, "配置RAID信息", 3, 10)
      g.add(Label("选择磁盘"), 0, 7)
      g.add(ct, 0, 8)
      g.add(TextboxReflowed(10, "RAID级别", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 1)
      g.add(RAIDLevelRB, 1, 2)
      g.add(TextboxReflowed(10, "条带深度", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 1)
      g.add(StripSizeRB, 2, 2)
      g.add(TextboxReflowed(10, "预读选项", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 3)
      g.add(RAPolicyRB, 1, 4)
      g.add(TextboxReflowed(10, "磁盘缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 3)
      g.add(DiskCachePolicyRB, 2, 4)
      g.add(TextboxReflowed(10, "无BBU也缓存", flexDown = 5, flexUp = 10, maxHeight = -1), 1, 5)
      g.add(BBUPolicyRB, 1, 6)
      g.add(TextboxReflowed(10, "RAID卡缓存策略", flexDown = 5, flexUp = 10, maxHeight = -1), 2, 5)
      g.add(CachePolicyRB, 2, 6)
      g.add(Label(" "), 1, 8)
      g.add(bb, 2, 8, growx = 1)
      rc = g.runOnce(25,3)
    else:
      warwindows(screen, "警告", "没有合适的磁盘")
      return CommandList(num)
    if rc == 'ESC' or str(bb.buttonPressed(rc)) == "cancel" :
      return CommandList(num)
    else:
      rx = conformwindows(screen, "确认操作")
      if rx[0] == "否" or rx[1] == "ESC":
        return AddDG(num)
      else:
        n = 0
        DiskSelection = ct.getSelection()
        CachePolicy = CachePolicyRB.getSelection()
        RAPolicy = RAPolicyRB.getSelection()
        DiskCachePolicy = DiskCachePolicyRB.getSelection()
        BBUPolicy = BBUPolicyRB.getSelection()
        StripSize = StripSizeRB.getSelection()
        RAIDLevel = RAIDLevelRB.getSelection()
        DiskSelection2 = []
        for i in DiskSelection:
          n = n + 1
        if n == 0:
          warwindows(screen, "警告", "至少选择一块磁盘")
          return AddDG(num)
        if str(RAIDLevel).strip('\n') == " -r1":
          if n != 2 :
            warwindows(screen, "警告", "RAID-1只能选择两块磁盘")
            return AddDG(num)
        elif str(RAIDLevel).strip('\n') == " -r5":
          if n < 3 or n > 12:
            warwindows(screen, "警告", "RAID-5需要大于2且小于13块磁盘")
            return AddDG(num)
        size = str(pdsize2[0]).strip('\n')
        for i in pdsize2:
          if size != str(i).strip('\n'):
            warwindows(screen, "警告", "请选择大小相同的磁盘")
        j = ' ['
        for i in DiskSelection:
          n = 0
          for k in pdshow2:
            if k.strip('\n') in i.replace('槽位','Slot Number').strip('\n'):
              DiskSelection2.append(str(pdedid2[n]).strip('\n') + ":")
              DiskSelection2.append(str(pdslnum2[n]).strip('\n') + ",")
            n = n + 1
        for i in DiskSelection2:
          j = j + str(i).strip('\n')
        j = j.rstrip(',') + "]"
        k = megacli + " -cfgldadd" + str(RAIDLevel).strip('\n') + j.strip('\n') + str(CachePolicy).strip('\n') + str(RAPolicy).strip('\n') + " -cached" + str(BBUPolicy).strip('\n') + str(StripSize).strip('\n') + " -a" + str(num).strip('\n') + " -nolog | grep VD | awk -F ' ' '{print$5}'"
        if str(DiskCachePolicy).strip('\n') != "on":
          ss = ProWin(screen, "请等待", "创建磁盘组中")
          ss.show()
          r, t, y = client.exec_command(k)
          getre = t.readlines()
          ss.update(40)
          if getre == []:
            ss.close()
            warwindows(screen, "警告", "创建磁盘组失败")
            return AddDG(num)
          else:
            l = megacli + " -ldsetprop -disdskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
            ss.update(60)
            r, t, y = client.exec_command(l)
            ss.close()
            warwindows(screen, "已完成", "创建磁盘组成功")
            return CommandList(num)
        else:
          r, t, y = client.exec_command(k)
          getre = t.readlines()
          if getre == []:
            ss.close()
            warwindows(screen, "警告", "创建磁盘组失败")
            return AddDG(num)
          else:
            l = megacli + "  -ldsetprop -endskcache -l" + str(getre[0]).strip('\n') + " -a" + str(num).strip('\n') + " -nolog"
            ss.update(60)
            r, t, y = client.exec_command(l)
            ss.close()
            warwindows(screen, "已完成", "创建磁盘组成功")
            return CommandList(num)
  else:
    warwindows(screen, "警告", "未能找到磁盘")
    return CommandList(num)

def ADPSelect():
  global adpl
  re = []
  r, t, y = client.exec_command(megacli + " -adpcount  -nolog | grep Controller | awk -F ': ' '{print $2}'")
  adpcount = t.readline().strip('\n').rstrip('.')
  li = Listbox(height = 15, width = 14, returnExit = 1, showCursor = 0)
  n = 0
  n1 = 1
  bb = CompactButton('返回')
  if int(adpcount) != 0 :
    while n < int(adpcount):
      n2 = "RAID卡: " + str(n1)
      li.append(n2,n1)
      n = n + 1
      n1 = n1 + 1
    h = GridForm(screen, "请选择", 1, 10)
    li.setCurrent(adpl)
    h.add(li, 0, 1)
    h.add(bb, 0, 9)
    rc = h.run(25,3)
    if "snack.CompactButton" in str(rc) or rc == 'ESC':
      return mainform()
    else :
      adpl = li.current()
      num = str(li.current() - 1)
      if mainl == 1:
        return details1(num)
      if mainl == 2:
        return CommandList(num)
      if mainl == 3:
        return QCCMDList(num)
  else:
    warwindows(screen, "警告", "未能找到任何RAID卡")
    return mainform()

def QCCMDList(num):
  li = Listbox(height = 12, width = 35, returnExit = 1, showCursor = 0, scroll = 1)
  li.append("a)将所有空余磁盘做成单盘RAID-0", 1)
  li.append("b)清除所有磁盘组配置", 2)
  li.append("c)定位磁盘(磁盘灯闪烁)", 3)
  li.append("d)打开/关闭JBOD模式", 4)
  li.append("e)刷新缓存", 5)
  bb = CompactButton('返回')
  g = GridForm(screen, "命令清单", 1, 10)
  g.add(li, 0, 1)
  g.add(bb, 0, 2)
  rc = g.runOnce(44, 3)
  if rc == 'ESC' or "snack.CompactButton" in str(rc):
    return ADPSelect()
  elif li.current() == 1:
    return MakeAllRaid0(num)
  elif li.current() == 2:
    return ClearCFG(num)
  elif li.current() == 3:
    return LocateDisk(num)
  elif li.current() == 4:
    return JBODMode(num)
  elif li.current() == 5:
    return FlushAdpCache(num)
  return mainform()

def MakeAllRaid0(num):
  rx = conformwindows(screen, "确认将所有空余的盘做成Raid-0吗")
  if rx[0] == "否" or rx[1] == "ESC":
    return QCCMDList(num)
  ss = ProWin(screen, "请等待", "创建磁盘组中")
  ss.show()
  ss.update(3)
  r, t, y = client.exec_command(megacli + " -CfgEachDskRaid0 -wt -ra -cached -nocachedbadbbu -strpsz128 -a" + str(num).strip('\n') + " -nolog | grep 'Created VD' | awk -F ' ' '{print$5}'")
  k = t.readlines()
  if k ==[]:
    ss.close()
    warwindows(screen, "警告", "单盘Raid-0创建失败")
    return QCCMDList(num)
  n = 5
  for i in k:
    r, t, y = client.exec_command(megacli + " -ldsetprop -disdskcache -l" + str(i).strip('\n') + " -a" + str(num).strip('\n') + " -nolog")
    ss.update(n+1)
  ss.close()
  warwindows(screen, "完成", "单盘Raid-0创建成功")
  return QCCMDList(num)

def ClearCFG(num):
  warwindows(screen, "抱歉", "研发中...")
  return QCCMDList(num)

def LocateDisk(num):
  p = GetPDInfo(num)
  pdisknum = p.pdisknum()
  pdiskrnum = p.pdiskrnum()
  pdtotalnum = p.pdtotalnum()
  pdshow = p.pdshow()
  pdsize = p.pdsize()
  pdstate = p.pdstate()
  pdslnum = p.pdslnum()
  n = 0
  li = Listbox(height = 20, width = 100, returnExit = 1, showCursor = 0, scroll = 1)
  if pdisknum != []:
    for i in pdshow:
      li.append(str(i).strip('\n').replace('Slot Number','槽位') + "\t大小: " + str(pdsize[n]).strip('\n') + "\t状态: " + str(pdstate[n]).strip('\n').replace(' ',''), n + 1)
      n = n + 1
    g = GridForm(screen, "选择需要定位的磁盘", 1, 10)
    bb = CompactButton('返回')
    g.add(li, 0, 1)
    g.add(bb, 0, 2)
    rc = g.runOnce(2,3)
    if "snack.CompactButton" in str(rc) or rc == 'ESC':
      return QCCMDList(num)
    else:
      selectPD = int(li.current() - 1)
    r, t, y = client.exec_command(megacli + " -pdlocate -start -physdrv [" + str(pdiskrnum[selectPD]).strip('\n') + ":" + str(pdslnum[selectPD]).strip('\n') + "] -a" + num + " -nolog")
    pd = t.read()
    if 'Start Command was successfully sent to Firmware' in pd:
      warwindows(screen, "开始定位", "请在面板上查看，按下确定停止定位")
      r, t, y = client.exec_command(megacli + " -pdlocate -stop -physdrv [" + str(pdiskrnum[selectPD]).strip('\n') + ":" + str(pdslnum[selectPD]).strip('\n') + "] -a" + num + " -nolog")
      pd = t.read()
      return QCCMDList(num)
    else:
      screen.finish()
      print s
      return 
      warwindows(screen, "失败", "无法定位磁盘")
      return QCCMDList(num)
  else:
    warwindows(screen, "警告", "未能找到磁盘")
    return details1(num)
  return QCCMDList(num)

def JBODMode(num):
  r, t, y = client.exec_command(megacli + " -adpallinfo -a" + num + " -nolog | grep 'JBOD                       ' | awk -F ': ' '{print$2}'")
  getjbodmode = t.read()
  if 'Yes' in getjbodmode:
    rx = conformwindows(screen, "确认关闭JBOD模式吗？")
    if rx[0] == "否" or rx[1] == "ESC":
      return QCCMDList(num)
    ss = ProWin(screen, "请等待", "关闭JBOD模式中..此操作耗时较长")
    ss.show()
    ss.update(30)
    r, t, y = client.exec_command(megacli + " -adpsetprop enablejbod -0 -a" + str(num).strip('\n') + " -nolog")
    k = t.read()
    if "Disable success" in k:
      ss.close()
      warwindows(screen, "完成", "JBOD模式已经关闭")
      return QCCMDList(num)
    ss.close()
    warwindows(screen, "警告", "JBOD模式关闭失败")
    return QCCMDList(num)
  rx = conformwindows(screen, "确认启用JBOD模式吗？")
  if rx[0] == "否" or rx[1] == "ESC":
    return QCCMDList(num)
  ss = ProWin(screen, "请等待", "打开JBOD模式中..此操作耗时较长")
  ss.show()
  ss.update(30)
  r, t, y = client.exec_command(megacli + " -adpsetprop enablejbod -1 -a" + str(num).strip('\n') + " -nolog")
  k = t.read()
  if "Enable success" in k:
    ss.close()
    warwindows(screen, "完成", "JBOD模式已经打开")
    return QCCMDList(num)
  else:
    ss.close()
    warwindows(screen, "警告", "JBOD模式打开失败")
    return QCCMDList(num)

def FlushAdpCache(num):
  rx = conformwindows(screen, "此操作将把RAID卡内缓存数据刷入磁盘")
  if rx[0] == "否" or rx[1] == "ESC":
    return QCCMDList(num)
  ss = ProWin(screen, "请等待", "写入中")
  ss.show()
  ss.update(30)
  r, t, y = client.exec_command(megacli + " -AdpCacheFlush -a" + str(num).strip('\n') + " -nolog")
  k = t.read()
  if 'successfully' in str(k):
    ss.close()
    warwindows(screen, "完成", "缓存数据已经写入磁盘")
    return QCCMDList(num)
  else:
    ss.close()
    warwindows(screen, "警告", "缓存数据回写失败")
    return QCCMDList(num)
  return QCCMDList(num)

def mainform():
#主界面
  sc()
  global mainl
  global adpl
  global getconfig
  adpl = 1
  li = Listbox(height = 15, width = 18, returnExit = 1, showCursor = 0)
  li.append("a)查看状态信息", 1)
  li.append("b)RAID卡配置", 2)
  li.append("c)快捷功能", 3)
  li.append("d)切换远程主机", 4)
  li.setCurrent(mainl)
  bb = CompactButton('|->退出<-|')
  g = GridForm(screen, "PtBUS", 1, 10)
  g.add(li, 0, 1)
  g.add(bb, 0, 2)
  g.add(Label(" "),0,3)
  g.add(Label("[LSI RAID卡]"),0,4)
  g.add(Label("[配置程序]"),0,5)
  g.add(Label("IP:" + ip + ""),0,6)
  screen.pushHelpLine("<Version 0.91 remote beta> Powered by Patrick Zheng...请使用TAB在选项间切换")
  rc=g.run(1,3)
  mainl = li.current()
  if rc == 'ESC' or 'snack.CompactButton' in str(rc) :
    return QUIT()
  if li.current() == 1:
    return ADPSelect()
  elif li.current() == 2:
    return ADPSelect()
  elif li.current() == 3:
    return ADPSelect()
  elif li.current() == 4:
    getconfig = config(getconfig)

def main():
  try:
    mainform()
  except:
    screen.finish()
    print traceback.format_exc()

def configwindows(screen, title, text, prompts, allowCancel = 1,
        width = 40, entryWidth = 20, buttons = [ '确定', '取消' ], 
        help = None):
    bb = ButtonBar(screen, buttons);
    t = TextboxReflowed(width, text)
    count = 0
    for n in prompts:
        count = count + 1
    sg = Grid(2, count)
    count = 0
    entryList = []
    for n in prompts:
        if str(n) == '密码：':
          e = e = Entry(entryWidth, password = 1)
        else :
          e = Entry(entryWidth, password = 0)
        sg.setField(Label(n), 0, count, padding=(0, 0, 1, 0), anchorRight=1)
        sg.setField(e, 1, count, anchorLeft=1)
        count = count + 1
        entryList.append(e)
    g = GridFormHelp(screen, title, help, 1, 3)
    g.add(t, 0, 0, padding = (0, 0, 0, 1))
    g.add(sg, 0, 1, padding = (0, 0, 0, 1))
    g.add(bb, 0, 2, growx = 1)
    result = g.runOnce(20,5)
    entryValues = []
    count = 0
    for n in prompts:
        entryValues.append(entryList[count].value())
        count = count + 1
    return (result, bb.buttonPressed(result), tuple(entryValues))

def config(getconfig = None):
  sc()
  global out
  global connectok
  set2 = getconfig
  screen.pushHelpLine("<Version 0.91 remote beta> Powered by Patrick Zheng...请使用TAB在选项间切换")
  set = configwindows(screen,"远端环境设定", "请输入远端信息", ["IP地址：","端口(一般是22): ", "用户名(需要root权限)：", "密码："], width = 60, entryWidth = 30, buttons = ["确定","取消"])
  if set[0] == "ESC" or set[1] == "取消":
    rx = conformwindows(screen, "要继续配置吗？")
    if rx[0] == "否" or rx[1] == "ESC":
      if connectok != 0:
        return set2
      out = 1
      return
    return config()
  return set


reload(sys)  
sys.setdefaultencoding('utf8')
connectok = 0
mainl = 1
adpl = 1
out = 0
getconfig = config()
while out != 1:
  if getconfig != None:
    try:
      client = paramiko.SSHClient()  
      client.load_system_host_keys()  
      ip = str(getconfig[2][0])
      port = int(getconfig[2][1])
      username = str(getconfig[2][2])
      password = str(getconfig[2][3])
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ss = ProWin(screen, "请等待", "远程链接创建中")
      ss.show()
      ss.update(35)
      client.connect(ip, port, username=username, password=password)
      sftpadd = paramiko.Transport((ip,port))
      ss.update(50)
      sftpadd.connect(username=username, password=password)
      sftp = paramiko.SFTPClient.from_transport(sftpadd)
      remotepath = '/tmp/storcli64'
      localpath = './storcli64'
      sftp.put(localpath,remotepath)
      sftpadd.close()
      client.exec_command("chmod +x /tmp/storcli64") 
      ss.close()
      connectok = 1
    except:
      screen.finish()
      print traceback.format_exc()
      print "指定的参数无效"
      break
    megacli = "/tmp/MegaCli64"
    r , test, t = client.exec_command(megacli + " -v -nolog")
    test = test.read()
    if "Exit Code: 0x00" in test: 
      main()
    else:
      screen.finish()
      print "远程命令执行失败"
      break
  else:
    warwindows(screen, "警告", "远程链接建立失败")
    getconfig = config()
screen.finish()
print "感谢使用!"