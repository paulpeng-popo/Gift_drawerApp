import pygsheets
import random as rd
import tkinter as tk
from PIL import Image, ImageTk

# -------------------------------------------------------------------- #
root = tk.Tk()
root.title("A simple login window")
root.configure(bg = "BlanchedAlmond")
root.geometry("600x300+550+200")

# -------------------------------------------------------------------- #
common = "https://docs.google.com/spreadsheets/d/"
url = "17YZ4geXbM_wc7WEiONyXQKl1RZmBQabu4gLybZ7z1Vs/"
grant = pygsheets.authorize(service_file="giftkey.json")
sheet = grant.open_by_url(common+url)
work = sheet.worksheet_by_title("gift_user")
img = ImageTk.PhotoImage(Image.open("xmas.png").resize((150, 150)))
message, name = "", ""
max_people = 5
login = False
draw_already = False

# -------------------------------------------------------------------- #
def init():

    # -------------------------------------------------------------------- #
    def named_title():
        direction = tk.Label(root, height = 1, width = 22,
                                   bg = "BlanchedAlmond", font = ("", 12),
                                   text = "Welcome to Xmas Gift System !!")
        direction.place(x = 20, y = 20)

        # -------------------------------------------------------------------- #
        def produce_image():
            picture = tk.Label(root, image = img, width = 150, height = 150)
            picture.place(x = 40, y = 80)

            # -------------------------------------------------------------------- #
            list_state = tk.Label(root, height = 1, width = 20,
                                        bg = "BlanchedAlmond", font = ("", 12),
                                        text = "ready")
            list_state.place(x = 400, y = 40)
            attender = tk.Label(root, height = 10, width = 20,
                                      bg = "BlanchedAlmond", font = ("", 12),
                                      text = "name_list")
            attender.place(x = 400, y = 100)

            # -------------------------------------------------------------------- #
            def drawing():
                global work, message, draw_already
                work.refresh()
                record = work.get_all_records()
                name_list = [ str(i["Name"]) for i in record ]
                send_list = name_list[:]

                # -------------------------------------------------------------------- #
                def test(name_list, send_list):
                    for i in range(len(name_list)):
                        if name_list[i] == send_list[i]:
                            return True
                    return False

                while(test(name_list, send_list)):
                    rd.shuffle(send_list)

                for i in range(len(send_list)):
                    work.update_value((i+2, 3), send_list[i])

                draw_already = True

                work.refresh()
                record = work.get_all_records()
                name_list = [ str(i["Name"]) for i in record ]
                send_list = [ str(i["Send_gift_to"]) for i in record ]
                send_name = send_list[name_list.index(name)]
                message["text"] = "You gift is to " + str(send_name) + " !"
                get_list()

            # -------------------------------------------------------------------- #
            draw = tk.Button(root, height = 1, width = 8,
                                   bg = "WhiteSmoke", text = "開始抽籤",
                                   cursor = "hand2", command = drawing)
            draw.place(x = 465, y = 260)
            draw["state"] = tk.DISABLED

            # -------------------------------------------------------------------- #
            def execute():
                global message
                username = tk.Label(root, height = 1, width = 20,
                                          bg = "BlanchedAlmond", font = ("", 12),
                                          text = "你的名字 ? (可中文)")
                username.place(x = 190, y = 80)
                nameinput = tk.Text(root, height = 1, width = 20, font = ("", 12))
                nameinput.place(x = 220, y = 115)
                password = tk.Label(root, height = 1, width = 8,
                                          bg = "BlanchedAlmond", font = ("", 12),
                                          text = "你的密碼 ?")
                password.place(x = 210, y = 155)
                passinput = tk.Text(root, height = 1, width = 20, font = ("", 12))
                passinput.place(x = 220, y = 190)
                message = tk.Label(root, height = 1, width = 25,
                                         bg = "BlanchedAlmond", font = ("", 12),
                                         text = "")
                message.place(x = 12, y = 250)

                # -------------------------------------------------------------------- #
                def getInput():
                    global name, work, message, login, draw_already
                    name = str(nameinput.get(1.0, tk.END + "-1c"))
                    pwd = str(passinput.get(1.0, tk.END + "-1c"))
                    name = name.strip()
                    pwd = pwd.strip()
                    if name == "":
                        message["text"] = "名字不可為空 !"
                    else:
                        work.refresh()
                        record = work.get_all_records(numericise_data=False)
                        name_list = [ str(i["Name"]) for i in record ]
                        code_list = [ str(i["Password"]) for i in record ]
                        if name not in name_list:
                            if draw_already:
                                message["text"] = "已完成抽籤，無法新增使用者 !"
                            else:
                                if pwd != "#clear#":
                                    work.update_value((len(name_list)+2, 1), name, False)
                                    work.update_value((len(name_list)+2, 2), pwd, False)
                                    message["text"] = "Register successfully !"
                                    login = True
                                else:
                                    message["text"] = "密碼為特殊指令 !"
                        elif name in name_list:
                            loc = name_list.index(name)
                            if pwd == "#clear#":
                                if draw_already:
                                    message["text"] = "已完成抽籤，無法清除使用者 !"
                                else:
                                    work.delete_rows(loc+2)
                                    message["text"] = "清除使用者 " + name + " !"
                            elif code_list[loc] != pwd:
                                message["text"] = "Wrong password !"
                            else:
                                message["text"] = "已登入，尚未抽籤 !"
                                login = True
                                send_to = record[name_list.index(name)]["Send_gift_to"]
                                if record[0]["Send_gift_to"] != "":
                                    message["text"] = "You gift is to " + str(send_to) + " !"

                    get_list()

                # -------------------------------------------------------------------- #
                start = tk.Button(root, height = 1, width = 6,
                                        bg = "WhiteSmoke", text = "Attend",
                                        cursor = "hand2", command = getInput)
                start.place(x = 250, y = 260)
                leave = tk.Button(root, height = 1, width = 6,
                                        bg = "WhiteSmoke", text = "Cancel",
                                        cursor = "hand2", command = root.destroy)
                leave.place(x = 330, y = 260)

                # -------------------------------------------------------------------- #
                global get_list
                def get_list():
                    global work, draw_already
                    work.refresh()
                    record = work.get_all_records()
                    total_namelist = "Present_Join:\n"
                    name_list = [ str(i["Name"]) for i in record ]
                    if len(record) == 0:
                        draw_already = False
                    else:
                        for idx in range(len(record)):
                            if record[idx]["Send_gift_to"] == "":
                                draw_already = False
                                break
                        else:
                            draw_already = True
                    list_state["text"] = str(len(name_list)) + " / " + str(max_people) + " Ready"
                    for name in name_list:
                        total_namelist += (name + '\n')
                    attender["text"] = total_namelist

                    if len(name_list) == max_people and login and not draw_already:
                        draw["state"] = tk.NORMAL
                    else:
                        draw["state"] = tk.DISABLED

                # -------------------------------------------------------------------- #
                get_list()

            # -------------------------------------------------------------------- #
            execute()
            root.mainloop()

        # -------------------------------------------------------------------- #
        produce_image()

    # -------------------------------------------------------------------- #
    named_title()

# -------------------------------------------------------------------- #
init()
