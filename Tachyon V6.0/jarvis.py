import os,sys,subprocess as sp,contextlib as cl,smtplib,time,random,re;from datetime import datetime;import xml.etree.ElementTree as ET,speech_recognition as sr;from gtts import gTTS
W,N,E,P,M="tachyon","Tachyon","your_email@gmail.com","your_app_password","recipient_email@gmail.com"
r,e,s,d,w,o,b=False,0,0,0,False,0,0
@cl.contextmanager
def ign():
 x=os.dup(2);sys.stderr.flush();os.dup2(os.open(os.devnull,os.O_WRONLY),2)
 try:yield
 finally:os.dup2(x,2);os.close(x)
def is_p():
 try:return'"Playing"' in sp.check_output(["dbus-send","--print-reply","--dest=org.mpris.MediaPlayer2.rhythmbox","/org/mpris/MediaPlayer2","org.freedesktop.DBus.Properties.Get","string:org.mpris.MediaPlayer2.Player","string:PlaybackStatus"],stderr=sp.DEVNULL).decode()
 except:return False
def spk(t,p=False):
 print(f"{N}: {t}");sp.run(["notify-send",f"{N} Assistant",str(t)]);mp=is_p()
 if mp:sp.run(["rhythmbox-client","--pause"],stderr=sp.DEVNULL,stdout=sp.DEVNULL)
 try:
  f="/tmp/s.mp3";gTTS(text=str(t),lang='en',tld='com').save(f);sp.run(["play","-q","-t","mp3",f]);os.remove(f) if os.path.exists(f) else None
 except:os.system(f"espeak '{t}'")
 if mp and not p:sp.run(["rhythmbox-client","--play"],stderr=sp.DEVNULL,stdout=sp.DEVNULL)
def f_s(q):
 try:
  for i in ET.parse(os.path.expanduser("~/.local/share/rhythmbox/rhythmdb.xml")).getroot().findall("entry"):
   if i.get("type")=="song":
    t,a,l=i.find("title"),i.find("artist"),i.find("location")
    if q.lower().strip() in (t.text.lower() if t is not None and t.text else "") or q.lower().strip() in (a.text.lower() if a is not None and a.text else ""):return l.text,t.text or q if l is not None and l.text else(None,None)
 except:pass
 return None,None
def g_cpu():
 try:return str(int(sp.check_output("cat /sys/class/thermal/thermal_zone*/temp",shell=True,stderr=sp.DEVNULL).decode().strip().split('\n')[0])//1000)+" °C"
 except:return"N/A"
def g_gpu():
 for c in ["nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits","rocm-smi --showtemp | grep 'GPU Temperature' | awk '{print $4}'","cat /sys/class/drm/card*/device/hwmon/hwmon*/temp1_input 2>/dev/null | head -n1"]:
  try:
   z=sp.check_output(c,shell=True,stderr=sp.DEVNULL).decode().strip()
   if z:return str(int(z)//1000 if 'cat' in c else z)+" °C"
  except:pass
 return"N/A"
def s_tm(m):global r,e,s,d;d=m*60;s=time.time();e=s+d;r=True;return True if m>0 else False
def g_sw():el=(time.time()-o) if w else b;return f"{int(el//60)}:{int(el%60):02d}"
def s_em(t,s,b):
 try:g=smtplib.SMTP('://gmail.com',587);g.starttls();g.login(E,P);g.sendmail(E,t,f"From: {E}\nTo: {t}\nSubject: {s}\n\n{b}");g.quit();return True
 except:return False
def l_and_c():
 global r,s,e,d,w,o,b;g=sr.Recognizer();g.energy_threshold,g.pause_threshold,g.non_speaking_duration=200,1.5,0.8
 with ign():m=sr.Microphone()
 with m as src:
  print(f"\n>>> [{W}]")
  try:
   if W in g.recognize_google(g.listen(src,timeout=10,phrase_time_limit=4)).lower():
    spk(f"{N}?");lc=time.time()
    while time.time()-lc<60:
     try:
      cmd=g.recognize_google(g.listen(src,timeout=6,phrase_time_limit=10)).lower();print(f"-> {cmd}");lc=time.time()
      if cmd in["play","play music","resume"]:sp.run(["rhythmbox-client","--play"]);spk("Resuming.")
      elif cmd in["pause","pause music","stop"]:sp.run(["rhythmbox-client","--pause"]);spk("Paused.",True)
      elif cmd in["next","next song","skip"]:sp.run(["rhythmbox-client","--next"]);spk("Skipped.")
      elif cmd in["previous","previous song","back"]:sp.run(["rhythmbox-client","--previous"]);spk("Back.")
      elif any(x in cmd for x in["what song","what is playing","recognize"]):
       try:spk(f"Track: {sp.check_output(['rhythmbox-client','--print-playing'],stderr=sp.DEVNULL).decode().strip() or 'None.'}")
       except:spk("Player err.")
      elif any(x in cmd for x in["play song","play track"]):
       q=cmd.replace("play the song","").replace("play track","").replace("play","").strip();u,t=f_s(q)
       spk(f"Playing {t}." if u else f"No {q}.")
       sp.run(["rhythmbox-client",f"--play-uri={u}"]) if u else None
      elif "volume up" in cmd or "increase volume" in cmd:sp.run(["amixer","-D","pulse","sset","Master","10%+"],stdout=sp.DEVNULL);spk("Vol up.")
      elif "volume down" in cmd or "decrease volume" in cmd:sp.run(["amixer","-D","pulse","sset","Master","10%-"],stdout=sp.DEVNULL);spk("Vol down.")
      elif "mute" in cmd or "silence volume" in cmd:sp.run(["amixer","-D","pulse","sset","Master","toggle"],stdout=sp.DEVNULL);spk("Muted.")
      elif "lock" in cmd:spk("Locking.");sp.run(["cinnamon-screensaver-command","--lock"])
      elif "sleep" in cmd or "suspend" in cmd:spk("Sleeping.",True);sp.run(["systemctl","suspend"])
      elif "time" in cmd:
       if " in " in cmd:
        try:
         cy=cmd.split(" in ")[-1].strip().replace(" ","_");tz=sp.check_output(f"find /usr/share/zoneinfo/ -type f,l -iname '*{cy}*' | head -n 1",shell=True).decode().strip().replace("/usr/share/zoneinfo/","")
         spk(f"In {cy.title()}: {sp.check_output(f'TZ={tz} date +%I:%M_%p',shell=True).decode().strip()}.")
        except:spk("TZ err.")
       else:spk(f"Time: {datetime.now().strftime('%I:%M %p')}.")
      elif any(x in cmd for x in["open","launch","start"]):
       ap={"browser":["xdg-open","https://google.com"],"chrome":["google-chrome"],"firefox":["firefox"],"terminal":["cinnamon-terminal"],"files":["nemo"],"calculator":["gnome-calculator"],"editor":["gedit"],"jellyfin":["sh","-c","jellyfin-desktop || flatpak run org.jellyfin.JellyfinDesktop || xdg-open http://localhost:8096"]}
       fl=False
       for k,v in ap.items():
        if k in cmd:spk(f"Opening {k}.");sp.Popen(v,stdout=sp.DEVNULL,stderr=sp.DEVNULL);fl=True;break
       if not fl:spk("No map.")
      elif any(x in cmd for x in["status","system","metrics"]):
       try:spk(f"Disk: {sp.check_output('df -h / | awk \"NR==2 {print \$4}\"',shell=True).decode().strip()}, RAM: {sp.check_output('free -h | awk \"NR==2 {print \$7}\"',shell=True).decode().strip()}, CPU: {g_cpu()}, GPU: {g_gpu()}.")
       except:spk("Active.")
      elif any(x in cmd for x in["cpu temp","temperature","temps","gpu temp"]):spk(f"CPU: {g_cpu()}, GPU: {g_gpu()}")
      elif "weather" in cmd or "forecast" in cmd:
       try:spk(f"Weather: {sp.check_output('curl -s \"wttr.in/?format=%C+and+%t\"',shell=True).decode().strip()}")
       except:spk("Weather err.")
      elif any(x in cmd for x in["timer","set timer","countdown"]):
       p,mins=cmd.split(),0
       for i,w_item in enumerate(p):
        try:
         if w_item in["minutes","min","m"] and i>0:mins=int(p[i-1])
         elif w_item in["hour","hours","h"] and i>0:mins=int(p[i-1])*60
        except:pass
       spk(f"Timer set: {mins}m." if s_tm(mins) else "No min.")
      elif any(x in cmd for x in["stop timer","pause timer","cancel timer"]):d=max(0,e-time.time()) if r else d;r=False;spk("Timer paused.")
      elif any(x in cmd for x in["resume timer","continue timer"]):
       if r:spk("Running.")
       else:r,s=True,time.time();e=s+d;spk("Resumed.")
      elif any(x in cmd for x in["remaining","time left"]):rem=int(max(0,e-time.time())) if r else None;spk(f"Left: {rem//60}m, {rem%60}s." if rem is not None else "No timer.")
      elif any(x in cmd for x in["stopwatch","start stopwatch","lap"]):
       if cmd in["lap","start stopwatch"] and not w:o=time.time()-b;w=True;spk("SW started.")
       elif any(x in cmd for x in["pause","stop"]) and w:b=time.time()-o;w=False;spk("SW paused.")
       spk(f"SW: {g_sw()}.")
      elif any(x in cmd for x in["reset stopwatch","clear stopwatch"]):w,o,b=False,0,0;spk("SW reset.")
      elif "surprise" in cmd:spk(f"Surprise! {random.choice(['Eiffel grows in summer.','Honey never spoils.','Octopuses have 3 hearts.','Flamingos flock is a stand.'])}")
      elif "fart" in cmd:
       spk("Excuse me...");sp.run(["play","-q","-n","-t","sine","freq","300","rate","8000","length","0.2","repeat","5","remix","1"],stderr=sp.DEVNULL);spk("BRAAAAAP!")
      elif any(x in cmd for x in["calendar","today","tomorrow"]):
       try:spk(sp.check_output("gcalcli --nocolor cal",shell=True,stderr=sp.DEVNULL).decode().strip() or "No events.")
       except:spk("No cal.")
      elif "files" in cmd and "in" in cmd:
       try:
        fld=cmd.split("in ",1)[1].strip();target=os.path.expanduser(fld) if not fld.startswith('/') else fld
        spk(f"Files: {'/'.join([f for f in os.listdir(target) if os.path.isfile(os.path.join(target,f))][:20])[:500]}")
       except:spk("Fld err.")
      elif "email" in cmd:
       try:
        tm,sm,bm=re.search(r"to\s+([\w.-]+@\w+\.\w+)",cmd),re.search(r"subject\s+(.+?)(?=\s*saying|$)",cmd),re.search(r"saying\s+(.+)",cmd)
        spk("Email sent!" if(tm and sm and bm and s_em(tm.group(1).strip(),sm.group(1).strip(),bm.group(1).strip())) else "Email missing info.")
       except:spk("Email err.")
      elif any(x in cmd for x in["show commands","list commands","what can you do"]):spk("I do music, shortcuts, files, cal, mail, weather, system status, timers, stopwatches.")
      elif any(x in cmd for x in["version","about","who are you"]):spk(f"I am {N}, your personal assistant.")
      elif any(x in cmd for x in["off","shut down","goodbye"]):spk("Goodbye.",True);return False
     except sr.WaitTimeoutError:continue
     except Exception as e_err:print(f"Cmd Err: {e_err}")
   else:return True
  except:pass
 return True
if __name__=="__main__":
 os.system('clear');spk(f"{N} online.");run=True
 while run:run=l_and_c()


