# 🪟📢 TTS HTTP server

A simple HTTP server that exposes the high-quality text-to-speech (TTS) service of the OS to other machines, especially Linux ones that have inferior TTS. The original purpose was to run this on Windows 10/11 (since we were unsatisfied with Linux's TTS performance), but you can actually use it on Linux (with epos) and Mac (with NSSS) as well.

Created for the Deace summer event which famously uses TTS public announcements. This is purposefully a very simple component, since the Raspberry Pi's used for the rest of the event's IT infrastructure can't run Windows, and thus this is expected to run on someone's personal laptop.

## 🛠️ Installation

The installation instructions assume Windows 11.

1. Go into **Settings > Time & language > Manage voices > Add voices** and install the voices you want.
2. Open a PowerShell administrative shell (**right-click Start > Terminal (admin)**), paste and run the following snippet:
    
    ```powershell
    ls 'HKLM:\software\Microsoft\Speech_OneCore\Voices\Tokens' | % {
        copy -r $_.PSPath 'HKLM:\SOFTWARE\Microsoft\Speech\Voices\Tokens'
        copy -r $_.PSPath 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\SPEECH\Voices\Tokens'
    }
    ```

    *This will unlock the TTS voices for other applications. No idea why this is necessary.*
3. Install [Python](https://www.python.org/downloads/) (at least version 3.10).
4. Install [Pipenv](https://pipenv.pypa.io/en/latest/) (`pip install pipenv`).
5. Open the project folder and run `pipenv install`.

After that, you can run the server using:

```powershell
pipenv run uvicorn --reload --port 8000 main:app
```

## 🔊 Usage

Try out using [HTTPie](https://httpie.org/):

```bash
http POST http://127.0.0.1:8000/read -- text=Hello voice=Zira -o output.wav
```

These are the available endpoints:

- `/voices`: returns a list of voices available for TTS
- `/read` accepts a JSON POST body with the following parameters, and returns a WAV file:
    - `text` is the text to be read.
    - `voice` is the name of the voice to be used. You can find the list of voices on the endpoint `/voices` (`http GET http://127.0.0.1:8000/voices`). You only need to specify a part of the voice's `name`, e.g. `Zira` will match `Microsoft Zira Desktop - English (United States)`.
    - `rate` is optional: integer, where 150 is about normal speed, 100 is slow, 200 is fast
