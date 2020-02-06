import vlc, easygui
media = easygui.fileopenbox(title="Choose media to open")
player = vlc.MediaPlayer(media)
image = "bigles.gif"
while True:
    choice = easygui.buttonbox(title="@biglesp Audio Player",msg="Press Play to start",image=image,choices=["Play","Pause","Stop","New"])
    print(choice)
    if choice == "Play":
        player.play()
    elif choice == "Pause":
        player.pause()
    elif choice == "Stop":
        player.stop()
    elif choice == "New":
        media = easygui.fileopenbox(title="Choose media to open")
        player = vlc.MediaPlayer(media)
    else:
        break