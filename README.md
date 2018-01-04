# Audio Calculator

This sample app leverages Microsoft Bing Speech APIs to offer the functionality of a (very) basic calculator. 

In order to run the app, you just need to execute the Python script without parameters (the script has been tested with Python 3.6). Note you need to install a couple of dependencies before, notably pyaudio and speech_recognition (the Python SDK for Microsoft Bing Speech API).

After successfully executing the program, you need to specify your API's key upon start. In order to get a key you need to have deployed the Speech API in your Azure subscription.

The calculator is in German (one of the purposes of the demo is showing the Speech API in a non-English language). After supplying the key, you can just dictate basic math operations such as "zwei plus zwei" or "fünf mal sechs". The calculator will return an audio sentence such as "Das Ergebnis ist vier".

You can expand this basic example to build more complex apps, even including Natural Language Processing programming for example with Microsoft LUIS cognitive service.