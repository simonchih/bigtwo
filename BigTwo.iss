; -- Example1.iess --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Simpy Big Two
AppVersion=0.3.3
DefaultDirName={pf}\Simpy Big Two
DefaultGroupName=Simpy Big Two
UninstallDisplayIcon={app}\main.exe
Compression=lzma2
SolidCompression=yes
OutputDir=E:\simpybigtwo

[Files]
Source: "E:\simpybigtwo\simpybigtwo_033\main.exe"; DestDir: "{app}"
Source: "E:\simpybigtwo\simpybigtwo_033\FreeSansBold.ttf"; DestDir: "{app}"
Source: "E:\simpybigtwo\simpybigtwo_033\readme.txt"; DestDir: "{app}"; Flags: isreadme
Source: "E:\simpybigtwo\simpybigtwo_033\Image\*.*"; DestDir: "{app}\Image"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Simpy Big Two"; Filename: "{app}\main.exe"; IconFilename: "{app}\Image\simpybigtwo_default.ico"
Name: "{group}\Uninstall Simpy Big Two"; Filename: "{uninstallexe}";
