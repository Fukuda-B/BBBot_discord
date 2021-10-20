# BBBot_discord  

Discord Bot with multiple functions written in python.  
Chat response, Calculation, Earthquake notification, Translation, ydl, TTS on voice channel..

---  
# Usage  
Add DiscordBot's [Token](https://discord.com/developers/applications), Channel to "my_key.py".  
Run discordbot."version".py  

If you are using the "AI" class, add the [A3RT](https://a3rt.recruit-tech.co.jp/product/talkAPI/) key to "my_key.py".  
If you want to use "Translate" class, set up main.gs in Google Apps Script and add url to "my_key.py".  

---  
  
# Command list
BBBot v2.6.13 (prefix is "?")
```c
?B hello            // -> Hello B!
?add 1000 11        // -> 1011
?asc_enc aBBBcdefg  // -> 97 66 66 66 99 100 101 102 103
```
**AI**
| command | outline |
--- | ---
| ai | a3rt AI TalkAPI  |
  
 **B**
 | command | outline |
--- | ---
| B greet | show version |
| B sysinfo | show execution environment (CPU, MEM, OS..) |
| B hello | Hello B! |
| B block | show block B |
| B typing | set typing state |
| B hattori | ﾊｯﾄﾘｨ- |
| BLOOP | send meny "B". (BLOOP number<=11) ex: `?BLOOP 5`|
  
 **BrainFuck** based on [BrainF-ck.py](https://github.com/Fukuda-B/BrainF-ck_py)
 | command | outline |
--- | ---
| bf | Exec BrainF\*ck |
| bf_debug | Debug BrainF\*ck |

 **Calc**
| command | outline |
--- | ---
| add | Add number + number |
| sub | Sub number - number |
| div | Div number / number |
| mul | Mul number * number |
| calc | Calc number Eval |
| ent | EntropyFunc H(p) |
| rand | Random(int) 1~x |
| randd | Random(float) 1.0~x |
| self_info | Self-information I(p) |

**Encode**
| command | outline |
--- | ---
| asc_dec | ASCII Decode |
| asc_enc | ASCII Encode |

**Image**  
| command | outline |
--- | ---
| b_img | b_img url file_name |
| img abya | abya picture |
| img b_pic | B picture |
| img melt | melt picture |
| img party | party parrot GIF |
| img presen | gaming presentation GIF |
| img shiran | shiran kedo~ picture |
| img majiyaba | maji yabakune |
| img bohe | bohe~ |
| img gyu | gyu GIF |
| img ha | ha! GIF |
| img hello | hello GIF|
| img maken | maken GIF |
| img onegai | onegai GIF |
| img b_pet | Pet the B !! |

**Translate**
| command | outline |
--- | ---
| trans | Translate  English -> Japanese |
| transJ | Translate Japanese -> English |

**VoiceChat**
| command | outline |
--- | ---
| v_bd | ALL D (Disconnect) |
| v_boice | Voice TTS (Japanese) |
| v_voice | Voice TTS (Japanese) (same as v_boice) |
| v_boice_en | Voice TTS (English) |
| v_voice_en | Voice TTS (English) (same as v_voice_en) |
| v_connect | Voice Connect |
| v_disconnect | Voice Disconnect |
| v_d | Voice Disconnect (same as v_disconnect) |
| v_list | voice channel member list |
| v_mute | mute member's voice (b = all) |
| v_unmute | unmute member's voice (b = all) |
| | |
| v_add "url" | add queue |
| v_volume | volume ( 0.0 - 1.0 ) |
| v_music b | recommended (random) |
| v_music b_loop | recommended (random & loop) |
| v_music b_loop "brand name" | select brand name (random & loop) |
| v_music b_list | recommended brand list |
| v_music "url" | youtube player |
| v_music skip | skip to next song |
| v_music queue | show queue |
| v_music queue_del | delete queue |
| v_music play | playback |
| v_music stop | stop playback |
| v_music pause | pause music |
| v_music resume | resume paused music |
| v_music nightcore | nightcore effect toggle |
| v_music bassboost | bassboost effect toggle |

**ydl**
| command | outline |
--- | ---
| ydl | youtube-dl audio only [ org ] |
| ydl_mp3 | youtube-dl audio only [ mp3 ] |
| ydl_m4a | youtube-dl audio only [ m4a ] |
| ydl_aac | youtube-dl audio only [ aac ] |

**Timer**
| command | outline |
--- | ---
| timer | Timer (s)  🍜`?timer 180` |
| pomodoro | set, work(min), break(min). Default: `?pomodoro 4 25 5` |

**URL**
| command | outline |
--- | ---
| url_short | Generate Shorter URL |
| url_expand | Restore the shortened URL |
| url_enc | URL encode |
| url_dec | URL decode |

**Archive**
| command | outline |
--- | ---
| ms_cnt | message counter |
| archive | Simple text arching |
| archive full | fill arching |
