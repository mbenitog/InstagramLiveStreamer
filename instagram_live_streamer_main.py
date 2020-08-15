import os, sys, json, time
import restream_control as rc
import instagram_live_controls as ilc
from InstagramAPI import InstagramAPI
from inputimeout import inputimeout, TimeoutOccurred


def ask_rs_login():
    print('\033[1m' + "\nRestream login" + '\033[0m' + "\nChrome will now open. The window will close automatically when the session is detected.")
    time.sleep(2)
    rc.change_key("", True)


def ask_ig_login():
    print('\033[1m' + "\nInstagram login" + '\033[0m')
    try:
        with open(sys.argv[0][:sys.argv[0].rfind("/")] + '/login.json', 'r') as infile:
            json.load(infile)
        file_ava = True
    except:
        file_ava = False

    if file_ava:
        lcf = input("Do you want to log-in with the saved credentials? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": ")
        while not lcf in ("y", "Y", "n", "N"):
            lcf = input("\nAnswer Y for yes or N for no. Do you want to log in with the saved credentials? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": ")

        if lcf in ("y", "Y"):
            with open(sys.argv[0][:sys.argv[0].rfind("/")] + '/login.json', 'r') as infile:
                data = json.load(infile)
            user = data[0]
            password = data[1]
        elif lcf in ("n", "N"):
            user = input("Username: ")
            password = input("Password: ")

            gc = input("Do you want to save your credentials? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": ")
            while not gc in ("y", "Y", "n", "N"):
                gc = input("\nAnswer Y for yes or N for no. Do you want to save your credentials? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": " )

            if gc in ("y", "Y"):
                data = user, password
                with open(sys.argv[0][:sys.argv[0].rfind("/")] + '/login.json', 'w') as outfile:
                    json.dump(data, outfile)

    else:
        user = input("Username: ")
        password = input("Password: ")

        gc = input("Do you want to save your credentials?" + '\033[92m' + "(y\\n)" + '\033[0m' + ": " )
        while not gc in ("y", "Y", "n", "N"):
            gc = input("\nAnswer Y for yes or N for no. Do you want to save your credentials? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": " )

        if gc in ("y", "Y"):
            data = user, password
            with open(sys.argv[0][:sys.argv[0].rfind("/")] + '/login.json', 'w') as outfile:
                json.dump(data, outfile)

    print("Trying login..." + '\033[30m')
    api = InstagramAPI(user, password, debug=False)

    if not (api.login()):
        if api.LastJson['message'] == "challenge_required":
            print('\033[91m' + "It looks like Instagram has banned your machine\nGo to https://www.instagram.com/challenge/ to fix the issue\nClosing ..." + '\033[0m')
            sys.exit()
        print('\033[91m' + "Invalid credentials\nClosing..." + '\033[0m')
        sys.exit()
    print('\033[0m' + "Login success!")
    return api

def initial_stream_config():
    print('\033[1m' + "\nStream configuration" + '\033[0m')

    res_opt = input("At which resolution do you wish to stream?\n\n"
                    "Options:\n1.1920x1080 (16:9)\n2.1280x720 (16:9)\n3.1080x1920 (9:16)\n4.720x1280 (9:16)\n5.Custom\n"
                    "\nChoose an option: ")

    while not res_opt in ("1", "2", "3", "4", "5"):
        res_opt = input("Write a number from 1 to 5 to select the resolution: ")

    if res_opt == "1":
        resolution = [1920, 1080]
    elif res_opt == "2":
        resolution = [1280, 720]
    elif res_opt == "3":
        resolution = [1080, 1920]
    elif res_opt == "4":
        resolution = [720, 1280]
    if res_opt == "5":
        res = input("\nIntroduce the resolution ([width]x[height]): ")
        while not "x" in res:
            res = input("Introduce the resolution with the following format [width]x[height] (ex. 1920x1080): ")
        resolution = list(map(int, res.split("x")))

    plf = input("Keep stream in Stories? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": " )
    while not plf in ("y", "Y", "n", "N"):
        plf = input("Answer Y for yes or N for no. Keep stream in Stories? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": " )

    if plf in ("y", "Y"):
        publish_to_live_feed = True
    elif plf in ("n", "N"):
        publish_to_live_feed = False

    sn = input("Do you want to notify your followers? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": ")
    while not sn in ("y", "Y", "n", "N"):
        sn = input("Answer Y for yes or N for no. Do you want to notify your followers? " + '\033[92m' + "(y\\n)" + '\033[0m' + ": ")

    if sn in ("y", "Y"):
        send_notifications = True
    elif sn in ("n", "N"):
        send_notifications = False


    return resolution, publish_to_live_feed, send_notifications


def start_stream(api, res, send_notifications):
    assert ilc.createBroadcast(api, res)
    broadcast_id = api.LastJson['broadcast_id']
    upload_url = api.LastJson['upload_url']

    assert ilc.startBroadcast(api, broadcast_id, send_notifications)

    return broadcast_id, upload_url


def stop_stream(api, broadcast_id, PUBLISH_TO_LIVE_FEED):
    assert ilc.stopBroadcast(api, broadcast_id)
    if PUBLISH_TO_LIVE_FEED:
        ilc.addBroadcastToFeed(api, broadcast_id)
        print('\nStream saved in Stories.')


def live_stream(api, interval, res, publish_to_live_feed, send_notifications):
    while True:
        try:
            broadcast_id, url = start_stream(api, res, send_notifications)
            key = url[43:]
            print("\n" + url[:43] + "\n" + key)
            rc.change_key(key, False)
            restart = inputimeout('\033[96m' + "\nDo you want to manually restart the stream?\nIf you want to continue, don't write anything.\nIt will restart automatically in " + str(interval/60) + " minutes." + '\033[92m' + "\n\n(Write R to restart it \\ Write ANY other letter(s) to close and exit)\n" + '\033[96m' + "After writing your command, press return to send it: " + '\033[0m', interval)
            if restart in ("r", "R"):
                continue
            else:
                stop_stream(api, broadcast_id, publish_to_live_feed)
                print("Stream ended successfully.")
                break

        except TimeoutOccurred:
            print('\033[1m' + "\n" + str(interval) + " seconds elapsed. Restarting stream." + '\033[0m')
            stop_stream(api, broadcast_id, publish_to_live_feed)
            continue


        except:
            stop_stream(api, broadcast_id, publish_to_live_feed)
            print('\033[91m' + 'Something went wrong... Stream closed successfully.' + '\033[0m')
            break


ask_rs_login()

api = ask_ig_login()

RESOLUTION, PUBLISH_TO_LIVE_FEED, SEND_NOTIFICATIONS = initial_stream_config()

live_stream(api, 3540, RESOLUTION, PUBLISH_TO_LIVE_FEED, SEND_NOTIFICATIONS)

print('\033[95m' + 'Stream ended' + '\033[0m')
