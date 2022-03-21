# BBBot_discord  

Discord Bot with multiple functions written in python.  
Chat response, Calculation, Earthquake notification, Translation, ydl, TTS on voice channel..

# Usage  
Add DiscordBot's [Token](https://discord.com/developers/applications) to [my_key.py](./modules/my_key.py) (TOKEN).  
Add Discord main channel id and bot logging channels id to [my_key.py](./modules/my_key.py) (LOG_C, MAIN_C) respectively.  
Run discordbot.py  

If you are using the "AI" class, add the [A3RT](https://a3rt.recruit-tech.co.jp/product/talkAPI/) key to [my_key.py](./modules/my_key.py) (A3RT_KEY).  
If you want to use "Translate" class, set up main.gs in Google Apps Script and add url to [my_key.py](./modules/my_key.py) (GoogleTranslateAPP_URL).  
  
# Command
BBBot v2.8.0b (prefix is "?")
```c
----- command examples

?B hello            // --> Hello B!
?add 1000 11        // --> 1011
?asc_enc aBBBcdefg  // --> 97 66 66 66 99 100 101 102 103
?timer 180          // --> 180s timer
?pomodoro           // --> Default pomodoro (?pomodoro 4 25 5)
?archive            // --> archive only 100 latest messages

----- sub class command examples

?v_music b_loop
?img abya
?img majiyaba
?archive full
```

### Command Class
```
AI:
  ai           a3rt AI TalkAPI

Archive:
  archive      Simple text archiving (only this channel)
  ms_cnt       message counter (count this channel) / This will take a long time

B:
  B            B (greet / sysinfo / hello / block / typing) -> ?help b
  BLOOP        BLOOP number<=11

BrainFuck:
  bf           Exec BrainF*ck
  bf_debug     Debug BrainF*ck

Calc:
  add          Add number + number
  calc         Calc number Eval
  div          Div number / number
  ent          EntropyFunc H(p)
  fractor      Factorization
  mul          Mul number * number
  rand         Random(int) 1~x
  randd        Random(float) 1.0~x
  self_info    Self-information I(p)
  sub          Sub number - number

Encode:
  asc_dec      ASCII Decode
  asc_enc      ASCII Encode

Image:
  b_img        b_img url file_name
  img          send img. (melt/abya/shiran/party/...) -> ?help img

Timer:
  pomodoro     pomodoro set, work(min), break(min)
  timer        Timer (s)

Translate:
  trans        Translate  English -> Japanese
  transJ       Translate Japanese -> English

URL:
  url_dec      URL decode
  url_enc      URL encode
  url_expand   Restore the shortened URL
  url_short    Generate shorter url

VoiceChat:
  v_add        add queue
  v_bd         Voice ALL D
  v_boice      Voice TTS (Japanese)
  v_boice_en   Voice TTS EN (English)
  v_connect    Voice Connect
  v_d          Voice Disconnect (same as ?v_disconnect)
  v_disconnect Voice Disconnect
  v_list       channel member list
  v_music      play music. (b/b_loop/b_list/stop/skip/queue/queue_del/play) -> ?help v_music
  v_mute       voice mute. (b = all)
  v_unmute     voice unmute. (b = all)
  v_voice      Voice TTS (Japanese) (same as ?v_boice)
  v_voice_en   Voice TTS EN (English) (same as v_boice_en)
  v_volume     change music volume

Youtube:
  ydl          youtube-dl audio only [ org ]
  ydl_aac      youtube-dl audio only [ aac ]
  ydl_m4a      youtube-dl audio only [ m4a ]
  ydl_mp3      youtube-dl audio only [ mp3 ]

No Category:
  help         Shows this message

-----
Sub class

VoiceChat.v_music:
  b            One song from Mr. B's recommendation
  b_list       b/b_loop brand list
  b_loop       infinity random play!
  bassboost 
  del_queue    delete queue
  nightcore 
  pause        pause music
  play         play queue
  queue        show queue
  resume       resume paused music
  skip         skip current music
  stop         stop music

Image.img:
  abya         abya picture
  b_pet        Pet the B GIF
  b_pic        B picture
  bohe         bohe
  gyu          gyu GIF
  ha           ha! GIF
  hello        hello GIF
  majiyaba     maji yabakune
  maken        maken GIF
  melt         melt picture
  onegai       onegai GIF
  party        party parrot GIF
  presen       gaming presentation GIF
  shiran       shiran kedo~ picture
  thx          thx GIF
 
 Archive.archive:
  full     Full archive of this channel. This will take a long time.
 
 B.b:
  block  
  button       B button
  greet   
  hattori      htr 
  hello   
  many_b       1011 of B
  more_b       11*1024 of B (11KB)
  most_b       11*1024**2 of B (11MB)
  ping    
  sysinfo 
  typing 
 ```
