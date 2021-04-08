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
BBBot v2.4.3 (prefix is "?")
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
| BLOOP | send meny "B". (BLOOP number<=11) ex: `?BLOOP 5`|
  
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
| abya | abya picture |
| b_img | b_img url file_name |
| b_pic | B picture |
| melt | melt picture |
| party | party parrot GIF |
| presen | gaming presentation GIF |
| shiran | shiran kedo~ picture |

**Translate** (v2.3.1+)
| command | outline |
--- | ---
| trans | Translate  English -> Japanese |
| transJ | Translate Japanese -> English |

**VoiceChat** (v2.4.0+)
| command | outline |
--- | ---
| v_bd | ALL D |
| v_boice | Voice TTS (Japanese) |
| v_boice_en | Voice TTS (English) |
| v_connect | Voice Connect |
| v_disconnect | Voice Disconnect |

**ydl**
| command | outline |
--- | ---
| ydl | youtube-dl audio only [ org ] |
| ydl_m | youtube-dl audio only [ mp3 ] |
| ydl_m4a | youtube-dl audio only [ m4a ] |
| ydl_m4a_min | youtube-dl audio only [ m4a 128kbps ] |

**Timer** (v2.4.3+)
| command | outline |
--- | ---
| timer | Timer (s)  🍜`?timer 180` |
| pomodoro | set, work(min), break(min). Default: `?pomodoro 4 25 5` |

**URL** (v2.4.4+)
| command | outline |
--- | ---
| url_short | Generate Shorter URL |
| url_expand | Restore the shortened URL |
| url_enc | URL encode |
| url_dec | URL decode |
