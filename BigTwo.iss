; -- Example1.iess --
; Demonstrates copying 3 files and creating an icon.

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=Simpy Big Two
AppVersion=0.3.6
DefaultDirName={pf}\Simpy Big Two
DefaultGroupName=Simpy Big Two
UninstallDisplayIcon={app}\main.exe
Compression=lzma2
SolidCompression=yes
OutputDir=D:\bigtwo

[Files]
Source: "D:\bigtwo\simpybigtwo_036\main.exe"; DestDir: "{app}"
Source: "D:\bigtwo\simpybigtwo_036\FreeSansBold.ttf"; DestDir: "{app}"
Source: "D:\bigtwo\simpybigtwo_036\readme.txt"; DestDir: "{app}"; Flags: isreadme
Source: "D:\bigtwo\simpybigtwo_036\Image\*.*"; DestDir: "{app}\Image"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Simpy Big Two"; Filename: "{app}\main.exe"; IconFilename: "{app}\Image\simpybigtwo_default.ico"
Name: "{group}\Uninstall Simpy Big Two"; Filename: "{uninstallexe}";
