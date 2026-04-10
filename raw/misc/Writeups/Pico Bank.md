[[APK]] [[Reverse Proxy]]
#completed 

In a bustling city where innovation meets finance, Pico Bank has emerged as a beacon of cutting-edge security. Promising state-of-the-art protection for your assets, the bank claims its mobile application is impervious to all forms of cyber threats. Pico Bank’s tagline, "Security Beyond the Limits," echoes through its high-tech marketing campaigns, assuring users of their utmost safety.As a cybersecurity enthusiast, your mission is to test these bold claims. You’ve been hired by a secretive organization to put Pico Bank’s mobile app through a rigorous security assessment. The flag might be in one or more locations, and additional information reveals that a Pico Bank user’s credentials were leaked in an unusual way. Your task is to crack the username and password based on the following profile information: His name is Alex Johnson with the email johnson@picobank.com, Date of Birth: March 14, 1990, Last Transaction Amount: $345.67, Pet name: tricky, and Favorite Color: Blue.To perform this challenge, you can use any Android emulator. Some examples include [Genymotion Android Emulator](https://www.genymotion.com/product-desktop/download/) or [Android Studio](https://developer.android.com/studio).Access the Pico Bank Website [Pico Bank Website](http://saffron-estate.picoctf.net:58246/) and download the application.

The given scenario is for an android app to be tested and penetrated. First download the apk given in the website and unpackage it with JadxGUI, which is a tool used for APK to produce java source code.

Given a little time, use the app and search for front end bugs if there is any way to get in the system without having to crack the password and username.

Based on the description it says that you should "crack" the username and password, but that is too unreliable and it should always be your last resort if there is no any other leads to follow.

When given the source code of the APK, analyze its directories and files.
![[Screenshot_20251031_110040.png]]

![[Screenshot_20251031_110952.png]]


After inspecting files, we can find out that the OTP is hardcoded and not need to analyze the server's response when handling otp request.
![[Screenshot_20251031_110826.png]]

You can also find out in the sources folder, that there is a .java file where the user credentials is hardcoded.
![[Screenshot_20251031_111118.png]]

