# RainSnek
a Discord bot that uses wunderground's API to tell you the weather.

## Triggers:
1. @<botname> weather (ex whats the weather (uses default city and state))
    * "tonight" (whats the weather tonight)
    * "today" (Whats the weather today)
    * "this week" (whats the weather this week)
2. @<botname> weather in (ex whats the weather in toronto canada (defaults the state to NC if not specified))
3. @<botname> "the high" or "the low" (Displays todays high and low)
4. @<botname> "sat" or "satellite" (Display the local satellite)
5. @<botname> "radar" (Display the local radar)
6. @<botname> "version" (Display the bot version)
5. @<botname> "reload" (Download the new bot, then exit) (must be whitelisted)
### Usage in conversation of
1. "weather in" (fetches city and or state)
2. "the weather" (uses default city and state)
    * "tonight" (whats the weather tonight)
    * "today" (Whats the weather today)
    * "this week" (whats the weather this week)
3. "the high today" or "the low today" (Displays todays high and low)
4. "weather sat" (Display the local satellite)
5. "weather radar" (Display the local radar)

---------
apiKeys.json should look like:

```
{
    "discord": "MzgspecialdiscordcodeKt0thatskindalongrcYanddoesthings",
    "wunderground": "yourspecialcode",
    "fileUrl": "https://wesring.com/RainSnek.py",
    "ownerid":  "01189998819991197253"
}
```

--------
Copyright 2017 Wesley Ring

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

