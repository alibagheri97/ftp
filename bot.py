import json
import random
import time
import time as timeSystem
import datetime
import uuid
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import dbTools
import qrcode
import io
import os
import threading
import sys
import secrets

while True:
    config = json.load(open("config.json", "r"))
    token = config["botToken"]
    bot = telebot.TeleBot(token)
    DBase = dbTools.DB()


    def test(id):
        bot.answer_callback_query(id, "Nothing Yet!\nBe patient...")


    def digit(num, digit):
        num = sup(str(num), ".")
        return float(num[0] + "." + num[1][:digit])


    def setErrorLog(e):
        try:
            with open("errorLog.txt", "r") as errorLog:
                val = errorLog.read()
                dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S: ")
                error = dt + e
                errorTxt = [error if val == "" else val + "\n" + error][0]
        except:
            with open("errorLog.txt", "w") as errorLog:
                dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S: ")
                errorTxt = dt + e
        with open("errorLog.txt", "w") as errorLog:
            errorLog.write(errorTxt)


    def sup(data, by):
        return DBase.sup(data, by)


    def table(tableName):
        return DBase.table(tableName)


    def decimal(data, dec=2):
        data = sup(str(data), ".")
        return float(f"{data[0]}.{data[1][:dec]}")


    def qrImage(content):
        img = qrcode.make(content)
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        return img_io


    class var:
        def __init__(self, tlid, init=""):
            self.mod = getChatMode(tlid)
            if init != "":
                self.out = self.initVal[init]

        initVal = {"email": "", "dbid": "", "chatKey": "", "val": "", "editFac": [], "staff": False}
        mod = {"login": False, "password": False, "neutral": True, "add": False, "edit": False, "message": False}
        email = ""
        dbid = ""
        chatKey = ""
        val = ""
        editFac = []
        # nothing with it just for passing the condition with time
        changeTextMenu = 0
        updateAdmin = False
        updateRe = False
        updateCounter = 0
        sniUpdate = True
        sniShow = False
        onlineUpdate = True
        warningServiceUpdated = True
        newUpdate = True
        orderUpdate = True


    def setLogVar(tlid, var, value=""):
        log = getLogFile()
        log = chatlogForamt(log, tlid)
        try:
            if type(var) != type(dict()):
                log["chat"][str(tlid)][var] = value
            else:
                for i in var.keys():
                    log["chat"][str(tlid)][i] = var[i]
            setValus(log, "log.json")
        except:
            raise Exception("ERROR CODE: 96")


    def getLogVar(tlid, var):
        log = getLogFile()
        log = chatlogForamt(log, tlid)
        out = None
        if not var in log["chat"][str(tlid)].keys():
            out = var(tlid, init=var).out
            log["chat"][str(tlid)][var] = out
            setValus(log, "log.json")
        if out is None:
            return log["chat"][str(tlid)][var]
        else:
            return out


    def getChatMode(tlid):
        log = getLogFile()
        chatMod = {}
        log = chatlogForamt(log, tlid)
        if not "chatMode" in log["chat"][str(tlid)].keys():
            log["chat"][str(tlid)]["chatMode"] = getChatModeDict("neutral")
            chatMod = getChatModeDict("neutral")
            setValus(log, "log.json")
        else:
            chatMod = getLogFile()["chat"][str(tlid)]["chatMode"]
        return chatMod


    def chatlogForamt(log, tlid):
        if not "chat" in log.keys():
            log["chat"] = {}
        if not str(tlid) in log["chat"].keys():
            log["chat"][str(tlid)] = {}
        return log


    def setChatLog(tlid, mode):
        log = getLogFile()
        log = chatlogForamt(log, tlid)
        log["chat"][str(tlid)]["chatMode"] = mode
        setValus(log, "log.json")


    def getChatModeDict(mode):
        modes = list(var.mod.keys())
        mod = dict.fromkeys(modes)
        for i in modes:
            if mode == i:
                mod[mode] = True
            else:
                mod[i] = False
        return mod


    def chatMode(tlid, mode):
        mod = getChatModeDict(mode)
        setChatLog(tlid, mod)


    def initValus():
        lst = ["log.json", "ticket.json", "payment.json", "paymentArchive.txt"]
        for i in lst:
            if not i in os.listdir(os.getcwd()):
                if ".json" in i:
                    with open(i, "w") as f:
                        f.write("{}")
                elif i == "paymentArchive.txt":
                    with open(i, "w") as f:
                        f.write(f"# Payment Archive {getTehranTime(time.time())[0]}\n\n")
        with open("paymentArchive.txt", "r") as f:
            paymentArchive = f.read()
        return [json.load(open("config.json", "r")), json.load(open("data.json", "r", encoding="utf-8")),
                json.load(open("log.json", "r")), json.load(open("ticket.json", "r")),
                json.load(open("payment.json", "r")), paymentArchive]


    def setValus(val, filename):
        if ".json" in filename:
            json.dump(val, open(filename, "w"))
        elif ".txt" in filename:
            with open(filename, "w") as f:
                f.write(val)


    def clearVars(tlid, but=[]):
        if tlid in DBase.getAdminTlId() + DBase.getStaffTlId():
            chatMode(tlid, "message")
            setLogVar(tlid, "chatKey", value="smartSearchUsers")
        else:
            chatMode(tlid, "neutral")
            setLogVar(tlid, {"email": "", "dbid": "", "chatKey": "", "val": "", "editFac": []})
        if not "changeTextMenu" in but:
            setLogVar(tlid, "changeTextMenu", value=0)
        if not "updateService" in but:
            var.updateAdmin = False
            var.updateRe = False


    def getTehranTime(time):
        tehranDateR = DBase.convert2Iran(time)
        tehranTime = DBase.getTehranTime()
        days = tehranDateR[0]
        dd = sup(days, "-")
        tehranDate = f"{dd[-1]}-{dd[-2]}-{dd[-3]}"
        h = tehranTime.hour
        m = tehranTime.minute
        s = tehranTime.second
        h = [str(h) if str(h).__len__() == 2 else "0" + str(h)][0]
        m = [str(m) if str(m).__len__() == 2 else "0" + str(m)][0]
        s = [str(s) if str(s).__len__() == 2 else "0" + str(s)][0]
        tehranHours = f"{h}:{m}:{s}"
        return [tehranDate, tehranHours]


    def getAdminsTlid():
        admin = dict()
        for i in DBase.getAdminTlId():
            admin[i] = ""
        return list(admin.keys())


    def getStaffsTlid():
        staffs = dict()
        for i in DBase.getStaffTlId():
            staffs[i] = ""
        return list(staffs.keys())


    def adminsMessage(mod, **data):
        # user Loged in
        if "#" in mod:
            user = DBase.getUserRow(int(data["dbid"]))
            for i in getAdminsTlid():
                tdate, thours = getTehranTime(timeSystem.time())
                inviteUser = DBase.getUserRow(user["invite_user_id"])
                invite = ["\n\n" + initValus()[1]["invite"].format(email=inviteUser["email"]) if not inviteUser in [0,
                                                                                                                    None] else ""][
                    0]
                textBudy = initValus()[1][mod[:-1]].format(
                    email=user["email"],
                    id=data["dbid"],
                    tlid=data["tlid"],
                    date=f"{tdate}",
                    invite=invite
                )
                try:
                    bot.send_message(i, textBudy, reply_markup=loginMarkup(user["id"]))
                except:
                    pass
        elif mod == "adminNoticRecharge":
            for i in getAdminsTlid():
                if "invit" in list(data.keys()):
                    if data["mode"] == "staff":
                        by = initValus()[1]["byInvite"]
                    elif data["mode"] == "user":
                        by = initValus()[1]["byUser"]
                    if "day" in data.keys():
                        try:
                            bot.send_message(i, initValus()[1]["successfullyCharged"].format(day=data["day"],
                                                                                             mod=initValus()[1]["day"],
                                                                                             email=data[
                                                                                                 "email"]) + "\n{invit}".format(
                                invit=by.format(email=data["invit"])))
                        except:
                            pass
                    elif "hour" in data.keys():
                        try:
                            bot.send_message(i, initValus()[1]["successfullyCharged"].format(day=data["hour"],
                                                                                             mod=initValus()[1]["hour"],
                                                                                             email=data[
                                                                                                 "email"]) + "\n{invit}".format(
                                invit=by.format(email=data["invit"])))
                        except:
                            pass
                else:
                    try:
                        bot.send_message(i, initValus()[1]["successfullyCharged"].format(day=data["day"],
                                                                                         mod=initValus()[1]["day"],
                                                                                         email=data["email"]))
                    except:
                        pass
        elif mod == "adminOnlineWarning":
            for i in getAdminsTlid():
                try:
                    bot.send_message(i,
                                     initValus()[1][mod].format(time=data["time"], email=data["email"], id=data["id"],
                                                                note=data["note"]),
                                     reply_markup=blockMarkup(data["id"]))
                except:
                    pass
        elif mod == "deleteAccount":
            if "invit" in data.keys():
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1]["deleteSuccessful"].format(
                            text=data["email"]) + f'\n{initValus()[1]["byInvite"].format(email=data["invit"])}')
                    except:
                        pass
            else:
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1]["deleteSuccessful"].format(text=data["email"]))
                    except:
                        pass

        elif mod == "banAccount":
            dataKey = ["banSuccessful" if not data["ban"] else "unbanSuccessful"][0]
            if "invit" in data.keys():
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1][dataKey].format(
                            text=data["email"]) + f'\n{initValus()[1]["byInvite"].format(email=data["invit"])}')
                    except:
                        pass

            else:
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1][dataKey].format(text=data["email"]))
                    except:
                        pass

        elif mod == "changeSub":
            dataKey = "changeSubSuccessful"
            subName = data["subName"]
            if "invit" in data.keys():
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1][dataKey].format(
                            email=data["email"],
                            sub=subName) + f'\n{initValus()[1]["byInvite"].format(email=data["invit"])}')
                    except:
                        pass

            else:
                for i in getAdminsTlid():
                    try:
                        bot.send_message(i, initValus()[1][dataKey].format(email=data["email"], sub=subName))
                    except:
                        pass

        elif mod == "newAccount":
            newList = data["newList"]
            for i in getAdminsTlid():
                for j in newList:
                    user = DBase.getUserRow(j)
                    email = user["email"]
                    invit = [DBase.getUserRow(user["invite_user_id"])["email"] if user[
                                                                                      "invite_user_id"] is not None else "None"][
                        0]
                    time = getTehranTime(user["created_at"])[0]
                    try:
                        bot.send_message(i,
                                         initValus()[1]["newAccount"].format(email=email, id=j, invit=invit, time=time))
                    except:
                        pass

        else:
            for i in getAdminsTlid():
                try:
                    bot.send_message(i, data["data"])
                except:
                    pass


    def secondToString(sec):
        #        s, m,   h,    d,    m,       y
        table = [1, 60, 3600, 86400, 2592000, 31104000]
        tableOut = [0] * 6
        seed = []
        out = []
        count = -1
        for i in table[::-1]:
            if sec % i < sec:
                tableOut[count] = sec / i
                break
            count -= 1
        count = -2
        for i in range(len(table) - 1):
            if tableOut[count + 1] != 0:
                dec = tableOut[count + 1] - int(tableOut[count + 1])
                if count != -6:
                    tableOut[count] = dec * table[count + 1] / table[count]
                else:
                    tableOut[count] = round(dec * table[count + 1] / table[count])
                tableOut[count + 1] = int(tableOut[count + 1])
            count -= 1
        return tableOut


    def userOnline():  # {id: [12879739, [0,0,1,0,0,0]]}

        users_state = DBase.getTableDict(table("v2_stat_user"))[::-1]
        users_state_ids = [i["user_id"] for i in users_state]
        users_lastUpdate = dict()
        users_id = DBase.getColumn(table("v2_user"), "id")
        out = []
        for id in users_id:
            found = False
            if id in users_state_ids:
                for i in users_state:
                    if i["user_id"] == id:
                        users_lastUpdate[str(id)] = timeSystem.time() - i["updated_at"]
                        found = True
                        break
            if not found:
                users_lastUpdate[str(id)] = None
        for i in users_lastUpdate.keys():
            if users_lastUpdate[i] is not None:
                lst = [users_lastUpdate[i], secondToString(users_lastUpdate[i])]
                out.append({i: lst})
            else:
                out.append({i: None})

        return out


    def getEmailByTlid(tlid):
        return DBase.getUserRow(DBase.getIdFromTlid(tlid))["email"]


    # def markup_inline():
    #     markup = InlineKeyboardMarkup()
    #     markup.width = 2
    #     markup.add(
    #         InlineKeyboardButton("Hi!", callback_data="uz"),
    #         InlineKeyboardButton("Hello!", callback_data="ru")
    #     )
    #     return markup

    def wrongToken(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["wrongToken"], reply_markup=wrongMarkup())
        except:
            pass
        chatMode(message.chat.id, "login")


    def wrongPass(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["wrongPass"], reply_markup=wrongMarkup())
        except:
            pass

        chatMode(message.chat.id, "login")


    def enterPass(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["enterPass"], reply_markup=wrongMarkup())
        except:
            pass

        chatMode(message.chat.id, "password")


    # start of Markups

    def mainMenuMarkup(message):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if initValus()[1]["subs"] != "":
            if initValus()[1]["rules"] != "":
                markup.add(
                    InlineKeyboardButton(initValus()[1]["buy"], callback_data="buy")
                ).add(
                    InlineKeyboardButton(initValus()[1]["subs"], callback_data="subs"),
                    InlineKeyboardButton(initValus()[1]["accounts"], callback_data="accounts")
                ).add(
                    InlineKeyboardButton(initValus()[1]["terms"], callback_data="terms"),
                    InlineKeyboardButton(initValus()[1]["contact"], callback_data="contact")
                )
            else:
                markup.add(
                    InlineKeyboardButton(initValus()[1]["buy"], callback_data="buy")
                ).add(
                    InlineKeyboardButton(initValus()[1]["subs"], callback_data="subs"),
                    InlineKeyboardButton(initValus()[1]["accounts"], callback_data="accounts")
                ).add(
                    InlineKeyboardButton(initValus()[1]["guide"], callback_data="guide"),
                    InlineKeyboardButton(initValus()[1]["contact"], callback_data="contact")
                )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["buy"], callback_data="buy")
            ).add(
                InlineKeyboardButton(initValus()[1]["accounts"], callback_data="accounts")
            )
            if initValus()[1]["rules"] != "":
                markup.add(
                    InlineKeyboardButton(initValus()[1]["terms"], callback_data="terms"),
                    InlineKeyboardButton(initValus()[1]["contact"], callback_data="contact")
                )
            else:
                markup.add(
                    InlineKeyboardButton(initValus()[1]["guide"], callback_data="guide"),
                    InlineKeyboardButton(initValus()[1]["contact"], callback_data="contact")
                )
        isAdmin = DBase.adminCheck(message.chat.id)
        isStaff = DBase.staffCheck(message.chat.id)
        if isStaff:
            markup.add(
                InlineKeyboardButton(initValus()[1]["distributorPanel"], callback_data="staffPanel")
            )
        if isAdmin:
            markup.add(
                InlineKeyboardButton(initValus()[1]["controlPanel"], callback_data="controlPanel")
            )
        # admin ??
        return markup


    def wrongMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data="accounts")
        )
        return markup


    def statusMarkup(message, dbId, mod="user", exitDestination=""):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        admins = DBase.getAdminsId()
        accounts = DBase.getAccountsFromTlid(message.chat.id)
        staffsTlIds = DBase.getStaffTlId()
        if mod == "user":
            if not DBase.checkAccountStatus(dbId):
                markup.add(
                    InlineKeyboardButton(initValus()[1]["renewal"], callback_data="subs")
                )
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data="accounts")
            )
        else:
            user = DBase.getUserRow(dbId)
            if user["expired_at"] is not None:
                if message.chat.id in DBase.getAdminTlId():
                    markup.add(
                        InlineKeyboardButton(initValus()[1]["emergency"], callback_data=f"{dbId}!"),
                        InlineKeyboardButton(initValus()[1]["customRecharge"], callback_data=f"{dbId}recharge"),
                        InlineKeyboardButton(initValus()[1]["recharge"], callback_data=f"{dbId}*")
                    )
                elif message.chat.id in staffsTlIds:
                    markup.add(
                        InlineKeyboardButton(initValus()[1]["emergency"], callback_data=f"{dbId}!"),
                        InlineKeyboardButton(initValus()[1]["recharge"], callback_data=f"coupon{dbId}#")
                    )
            if user["id"] != initValus()[0]["superAdminDBid"]:
                if not user["id"] in admins or str(initValus()[0]["superAdminDBid"]) in accounts.keys():
                    log = getLogFile()
                    if not "block" in list(log.keys()):
                        log["block"] = []
                    if int(user["id"]) in log["block"]:
                        markup.add(
                            InlineKeyboardButton(initValus()[1]["unblock"], callback_data=f'onlineBlock{user["id"]}-'),
                            InlineKeyboardButton(
                                initValus()[1][["ban" if not bool(user["banned"]) else "unban"][0]],
                                callback_data=
                                [f"users{dbId}ban" if bool(user["banned"]) else f"users{dbId}unban"][0])
                        )
                    else:
                        markup.add(
                            InlineKeyboardButton(initValus()[1]["block"], callback_data=f'onlineBlock{user["id"]}+'),
                            InlineKeyboardButton(initValus()[1][["ban" if not bool(user["banned"]) else "unban"][0]],
                                                 callback_data=
                                                 [f"users{dbId}ban" if bool(user["banned"]) else f"users{dbId}unban"][
                                                     0])
                        )
                    markup.add(
                        InlineKeyboardButton(initValus()[1]["delete"], callback_data=f"deleteAccount{dbId}")
                    )
            if mod == "admin":
                if user["id"] != initValus()[0]["superAdminDBid"]:
                    if str(initValus()[0]["superAdminDBid"]) in accounts.keys():
                        markup.add(
                            InlineKeyboardButton(initValus()[1]["distributor"].format(
                                mod=
                                [initValus()[1]["active"] if bool(user["is_staff"]) else initValus()[1]["deactive"]][
                                    0]),
                                callback_data=f'{["-" if bool(user["is_staff"]) else "+"][0]}distributor{user["id"]}'),
                            InlineKeyboardButton(initValus()[1]["admin"].format(
                                mod=
                                [initValus()[1]["active"] if bool(user["is_admin"]) else initValus()[1]["deactive"]][
                                    0]),
                                callback_data=f'{["-" if bool(user["is_admin"]) else "+"][0]}admin{user["id"]}')
                        )
                    elif [True for i in accounts.keys() if int(i) in admins].__len__() != 0:
                        if not user["id"] in admins:
                            markup.add(
                                InlineKeyboardButton(initValus()[1]["distributor"].format(
                                    mod=[initValus()[1]["active"] if bool(user["is_staff"]) else initValus()[1][
                                        "deactive"]][
                                        0]),
                                    callback_data=f'{["-" if bool(user["is_staff"]) else "+"][0]}distributor{user["id"]}')
                            )
            if user["id"] != initValus()[0]["superAdminDBid"]:
                payemntStatus = payStatus(dbId)
                if payemntStatus is not None:
                    markup.add(
                        InlineKeyboardButton(initValus()[1][payemntStatus[0]], callback_data=payemntStatus[1])
                    )
                markup.add(
                    InlineKeyboardButton(initValus()[1]["editNote"], callback_data=f'{dbId}note')
                )
                markup.add(
                    InlineKeyboardButton(initValus()[1]["changeSub"], callback_data=f"changeSub{dbId}"),
                    InlineKeyboardButton(initValus()[1]["resetAccount"], callback_data=f"resetAccount{dbId}|{mod}")
                )
                markup.add(
                    InlineKeyboardButton(initValus()[1]["clearTraffic"], callback_data=f"clearTraffic{dbId}|{mod}"),
                )
                markup.add(
                    InlineKeyboardButton(initValus()[1]["refresh"], callback_data=f"refresh{dbId}|{mod}"),
                )
            if exitDestination == "":
                markup.add(
                    InlineKeyboardButton(initValus()[1]["return"], callback_data="users^")
                )
            else:
                markup.add(
                    InlineKeyboardButton(initValus()[1]["return"], callback_data=exitDestination)
                )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def androidMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["directLink"], callback_data="directLink")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="guide")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def returnMarkup(returnLocation):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if returnLocation != "mainMenu":
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data=returnLocation)
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data=returnLocation)
            )
        return markup


    def accountsMarkup(message):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        acc = DBase.getAccountsFromTlid(message.chat.id)
        inlines = []
        for i in list(acc.keys()):
            markup.add(
                InlineKeyboardButton(acc[i], callback_data=f"status{i}")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["addAccount"], callback_data="addAccount"),
            InlineKeyboardButton(initValus()[1]["removeAccount"], callback_data="removeAccount")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def removeMarkup(message):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        acc = DBase.getAccountsFromTlid(message.chat.id)
        inlines = []
        for i in list(acc.keys()):
            markup.add(
                InlineKeyboardButton(acc[i], callback_data=i + "&")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data="accounts")
        )
        return markup


    def termsMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["guide"], callback_data="guide"),
            InlineKeyboardButton(initValus()[1]["rules"], callback_data="rules")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def platformMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["android"], callback_data="android"),
            InlineKeyboardButton(initValus()[1]["iphone"], callback_data="iphone")
        )
        if initValus()[1]["rules"] != "":
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data="terms")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
            )
        return markup


    def subsMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        subsBudy = []
        for i in list(initValus()[1].keys()):
            if "@" in i:
                subId = sup(i, "@")[-1]
                subBudy = initValus()[1][i]
                subsBudy.append([subId, subBudy])
        for i in subsBudy:
            markup.add(
                InlineKeyboardButton(i[1], callback_data="nothing")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def controlPanelMarkup(tlid):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        adminId = DBase.getIdFromTlid(tlid)
        markup.add(
            InlineKeyboardButton(initValus()[1]["users"], callback_data="users#"),
            InlineKeyboardButton(initValus()[1]["staffs"], callback_data="staffs#")
        )
        if adminId == initValus()[0]["superAdminDBid"]:
            markup.add(
                InlineKeyboardButton(initValus()[1]["coupons"], callback_data="setCoupon#")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["editText"], callback_data="textMenu#"),
            InlineKeyboardButton(initValus()[1]["sendMessage"], callback_data="sendMessage")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["rechargeEveryone"], callback_data="allRech"),
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["updateForce"], callback_data="updateForce"),
            InlineKeyboardButton(initValus()[1]["ticket"], callback_data="ticket")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["services"], callback_data="services")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def distributorPanelMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["users"], callback_data="staffusers^")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["wallet"], callback_data="staff|wallet")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def go2Markup(markupShow, destnation, returnMod=False):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1][markupShow], callback_data=destnation)
        )
        if returnMod:
            markup.add(
                InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
            )
        return markup


    def setupMessageMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["setupNew"], callback_data="buyInit")
        )
        return markup


    def editTextMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        itms = initValus()[1]
        itemskeys = list(itms.keys())
        itemsLen = itemskeys.__len__()
        f = itemsLen // 10
        lstMain = []
        if f != 0:
            l = itemsLen % 10
            lstLen = f + int(bool(l))
        else:
            lstLen = 1
        for i in range(lstLen):
            counter = i * 10
            ilst = itemskeys[counter:counter + 10]
            if bool(ilst.__len__()):
                lstMain.append(ilst)
            else:
                break
        if var.changeTextMenu > lstMain.__len__() - 1:
            var.changeTextMenu = lstMain.__len__() - 1
        elif var.changeTextMenu < 0:
            var.changeTextMenu = 0
        for i in lstMain[var.changeTextMenu]:
            if itms[i] == "":
                itms[i] = f"NaN, key={i}"
            if sup(itms[i], " ").__len__() <= 4:
                show = itms[i]
            else:
                show = ""
                words = sup(itms[i], " ")
                for index in range(4):
                    show += words[index] + " "
                show[:-1]
                show += "..."
            markup.add(
                InlineKeyboardButton(show, callback_data=f"$textMenu{i}#")
            )
        if var.changeTextMenu == 0:
            markup.add(
                InlineKeyboardButton(f"Next Page ▶️\n(1/{lstMain.__len__()})", callback_data="+textMenu#")
            )

        elif var.changeTextMenu == lstMain.__len__() - 1:
            markup.add(
                InlineKeyboardButton(f"◀️ Previous Page\n({lstMain.__len__()}/{lstMain.__len__()})",
                                     callback_data="-textMenu#")
            )
        else:
            markup.add(
                InlineKeyboardButton("◀️ Previous Page", callback_data="-textMenu#"),
                InlineKeyboardButton(f"Page ({var.changeTextMenu + 1}/{lstMain.__len__()})",
                                     callback_data="textMenuSearch#"),
                InlineKeyboardButton("Next Page ▶️", callback_data="+textMenu#")
            )
        markup.add(
            InlineKeyboardButton("Exit ❌", callback_data="controlPanel")
        )
        return markup


    def usersMarkup(usersList, mod="admin", menuIdx=0):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        data = dict()
        for i in usersList.keys():
            if type(usersList[i]) != type(list()):
                data[f'$users{i}#'] = f'{usersList[i]}'
            else:
                data[f'$users{i}#'] = [str(j) for j in usersList[i]]
        if usersList.__len__() != 0:
            markup = menuMarkup(markup, data, "users", menuIdx=menuIdx)
        markup.add(
            InlineKeyboardButton("Search 🔎", callback_data="usersSmartSearch#")
        )
        if mod == "adminStaff":
            markup.add(
                InlineKeyboardButton("Exit ❌", callback_data="staffs")
            )
        elif mod == "admin":
            markup.add(
                InlineKeyboardButton("Exit ❌", callback_data="controlPanel")
            )
        else:
            markup.add(
                InlineKeyboardButton("Exit ❌", callback_data="staffPanel")
            )
        return markup


    def cancelMarkup(destenation):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data=destenation)
        )
        return markup


    def updateForceMarkup(rep, admin):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data=f"updateForceConfirm-{rep}-{admin}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data="controlPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def updateForceOptionMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["repeat"], callback_data="repeat"),
            InlineKeyboardButton(initValus()[1]["norepeat"], callback_data="norepeat")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="controlPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def emergencyRechargeMarkup(id):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["emergency"], callback_data=f"{id}!")
        )
        return markup


    def rechargeMarkup(id, mod="admin"):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if mod == "admin":
            markup.add(
                InlineKeyboardButton(initValus()[1]["emergency"], callback_data=f"{id}!#"),
                InlineKeyboardButton(initValus()[1]["recharge"], callback_data=f"{id}*#")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["emergency"], callback_data=f"{id}!#"),
                InlineKeyboardButton(initValus()[1]["recharge"], callback_data=f"coupon{id}#")
            )
        log = getLogFile()
        if not "block" in list(log.keys()):
            log["block"] = []
        if mod == "amdin":
            if int(id) in log["block"]:
                markup.add(
                    InlineKeyboardButton(initValus()[1]["unblock"], callback_data=f"onlineBlock{id}-"),
                    InlineKeyboardButton(initValus()[1]["accountStatus"], callback_data=f'$users{id}#')
                )
            else:
                markup.add(
                    InlineKeyboardButton(initValus()[1]["block"], callback_data=f"onlineBlock{id}+"),
                    InlineKeyboardButton(initValus()[1]["accountStatus"], callback_data=f'$users{id}#')
                )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["accountStatus"], callback_data=f'$users{id}#')
            )
        return markup


    def contactMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["askHelp"], callback_data="askHelp")
        ).add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="mainMenu")
        )
        return markup


    def respondSupportMarkup(message):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["respond"], callback_data=f"{message.chat.id}^#")
        )
        return markup


    def respondSupportMarkupReturn(tlid):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["respond"], callback_data=f"{tlid}^#")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="ticket")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def viewTicketMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        out = getTicketsForShow()
        if out.__len__() % 2 == 0:
            for i in range(0, len(out), 2):
                markup.add(
                    InlineKeyboardButton(
                        sup(initValus()[1]["ticketId"].format(id=out[i][1], email="", tlid=""), "\n")[0],
                        callback_data=f"{out[i][1]}+ticket"),
                    InlineKeyboardButton(
                        sup(initValus()[1]["ticketId"].format(id=out[i + 1][1], email="", tlid=""), "\n")[0],
                        callback_data=f"{out[i + 1][1]}+ticket")
                )
        else:
            markup.add(
                InlineKeyboardButton(sup(initValus()[1]["ticketId"].format(id=out[0][1], email="", tlid=""), "\n")[0],
                                     callback_data=f"{out[0][1]}+ticket")
            )
            for i in range(1, len(out), 2):
                markup.add(
                    InlineKeyboardButton(
                        sup(initValus()[1]["ticketId"].format(id=out[i][1], email="", tlid=""), "\n")[0],
                        callback_data=f"{out[i][1]}+ticket"),
                    InlineKeyboardButton(
                        sup(initValus()[1]["ticketId"].format(id=out[i + 1][1], email="", tlid=""), "\n")[0],
                        callback_data=f"{out[i + 1][1]}+ticket")
                )
        if getTicketsForShow().__len__() != 0:
            markup.add(
                InlineKeyboardButton(initValus()[1]["clearTickets"], callback_data="delete+ticket")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["thereIsNoTicket"], callback_data="controlPanel")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="controlPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def adminOrAllMarkup(repeat=False):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        rep = ["repeat" if repeat else "norepeat"][0]
        markup.add(
            InlineKeyboardButton(initValus()[1]["justAdmin"], callback_data=f"justAdmin-{rep}"),
            InlineKeyboardButton(initValus()[1]["forAll"], callback_data=f"forAll-{rep}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="updateForce")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def sniMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if bool(initValus()[0]["sniEnable"]):
            markup.add(
                InlineKeyboardButton(initValus()[1]["setDeactive"], callback_data="-sni")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["showSni"], callback_data="sniShow")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["add"], callback_data="sniAdd"),
                InlineKeyboardButton(initValus()[1]["takeaway"], callback_data="sniSub")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["setActive"], callback_data="+sni")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["showSni"], callback_data="sniShow")
            )
        markup.add(
            InlineKeyboardButton(
                [initValus()[1]["silentNotic"] if bool(initValus()[0]["sniNotic"]) else initValus()[1]["allowNotic"]][
                    0], callback_data="sniSwitchNotic")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["updateNow"], callback_data="sniUpdateNow")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="services")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def warningMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if bool(initValus()[0]["warningEnable"]):
            markup.add(
                InlineKeyboardButton(initValus()[1]["setDeactive"], callback_data="-warning")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["add"], callback_data="warningAdd"),
                InlineKeyboardButton(initValus()[1]["takeaway"], callback_data="warningSub")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["setActive"], callback_data="+warning")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["updateNow"], callback_data="updateForce")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="services")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def subSniMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        times = sup(initValus()[0]["serviceSniTime"], ";")
        if times.__len__() != 0:
            for i in times:
                markup.add(InlineKeyboardButton(i, callback_data=f"sni&{i}"))
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="sni")
        )
        return markup


    def subOnlineMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        times = sup(initValus()[0]["serviceOnlineTime"], ";")
        if times.__len__() != 0:
            for i in times:
                markup.add(InlineKeyboardButton(i, callback_data=f"online&{i}"))
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="online")
        )
        return markup


    def subWarningMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        times = sup(initValus()[0]["serviceWarningTime"], ";")
        if times.__len__() != 0:
            for i in times:
                markup.add(InlineKeyboardButton(i, callback_data=f"warning&{i}"))
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="warning")
        )
        return markup


    def confirmTicketMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data="confirm+ticket"),
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data="ticket")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="ticket")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def servicesMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["online"], callback_data="online")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["new"], callback_data="new")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["sni"], callback_data="sni"),
            InlineKeyboardButton(initValus()[1]["warning"], callback_data="warning")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="controlPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def onlineMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if bool(initValus()[0]["onlineEnable"]):
            markup.add(
                InlineKeyboardButton(initValus()[1]["setDeactive"], callback_data="-online")
            )
            # markup.add(
            #     InlineKeyboardButton(initValus()[1]["showOnline"], callback_data="onlineShow")
            # )
            markup.add(
                InlineKeyboardButton(initValus()[1]["add"], callback_data="onlineAdd"),
                InlineKeyboardButton(initValus()[1]["takeaway"], callback_data="onlineSub")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["setActive"], callback_data="+online")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["showOnline"], callback_data="onlineShow")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["updateNow"], callback_data="onlineUpdateNow")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="services")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def blockMarkup(id):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        log = getLogFile()
        if not "block" in list(log.keys()):
            log["block"] = []
        if int(id) in log["block"]:
            markup.add(
                InlineKeyboardButton(initValus()[1]["unblock"], callback_data=f"onlineBlock{id}-")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["block"], callback_data=f"onlineBlock{id}+")
            )
        return markup


    def menuMarkup(markup, data, destination, exitDestination="", menuIdx=0, raw_data=""):
        itms = data
        menuLength = initValus()[0]["menuListLength"]
        itemskeys = list(itms.keys())
        itemsLen = itemskeys.__len__()
        f = itemsLen // menuLength
        lstMain = []
        if f != 0:
            l = itemsLen % menuLength
            lstLen = f + int(bool(l))
        else:
            lstLen = 1
        for i in range(lstLen):
            counter = i * menuLength
            ilst = itemskeys[counter:counter + menuLength]
            if bool(ilst.__len__()):
                lstMain.append(ilst)
            else:
                break
        if menuIdx > lstMain.__len__() - 1:
            menuIdx = lstMain.__len__() - 1
        elif menuIdx < 0:
            menuIdx = 0
        for i in lstMain[menuIdx]:
            if type(itms[i]) != type(str()):
                buttonList = []
                for j in itms[i]:
                    buttonList.append(InlineKeyboardButton(j, callback_data=f"{i}"))
                markup.add(*buttonList)
            else:
                if itms[i] == "":
                    itms[i] = f"NaN, key={i}"
                show = itms[i]
                markup.add(
                    InlineKeyboardButton(show, callback_data=f"{i}")
                )
        if lstMain.__len__() != 1:
            if menuIdx == 0:
                markup.add(
                    InlineKeyboardButton(f"Next Page ▶️\n(1/{lstMain.__len__()})",
                                         callback_data=f"+{destination}{menuIdx}|{raw_data}#")
                )

            elif menuIdx == lstMain.__len__() - 1:
                markup.add(
                    InlineKeyboardButton(f"◀️ Previous Page\n({lstMain.__len__()}/{lstMain.__len__()})",
                                         callback_data=f"-{destination}{menuIdx}|{raw_data}#")
                )
            else:
                markup.add(
                    InlineKeyboardButton("◀️ Previous Page", callback_data=f"-{destination}{menuIdx}|{raw_data}#"),
                    InlineKeyboardButton(f"Page ({menuIdx + 1}/{lstMain.__len__()})",
                                         callback_data=f"*{destination}{raw_data}#"),
                    InlineKeyboardButton("Next Page ▶️", callback_data=f"+{destination}{menuIdx}|{raw_data}#")
                )
        if exitDestination != "":
            markup.add(
                InlineKeyboardButton("Exit ❌", callback_data=exitDestination)
            )
        return markup


    def smartSearchMarkup(searchPhrase, tlid, menuIdx=0):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        resultList = smartSearch(searchPhrase, tlid)
        lst = []
        if resultList.__len__() <= initValus()[0]["menuListLength"]:
            for i in resultList:
                markup.add(
                    InlineKeyboardButton(f"{i[-1]}: {i[1]}", callback_data=f"$users{i[0]}#")
                )
            markup.add(
                InlineKeyboardButton("Exit ❌", callback_data="users^")
            )
        else:
            data = dict()
            for i in resultList:
                data[f"$users{i[0]}#"] = f"{i[-1]}: {i[1]}"
            markup = menuMarkup(markup, data, "usersSearchSmart", exitDestination="users^", menuIdx=menuIdx,
                                raw_data=searchPhrase)
        return markup


    # set staffs automatically
    def setStaffs():
        inviters = DBase.getColumn(table("v2_user"), "invite_user_id")
        admins = DBase.getAdminsId()
        for i in inviters:
            if i is not None and not i in admins and DBase.getUserRow(i)["is_staff"] != 1 and DBase.getUserRow(i)[
                "banned"] != 1:
                DBase.setValue(table("v2_user"), "is_staff", 1, i)


    def getAdminsWhoStaffs():
        inviters = DBase.getColumn(table("v2_user"), "invite_user_id")
        admins = DBase.getAdminsId()
        users = DBase.getTableDict(table("v2_user"))
        out = {}
        for i in inviters:
            if i is not None and i in admins:
                for j in users:
                    if j["id"] == i:
                        out[str(i)] = j["email"]
        return out


    def getStaffsDeactive():
        inviters = DBase.getColumn(table("v2_user"), "invite_user_id")
        admins = DBase.getAdminsId()
        users = DBase.getTableDict(table("v2_user"))
        out = {}
        for i in inviters:
            if i is not None and not i in admins and DBase.getUserRow(i)["is_staff"] != 1:
                for j in users:
                    if j["id"] == i:
                        out[str(i)] = j["email"]
        return out


    def staffsMarkup(menuIdx=0):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        data = dict()
        setStaffs()
        staffDictRaw = DBase.getStaffs()
        staffDict = staffDictRaw.copy()
        adminsDict = getAdminsWhoStaffs()
        staffsDeactiveDict = getStaffsDeactive()
        for i in adminsDict.keys():
            staffDict[i] = adminsDict[i]
        for i in staffsDeactiveDict.keys():
            staffDict[i] = staffsDeactiveDict[i]
        sign = ""
        superAdminId = initValus()[0]["superAdminDBid"]
        for i in list(staffDict.keys())[::-1]:
            if int(i) == superAdminId:
                sign = initValus()[1]["superAdmin"]
                data[f'$users{i}|staffs^#'] = f'{staffDict[i]}' + f" {sign}"
                break
        for i in list(staffDict.keys())[::-1]:
            if i in adminsDict.keys():
                sign = initValus()[1]["adminSign"]
            elif i in staffDictRaw.keys():
                sign = initValus()[1]["activeSign"]
            elif i in staffsDeactiveDict.keys():
                sign = initValus()[1]["deactiveSign"]
            if not int(i) == superAdminId:
                data[f'$users{i}|staffs^#'] = f'{staffDict[i]}' + f" {sign}"
        if staffDict.__len__() != 0:
            markup = menuMarkup(markup, data, "staffs", menuIdx=menuIdx)
        markup.add(
            InlineKeyboardButton("Search 🔎", callback_data="staffsSmartSearch#")
        )
        markup.add(
            InlineKeyboardButton("Exit ❌", callback_data="controlPanel")
        )
        return markup


    def setCouponsMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        coupons = DBase.getTableDict(table("v2_coupon"))
        for i in coupons:
            markup.add(
                InlineKeyboardButton(f'{i["code"]}', callback_data=f'$setCoupon{i["id"]}')
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="controlPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def couponSettingsMarkup(couponId):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        coupon = DBase.getTableRowId(table("v2_coupon"), couponId)
        markup.add(
            InlineKeyboardButton(initValus()[1]["rechargeCoupon"], callback_data=f"setCoupon{couponId}*"),
            InlineKeyboardButton(initValus()[1]["customRecharge"], callback_data=f"setCoupon{couponId}&")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1][["active" if int(coupon["show"]) == 0 else "deactive"][0]],
                                 callback_data=f'setCoupon{couponId}{["on" if int(coupon["show"]) == 0 else "off"][0]}')
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["edit"], callback_data=f'setCoupon{couponId}edit')
        )
        markup.add(
            InlineKeyboardButton("Exit ❌", callback_data="setCoupon")
        )
        return markup


    def loginMarkup(id):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["accountStatus"], callback_data=f'$users{id}#')
        )
        return markup


    def changeSubMarkup(dbid, mod):
        markup = InlineKeyboardMarkup()
        markup.width = 2
        subs = [i for i in DBase.getTableDict(table("v2_plan")) if i["show"] == 1]
        for i in subs:
            markup.add(
                InlineKeyboardButton(i["name"], callback_data=f'changeSub{dbid}|{i["id"]}')
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data=f"status{dbid}{mod}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def confirmMarkup(data, mod, cancelDestination, supVal=""):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data=f"confirm{data}{supVal}{mod}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data=f"{cancelDestination}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def newMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        if bool(initValus()[0]["newEnable"]):
            markup.add(
                InlineKeyboardButton(initValus()[1]["setDeactive"], callback_data="-new")
            )
            markup.add(
                InlineKeyboardButton(initValus()[1]["add"], callback_data="newAdd"),
                InlineKeyboardButton(initValus()[1]["takeaway"], callback_data="newSub")
            )
        else:
            markup.add(
                InlineKeyboardButton(initValus()[1]["setActive"], callback_data="+new")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["updateNow"], callback_data="newUpdateNow")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="services")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def subNewMarkup():
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        times = sup(initValus()[0]["serviceNewTime"], ";")
        if times.__len__() != 0:
            for i in times:
                markup.add(InlineKeyboardButton(i, callback_data=f"new&{i}"))
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="new")
        )
        return markup


    def allRechMarkup(day):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data=f"confirm{day}AllRech")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="controlPanel")
        )
        return markup


    def enterAmountMarkup(dbid, mod):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        defaultAmounts = sup(initValus()[0]["defaultPrices"], ";")[::-1]
        buttons = [[]]
        defaultPer = 2
        count = 0
        for i in defaultAmounts:
            buttons[count].append(InlineKeyboardButton(i, callback_data=f"both|payment|payReq|{dbid}|{i}"))
            if buttons[count].__len__() >= defaultPer:
                buttons.append([])
                count += 1
        buttons.reverse()
        for i in buttons:
            markup.add(*i)
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data=f"status{dbid}{mod}")
        )
        return markup


    def orderMarkup(dbid):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data=f"both|payment|payReq|confirm|{dbid}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data=f"both|payment|payReq|denied|{dbid}")
        )
        return markup


    def walletMarkup(staffId):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["reciveReq"], callback_data=f"staff|payReq|{staffId}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="staffPanel")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def amountReciveMarkup(staffId):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["wholeMoney"], callback_data=f"staff|payReq|amount|all|{staffId}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data="staff|wallet")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def choseCardMarkup(staffId, amount):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        payment = getPaymentFile()
        userPayment = payment["staffBank"][str(staffId)]
        cardsList = userPayment["cardsNumber"]
        for i in cardsList:
            markup.add(
                InlineKeyboardButton(i, callback_data=f"staff|payReq|req|{staffId}|{amount}|{i}")
            )
        markup.add(
            InlineKeyboardButton(initValus()[1]["return"], callback_data=f"staff|payReq|{staffId}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["statusMenu"], callback_data="mainMenu")
        )
        return markup


    def payRequestAdminMarkup(staffId):
        markup = InlineKeyboardMarkup()
        markup.widh = 2
        markup.add(
            InlineKeyboardButton(initValus()[1]["confirm"], callback_data=f"both|reciveBank|confirm|{staffId}")
        )
        markup.add(
            InlineKeyboardButton(initValus()[1]["cancel"], callback_data=f"both|reciveBank|denied|{staffId}")
        )
        return markup


    # end of Markups:

    def chackUserNameValid(message):
        fb = False
        dbid = None
        if "@" in str(message.text).lower():
            emailBudy = str(message.text).lower()
            fb, dbid = DBase.emailCheck(emailBudy)
            if fb:
                # var.email = message.text
                # var.dbid = dbid
                setLogVar(message.chat.id, {"email": message.text, "dbid": dbid})
            else:
                setLogVar(message.chat.id, {"email": "", "dbid": ""})
            enterPass(message)
            fb = None
            dbid = None
        elif "http" in message.text:
            fb, dbid = DBase.tokenCheck(message.text)
        return [fb, dbid]


    def editAction(message):
        lst = []
        editFac = getLogVar(message.chat.id, "editFac")
        for i in sup(initValus()[1][editFac[0]], "{")[1:]:
            lst.append(sup(i, "}")[0])
        lstInp = []
        for i in sup(message.text, "{")[1:]:
            lstInp.append(sup(i, "}")[0])
        if "ipConnected" in lst:
            lst.remove("ipConnected")
        if "ipConnected" in lstInp:
            lstInp.remove("ipConnected")
        lst.sort()
        lstInp.sort()
        if lst == lstInp:
            perv = initValus()[1]
            if message.text == "#":
                perv[editFac[0]] = ""
            else:
                perv[editFac[0]] = message.text
            setValus(perv, "data.json")
            try:
                bot.send_message(message.chat.id, initValus()[1]["successfully"],
                                 reply_markup=returnMarkup("textMenu^"))
            except:
                pass

            setLogVar(message.chat.id, "editFac", value=[])
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"],
                                 reply_markup=cancelMarkup("textMenu#"))
            except:
                pass

        clearVars(message.chat.id)


    def loginAction(message):
        fb, dbid = chackUserNameValid(message)
        if fb is None:
            pass
        elif fb:
            DBase.setTlId(dbid, message.from_user.id)
            adminsMessage("userLogedIn#", dbid=dbid, tlid=message.chat.id)
            if initValus()[0]["mode"] == "menu":
                mainMenu(message)
            else:
                status(message, dbid)
        elif not fb:
            wrongToken(message)


    def passwordAction(message):
        # if var.email != "":
        email = getLogVar(message.chat.id, "email")
        if email:
            emails = DBase.getColumnWithId(table("v2_user"), "email")
            dbid = [i[1] for i in emails if email == i[0]]
            if dbid.__len__() == 1:
                dbid = dbid[0]
                fb = DBase.checkIncriptPassword(message.text, DBase.getUserRow(dbid)["password"])
                if fb:
                    DBase.setTlId(dbid, message.from_user.id)
                    adminsMessage("userLogedIn#", dbid=dbid, tlid=message.chat.id)
                    if initValus()[0]["mode"] == "menu":
                        mainMenu(message)
                    else:
                        status(message, dbid)
                else:
                    wrongPass(message)
            else:
                wrongPass(message)
        else:
            wrongPass(message)


    def messageAction(message):
        tlids = [int(x) for x in list(dict().fromkeys([str(x) for x in DBase.getTlId().values()]).keys())]
        for i in tlids:
            if i not in [None, 0]:
                try:
                    bot.send_message(i, message.text)
                except:
                    pass
        clearVars(message.chat.id)
        controlPanel(message)


    def ticketAction(message):
        messageBudy = message.text
        dbid = DBase.getIdFromTlid(message.chat.id)
        user = DBase.getUserRow(dbid)
        ticketFile = initValus()[3]
        textSend = initValus()[1]["supportBudy"].format(
            email=user["email"],
            id=dbid,
            tlid=message.chat.id,
            date=getTehranTime(timeSystem.time())[0]
        ) + messageBudy
        if not f"{message.chat.id}" in ticketFile.keys():
            ticketFile[f"{message.chat.id}"] = [(ticketFile["time"], textSend, message.chat.id)]
        else:
            ticketFile[f"{message.chat.id}"].append((ticketFile["time"], textSend, message.chat.id))
        ticketFile["time"] += 1
        try:
            bot.send_message(initValus()[0]["supportId"], textSend, reply_markup=respondSupportMarkup(message))
        except:
            pass

        try:
            bot.send_message(message.chat.id, initValus()[1]["successfullySent"])
        except:
            pass

        setValus(ticketFile, "ticket.json")
        clearVars(message.chat.id)
        mainMenu(message)


    def respondAction(message):
        ticketFile = initValus()[3]
        respondBudy = message.text
        textSend = initValus()[1]["respondSend"] + respondBudy
        val = getLogVar(message.chat.id, "val")
        if not f"{message.chat.id}" in ticketFile.keys():
            ticketFile[f"{message.chat.id}"] = [(ticketFile["time"], textSend, val)]
        else:
            ticketFile[f"{message.chat.id}"].append((ticketFile["time"], textSend, val))
        ticketFile["time"] += 1
        setValus(ticketFile, "ticket.json")
        try:
            bot.send_message(val, textSend)
        except:
            pass
        try:
            bot.send_message(message.chat.id, initValus()[1]["successfullySent"])
        except:
            pass
        clearVars(message.chat.id)
        mainMenu(message)


    def searchTextAction(message):
        textBudy = message.text
        try:
            var.changeTextMenu = abs(int(textBudy)) - 1
            editText(message)
        except:
            try:
                bot.send_message(message.chat.id, "Invalid Parameter ❌")
            except:
                pass
            editText(message)


    def smartSearch(text, tlid):
        keySearch = ""
        resultList = []
        accounts = DBase.getAccountsFromTlid(tlid)
        staffDBids = []
        for i in accounts.keys():
            if DBase.getUserRow(int(i))["is_staff"] == 1:
                staffDBids.append(int(i))
        usersList = DBase.getTableDict(table("v2_user"))
        if "token=" in text:
            text = sup(text, "=")[-1]
        for user in usersList:
            data = [*[[user["token"], "token"],
                      [user["uuid"], "uuid"],
                      [user["telegram_id"], "telegram_id"] if text.__len__() > 6 else [None, None]],
                    [user["remarks"], "remarks"],
                    [user["email"], "email"],
                    [user["id"], "id"],
                    [user["invite_user_id"],
                     "invite_user_id"]]
            keyFound = ""
            for i in data:
                if i[0] is not None and text.lower() in str(i[0]).lower():
                    keyFound = i[1]
                    break
            if keyFound != "":
                if not tlid in getStaffsTlid():
                    resultList.append((user["id"], user["email"], keyFound))
                else:
                    if user["invite_user_id"] is not None and user["invite_user_id"] in staffDBids:
                        resultList.append((user["id"], user["email"], keyFound))
        return resultList


    def smartSearchUsersAction(message):
        textBudy = message.text
        chatKey = getLogVar(message.chat.id, "chatKey")
        if "|" in chatKey:
            try:
                idx = [abs(int(textBudy)) - 1 if int(textBudy) != 0 else 1][0]
                _, textBudy = sup(chatKey, "|")
                try:
                    bot.send_message(message.chat.id, f"User Found by Key:\n{textBudy} ✅",
                                     reply_markup=smartSearchMarkup(textBudy, message.chat.id, menuIdx=int(idx)))
                except:
                    pass

            except:
                try:
                    bot.send_message(message.chat.id, "Wrong Parameter ❌")
                except:
                    pass

                return
        else:
            resultList = smartSearch(textBudy, message.chat.id)
            if resultList.__len__() != 0:
                try:
                    bot.send_message(message.chat.id, f"User Found by Key:\n{textBudy} ✅",
                                     reply_markup=smartSearchMarkup(textBudy, message.chat.id))
                except:
                    pass

            else:
                try:
                    bot.send_message(message.chat.id, "User Not Found ❌", reply_markup=returnMarkup("users^#"))

                except:
                    pass


    def searchUsersAction(message):
        textBudy = message.text
        chatKey = getLogVar(message.chat.id, "chatKey")
        if "|" in chatKey:
            try:
                idx = [abs(int(textBudy)) - 1 if int(textBudy) != 0 else 1][0]
                users(message, menuIdx=idx)
            except:
                try:
                    bot.send_message(message.chat.id, "Wrong Parameter ❌")
                except:
                    pass
                users(message)
                return
        else:
            pass


    def searchStaffsAction(message):
        textBudy = message.text
        chatKey = getLogVar(message.chat.id, "chatKey")
        if "|" in chatKey:
            try:
                idx = [abs(int(textBudy)) - 1 if int(textBudy) != 0 else 1][0]
                staffs(message, menuIdx=idx)
            except:
                try:
                    bot.send_message(message.chat.id, "Wrong Parameter ❌")
                except:
                    pass
                staffs(message)
                return
        else:
            pass


    def noteAction(message):
        textBudy = message.text
        dbid = getLogVar(message.chat.id, "dbid")
        mod = getLogVar(message.chat.id, "val")
        if textBudy == "#":
            textBudy = "NULL"
        fb = DBase.setValue(table("v2_user"), "remarks", str(textBudy).encode("utf-8"), dbid)
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["successfully"])
            except:
                pass
            status(message, dbid, mod=mod)
        else:
            try:
                bot.send_message(message.chat.id, "There's an Error, Error code: 1559 ❌")
            except:
                pass
            mainMenu(message)
        clearVars(message.chat.id)


    def addSniAction(message):
        textBudy = message.text
        if ":" in textBudy and textBudy.__len__() == 5:
            if int(sup(textBudy, ":")[0]) <= 23 and int(sup(textBudy, ":")[1]) <= 59:
                conf = initValus()[0]
                if conf["serviceSniTime"] != "" and (
                        ";" in conf["serviceSniTime"] or str(conf["serviceSniTime"]).count(":") == 1):
                    conf["serviceSniTime"] += f";{textBudy}"
                else:
                    conf["serviceSniTime"] += f"{textBudy}"
                fb = setValus(conf, "config.json")
                try:
                    bot.send_message(message.chat.id, initValus()[1]["addedSuccessfully"])
                except:
                    pass

                sni(message)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
                except:
                    pass

                sni(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
            except:
                pass

            sni(message)


    def addWarningAction(message):
        textBudy = message.text
        if ":" in textBudy and textBudy.__len__() == 5:
            if int(sup(textBudy, ":")[0]) <= 23 and int(sup(textBudy, ":")[1]) <= 59:
                conf = initValus()[0]
                if conf["serviceWarningTime"] != "" and (
                        ";" in conf["serviceWarningTime"] or str(conf["serviceWarningTime"]).count(":") == 1):
                    conf["serviceWarningTime"] += f";{textBudy}"
                else:
                    conf["serviceWarningTime"] += f"{textBudy}"
                fb = setValus(conf, "config.json")
                try:
                    bot.send_message(message.chat.id, initValus()[1]["addedSuccessfully"])
                except:
                    pass

                warning(message)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
                except:
                    pass

                warning(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
            except:
                pass

            warning(message)


    def addOnlineAction(message):
        textBudy = message.text
        if ":" in textBudy and textBudy.__len__() == 5:
            if int(sup(textBudy, ":")[0]) <= 23 and int(sup(textBudy, ":")[1]) <= 59:
                conf = initValus()[0]
                if conf["serviceOnlineTime"] != "" and (
                        ";" in conf["serviceOnlineTime"] or str(conf["serviceOnlineTime"]).count(":") == 1):
                    conf["serviceOnlineTime"] += f";{textBudy}"
                else:
                    conf["serviceOnlineTime"] += f"{textBudy}"
                fb = setValus(conf, "config.json")
                try:
                    bot.send_message(message.chat.id, initValus()[1]["addedSuccessfully"])
                except:
                    pass

                online(message)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
                except:
                    pass

                online(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
            except:
                pass

            online(message)


    def addNewAction(message):
        textBudy = message.text
        if ":" in textBudy and textBudy.__len__() == 5:
            if int(sup(textBudy, ":")[0]) <= 23 and int(sup(textBudy, ":")[1]) <= 59:
                conf = initValus()[0]
                if conf["serviceNewTime"] != "" and (
                        ";" in conf["serviceNewTime"] or str(conf["serviceNewTime"]).count(":") == 1):
                    conf["serviceNewTime"] += f";{textBudy}"
                else:
                    conf["serviceNewTime"] += f"{textBudy}"
                fb = setValus(conf, "config.json")
                try:
                    bot.send_message(message.chat.id, initValus()[1]["addedSuccessfully"])
                except:
                    pass

                new(message)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
                except:
                    pass

                new(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
            except:
                pass

            online(message)


    def customRechargeAction(message):
        textBudy = message.text
        val = getLogVar(message.chat.id, "val")
        mod = ""
        if message.chat.id in DBase.getStaffTlId():
            mod = "staff"
        elif message.chat.id in DBase.getAdminTlId():
            mod = "admin"
        try:
            if textBudy.isdigit():
                textBudy = int(textBudy)
                days = int(textBudy * 86400)
                nowTime = int(timeSystem.time())
                DBase.setValue(table("v2_user"), "expired_at", nowTime + days, val)
                if mod == "staff":
                    adminsMessage("adminNoticRecharge", day=textBudy, email=DBase.getUserRow(val)["email"],
                                  invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"], mode="staff")
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["successfullyCharged"].format(day=textBudy,
                                                                                                       email=
                                                                                                       DBase.getUserRow(
                                                                                                           val)[
                                                                                                           "email"],
                                                                                                       mod=
                                                                                                       initValus()[1][
                                                                                                           "day"]))
                    except:
                        pass

                elif mod == "admin":
                    adminsMessage("adminNoticRecharge", day=textBudy, email=DBase.getUserRow(val)["email"])
            else:
                if ":" in textBudy:
                    if textBudy.count(":") == 2:
                        hour, minut, sec = [int(i) for i in sup(textBudy, ":")]
                        hour = int(hour * 3600)
                        minut = int(minut * 60)
                        nowTime = int(timeSystem.time())
                        DBase.setValue(table("v2_user"), "expired_at", nowTime + hour + minut + sec, val)
                        strHour = sup(str(float((hour + minut + sec) / 3600)), ".")
                        strHour = strHour[0] + "." + strHour[1][:2]
                        if mod == "staff":
                            adminsMessage("adminNoticRecharge", hour=strHour, email=DBase.getUserRow(val)["email"],
                                          invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"],
                                          mode="staff")
                            try:
                                bot.send_message(message.chat.id,
                                                 initValus()[1]["successfullyCharged"].format(day=strHour,
                                                                                              email=
                                                                                              DBase.getUserRow(
                                                                                                  val)[
                                                                                                  "email"],
                                                                                              mod=
                                                                                              initValus()[
                                                                                                  1][
                                                                                                  "hour"]))
                            except:
                                pass

                        elif mod == "admin":
                            adminsMessage("adminNoticRecharge", hour=strHour, email=DBase.getUserRow(val)["email"])
                    elif textBudy.count(":") == 3:
                        days, hour, minut, sec = [int(i) for i in sup(textBudy, ":")]
                        days = int(days * 86400)
                        hour = int(hour * 3600)
                        minut = int(minut * 60)
                        nowTime = int(timeSystem.time())
                        DBase.setValue(table("v2_user"), "expired_at", nowTime + days + hour + minut + sec, val)
                        strDay = sup(str(float((days + hour + minut + sec) / 86400)), ".")
                        strDay = strDay[0] + "." + strDay[1][:2]
                        if mod == "staff":
                            adminsMessage("adminNoticRecharge", day=strDay, email=DBase.getUserRow(val)["email"],
                                          invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"],
                                          mode="staff")
                            try:
                                bot.send_message(message.chat.id,
                                                 initValus()[1]["successfullyCharged"].format(day=strDay,
                                                                                              email=
                                                                                              DBase.getUserRow(
                                                                                                  val)[
                                                                                                  "email"],
                                                                                              mod=
                                                                                              initValus()[
                                                                                                  1][
                                                                                                  "day"]))
                            except:
                                pass

                        elif mod == "admin":
                            adminsMessage("adminNoticRecharge", day=strDay, email=DBase.getUserRow(val)["email"])
                    else:
                        try:
                            bot.send_message(message.chat.id, "Wrong Parameter ❌")
                        except:
                            pass

                elif textBudy == "#":
                    DBase.setValue(table("v2_user"), "expired_at", None, val)

        except:
            try:
                bot.send_message(message.chat.id, "Wrong Parameter ❌")
            except:
                pass

        status(message, val, mod=mod)


    def allRechAction(message):
        textBudy = message.text
        if textBudy.isdigit():
            try:
                bot.send_message(message.chat.id, initValus()[1]["allRechBudy"].format(day=int(textBudy)),
                                 reply_markup=allRechMarkup(int(textBudy)))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
            except:
                pass


    def checkCoupon(couponText):
        coupons = DBase.getTableDict(table("v2_coupon"))
        try:
            for i in coupons:
                if i["code"] == couponText:
                    if i["limit_use"] is None:
                        return [True, ""]
                    if i["limit_use"] > 0:
                        fb = DBase.setValue(table("v2_coupon"), "limit_use", i["limit_use"] - 1, i["id"])
                        if fb:
                            return [True, i["limit_use"] - 1]
                        else:
                            return [False]
                    else:
                        return [-1]
            return [None]
        except:
            return [False]


    def couponAction(message):
        textBudy = message.text
        dbid = getLogVar(message.chat.id, "dbid")
        fb = checkCoupon(textBudy)
        if None in fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["couponFalse"])
            except:
                pass

        elif -1 in fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["couponExpired"])
            except:
                pass

        elif True in fb:
            if fb[1] != "":
                try:
                    bot.send_message(message.chat.id, initValus()[1]["couponLeft"].format(count=fb[1]))
                except:
                    pass

            recharge(message, dbid, mod="staff")
            status(message, dbid, mod="staff", exitDestination="users^")
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["couponError"])
            except:
                pass

        clearVars(message.chat.id)


    def customCouponAction(message):
        textBudy = message.text
        couponId = getLogVar(message.chat.id, "dbid")
        if textBudy != "#":
            if textBudy.isdigit():
                count = int(textBudy)
                couponRecharge(message, couponId, count)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])
                except:
                    pass

        else:
            couponRecharge(message, couponId, "NULL")
        couponSettings(message, couponId)
        clearVars(message.chat.id)


    def couponEditAction(message):
        textBudy = message.text
        couponId = getLogVar(message.chat.id, "dbid")
        fb = DBase.setValue(table("v2_coupon"), "code", textBudy, couponId)
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["couponEditSuccessful"].format(code=textBudy))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id, "There's an ERROR, ERROR CODE: 1836")
            except:
                pass

        couponSettings(message, couponId)
        clearVars(message.chat.id)


    def paymentAction(message):
        textBudy = message.text
        dbid = int(getLogVar(message.chat.id, "val"))
        if textBudy.isdigit():
            payment(message, f"both|payment|payReq|{dbid}|{textBudy}")
        else:
            bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])


    def payReqAmountAction(message):
        textBudy = message.text
        dbid = int(getLogVar(message.chat.id, "val"))
        if textBudy.isdigit():
            payRequestAmount(message, f"staff|payReq|amount|{textBudy}|{dbid}")
        else:
            bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])


    def payReqCardAction(message):
        textBudy = message.text
        textBudy = textBudy.replace(" ", "")
        dbid, amount = sup(getLogVar(message.chat.id, "val"), "|")
        if textBudy.isdigit():
            requestPaymentAdmin(message, f"staff|payReq|req|{dbid}|{amount}|{textBudy}")
        else:
            bot.send_message(message.chat.id, initValus()[1]["wrongParameters"])


    #
    # def checkLog():
    #     ids = DBase.getColumnCustom("v2_user", "id")
    #     for id in ids:
    #         checkWarningLog(id)
    #     for id in ids:
    #         userStatus = DBase.getUserStatus(id)
    #         try:
    #             expLast = int(sup(userStatus["expireLast"], " ")[-1][:-1])
    #         except:
    #             expLast = 10E10
    #         if expLast > initValus()[0]["warningTerm"]:
    #             val = initValus()[2]
    #             val["warning"][str(id)].clear()
    #             setValus(val, "log.json")

    # def updateService():
    #     # do the things
    #     counter = int(getTehranTime().timestamp())
    #     var.updateCounter = counter
    #     while True:
    #         time.sleep(1)
    #         if int(getTehranTime().timestamp()) - counter > initValus()[0]["serviceTime"]:
    #             service()
    #             counter = int(getTehranTime().timestamp())
    #             var.updateCounter = counter

    @bot.message_handler(commands=['start'])
    def start(message):
        log = getLogFile()
        if not str(initValus()[0]["superAdminDBid"]) in DBase.getAccountsFromTlid(
                message.chat.id).keys() and True in [True for i in
                                                     list(DBase.getAccountsFromTlid(message.chat.id).keys())
                                                     if int(i) in log["block"]]:
            return None
        clearVars(message.chat.id)
        if initValus()[0]["mode"] == "menu":
            id = message.chat.id
            if list(DBase.getTlId().values()).count(id) == 0:
                setupMessage(message)
            else:
                mainMenu(message)
        else:
            id = message.chat.id
            if list(DBase.getTlId().values()).count(id) == 0:
                setupMessage(message)
            else:
                status(message, DBase.getIdFromTlid(id))


    @bot.message_handler(func=lambda message: True)
    def start(message):
        log = getLogFile()
        if not str(initValus()[0]["superAdminDBid"]) in DBase.getAccountsFromTlid(
                message.chat.id).keys() and True in [True for i in
                                                     list(DBase.getAccountsFromTlid(message.chat.id).keys())
                                                     if int(i) in log["block"]]:
            return None
        if var(message.chat.id).mod["login"]:
            loginAction(message)
        elif var(message.chat.id).mod["password"]:
            passwordAction(message)
        elif var(message.chat.id).mod["neutral"]:
            if DBase.userExist(message.chat.id):
                mainMenu(message)
            else:
                setupMessage(message)
        elif var(message.chat.id).mod["add"]:
            passwordAction(message)
        elif var(message.chat.id).mod["edit"]:
            editAction(message)
        elif var(message.chat.id).mod["message"]:
            chatKey = getLogVar(message.chat.id, "chatKey")
            if chatKey == "messageAll":
                messageAction(message)
            elif chatKey == "ticket":
                ticketAction(message)
            elif chatKey == "respond":
                respondAction(message)
            elif chatKey == "searchEditTextMenu":
                searchTextAction(message)
            elif chatKey == "addSni":
                addSniAction(message)
            elif chatKey == "addWarning":
                addWarningAction(message)
            elif chatKey == "addOnline":
                addOnlineAction(message)
            elif "searchUsers" in chatKey:
                searchUsersAction(message)
            elif "smartSearchUsers" in chatKey:
                smartSearchUsersAction(message)
            elif "customRecharge" in chatKey:
                customRechargeAction(message)
            elif "searchStaffs" in chatKey:
                searchStaffsAction(message)
            elif "note" in chatKey:
                noteAction(message)
            elif "couponEdit" in chatKey:
                couponEditAction(message)
            elif "coupon" in chatKey:
                couponAction(message)
            elif "customCouponRecharge" in chatKey:
                customCouponAction(message)
            elif "addNew" in chatKey:
                addNewAction(message)
            elif "allRech" in chatKey:
                allRechAction(message)
            elif "payment" in chatKey:
                paymentAction(message)
            elif "payReqAmount" in chatKey:
                payReqAmountAction(message)
            elif "payReqCard" in chatKey:
                payReqCardAction(message)


    @bot.callback_query_handler(func=lambda message: True)
    def callback_query(call):
        log = getLogFile()
        if not str(initValus()[0]["superAdminDBid"]) in DBase.getAccountsFromTlid(
                call.message.chat.id).keys() and True in [True for i in
                                                          list(DBase.getAccountsFromTlid(call.message.chat.id).keys())
                                                          if int(i) in log["block"]]:
            return None
        clearVars(call.message.chat.id, but=["changeTextMenu", "updateService", "changeUserMenu"])
        chatid = int(call.message.chat.id)
        usrEx = DBase.userExist(chatid)
        deleteFac = False
        if not "Link" in call.data and not "#" in call.data:
            try:
                bot.delete_message(chatid, call.message.message_id)
                deleteFac = True
            except:
                pass
        callData = str(call.data).replace("#", "")
        if callData == "buyInit":
            buy(call.message, init=True)
        elif usrEx:
            if "status" in callData:
                if not "textMenu" in callData:
                    callData = callData.replace("status", "")
                    if "admin" in callData:
                        callData = callData.replace("admin", "")
                        status(call.message, int(callData), mod="admin")
                    elif "staff" in callData:
                        callData = callData.replace("staff", "")
                        status(call.message, int(callData), mod="staff")
                    else:
                        status(call.message, int(callData))
                    callData = ""

            if call.message.chat.id in DBase.getStaffTlId() + DBase.getAdminTlId():
                if "both" in callData:
                    switch = sup(callData, "|")[1]
                    if switch == "payment":
                        payment(call.message, callData)
                    elif switch == "reciveBank":
                        reciveBank(call.message, callData)
                if "note" in callData:
                    dbid = int(callData.replace("note", ""))
                    note(call.message, dbid)
                if "confirm" in callData:
                    if "resetAccount" in callData:
                        callData = callData.replace("confirm", "")
                        dbid, mod = sup(callData.replace("resetAccount", ""), "|")
                        resetAccount(call.message, int(dbid), mod=mod, confirm=True)
                        callData = ""
                    elif "clearTraffic" in callData:
                        callData = callData.replace("confirm", "")
                        _, dbid, mod = sup(callData, "|")
                        resetTrafficSet(int(dbid))
                        status(call.message, int(dbid), mod=mod, exitDestination="users^")
                        callData = ""
                if "resetAccount" in callData:
                    dbid, mod = sup(callData.replace("resetAccount", ""), "|")
                    resetAccount(call.message, int(dbid), mod=mod)
                    callData = ""
                if "coupon" in callData:
                    dbid = int(callData.replace("coupon", ""))
                    coupon(call.message, dbid)
                if "changeSub" in callData:
                    callData = callData.replace("changeSub", "")
                    if "|" in callData:
                        dbid, subid = sup(callData, "|")
                        changeSub(call.message, int(dbid), subid=subid)
                    else:
                        dbid = int(callData)
                        changeSub(call.message, int(dbid))
                if "clearTraffic" in callData:
                    data = sup(callData.replace("clearTraffic", ""), "|")
                    dbid, mod = int(data[0]), data[1]
                    confirmForm(call.message, "clearTraffic", mod,
                                initValus()[1]["clearTrafficOfUser"].format(email=DBase.getUserRow(dbid)["email"]),
                                supVal=f"|{dbid}|")
                    callData = ""
                if "refresh" in callData:
                    data = sup(callData.replace("refresh", ""), "|")
                    dbid, mod = int(data[0]), data[1]
                    status(call.message, dbid, mod=mod, exitDestination="users^")
                    callData = ""
                if "allRech" in callData:
                    allRech(call.message)
            if call.message.chat.id in DBase.getAdminTlId():
                if callData == "controlPanel":
                    controlPanel(call.message)
                if "textMenu" in callData:
                    callData = callData.replace("textMenu", "", 1)
                    fb = True
                    if "$" in callData:
                        callData = sup(callData, "$")[1]
                        for i in list(initValus()[1].keys()):
                            if callData == i:
                                setText(call.message, i, initValus()[1][i])
                                fb = False
                                break
                        callData = ""
                    if "-" in callData:
                        if var.changeTextMenu != 0:
                            var.changeTextMenu -= 1
                    elif "+" in callData:
                        var.changeTextMenu += 1
                    if "Search" in callData:
                        textSearch(call.message)
                        fb = False
                    if fb:
                        if "^" in callData:
                            editText(call.message)
                        else:
                            editText(call.message, deleteFac=False)
                    callData = ""
                if "new" in callData:
                    if "+" in callData:
                        newActive(call.message, True)
                    elif "-" in callData:
                        newActive(call.message, False)
                    elif "Add" in callData:
                        addNewTime(call.message)
                    elif "Sub" in callData:
                        subNewTime(call.message)
                    elif "UpdateNow" in callData:
                        manualNewReport(DBase, call.message)
                        new(call.message)
                    elif "&" in callData:
                        newDeleteTime(call.message, sup(callData, "&")[-1])
                    else:
                        new(call.message)
                    callData = ""
                if "setCoupon" in callData:
                    callData = callData.replace("setCoupon", "")
                    if "$" in callData:
                        callData = callData.replace("$", "")
                        couponSettings(call.message, int(callData))
                    elif "*" in callData:
                        callData = callData.replace("*", "")
                        limitLast = DBase.getTableRowId(table("v2_coupon"), int(callData))["limit_use"]
                        if limitLast is not None:
                            couponRecharge(call.message, int(callData),
                                           initValus()[0]["rechargeCouponTerm"] + limitLast)
                        couponSettings(call.message, int(callData))
                    elif "&" in callData:
                        callData = callData.replace("&", "")
                        try:
                            bot.send_message(call.message.chat.id, initValus()[1]["customCouponBudy"],
                                             reply_markup=cancelMarkup(f"$setCoupon{int(callData)}"))
                        except:
                            pass

                        setLogVar(call.message.chat.id, "chatKey", value="customCouponRecharge")
                        setLogVar(call.message.chat.id, "dbid", value=int(callData))
                        chatMode(call.message.chat.id, "message")
                    elif "on" in callData:
                        callData = callData.replace("on", "")
                        setCouponStatus(call.message, 1, int(callData))
                    elif "off" in callData:
                        callData = callData.replace("off", "")
                        setCouponStatus(call.message, 0, int(callData))
                    elif "edit" in callData:
                        callData = callData.replace("edit", "")

                        try:
                            bot.send_message(call.message.chat.id,
                                             DBase.getTableRowId(table("v2_coupon"), int(callData))["code"],
                                             reply_markup=cancelMarkup(f"$setCoupon{int(callData)}"))
                        except:
                            pass

                        setLogVar(call.message.chat.id, "chatKey", value="couponEdit")
                        setLogVar(call.message.chat.id, "dbid", value=int(callData))
                        chatMode(call.message.chat.id, "message")
                    else:
                        setCouponsShow(call.message)
                if "admin" in callData:
                    callData = callData.replace("admin", "")
                    if "+" in callData:
                        callData = callData.replace("+", "")
                        makeUserAdmin(int(callData), mod=True)
                    elif "-" in callData:
                        callData = callData.replace("-", "")
                        makeUserAdmin(int(callData), mod=False)
                    status(call.message, int(callData), mod="admin")
                    callData = ""
                if "distributor" in callData:
                    callData = callData.replace("distributor", "")
                    if "+" in callData:
                        callData = callData.replace("+", "")
                        makeUserDistributor(int(callData), mod=True)
                    elif "-" in callData:
                        callData = callData.replace("-", "")
                        makeUserDistributor(int(callData), mod=False)
                    status(call.message, int(callData), mod="admin")
                    callData = ""
                if "users" in callData:
                    callData = callData.replace("users", "", 1)
                    fb = False
                    if "$" in callData:
                        callData = sup(callData, "$")[1]
                        userId = ""
                        exitDestination = ""
                        if "|" in callData:
                            userId, exitDestination = sup(callData, "|")
                        else:
                            userId = callData
                        status(call.message, int(userId), mod="admin", exitDestination=exitDestination)
                        callData = ""
                    elif "Search" in callData:
                        callData = callData.replace("Search", "")
                        if "Smart" in callData:
                            callData = callData.replace("Smart", "")
                            if "-" in callData:
                                callData = callData.replace("-", "")
                                idx, searchPhrase = sup(callData, "|")
                                idx = int(idx)
                                if int(idx) != 0:
                                    idx -= 1
                                bot.edit_message_text(f"User Found by Key:{searchPhrase} ✅", call.message.chat.id,
                                                      call.message.message_id,
                                                      reply_markup=smartSearchMarkup(searchPhrase, call.message.chat.id,
                                                                                     menuIdx=idx))
                            elif "*" in callData:
                                callData = callData.replace("*", "")
                                searchPhrase = callData.replace("|", "")
                                chatMode(call.message.chat.id, "message")
                                setLogVar(call.message.chat.id, "chatKey", value=f"smartSearchUsers|{searchPhrase}")
                                try:
                                    bot.send_message(call.message.chat.id, "what page?: ",
                                                     reply_markup=cancelMarkup("users^"))
                                except:
                                    pass

                            elif "+" in callData:
                                callData = callData.replace("+", "")
                                idx, searchPhrase = sup(callData, "|")
                                idx = int(idx) + 1
                                bot.edit_message_text(f"User Found by Key:{searchPhrase} ✅", call.message.chat.id,
                                                      call.message.message_id,
                                                      reply_markup=smartSearchMarkup(searchPhrase, call.message.chat.id,
                                                                                     menuIdx=idx))
                            else:
                                usersSmartSearch(call.message)
                        else:
                            usersSearch(call.message)
                        callData = ""
                    elif "-" in callData:
                        callData = callData.replace("-", "")
                        idx = callData.replace("|", "")
                        idx = int(idx)
                        if int(idx) != 0:
                            idx -= 1
                        users(call.message, menuIdx=idx, deleteFac=False, mod="admin")
                    elif "*" in callData:
                        callData = callData.replace("*", "")
                        chatMode(call.message.chat.id, "message")
                        setLogVar(call.message.chat.id, "chatKey", value=f"searchUsers|")
                        try:
                            bot.send_message(call.message.chat.id, "what page?: ", reply_markup=cancelMarkup("users^"))
                        except:
                            pass

                    elif "+" in callData:
                        callData = callData.replace("+", "")
                        idx = callData.replace("|", "")
                        idx = int(idx) + 1
                        users(call.message, menuIdx=idx, deleteFac=False, mod="admin")
                    elif "ban" in callData:
                        if "unban" in callData:
                            callData = callData.replace("unban", "")
                            banAccount(call.message, int(callData), ban=False)
                        else:
                            callData = callData.replace("ban", "")
                            banAccount(call.message, int(callData))
                    else:
                        fb = True
                    if fb:
                        if "^" in callData:
                            users(call.message, mod="admin")
                        else:
                            users(call.message, deleteFac=False, mod="admin")
                    callData = ""
                if "staffs" in callData:
                    callData = callData.replace("staffs", "", 1)
                    if "+" in callData:
                        callData = callData.replace("+", "")
                        idx = int(callData.replace("|", "")) + 1
                        staffs(call.message, menuIdx=idx, edit=True)
                    elif "*" in callData:
                        callData = callData.replace("*", "")
                        chatMode(call.message.chat.id, "message")
                        setLogVar(call.message.chat.id, "chatKey", value=f"searchStaffs|")
                        try:
                            bot.send_message(call.message.chat.id, "what page?: ", reply_markup=cancelMarkup("staffs^"))
                        except:
                            pass

                    elif "-" in callData:
                        callData = callData.replace("-", "")
                        idx = int(callData.replace("|", ""))
                        if idx != 0:
                            idx -= 1
                        staffs(call.message, menuIdx=idx, edit=True)
                    elif "$" in callData:
                        callData = callData.replace("$", "")
                        staffs(int(callData))
                    else:
                        if "^" in callData:
                            staffs(call.message)
                        else:
                            staffs(call.message, edit=True)
                    callData = ""
                if "services" in callData:
                    services(call.message)
                if "online" in callData:
                    if "Block" in callData:
                        callData = callData.replace("onlineBlock", "")
                        key = [True if "+" in callData else False][0]
                        onlineBlock(call.message, int(callData[:-1]), key)
                        status(call.message, int(callData[:-1]), mod="admin")
                        callData = ""
                    elif "+" in callData:
                        onlineActive(call.message, True)
                    elif "-" in callData:
                        onlineActive(call.message, False)
                    elif "Add" in callData:
                        addOnlineTime(call.message)
                    elif "Sub" in callData:
                        subOnlineTime(call.message)
                    elif "UpdateNow" in callData:
                        manualOnlineWarning(DBase, call.message, force=True)
                        online(call.message)
                    elif "Show" in callData:
                        manualOnline(DBase, call.message)
                        online(call.message)
                    elif "&" in callData:
                        onlineDeleteTime(call.message, sup(callData, "&")[-1])
                    else:
                        online(call.message)
                    callData = ""
                if "sni" in callData:
                    if "+" in callData:
                        sniActive(call.message, True)
                    elif "-" in callData:
                        sniActive(call.message, False)
                    elif "Add" in callData:
                        addSniTime(call.message)
                    elif "Sub" in callData:
                        subSniTime(call.message)
                    elif "UpdateNow" in callData:
                        manualSniRandom(DBase, call.message)
                        sni(call.message)
                    elif "&" in callData:
                        sniDeleteTime(call.message, sup(callData, "&")[-1])
                    elif "SwitchNotic" in callData:
                        switchSniNotic(call.message)
                    elif "Show" in callData:
                        var.sniShow = True
                        manualSniRandom(DBase, call.message)
                        var.sniShow = False
                        sni(call.message)
                    else:
                        sni(call.message)
                    callData = ""
                if "warning" in callData:
                    if "+" in callData:
                        warningActive(call.message, True)
                    elif "-" in callData:
                        warningActive(call.message, False)
                    elif "Add" in callData:
                        addWarningTime(call.message)
                    elif "Sub" in callData:
                        subWarningTime(call.message)
                    elif "&" in callData:
                        warningDeleteTime(call.message, sup(callData, "&")[-1])
                    else:
                        warning(call.message)
                    callData = ""
                if callData == "sendMessage":
                    sendMessage(call.message)
                if callData == "updateForce":
                    updateForce(call.message)
                if "ticket" in callData:
                    callData = callData.replace("ticket", "")
                    if "+" in callData:
                        if "delete" in callData:
                            try:
                                bot.send_message(call.message.chat.id, initValus()[1]["confirmClickTicket"],
                                                 reply_markup=confirmTicketMarkup())
                            except:
                                pass

                        elif "confirm" in callData:
                            dic = {"time": 0}
                            setValus(dic, "ticket.json")
                            try:
                                bot.send_message(call.message.chat.id, initValus()[1]["successfullDeleted"])
                            except:
                                pass

                            viewTicket(call.message)
                        else:
                            ticketId = int(str(callData).replace("+", ""))
                            ticketShow(call.message, ticketId)
                        callData = ""
                    else:
                        viewTicket(call.message)
                if "confirm" in callData:
                    if "deleteAccount" in callData:
                        callData = callData.replace("confirm", "")
                        callData = callData.replace("deleteAccount", "")
                        deleteAccount(call.message, int(callData), confirm=True)
                        callData = ""
                    if "AllRech" in callData:
                        callData = callData.replace("confirm", "")
                        callData = callData.replace("AllRech", "")
                        day = int(callData)
                        allRech(call.message, confirm=True, days=day)
                if "deleteAccount" in callData:
                    callData = callData.replace("deleteAccount", "")
                    deleteAccount(call.message, int(callData))
                if "updateForceConfirm" in callData:
                    rep = sup(callData, "-")[1]
                    adminOrAll = sup(callData, "-")[2]
                    updateForceConfirm(call.message, rep, adminOrAll)
                    callData = ""
                if "justAdmin" in callData:
                    rep = sup(callData, "-")[1]
                    justAdmin(call.message, rep)
                    callData = ""
                elif "forAll" in callData:
                    rep = sup(callData, "-")[1]
                    forAll(call.message, rep)
                    callData = ""
                if "repeat" in callData:
                    callData = callData.replace("repeat", "")
                    if "no" in callData:
                        norepeat(call.message)
                    else:
                        repeat(call.message)
                    callData = ""
                if "*" in callData:
                    dbId = int(str(callData).replace("*", ""))
                    recharge(call.message, dbId)
                if "recharge" in callData:
                    callData = callData.replace("recharge", "")
                    customRecharge(call.message, int(callData))
                if "!" in callData:
                    dbId = int(str(callData).replace("!", ""))
                    emergency(call.message, dbId, mod="admin")
                    callData = ""
                if "tickets" in callData:
                    ticketId = int(str(callData).replace("+", ""))
                    ticketShow(call.message, ticketId)
            elif call.message.chat.id in DBase.getStaffTlId():
                if "online" in callData:
                    if "Block" in callData:
                        callData = callData.replace("onlineBlock", "")
                        key = [True if "+" in callData else False][0]
                        onlineBlock(call.message, int(callData[:-1]), key)
                        status(call.message, int(callData[:-1]), mod="staff")
                        callData = ""
                if "staff" in callData and "|" in callData:
                    switch = sup(callData, "|")[1]
                    if switch == "wallet":
                        wallet(call.message)
                    elif switch == "payReq":
                        print("payReq")
                        try:
                            key = sup(callData, "|")[2]
                            print("key")
                            if key == "amount":
                                print("amount")
                                payRequestAmount(call.message, callData)
                            elif key == "req":
                                requestPaymentAdmin(call.message, callData)
                            else:
                                staffId = int(key)
                                payRequest(call.message, staffId)
                        except:
                            try:
                                bot.send_message(call.message.chat.id, "There is an ERROR, Error code: 2950")
                            except:
                                pass

                if "staff" in callData:
                    callData = callData.replace("staff", "")
                if callData == "Panel":
                    distributorPanel(call.message)
                if "users" in callData:
                    callData = callData.replace("users", "", 1)
                    fb = False
                    if "$" in callData:
                        callData = sup(callData, "$")[1]
                        status(call.message, int(callData), mod="staff")
                        callData = ""
                    elif "Search" in callData:
                        callData = callData.replace("Search", "")
                        if "Smart" in callData:
                            callData = callData.replace("Smart", "")
                            if "-" in callData:
                                callData = callData.replace("-", "")
                                idx, searchPhrase = sup(callData, "|")
                                idx = int(idx)
                                if int(idx) != 0:
                                    idx -= 1
                                bot.edit_message_text(f"User Found by Key:{searchPhrase} ✅", call.message.chat.id,
                                                      call.message.message_id,
                                                      reply_markup=smartSearchMarkup(searchPhrase, message.chat.id,
                                                                                     menuIdx=idx))
                            elif "*" in callData:
                                callData = callData.replace("*", "")
                                searchPhrase = callData.replace("|", "")
                                chatMode(call.message.chat.id, "message")
                                setLogVar(call.message.chat.id, "chatKey", value=f"smartSearchUsers|{searchPhrase}")
                                try:
                                    bot.send_message(call.message.chat.id, "what page?: ",
                                                     reply_markup=cancelMarkup("users^"))
                                except:
                                    pass


                            elif "+" in callData:
                                callData = callData.replace("+", "")
                                idx, searchPhrase = sup(callData, "|")
                                idx = int(idx) + 1
                                bot.edit_message_text(f"User Found by Key:{searchPhrase} ✅", call.message.chat.id,
                                                      call.message.message_id,
                                                      reply_markup=smartSearchMarkup(searchPhrase, message.chat.id,
                                                                                     menuIdx=idx))
                            else:
                                usersSmartSearch(call.message)
                        else:
                            usersSearch(call.message)
                        callData = ""
                    elif "-" in callData:
                        callData = callData.replace("-", "")
                        idx = callData.replace("|", "")
                        idx = int(idx)
                        if int(idx) != 0:
                            idx -= 1
                        users(call.message, menuIdx=idx, deleteFac=False, mod="staff")
                    elif "*" in callData:
                        callData = callData.replace("*", "")
                        chatMode(call.message.chat.id, "message")
                        setLogVar(call.message.chat.id, "chatKey", value=f"searchUsers|")
                        try:
                            bot.send_message(call.message.chat.id, "what page?: ", reply_markup=cancelMarkup("users^"))
                        except:
                            pass

                    elif "+" in callData:
                        callData = callData.replace("+", "")
                        idx = callData.replace("|", "")
                        idx = int(idx) + 1
                        users(call.message, menuIdx=idx, deleteFac=False, mod="staff")
                    elif "ban" in callData:
                        if "unban" in callData:
                            callData = callData.replace("unban", "")
                            banAccount(call.message, int(callData), mod="staff", ban=False)
                        else:
                            callData = callData.replace("ban", "")
                            banAccount(call.message, int(callData), mod="staff")
                    else:
                        fb = True
                    if fb:
                        if "^" in callData:
                            users(call.message, mod="staff")
                        else:
                            users(call.message, deleteFac=False, mod="staff")
                    callData = ""
                if "confirm" in callData:
                    callData = callData.replace("confirm", "")
                    if "deleteAccount" in callData:
                        callData = callData.replace("deleteAccount", "")
                        deleteAccount(call.message, int(callData), mod="staff", confirm=True)
                        callData = ""
                if "deleteAccount" in callData:
                    callData = callData.replace("deleteAccount", "")
                    deleteAccount(call.message, int(callData), mod="staff")
                if "*" in callData:
                    dbId = int(str(callData).replace("*", ""))
                    recharge(call.message, dbId, mod="staff")
                if "recharge" in callData:
                    callData = callData.replace("recharge", "")
                    customRecharge(call.message, int(callData))
                if "!" in callData:
                    dbId = int(str(callData).replace("!", ""))
                    emergency(call.message, dbId, mod="staff")
                    callData = ""

            if callData == "buy":
                buy(call.message)
            if "&" in callData:
                dbId = str(callData).replace("&", "")
                logout(call.message, dbId)
            if "!" in callData:
                dbId = int(str(callData).replace("!", ""))
                emergency(call.message, dbId)
            if "^" in callData:
                try:
                    tlid = int(str(callData).replace("^", ""))
                    respond(call.message, tlid)
                except:
                    pass
            if callData == "accounts":
                chatMode(call.message.chat.id, "neutral")
                accounts(call.message)
            if callData == "mainMenu":
                mainMenu(call.message)
            if callData == "addAccount":
                addAccount(call.message)
            if callData == "removeAccount":
                removeAccount(call.message)
            if callData == "contact":
                contact(call.message)
            if callData == "terms":
                terms(call.message)
            if callData == "subs":
                subs(call.message)
            if callData == "guide":
                guide(call.message)
            if callData == "rules":
                rules(call.message)
            if callData == "android":
                android(call.message)
            if callData == "iphone":
                iphone(call.message)
            if callData == "directLink":
                directLink(call.message)
            if callData == "askHelp":
                askHelp(call.message)
        else:
            setupMessage(call.message)


    # call Data

    # f"both|reciveBank|confirm|{staffId}"
    def reciveBank(message, data):
        status = [True if sup(data, "|")[2] == "confirm" else False][0]
        staffId = int(sup(data, "|")[3])
        staffUser = DBase.getUserRow(staffId)
        nowTime = getTehranTime(timeSystem.time())
        date = f"{nowTime[1]} {nowTime[0]}"
        payLog = getPaymentFile()
        fount = False
        amount = 0
        cardNum = 0
        found = False
        for i in payLog["request"]:
            if i["staffId"] == staffId:
                req = i
                found = True
                break
        if found:
            if status:
                for i in range(payLog["request"].__len__()):
                    if payLog["request"][i]["staffId"] == staffId:
                        amount = payLog["request"][i]["amount"]
                        cardNum = payLog["request"][i]["cardNum"]
                        archivePayment({"staffId": staffId, "date": date, "amount": amount,
                                        "cardNum": cardNum, "payRequestStatus": "Done!"})
                        del payLog["request"][i]
                        break
                staffTlid = staffUser["telegram_id"]
                if not staffTlid in [0, None]:
                    try:
                        bot.send_message(staffTlid, initValus()[1]["recivedConfirmed"].format(email=staffUser["email"], amount=amount, cardNum=cardNum))
                    except:
                        pass
                    payLog["staffBank"][str(staffId)]["payedAmount"] -= int(amount)
                    payLog["staffBank"][str(staffId)]["reciveStatus"] = f"{date}|{amount}"
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["successfullySent"])
                    except:
                        pass
                else:
                    try:
                        bot.send_message(message.chat.id, "There is an ERROR, Error code: 3137")
                    except:
                        pass
            else:
                for i in range(payLog["request"].__len__()):
                    if payLog["request"][i]["staffId"] == staffId:
                        amount = payLog["request"][i]["amount"]
                        cardNum = payLog["request"][i]["cardNum"]
                        archivePayment({"staffId": staffId, "date": date, "amount": amount,
                                        "cardNum": cardNum, "payRequestStatus": "Denied!"})
                        del payLog["request"][i]
                        break
                staffTlid = staffUser["telegram_id"]
                if not staffTlid in [0, None]:
                    try:
                        bot.send_message(staffTlid, initValus()[1]["recivedDenied"].format(email=staffUser["email"]))
                    except:
                        pass
                    payLog["staffBank"][str(staffId)]["reciveStatus"] = ""
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["successfullySent"])
                    except:
                        pass
                else:
                    try:
                        bot.send_message(message.chat.id, "There is an ERROR, Error code: 3154")
                    except:
                        pass
            setValus(payLog, "payment.json")
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
            except:
                pass


    def requestPaymentAdmin(message, data):
        _, _, _, staffId, amount, cardNum = sup(data, "|")
        cardNum = int(cardNum)
        staffUser = DBase.getUserRow(int(staffId))
        payment = getPaymentFile()
        per = True
        for i in payment["request"]:
            if int(i["staffId"]) == int(staffId):
                per = False
                break
        if per:
            if not cardNum in payment["staffBank"][staffId]["cardsNumber"]:
                payment["staffBank"][staffId]["cardsNumber"].append(cardNum)
            nowTime = getTehranTime(timeSystem.time())
            date = f"{nowTime[1]} {nowTime[0]}"
            email = staffUser["email"]
            req = {"staffId": int(staffId), "date": date, "amount": amount, "cardNum": cardNum}
            payment["request"].append(req)
            payment["staffBank"][staffId]["reciveStatus"] = "pending"
            setValus(payment, "payment.json")
            archivePayment(req)
            admins = DBase.getAdminTlId()
            for i in admins:
                try:
                    bot.send_message(i, initValus()[1]["sendRequestToAdmin"].format(email=email, amount=amount, card=cardNum,
                                                                                    date=date),
                                     reply_markup=payRequestAdminMarkup(staffId))
                except:
                    pass
            try:
                bot.send_message(message.chat.id, initValus()[1]["succssfullySentToAdmin"])
            except:
                pass
            clearVars(message.chat.id)
            wallet(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
            except:
                pass
            clearVars(message.chat.id)
            wallet(message)


    def payRequestAmount(message, data):
        amount = sup(data, "|")[3]
        staffId = sup(data, "|")[4]
        payment = getPaymentFile()
        if not str(staffId) in list(payment["staffBank"].keys()):
            payment["staffBank"][str(staffId)] = {"payedAmount": 0,
                                                  "payedAll": 0,
                                                  "payedCount": 0,
                                                  "percent": initValus()[0]["defaultPercentPayment"],
                                                  "reciveStatus": "",
                                                  "cardsNumber": []}
        userPayment = payment["staffBank"][staffId]
        per = True
        for i in payment["request"]:
            if i["staffId"] == int(staffId):
                per = False
                break
        if amount == "all":
            amount = int(userPayment["payedAmount"])
        elif amount.isdigit():
            amount = int(amount)
        if per:
            if 0 < amount <= userPayment["payedAmount"]:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["choseCard"], reply_markup=choseCardMarkup(int(staffId), amount))
                except:
                    pass
                chatMode(message.chat.id, "message")
                setLogVar(message.chat.id, "chatKey", value="payReqCard")
                setLogVar(message.chat.id, "val", value=f"{staffId}|{amount}")
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["amountIsOver"])
                except:
                    pass
                wallet(message)
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["lastReqPending"])
                wallet(message)
            except:
                pass

    def payRequest(message, staffId):
        staffUser = DBase.getUserRow(staffId)
        email = staffUser["email"]
        payment = getPaymentFile()
        if not str(staffId) in list(payment["staffBank"].keys()):
            payment["staffBank"][str(staffId)] = {"payedAmount": 0,
                                                         "payedAll": 0,
                                                         "payedCount": 0,
                                                         "percent": initValus()[0]["defaultPercentPayment"],
                                                         "reciveStatus": "",
                                                         "cardsNumber": []}
        userPayment = payment["staffBank"][str(staffId)]
        amount = int(userPayment["payedAmount"])
        if amount > 0:
            per = True
            for i in payment["request"]:
                if i["staffId"] == staffId:
                    per = False
                    break
            if per:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["amountRecive"].format(email=email, amount=amount),
                                 reply_markup=amountReciveMarkup(staffId))
                except:
                    pass
                chatMode(message.chat.id, "message")
                setLogVar(message.chat.id, "chatKey", value="payReqAmount")
                setLogVar(message.chat.id, "val", value=staffId)
            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["lastReqPending"])
                    wallet(message)
                except:
                    pass
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["amountZero"])
            except:
                pass
            wallet(message)


    def wallet(message):
        clearVars(message.chat.id)
        logPay = getPaymentFile()
        userStaff = DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))
        email = userStaff["email"]
        usersOfStaff = getStaffUsers(message.chat.id)
        allUsersCount = list(usersOfStaff.keys()).__len__()
        if not str(userStaff["id"]) in list(logPay["staffBank"].keys()):
            logPay["staffBank"][str(userStaff["id"])] = {"payedAmount": 0,
                                                         "payedAll": 0,
                                                         "payedCount": 0,
                                                         "percent": initValus()[0]["defaultPercentPayment"],
                                                         "reciveStatus": "",
                                                         "cardsNumber": []}
        staffPayment = logPay["staffBank"][str(userStaff["id"])]
        payedAmount = staffPayment["payedAll"]
        payedCount = staffPayment["payedCount"]
        percent = staffPayment["percent"]
        amountRecive = staffPayment["payedAmount"]
        reciveStatus = staffPayment["reciveStatus"]
        if reciveStatus == "":
            reciveStatus = initValus()[1]["noPayReq"]
        elif reciveStatus == "pending":
            reciveStatus = initValus()[1]["pendingPayReq"]
        else:
            date, amount = sup(reciveStatus, "|")
            reciveStatus = initValus()[1]["lastPayReq"].format(date=date, amount=amount)
        try:
            bot.send_message(message.chat.id,
                             initValus()[1]["walletBudy"].format(email=email, all=allUsersCount, payedCount=payedCount,
                                                                 payedAmount=payedAmount, percent="% "+str(percent),
                                                                 amountRecive=amountRecive, reciveStatus=reciveStatus),
                             reply_markup=walletMarkup(userStaff["id"]))
        except:
            pass

    def reportOrder(dbid, status):
        user = DBase.getUserRow(dbid)
        userStatus = DBase.getUserStatus(dbid)
        staff = user["invite_user_id"]
        admins = DBase.getAdminsId()
        staffUser = DBase.getUserRow(staff)
        if staff is None or staff in admins:
            for i in DBase.getAdminTlId():
                try:
                    bot.send_message(i, initValus()[1]["reportOrderConfirm"].format(user=user["email"], staff=
                    [staffUser["email"] if staff is not None else None][0], time=userStatus["expireLast"][0]))
                except:
                    pass
        else:
            staffTlid = staffUser["telegram_id"]
            if status:
                for i in DBase.getAdminTlId():
                    try:
                        bot.send_message(i, initValus()[1]["reportOrderConfirm"].format(user=user["email"], staff=
                        [staffUser["email"] if staff is not None else None][0],
                                                                                        time=userStatus["expireLast"][
                                                                                            0]))
                    except:
                        pass

                if not staffTlid in [0, None]:
                    try:
                        bot.send_message(staffTlid,
                                         initValus()[1]["reportOrderConfirm"].format(user=user["email"], staff=
                                         [staffUser["email"] if staff is not None else None][0],
                                                                                     time=userStatus["expireLast"][0]))
                        wallet(message)
                    except:
                        pass

            else:
                for i in DBase.getAdminTlId():
                    try:
                        bot.send_message(i, initValus()[1]["reportOrderDenied"].format(staff=staffUser["email"],
                                                                                       user=user["email"]))
                    except:
                        pass

                if not staffTlid in [0, None]:
                    try:
                        bot.send_message(staffTlid, initValus()[1]["reportOrderDenied"].format(staff=staffUser["email"],
                                                                                               user=user["email"]))
                    except:
                        pass


    def adminConfirmOrder(message, order, mod="staff"):
        if mod == "staff":
            sendOrderToAdmin(DBase, message, order, DBase.getAdminTlId())
        else:
            archivePayment(order)
            logPay = getPaymentFile()
            logPay["payed"].append([order["id"], DBase.getUserRow(order["id"])["expired_at"]])
            setValus(logPay, "payment.json")
            reportOrder(order["id"], True)


    def archivePayment(order):
        archive = initValus()[5]
        archive += f"{order}\n"
        setValus(archive, "paymentArchive.txt")


    def setWallet(message, order):
        logPay = getPaymentFile()
        staffId = str(order["staffId"])
        if not staffId in logPay["staffBank"].keys():
            logPay["staffBank"][staffId] = {"payedAmount": 0,
                                            "payedAll": 0,
                                            "payedCount": 0,
                                            "percent": initValus()[0]["defaultPercentPayment"],
                                            "reciveStatus": "",
                                            "cardsNumber": []}
        logPay["staffBank"][staffId]["payedAll"] += order["amount"]
        logPay["staffBank"][staffId]["payedAmount"] += int(order["amount"] * logPay["staffBank"][staffId]["percent"] / 100)
        logPay["staffBank"][staffId]["payedCount"] += 1
        setValus(logPay, "payment.json")


    def payment(message, data):
        key = sup(data, "|")[2]
        if key == "payed":
            bot.send_message(message.chat.id, initValus()[1]["alreadyPayed"])
        elif key == "pending":
            bot.send_message(message.chat.id, initValus()[1]["adminPending"])
        elif key == "payReq":
            confKey = sup(data, "|")[3]
            if confKey == "amount":
                dbid = int(sup(data, "|")[4])
                mod = ""
                if message.chat.id in DBase.getAdminTlId():
                    mod = "admin"
                elif message.chat.id in DBase.getStaffTlId():
                    mod = "staff"
                logPay = getPaymentFile()
                if not dbid in logPay["payed"]:
                    bot.send_message(message.chat.id,
                                     initValus()[1]["enterAmount"].format(user=DBase.getUserRow(dbid)["email"]),
                                     reply_markup=enterAmountMarkup(dbid, mod))
                    chatMode(message.chat.id, "message")
                    setLogVar(message.chat.id, "chatKey", value="payment")
                    setLogVar(message.chat.id, "val", value=dbid)
                else:
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
                    except:
                        pass
            elif confKey == "confirm":
                dbid = int(sup(data, "|")[4])
                logPay = getPaymentFile()
                order = {}
                found = False
                for i in logPay["order"]:
                    if dbid == i["id"]:
                        order = i
                        found = True
                        break
                if found and not i["id"] in logPay["payed"]:
                    archivePayment(order)
                    logPay["payed"].append([order["id"], DBase.getUserRow(order["id"])["expired_at"]])
                    for i in range(logPay["order"].__len__()):
                        if dbid == logPay["order"][i]["id"]:
                            del logPay["order"][i]
                            break
                    setValus(logPay, "payment.json")
                    setWallet(message, order)
                    reportOrder(dbid, True)
                else:
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
                    except:
                        pass
            elif confKey == "denied":
                dbid = int(sup(data, "|")[4])
                logPay = getPaymentFile()
                found = False
                for i in range(logPay["order"].__len__()):
                    if dbid == logPay["order"][i]["id"]:
                        del logPay["order"][i]
                        found = True
                        break
                if found:
                    setValus(logPay, "payment.json")
                    reportOrder(dbid, False)
                else:
                    bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
            else:
                clearVars(message.chat.id)
                mod = ""
                if message.chat.id in DBase.getAdminTlId():
                    mod = "admin"
                elif message.chat.id in DBase.getStaffTlId():
                    mod = "staff"
                else:
                    return None
                nowTime = getTehranTime(timeSystem.time())
                date = f"{nowTime[1]} {nowTime[0]}"
                dbid = int(confKey)
                amount = int(sup(data, "|")[4])
                requestedId = DBase.getIdFromTlid(message.chat.id)
                logPay = getPaymentFile()
                per = True
                for i in logPay["order"]:
                    if i["id"] == dbid:
                        per = False
                        break
                if per and not dbid in logPay["payed"]:
                    order = {"staffId": requestedId, "time": date, "id": dbid, "amount": amount}
                    if mod == "staff":
                        logPay["order"].append(order)
                        setValus(logPay, "payment.json")
                    adminConfirmOrder(message, order, mod=mod)
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["succssfullySentToAdmin"])
                    except:
                        pass
                    status(message, dbid, mod=mod, exitDestination="mainMenu")
                else:
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["alreadyProcessed"])
                    except:
                        pass

    def allRech(message, confirm=False, days=0):
        if not confirm:
            try:
                bot.send_message(message.chat.id, initValus()[1]["rechargeEveryoneBudy"],
                                 reply_markup=cancelMarkup("mainMenu"))
            except:
                pass

            setLogVar(message.chat.id, "chatKey", value="allRech")
            chatMode(message.chat.id, "message")
        else:
            users = DBase.getTableDict(table("v2_user"))
            usersLstId = []
            for i in users:
                if i["expired_at"] is not None and (
                        (((i["expired_at"] < timeSystem.time()) and (
                                (timeSystem.time() - i["expired_at"]) <= 2 * 86400))) or i[
                            "expired_at"] > timeSystem.time()):
                    DBase.setValue(table("v2_user"), "expired_at", i["expired_at"] + (days * 86400), i["id"])
                    usersLstId.append((i["id"], i["email"]))
            txtBudy = ""
            for i in usersLstId:
                txtBudy += initValus()[1]["successfullyCharged"].format(day=days, mod=initValus()[1]["day"],
                                                                        email=i[1]) + "\n"
            sndLst = [""]
            if txtBudy.__len__() > 4000:
                count = 0
                for i in sup(txtBudy, "\n"):
                    sndLst[count] += i + "\n"
                    if sndLst[count].__len__() > 4000:
                        sndLst.append("")
                        count += 1
                for i in range(len(sndLst)):
                    txtBudy = f"({i + 1}/{sndLst.__len__()})\n\n" + sndLst[i]
                    adminsMessage("", data=txtBudy)
                    timeSystem.sleep(.5)
            else:
                adminsMessage("", data=txtBudy)
            users = DBase.getColumnWithKey(table("v2_user"), "telegram_id")
            for i in usersLstId:
                user = users[i[0]]
                if user[0] is not None:
                    try:
                        bot.send_message(user[0], initValus()[1]["successfullyCharged"].format(day=days,
                                                                                               mod=initValus()[1][
                                                                                                   "day"], email=i[1]))
                    except:
                        pass


    def newDeleteTime(message, timeDelete):
        conf = initValus()[0]
        times = sup(conf["serviceNewTime"], ";")
        if timeDelete in times:
            times.remove(timeDelete)
            out = ""
            for i in times:
                out += f"{i};"
            out = out[:-1]
            conf["serviceNewTime"] = out
            fb = setValus(conf, "config.json")
            try:
                bot.send_message(message.chat.id, initValus()[1]["deleteSuccessfully"])
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 f"❌ Time Delete ERROR ❌\n\nAn Error Raised During Delete Time, Call Developer..!")
            except:
                pass

        new(message)


    def subNewTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["deleteTime"], reply_markup=subNewMarkup())

        except:
            pass


    def addNewTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["inputTime"], reply_markup=cancelMarkup("new"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="addNew")
        chatMode(message.chat.id, "message")


    def newActive(message, key):
        conf = initValus()[0]
        conf["newEnable"] = int(key)
        fb = setValus(conf, "config.json")
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["setStatus"].format(
                    mod=[initValus()[1]["active"] if key else initValus()[1]["deactive"]][0]))
            except:
                pass
        new(message)


    def new(message):
        newEnable = bool(initValus()[0]["newEnable"])
        if newEnable:
            statusBudy = initValus()[1]["active"]
            val = ""
            newTimes = initValus()[0]["serviceNewTime"]
            if newTimes != "":
                for i in sup(newTimes, ";"):
                    val += i + "\n"
            newEnableBudy = initValus()[1]["ifNewEnable"].format(time=val)
        else:
            statusBudy = initValus()[1]["deactive"]
            newEnableBudy = ""
        try:
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["newBudy"].format(status=statusBudy, ifNewEnable=newEnableBudy),
                                 reply_markup=newMarkup())
            except:
                pass

        except:
            pass


    def setSub(dbid, subid):
        try:
            plan = DBase.getTableRowId(table("v2_plan"), subid)
            groupId = plan["group_id"]
            transfer_enable = plan["transfer_enable"]
            DBase.setValue(table("v2_user"), "plan_id", subid, dbid)
            DBase.setValue(table("v2_user"), "group_id", groupId, dbid)
            DBase.setValue(table("v2_user"), "transfer_enable", int(transfer_enable * 1073741824), dbid)
            return True
        except:
            return False


    def changeSub(message, dbid, **data):
        mod = ["admin" if message.chat.id in DBase.getAdminTlId() else "staff"][0]
        if "subid" in data.keys():
            fb = setSub(dbid, int(data["subid"]))
            if fb:
                inviteUser = DBase.getUserRow(dbid)["invite_user_id"]
                if message.chat.id in DBase.getAdminTlId():
                    try:
                        bot.send_message(message.chat.id,
                                         initValus()[1]["changeSubSuccessful"].format(
                                             email=DBase.getUserRow(dbid)["email"],
                                             sub=
                                             DBase.getTableRowId(table("v2_plan"),
                                                                 int(data[
                                                                         "subid"]))[
                                                 "name"]))
                    except:
                        pass

                else:
                    try:
                        bot.send_message(message.chat.id,
                                         initValus()[1]["changeSubSuccessful"].format(
                                             email=DBase.getUserRow(dbid)["email"],
                                             sub=
                                             DBase.getTableRowId(table("v2_plan"),
                                                                 int(data[
                                                                         "subid"]))[
                                                 "name"]))
                    except:
                        pass

                    adminsMessage("changeSub",
                                  subName=DBase.getTableRowId(table("v2_plan"), int(data["subid"]))["name"],
                                  email=DBase.getUserRow(dbid)["email"], invit=
                                  [DBase.getUserRow(inviteUser)["email"] if not inviteUser in [0, None] else "None"][0])
                status(message, dbid, mod=mod, exitDestination="users^")
            else:
                try:
                    bot.send_message(message.chat.id, "There is an ERROR, ERROR CODE: 2611")
                except:
                    pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["changeSubBudy"].format(email=DBase.getUserRow(dbid)["email"]),
                                 reply_markup=changeSubMarkup(dbid, mod))
            except:
                pass


    def setCouponStatus(message, mod, couponId):
        fb = DBase.setValue(table("v2_coupon"), "show", str(mod), couponId)
        couponSettings(message, couponId)


    def couponRecharge(message, couponId, count):
        coupon = DBase.getTableRowId(table("v2_coupon"), couponId)
        fb = DBase.setValue(table("v2_coupon"), "limit_use", count, couponId)
        if fb:
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["rechargeCouponSuccessful"].format(code=coupon["code"], count=count))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id, "There's an ERROR, ERROR CODE: 2423")
            except:
                pass


    def couponSettings(message, couponId):
        coupon = DBase.getTableRowId(table("v2_coupon"), couponId)
        try:
            bot.send_message(message.chat.id,
                             initValus()[1]["couponsSettings"].format(remain=coupon["limit_use"], code=coupon["code"],
                                                                      mod=initValus()[1][
                                                                          ["active" if coupon[
                                                                                           "show"] == 1 else "deactive"][
                                                                              0]]),
                             reply_markup=couponSettingsMarkup(couponId))
        except:
            pass


    def setCouponsShow(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["couponsList"], reply_markup=setCouponsMarkup())

        except:
            pass


    def coupon(message, dbid):
        try:
            bot.send_message(message.chat.id, initValus()[1]["enterCoupon"], reply_markup=cancelMarkup("users^"))
        except:
            pass

        setLogVar(message.chat.id, "dbid", value=dbid)
        setLogVar(message.chat.id, "chatKey", value="coupon")
        chatMode(message.chat.id, "message")


    def tokenGenerate(tokenLength=32):
        return secrets.token_hex(tokenLength // 2)


    def uuidGenerate():
        return uuid.uuid4().__str__()


    def resetAccount(message, dbid, mod="admin", confirm=False):
        if confirm:
            fb = DBase.setValue(table("v2_user"), "token", tokenGenerate(), dbid)
            fb = fb and DBase.setValue(table("v2_user"), "uuid", uuidGenerate(), dbid)
            if fb:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["successfully"])
                except:
                    pass

            else:
                try:
                    bot.send_message(message.chat.id, "There's an ERROR, ERROR CODE: 2313 ❌")
                except:
                    pass

            status(message, dbid, mod=mod, exitDestination="mainMenu")
        else:
            confirmForm(message, f"resetAccount{dbid}", mod,
                        initValus()[1]["resetAccountBudy"].format(email=DBase.getUserRow(dbid)["email"]),
                        cancelDestination=f"status{dbid}{mod}", supVal="|")


    def note(message, dbid):
        user = DBase.getUserRow(dbid)
        permission = ["admin" if message.chat.id in DBase.getAdminTlId() else
                      ["staff" if message.chat.id in getStaffsTlid() else ""][0]][0]
        if user["remarks"] is None:
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["noteBudy"].format(email=DBase.getUserRow(dbid)["email"]),
                                 reply_markup=cancelMarkup(f"status{dbid}{permission}"))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["noteBudy"].format(email=DBase.getUserRow(dbid)["email"]))
                bot.send_message(message.chat.id, user["remarks"],
                                 reply_markup=cancelMarkup(f"status{dbid}{permission}"))
            except:
                pass
        chatMode(message.chat.id, "message")
        setLogVar(message.chat.id, "chatKey", value="note")
        setLogVar(message.chat.id, "dbid", value=dbid)
        setLogVar(message.chat.id, "val", value=permission)


    def staffs(message, menuIdx=0, edit=False):
        if edit:
            bot.edit_message_text(initValus()[1]["staffsBudy"], message.chat.id, message.message_id,
                                  reply_markup=staffsMarkup(menuIdx=menuIdx))
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["staffsBudy"],
                                 reply_markup=staffsMarkup(menuIdx=menuIdx))

            except:
                pass


    def makeUserAdmin(dbid, mod=True):
        if mod:
            DBase.setValue(table("v2_user"), "is_admin", 1, dbid)
            DBase.setValue(table("v2_user"), "is_staff", 0, dbid)
        else:
            DBase.setValue(table("v2_user"), "is_admin", 0, dbid)


    def makeUserDistributor(dbid, mod=True):
        if mod:
            DBase.setValue(table("v2_user"), "is_staff", 1, dbid)
            DBase.setValue(table("v2_user"), "is_admin", 0, dbid)
        else:
            DBase.setValue(table("v2_user"), "is_staff", 0, dbid)


    def customRecharge(message, dbid):
        setLogVar(message.chat.id, "chatKey", value="customRecharge")
        setLogVar(message.chat.id, "val", value=dbid)
        try:
            bot.send_message(message.chat.id, initValus()[1]["customRechargeBudy"])
        except:
            pass
        chatMode(message.chat.id, "message")


    def banAccount(message, dbid, mod="admin", ban=True):
        fb = DBase.setValue(table("v2_user"), "banned", [1 if not ban else 0][0], dbid)
        if mod == "admin":
            adminsMessage("banAccount", email=DBase.getUserRow(dbid)["email"], ban=ban)
        else:
            adminsMessage("banAccount", email=DBase.getUserRow(dbid)["email"], ban=ban,
                          invit=getEmailByTlid(message.chat.id))

        if fb:
            status(message, dbid, mod=mod)
        else:
            try:
                bot.send_message(message.chat.id, "Error raised\nError code:1674")
            except:
                pass


    def confirmForm(message, data, mod, budyText, cancelDestination="mainMenu", supVal=""):
        try:
            bot.send_message(message.chat.id, initValus()[1]["confirmRaw"] + f"\n{budyText}",
                             reply_markup=confirmMarkup(data, mod, cancelDestination=cancelDestination, supVal=supVal))
        except:
            pass


    def deleteAccount(message, dbid, mod="admin", confirm=False):
        if not confirm:
            confirmForm(message, dbid, "deleteAccount",
                        initValus()[1]["deleteUser"].format(user=DBase.getUserRow(dbid)["email"]),
                        cancelDestination=f"status{dbid}{mod}")
        else:
            email = DBase.getUserRow(dbid)["email"]
            fb = DBase.deleteAccount(dbid)
            if fb:
                if mod == "admin":
                    adminsMessage("deleteAccount", email=email)
                else:
                    adminsMessage("deleteAccount", email=email, invit=getEmailByTlid(message.chat.id))
                    try:
                        bot.send_message(message.chat.id, initValus()[1]["deleteSuccessful"].format(text=email))
                    except:
                        pass

            else:
                try:
                    bot.send_message(message.chat.id, "Error raised\nError code:1671")

                except:
                    pass


    def usersSmartSearch(message):
        setLogVar(message.chat.id, "chatKey", value="smartSearchUsers")
        chatMode(message.chat.id, "message")
        try:
            bot.send_message(message.chat.id, "Id, Uuid, Email, Token, Telegram-Id?: ",
                             reply_markup=cancelMarkup("users^"))

        except:
            pass


    def usersSearch(message):
        setLogVar(message.chat.id, "chatKey", value="searchUsers")
        chatMode(message.chat.id, "message")
        try:
            bot.send_message(message.chat.id, "what page?: ", reply_markup=cancelMarkup("users^"))

        except:
            pass


    def getStaffUsers(tlid):
        accounts = DBase.getAccountsFromTlid(tlid)
        staffDBids = []
        for i in accounts.keys():
            if DBase.getUserRow(int(i))["is_staff"] == 1:
                staffDBids.append(int(i))
        allUsers = DBase.getTableDict(table("v2_user"))
        lst = dict()
        for i in allUsers:
            if i["invite_user_id"] in staffDBids:
                lst[str(i["id"])] = i["email"]
        return lst


    def users(message, menuIdx=0, deleteFac=True, mod="admin", staffTlid=None):
        if mod == "admin":
            raw_usersList = DBase.getColumnWithKey(table("v2_user"), "email", "u", "d")
            usersList = dict()
            fac = 1.073741824 * (10 ** 9)
            for i in list(raw_usersList.keys()):
                usersList[i] = [raw_usersList[i][0],
                                str(digit((raw_usersList[i][1] + raw_usersList[i][2]) / fac, 2)) + f" GB"]
        else:
            if staffTlid is None:
                staffTlid = message.chat.id
            else:
                mod = "adminStaff"
            usersList = getStaffUsers(staffTlid)
        setLogVar(message.chat.id, "chatKey", value="smartSearchUsers")
        chatMode(message.chat.id, "message")
        # bot.send_message(message.chat.id, initValus()[1]["editTextBudy"], reply_markup=editTextMarkup())
        if deleteFac:
            try:
                bot.send_message(message.chat.id, initValus()[1]["usersBudy"],
                                 reply_markup=usersMarkup(usersList, mod=mod, menuIdx=menuIdx))
            except:
                pass

        else:
            try:
                bot.edit_message_text(initValus()[1]["usersBudy"], message.chat.id, message.message_id,
                                      reply_markup=usersMarkup(usersList, mod=mod, menuIdx=menuIdx))

            except:
                pass


    def onlineBlock(message, id, key):
        log = getLogFile()
        if not "block" in list(log.keys()):
            log["block"] = []
        if key:
            log["block"].append(id)
            try:
                bot.send_message(message.chat.id,
                                 initValus()[1]["blockSuccess"].format(email=DBase.getUserRow(id)["email"]))
            except:
                pass

        else:
            try:
                log["block"].remove(id)
                try:
                    bot.send_message(message.chat.id,
                                     initValus()[1]["unblockSuccess"].format(email=DBase.getUserRow(id)["email"]))
                except:
                    pass

            except:
                pass
        setValus(log, "log.json")


    def onlineDeleteTime(message, timeDelete):
        conf = initValus()[0]
        times = sup(conf["serviceOnlineTime"], ";")
        if timeDelete in times:
            times.remove(timeDelete)
            out = ""
            for i in times:
                out += f"{i};"
            out = out[:-1]
            conf["serviceOnlineTime"] = out
            fb = setValus(conf, "config.json")
            try:
                bot.send_message(message.chat.id, initValus()[1]["deleteSuccessfully"])
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 f"❌ Time Delete ERROR ❌\n\nAn Error Raised During Delete Time, Call Developer..!")
            except:
                pass

        online(message)


    def subOnlineTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["deleteTime"], reply_markup=subOnlineMarkup())

        except:
            pass


    def addOnlineTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["inputTime"], reply_markup=cancelMarkup("online"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="addOnline")
        chatMode(message.chat.id, "message")


    def onlineActive(message, key):
        conf = initValus()[0]
        conf["onlineEnable"] = int(key)
        fb = setValus(conf, "config.json")
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["setStatus"].format(
                    mod=[initValus()[1]["active"] if key else initValus()[1]["deactive"]][0]))
            except:
                pass

        online(message)


    def online(message):
        onlineEnable = bool(initValus()[0]["onlineEnable"])
        if onlineEnable:
            statusBudy = initValus()[1]["active"]
            val = ""
            onlineTimes = initValus()[0]["serviceOnlineTime"]
            if onlineTimes != "":
                for i in sup(onlineTimes, ";"):
                    val += i + "\n"
            onlineEnableBudy = initValus()[1]["ifOnlineEnable"].format(time=val)
        else:
            statusBudy = initValus()[1]["deactive"]
            onlineEnableBudy = ""
        try:
            bot.send_message(message.chat.id,
                             initValus()[1]["onlineBudy"].format(status=statusBudy, ifOnlineEnable=onlineEnableBudy),
                             reply_markup=onlineMarkup())
        except:
            pass


    def services(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["servicesBudy"], reply_markup=servicesMarkup())

        except:
            pass


    def warningDeleteTime(message, timeDelete):
        conf = initValus()[0]
        times = sup(conf["serviceWarningTime"], ";")
        if timeDelete in times:
            times.remove(timeDelete)
            out = ""
            for i in times:
                out += f"{i};"
            out = out[:-1]
            conf["serviceWarningTime"] = out
            fb = setValus(conf, "config.json")
            try:
                bot.send_message(message.chat.id, initValus()[1]["deleteSuccessfully"])
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 f"❌ Time Delete ERROR ❌\n\nAn Error Raised During Delete Time, Call Developer..!")
            except:
                pass

        warning(message)


    def subWarningTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["deleteTime"], reply_markup=subWarningMarkup())


        except:
            pass


    def addWarningTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["inputTime"], reply_markup=cancelMarkup("warning"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="addWarning")
        chatMode(message.chat.id, "message")


    def warningActive(message, key):
        conf = initValus()[0]
        conf["warningEnable"] = int(key)
        fb = setValus(conf, "config.json")
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["setStatus"].format(
                    mod=[initValus()[1]["active"] if key else initValus()[1]["deactive"]][0]))
            except:
                pass

        warning(message)


    def warning(message):
        # bot.send_message(message.chat.id, initValus()[1]["warningBudy"])
        warningEnable = bool(initValus()[0]["warningEnable"])
        if warningEnable:
            statusBudy = initValus()[1]["active"]
            val = ""
            warningTimes = initValus()[0]["serviceWarningTime"]
            if warningTimes != "":
                for i in sup(warningTimes, ";"):
                    val += i + "\n"
            warningEnableBudy = initValus()[1]["ifWarningEnable"].format(time=val)
        else:
            statusBudy = initValus()[1]["deactive"]
            warningEnableBudy = ""
        try:
            bot.send_message(message.chat.id,
                             initValus()[1]["warningBudy"].format(status=statusBudy, ifWarningEnable=warningEnableBudy),
                             reply_markup=warningMarkup())
        except:
            pass


    def switchSniNotic(message):
        conf = initValus()[0]
        if bool(conf["sniNotic"]):
            conf["sniNotic"] = 0
        else:
            conf["sniNotic"] = 1
        setValus(conf, "config.json")
        try:
            bot.send_message(message.chat.id, initValus()[1]["setStatus"].format(
                mod=[initValus()[1]["active"] if bool(conf["sniNotic"]) else initValus()[1]["deactive"]][0]))
        except:
            pass

        sni(message)


    def sniDeleteTime(message, timeDelete):
        conf = initValus()[0]
        times = sup(conf["serviceSniTime"], ";")
        if timeDelete in times:
            times.remove(timeDelete)
            out = ""
            for i in times:
                out += f"{i};"
            out = out[:-1]
            conf["serviceSniTime"] = out
            fb = setValus(conf, "config.json")
            try:
                bot.send_message(message.chat.id, initValus()[1]["deleteSuccessfully"])
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id,
                                 f"❌ Time Delete ERROR ❌\n\nAn Error Raised During Delete Time, Call Developer..!")
            except:
                pass

        sni(message)


    def subSniTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["deleteTime"], reply_markup=subSniMarkup())

        except:
            pass


    def addSniTime(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["inputTime"], reply_markup=cancelMarkup("sni"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="addSni")
        chatMode(message.chat.id, "message")


    def sniActive(message, key):
        conf = initValus()[0]
        conf["sniEnable"] = int(key)
        fb = setValus(conf, "config.json")
        if fb:
            try:
                bot.send_message(message.chat.id, initValus()[1]["setStatus"].format(
                    mod=[initValus()[1]["active"] if key else initValus()[1]["deactive"]][0]))
            except:
                pass

        sni(message)


    def sni(message):
        sniEnable = bool(initValus()[0]["sniEnable"])
        sniNotic = bool(initValus()[0]["sniNotic"])
        if sniEnable:
            statusBudy = initValus()[1]["active"]
            val = ""
            sniTimes = initValus()[0]["serviceSniTime"]
            if sniTimes != "":
                for i in sup(sniTimes, ";"):
                    val += i + "\n"
            sniEnableBudy = initValus()[1]["ifSniEnable"].format(time=val)
        else:
            statusBudy = initValus()[1]["deactive"]
            sniEnableBudy = ""
        if sniNotic:
            mod = initValus()[1]["active"]
        else:
            mod = initValus()[1]["deactive"]
        try:
            bot.send_message(message.chat.id,
                             initValus()[1]["sniBudy"].format(status=statusBudy, ifSniEnable=sniEnableBudy, mod=mod),
                             reply_markup=sniMarkup())

        except:
            pass


    def textSearch(message):
        setLogVar(message.chat.id, "chatKey", value="searchEditTextMenu")
        chatMode(message.chat.id, "message")
        try:
            bot.send_message(message.chat.id, "what page?: ", reply_markup=cancelMarkup("textMenu^"))

        except:
            pass


    def justAdmin(message, rep):
        try:
            bot.send_message(message.chat.id, initValus()[1]["updateForceBudy"], reply_markup=updateForceMarkup(rep, 1))
        except:
            pass

        chatMode(message.chat.id, "neutral")


    def forAll(message, rep):
        try:
            bot.send_message(message.chat.id, initValus()[1]["updateForceBudy"], reply_markup=updateForceMarkup(rep, 0))
        except:
            pass

        chatMode(message.chat.id, "neutral")


    def norepeat(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["noAdminOrAll"],
                             reply_markup=adminOrAllMarkup(repeat=False))
        except:
            pass

        chatMode(message.chat.id, "neutral")


    def repeat(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["adminOrAll"], reply_markup=adminOrAllMarkup(repeat=True))
        except:
            pass

        chatMode(message.chat.id, "neutral")


    def getTicketsForShow():
        tick = initValus()[3]
        ticks = []
        tlidTicks = []
        for i in tick.keys():
            if i != "time":
                for j in range(tick[i].__len__()):
                    ticks.append(tick[i][j])
                    tlidTicks.append(i)
        ticks.sort(reverse=True)
        out = []
        count = 0
        for i in ticks:
            gmail = sup(i[1], "")
            for j in gmail:
                if "@" in j:
                    gmail = j
            try:
                out.append((initValus()[1]["ticketId"].format(id=i[0], email=
                DBase.getUserRow(DBase.getIdFromTlid(int(tlidTicks[count])))["email"],
                                                              tlid=tlidTicks[count]) + f"\n\n\n\n{i[1]}", i[0], i[2]))
            except:
                out.append((initValus()[1]["ticketId"].format(id=i[0], email="",
                                                              tlid=tlidTicks[count]) + f"\n\n\n\n{i[1]}", i[0], i[2]))

            count += 1
        return out


    def ticketShow(message, ticketId):
        out = getTicketsForShow()
        messageBudy = ""
        for i in out:
            if i[1] == ticketId:
                messageBudy = i[0]
                tlid = i[2]
                break
        try:
            bot.send_message(message.chat.id, messageBudy, reply_markup=respondSupportMarkupReturn(tlid))

        except:
            pass


    def viewTicket(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["ticketBudy"], reply_markup=viewTicketMarkup())
        except:
            pass


    def respond(message, tlid):
        try:
            bot.send_message(message.chat.id, initValus()[1]["respondBudy"], reply_markup=cancelMarkup("mainMenu"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="respond")
        setLogVar(message.chat.id, "val", value=tlid)
        chatMode(message.chat.id, "message")


    def askHelp(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["askHelpBudy"], reply_markup=cancelMarkup("contact"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="ticket")
        chatMode(message.chat.id, "message")


    def recharge(message, dbid, mod="admin"):
        if message.chat.id in DBase.getAdminTlId() + DBase.getStaffTlId():
            user = DBase.getUserRow(dbid)
            exp = user["expired_at"]
            # if (exp - time.time()) / 86400 <= initValus()[0]["warningTerm"]:
            if timeSystem.time() > exp:
                term = int(timeSystem.time())
            else:
                term = exp
            fb = expireSet(dbid, term)
            if fb:
                if mod != "staff":
                    adminsMessage("adminNoticRecharge", day=initValus()[0]["rechargeTerm"],
                                  email=user["email"])
                else:
                    try:
                        bot.send_message(message.chat.id,
                                         initValus()[1]["successfullyCharged"].format(
                                             day=initValus()[0]["rechargeTerm"],
                                             email=user["email"],
                                             mod=initValus()[1]["day"]))
                    except:
                        pass

                    adminsMessage("adminNoticRecharge", day=initValus()[0]["rechargeTerm"],
                                  email=user["email"],
                                  invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"], mode="staff")
                if not user["telegram_id"] in [0, None]:
                    bot.send_message(user["telegram_id"],
                                     initValus()[1]["successfullyCharged"].format(
                                         day=initValus()[0]["rechargeTerm"],
                                         email=user["email"], mod=initValus()[1]["day"]))
            # else:
            #     bot.send_message(message.chat.id, initValus()[1]["afterWarningError"])
        mainMenu(message)


    def emergency(message, dbid, mod="user"):
        dbid = int(dbid)
        if allowEmergency(DBase, dbid) or message.chat.id in DBase.getAdminTlId() + DBase.getStaffTlId():
            log = getLogFile()
            user = DBase.getUserRow(dbid)
            exp = user["expired_at"]
            if timeSystem.time() > exp:
                term = int(timeSystem.time())
            else:
                term = exp
            em = ""
            sent = False
            if not message.chat.id in DBase.getAdminTlId() + DBase.getStaffTlId():
                if not dbid in log["emergency"]:
                    log["emergency"].append(dbid)
                    setValus(log, "log.json")
                    em = initValus()[1]["you"]
                    sent = True
                else:
                    sent = False
            else:
                em = DBase.getUserRow(dbid)["email"]
                sent = True
            if sent:
                fb = expireEmergencySet(dbid, term)
                if fb:
                    try:
                        bot.send_message(message.chat.id,
                                         initValus()[1]["successfullyCharged"].format(
                                             day=initValus()[0]["emergencyTerm"],
                                             email=em, mod=initValus()[1]["day"]))
                    except:
                        pass

                    if mod == "staff":
                        adminsMessage("adminNoticRecharge", day=initValus()[0]["emergencyTerm"],
                                      email=DBase.getUserRow(dbid)["email"],
                                      invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"],
                                      mode="staff")
                    elif mod == "user":
                        adminsMessage("adminNoticRecharge", day=initValus()[0]["emergencyTerm"],
                                      email=DBase.getUserRow(dbid)["email"],
                                      invit=DBase.getUserRow(DBase.getIdFromTlid(message.chat.id))["email"],
                                      mode="user")
                else:
                    try:
                        bot.send_message(message.chat.id, "❌ ERROR ❌\n\nError Code: 1237")
                    except:
                        pass


            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["notAllowToEmergency"])
                except:
                    pass


    def resetTrafficSet(dbid):
        fb1 = DBase.setValue(table("v2_user"), "t", 0, dbid)
        fb2 = DBase.setValue(table("v2_user"), "u", 0, dbid)
        fb3 = DBase.setValue(table("v2_user"), "d", 0, dbid)
        return fb1 and fb2 and fb3


    def expireEmergencySet(dbid, term):
        fb = DBase.setValue(table("v2_user"), "expired_at", term + (86400 * initValus()[0]["emergencyTerm"]), dbid)
        return fb


    def expireSet(dbid, term):
        fb = DBase.setValue(table("v2_user"), "expired_at", term + (86400 * initValus()[0]["rechargeTerm"]), dbid)
        return fb


    def expireSetCustom(dbid, time):
        fb = DBase.setValue(table("v2_user"), "expired_at", int(time), dbid)
        return fb


    def updateForceConfirm(message, rep, adminOrAll):
        var.updateCounter = int(timeSystem.time())
        if rep == "repeat":
            var.updateRe = True
        if bool(int(adminOrAll)):
            var.updateAdmin = True
        else:
            var.updateAdmin = False
        manualWarning(DBase, message, force=True)
        controlPanel(message)


    def updateForce(message):
        # bot.send_message(message.chat.id, initValus()[1]["updateForceBudy"], reply_markup=updateForceMarkup())
        try:
            bot.send_message(message.chat.id, initValus()[1]["updateForceBudy"], reply_markup=updateForceOptionMarkup())
        except:
            pass

        chatMode(message.chat.id, "neutral")


    def sendMessage(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["sendMessageBudy"],
                             reply_markup=cancelMarkup("controlPanel"))
        except:
            pass

        setLogVar(message.chat.id, "chatKey", value="messageAll")
        chatMode(message.chat.id, "message")


    def setText(message, key, val):
        try:
            bot.send_message(message.chat.id, initValus()[1]["setTextBudy"] + initValus()[1]["selectedText"])
        except:
            pass

        if val == "":
            val = f"Nan, key={key}"
        try:
            bot.send_message(message.chat.id, val, reply_markup=cancelMarkup("textMenu^"))
        except:
            pass

        setLogVar(message.chat.id, "editFac", value=[key, val])
        chatMode(message.chat.id, "edit")


    def editText(message, deleteFac=True):
        setLogVar(message.chat.id, "chatKey", value="searchEditTextMenu")
        chatMode(message.chat.id, "message")
        # bot.send_message(message.chat.id, initValus()[1]["editTextBudy"], reply_markup=editTextMarkup())
        if not deleteFac:
            bot.edit_message_text(initValus()[1]["editTextBudy"], message.chat.id, message.message_id,
                                  reply_markup=editTextMarkup())
        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["editTextBudy"], reply_markup=editTextMarkup())


            except:
                pass


    def addUser(message):
        chatMode(message.chat.id, "add")


    def setupMessage(message):
        chatMode(message.chat.id, "login")
        try:
            bot.send_message(message.chat.id, initValus()[1]["setupMessage"], reply_markup=setupMessageMarkup())


        except:
            pass


    def subs(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["subsBudy"],
                             reply_markup=subsMarkup())

        except:
            pass


    def buy(message, init=False):
        chatMode(message.chat.id, "neutral")
        if not init:
            try:
                bot.send_message(message.chat.id, initValus()[1]["buyBudy"].format(admin=initValus()[0]["adminId"]),
                                 reply_markup=returnMarkup("mainMenu"))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id, initValus()[1]["buyBudyInit"].format(admin=initValus()[0]["adminId"]),
                                 reply_markup=returnMarkup("mainMenu"))
            except:
                pass


    def distributorPanel(message):
        clearVars(message.chat.id)
        try:
            bot.send_message(message.chat.id, initValus()[1]["distributorPanelBudy"],
                             reply_markup=distributorPanelMarkup())

        except:
            pass


    def controlPanel(message):
        clearVars(message.chat.id, but=["updateService"])
        try:
            bot.send_message(message.chat.id, initValus()[1]["controlPanelBudy"],
                             reply_markup=controlPanelMarkup(message.chat.id))
        except:
            pass


    def directLink(message):
        bot.send_document(message.chat.id, document=open(os.getcwd() + "/assets/app.apk", "rb"))


    def android(message):
        bot.send_video(message.chat.id, video=open(os.getcwd() + "/assets/android.mp4", "rb"),
                       caption=initValus()[1]["androidBudy"].format(androidLink=initValus()[0]["androidLink"]),
                       reply_markup=androidMarkup())


    def iphone(message):
        bot.send_video(message.chat.id, video=open(os.getcwd() + "/assets/iphone.mp4", "rb"),
                       caption=initValus()[1]["iphoneBudy"].format(iphoneLink=initValus()[0]["iphoneLink"]),
                       reply_markup=returnMarkup("guide"))


    def guide(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["selectPlatform"],
                             reply_markup=platformMarkup())

        except:
            pass


    def rules(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["rulesBudy"],
                             reply_markup=returnMarkup("terms"))
        except:
            pass


    def terms(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["termsBudy"],
                             reply_markup=termsMarkup())
        except:
            pass


    def contact(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["contactBudy"].format(adminId=initValus()[0]["adminId"]),
                             reply_markup=contactMarkup())
        except:
            pass


    def mainMenu(message):
        userTlIdCount = DBase.tlidCount(message.chat.id)
        if userTlIdCount == 0:
            text = initValus()[1]["mainMenuInit"].format(brand=initValus()[1]["brand"])
        elif userTlIdCount >= 1:
            text = initValus()[1]["mainMenu"].format(brand=initValus()[1]["brand"])
        try:
            bot.send_message(message.chat.id, text, reply_markup=mainMenuMarkup(message))
        except:
            pass

        clearVars(message.chat.id)


    def getOnlineStatus(dbId):
        onlineList = userOnline()
        for i in onlineList:
            if str(dbId) in i.keys():
                val = i[str(dbId)]

        try:
            if val[0] < initValus()[0]["onlineTerm"] * 60:
                return 1
            else:
                return val[1]
        except:
            return [0, 0, 0, 0, 0, 0]


    def status(message, dbId, mod="user", exitDestination=""):
        # # bot.answer_callback_query(call.id, "hii")
        user = DBase.getUserRow(dbId)
        if user is not None:
            userStatus = DBase.getUserStatus(dbId)
            enableUser = DBase.checkAccountStatus(dbId)
            expLast = userStatus["expireLast"][1]
            expForm = userStatus["expireLast"][0]
            subid = userStatus["subType"]
            if expLast == "":
                expLast = 10000
            statusBudy = str(initValus()[1]["status"])
            if "{ipConnected}" in statusBudy:
                connectesIps = userStatus["connectedIps"]
            else:
                statusBudy += "{ipConnected}"
                connectesIps = ""
            onlineStatus = getOnlineStatus(dbId)
            onlineOut = ""
            invite = ""
            id = ""
            tlid = ""
            dateCreate = ""
            permissionText = ""
            permission = ""
            if dbId == initValus()[0]["superAdminDBid"]:
                permissionText = initValus()[1]["itsSuperadmin"]
            elif dbId in DBase.getAdminsId():
                permissionText = initValus()[1]["itsAdmin"]
            elif dbId in list(DBase.getStaffs().keys()):
                permissionText = initValus()[1]["itsDistributor"]
            else:
                permissionText = initValus()[1]["itsUser"]
            if mod != "user":
                id = initValus()[1]["id"].format(id=user["id"]) + "\n"
                dateCreate = initValus()[1]["createAccount"].format(date=getTehranTime(user["created_at"])[0]) + "\n"
                permission = initValus()[1]["permission"].format(text=permissionText) + "\n"
                if user["telegram_id"] is not None:
                    if user["telegram_id"] != 0:
                        tlid = initValus()[1]["tlid"].format(tlid=user["telegram_id"]) + "\n"
                    else:
                        tlid = initValus()[1]["tlid"].format(tlid=initValus()[1]["logedOut"]) + "\n"
                else:
                    tlid = initValus()[1]["tlid"].format(tlid=initValus()[1]["notSet"]) + "\n"
                if user["invite_user_id"] is not None:
                    inviteUser = DBase.getUserRow(user["invite_user_id"])
                    invite = initValus()[1]["invite"].format(email=inviteUser["email"]) + "\n"
            if onlineStatus != 1:
                onlineStatus = onlineStatus[::-1]
                for i in range(len(onlineStatus)):
                    if onlineStatus[i] != 0:
                        if i == 2:
                            onlineOut = initValus()[1]["lastOnlineStatus"].format(
                                lastOnline=initValus()[1]["lastOnline"].format(val=onlineStatus[i],
                                                                               mod=initValus()[1]["day"]))
                            break
                        elif i == 3:
                            onlineOut = initValus()[1]["lastOnlineStatus"].format(
                                lastOnline=initValus()[1]["lastOnline"].format(val=onlineStatus[i],
                                                                               mod=initValus()[1]["hour"]))
                            break
                        elif i == 4:
                            onlineOut = initValus()[1]["lastOnlineStatus"].format(
                                lastOnline=initValus()[1]["lastOnline"].format(val=onlineStatus[i],
                                                                               mod=initValus()[1]["minute"]))
                            break
                if onlineOut == "":
                    onlineOut = initValus()[1]["lastOnlineStatus"].format(lastOnline=initValus()[1]["noUse"])
            else:
                onlineOut = initValus()[1]["lastOnlineStatus"].format(lastOnline=initValus()[1]["onlineStatus"])
            Note = \
                ["\n\nNote:\n" + user["remarks"] if mod in ["admin", "staff"] and user["remarks"] is not None else ""][
                    0]
            messageBudy = statusBudy.format(email=userStatus["username"],
                                            lastOnline=onlineOut,
                                            id=id,
                                            tlid=tlid,
                                            createAccount=dateCreate,
                                            permission=permission,
                                            enable=[[initValus()[1]["active"] if (
                                                    expLast > initValus()[0]["warningTerm"]) else initValus()[1][
                                                "warningActive"]][0] if enableUser else initValus()[1]["deactive"]][0],
                                            useData=decimal(userStatus["total"]),
                                            download=decimal(userStatus["download"]),
                                            upload=decimal(userStatus["upload"]),
                                            dataLeft=userStatus["left"],
                                            expireLast=expForm,
                                            expire=[
                                                userStatus["expire"] if enableUser else
                                                initValus()[1][
                                                    "expired"]][0],
                                            ipConnected=connectesIps,
                                            invite=invite,
                                            link=userStatus["link"],
                                            subType=[initValus()[1]["stype"].format(
                                                subType=DBase.getTableRowId(table("v2_plan"), user["plan_id"])[
                                                    "content"]) if (
                                                    user["plan_id"] is not None and initValus()[1][
                                                "stype"] != "") else ""][0]
                                            ) + Note
            try:
                bot.send_photo(message.chat.id, qrImage(userStatus["link"]), caption=messageBudy,
                               reply_markup=statusMarkup(message, dbId, mod=mod, exitDestination=exitDestination))
            except:
                pass

        else:
            try:
                bot.send_message(message.chat.id, "User Not Found ❌")

            except:
                pass


    def logout(message, dbId):
        adminsMessage("userLogedOut#", dbid=dbId, tlid=message.chat.id)
        DBase.setTlId(dbId, 0)
        if DBase.userExist(message.chat.id):
            accounts(message)
        else:
            setupMessage(message)


    def addAccount(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["login"], reply_markup=wrongMarkup())
        except:
            pass

        chatMode(message.chat.id, "login")


    def removeAccount(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["removeNotice"],
                             reply_markup=removeMarkup(message))

        except:
            pass


    def accounts(message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["accountsList"],
                             reply_markup=accountsMarkup(message))

        except:
            pass


    def getPaymentFile():
        f = json.load(open("payment.json", "r"))
        args = ["order", "payed", "request", "staffBank"]
        for i in args:
            if not i in f.keys():
                if i == "staffBank":
                    f[i] = {}
                    setValus(f, "payment.json")
                else:
                    f[i] = []
                    setValus(f, "payment.json")
        return f


    def payStatus(dbid):
        lst = DBase.getAdminsId() + list(DBase.getStaffs().keys())
        userExp = DBase.getUserRow(dbid)["expired_at"]
        if not dbid in lst and (userExp is not None and (userExp - timeSystem.time()) > 0):
            logPay = getPaymentFile()
            for i in logPay["order"]:
                if dbid == i["id"]:
                    return "pending", f"#both|payment|pending"
            for i in logPay["payed"]:
                if dbid in i:
                    return "payed", f"#both|payment|payed"
            return "notPayed", f"both|payment|payReq|amount|{dbid}"
        else:
            return None


    def getLogFile():
        return json.load(open("log.json", "r"))


    def nearExpire(expireTime):
        if expireTime is not None:
            daysToExp = (expireTime - timeSystem.time()) / 86400
            if daysToExp < 0 or expireTime == 0:
                return -1
            if daysToExp < initValus()[0]["warningTerm"]:
                return True
            else:
                return False
        else:
            return None


    def checkLog(db):
        log = getLogFile()
        try:
            warns = log["warning"]
        except:
            log["warning"] = dict()
            warns = dict()
        expireDict = db.getColumnWithKey(table("v2_user"), "expired_at")
        keys = list(log["warning"].keys())
        # check if is there any dbid inside log that is not in DB and delete it
        for id in keys:
            if not id in expireDict.keys():
                del warns[id]
            else:
                # check if user is not close to the expiration (they are recharged) delete its log
                expireResult = nearExpire(expireDict[id])
                if not expireResult:
                    del warns[id]

            log["warning"] = warns
        setValus(log, "log.json")


    def getExpireIds(db):
        log = getLogFile()
        users = db.getTableDict(table("v2_user"))
        expireList = []
        for i in range(len(users)):
            exp = users[i]["expired_at"]
            if exp is not None and not bool(users[i]["banned"]):
                daysLeft = (exp - timeSystem.time()) / 86400
                daysLeft = [daysLeft if exp != 0 else -1][0]
                if daysLeft < initValus()[0]["warningTerm"]:
                    userId = users[i]["id"]
                    if var.updateRe or not str(userId) in log["warning"].keys() or not int(daysLeft) in log["warning"][
                        str(userId)]:
                        expireList.append(userId)
        return expireList


    def allowEmergency(db, id):
        exp = db.getUserRow(id)["expired_at"]
        if not exp in [None, 0]:
            expireTerm = (exp - timeSystem.time()) / 86400
            limD, limU = initValus()[0]["emergencyLim"]
            log = getLogFile()
            if limD < exp < limU:
                if not id in log["emergency"]:
                    return True
                else:
                    return False
            elif exp > limU:
                if id in log["emergency"]:
                    log["emergency"].remove(id)
                return True
        else:
            return False


    def sendWarnings(idListRow, db, force=False):
        # sorting by expire Term time
        idList = []
        for id in idListRow:
            if not id in getLogFile()["block"] or force:
                user = db.getUserRow(id)
                expTerm = (user["expired_at"] - timeSystem.time()) / 86400
                expireTerm = [int(expTerm) if expTerm >= 0 else -1][0]
                idList.append((expireTerm, id))
        idList.sort()
        # idList = idList[::-1]
        idList = [i[1] for i in idList]

        # after sorting, send warnings
        for id in idList:
            emergencyPermission = allowEmergency(db, id)
            user = db.getUserRow(id)
            tlid = user["telegram_id"]
            expTerm = (user["expired_at"] - timeSystem.time()) / 86400
            expireTerm = [int(expTerm) if expTerm >= 0 else -1][0]
            isExpired = timeSystem.time() > user["expired_at"]
            if var.updateAdmin:
                # check if user has inviter
                inviteUser = ""
                if user["invite_user_id"] is not None and not user["invite_user_id"] in DBase.getAdminsId():
                    inviteUser = DBase.getUserRow(int(user["invite_user_id"]))

                for admin in db.getAdminTlId():
                    if isExpired:
                        budyMessage = initValus()[1]["adminWarningExpired"].format(email=user["email"], id=user["id"],
                                                                                   note=["\nNote:\n" + user[
                                                                                       "remarks"] if not user[
                                                                                                             "remarks"] in [
                                                                                                             None,
                                                                                                             ""] else ""][
                                                                                       0],
                                                                                   invite=["\n\n" + initValus()[1][
                                                                                       "invite"].format(
                                                                                       email=inviteUser[
                                                                                           "email"]) if inviteUser != "" else ""][
                                                                                       0])
                        try:
                            bot.send_message(admin, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                        except:
                            pass
                    else:
                        budyMessage = initValus()[1]["adminWarning"].format(email=user["email"], days=
                        [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0], id=user["id"], note=[
                            "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0], invite=[
                            "\n\n" + initValus()[1]["invite"].format(
                                email=inviteUser["email"]) if inviteUser != "" else ""][0])
                        try:
                            bot.send_message(admin, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                        except:
                            pass
            else:
                if not tlid in [0, None]:
                    if isExpired:
                        if emergencyPermission:
                            budyMessage = initValus()[1]["userWarningExpired"].format(email=user["email"],
                                                                                      admin=initValus()[0]["adminId"])
                            try:
                                bot.send_message(user["telegram_id"], budyMessage,
                                                 reply_markup=emergencyRechargeMarkup(user["id"]))
                            except:
                                pass
                        else:
                            budyMessage = initValus()[1]["userWarningExpired"].format(email=user["email"],
                                                                                      admin=initValus()[0]["adminId"])
                            try:
                                bot.send_message(user["telegram_id"], budyMessage)
                            except:
                                pass

                        # check if user has inviter
                        inviteUser = ""
                        if user["invite_user_id"] is not None and not user["invite_user_id"] in DBase.getAdminsId():
                            inviteUser = DBase.getUserRow(int(user["invite_user_id"]))

                        # check if inviter exist send reports
                        if inviteUser != "":
                            if not inviteUser["telegram_id"] in [0, None]:
                                budyMessage = initValus()[1]["staffUserExpired"].format(email=user["email"],
                                                                                        id=user["id"],
                                                                                        note=["\nNote:\n" + user[
                                                                                            "remarks"] if not user[
                                                                                                                  "remarks"] in [
                                                                                                                  None,
                                                                                                                  ""] else ""][
                                                                                            0])
                                try:
                                    bot.send_message(inviteUser["telegram_id"], budyMessage,
                                                     reply_markup=rechargeMarkup(user["id"], mod="staff"))
                                except:
                                    pass
                                    # budy message for admins
                        budyMessage = initValus()[1]["adminUserExpired"].format(email=user["email"], id=user["id"],
                                                                                note=["\nNote:\n" + user[
                                                                                    "remarks"] if not user[
                                                                                                          "remarks"] in [
                                                                                                          None,
                                                                                                          ""] else ""][
                                                                                    0], invite=[
                                "\n\n" + initValus()[1]["invite"].format(
                                    email=inviteUser["email"]) if inviteUser != "" else ""][0])

                        # senf reports to admins
                        for admin in db.getAdminTlId():
                            try:
                                bot.send_message(admin, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                            except:
                                pass

                    else:
                        if emergencyPermission:
                            budyMessage = initValus()[1]["userWarning"].format(email=user["email"], days=
                            [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0],
                                                                               admin=initValus()[0]["adminId"])
                            try:
                                bot.send_message(user["telegram_id"], budyMessage,
                                                 reply_markup=emergencyRechargeMarkup(user["id"]))
                            except:
                                pass
                        else:
                            budyMessage = initValus()[1]["userWarning"].format(email=user["email"], days=
                            [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0],
                                                                               admin=initValus()[0]["adminId"])
                            try:
                                bot.send_message(user["telegram_id"], budyMessage)
                            except:
                                pass

                        # check if user has inviter
                        inviteUser = ""
                        if user["invite_user_id"] is not None and not user["invite_user_id"] in DBase.getAdminsId():
                            inviteUser = DBase.getUserRow(int(user["invite_user_id"]))

                        # check if inviter exist send reports
                        if inviteUser != "":
                            if not inviteUser["telegram_id"] in [0, None]:
                                budyMessage = initValus()[1]["staffUserWarning"].format(email=user["email"], days=
                                [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0], id=user["id"], note=[
                                    "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0])
                                try:
                                    bot.send_message(inviteUser["telegram_id"], budyMessage,
                                                     reply_markup=rechargeMarkup(user["id"], mod="staff"))
                                except:
                                    pass

                        # message budy for sending to admins
                        budyMessage = initValus()[1]["adminUserWarning"].format(email=user["email"], days=
                        [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0], id=user["id"], note=[
                            "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0], invite=[
                            "\n\n" + initValus()[1]["invite"].format(
                                email=inviteUser["email"]) if inviteUser != "" else ""][0])
                        # send reports to admins
                        for i in db.getAdminTlId():
                            try:
                                bot.send_message(i, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                            except:
                                pass

                else:
                    # check if inviter exist
                    inviteUser = ""
                    if user["invite_user_id"] is not None and not user["invite_user_id"] in DBase.getAdminsId():
                        inviteUser = DBase.getUserRow(int(user["invite_user_id"]))

                    # check and send report to inviter
                    if inviteUser != "":
                        if not inviteUser["telegram_id"] in [0, None]:
                            if isExpired:
                                budyMessage = initValus()[1]["staffWarningExpired"].format(email=user["email"],
                                                                                           id=user["id"], note=[
                                        "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][
                                        0])
                                try:
                                    bot.send_message(inviteUser["telegram_id"], budyMessage,
                                                     reply_markup=rechargeMarkup(user["id"], mod="staff"))
                                except:
                                    pass
                            else:
                                budyMessage = initValus()[1]["staffWarning"].format(email=user["email"], days=
                                [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0], id=user["id"], note=[
                                    "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0])
                                try:
                                    bot.send_message(inviteUser["telegram_id"], budyMessage,
                                                     reply_markup=rechargeMarkup(user["id"], mod="staff"))
                                except:
                                    pass

                    for admin in db.getAdminTlId():
                        if isExpired:
                            budyMessage = initValus()[1]["adminWarningExpired"].format(email=user["email"],
                                                                                       id=user["id"], note=[
                                    "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0],
                                                                                       invite=["\n\n" + initValus()[1][
                                                                                           "invite"].format(
                                                                                           email=inviteUser[
                                                                                               "email"]) if inviteUser != "" else ""][
                                                                                           0])
                            try:
                                bot.send_message(admin, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                            except:
                                pass
                        else:
                            budyMessage = initValus()[1]["adminWarning"].format(email=user["email"], days=
                            [expireTerm if expireTerm >= 1 else initValus()[1]["lessOne"]][0], id=user["id"], note=[
                                "\nNote:\n" + user["remarks"] if not user["remarks"] in [None, ""] else ""][0], invite=[
                                "\n\n" + initValus()[1]["invite"].format(
                                    email=inviteUser["email"]) if inviteUser != "" else ""][0])
                            try:
                                bot.send_message(admin, budyMessage, reply_markup=rechargeMarkup(user["id"]))
                            except:
                                pass

            # set log warnings
            log = getLogFile()
            if not var.updateAdmin:
                if str(user["id"]) in log["warning"].keys():
                    # just for making sure becuase we check that in getExpireIds()
                    if not expireTerm in log["warning"][str(user["id"])]:
                        log["warning"][str(user["id"])].append(expireTerm)
                        setValus(log, "log.json")
                else:
                    log["warning"][str(user["id"])] = [expireTerm]
                    setValus(log, "log.json")


    def randomChar(n):
        try:
            n = abs(int(n))
        except:
            n = 0
        seed = "abcdefghijklmnopqrstuvwxyz"
        num = "9876543210"
        seed += seed.upper() + num
        lstSeed = list(seed)
        random.shuffle(lstSeed)
        out = ""
        counter = 0
        while True:
            if out.__len__() == 0:
                try:
                    nom = int(lstSeed[counter])
                    pass
                except:
                    out += lstSeed[counter]
            else:
                out += lstSeed[counter]
            if out.__len__() == n:
                break
            counter += 1
        return out


    def manualOnline(DBase, message):
        try:
            bot.send_message(message.chat.id, initValus()[1]["duringSending"])
        except:
            pass

        lst = userOnline()
        sendLst = []
        for i in lst:
            key = list(i.keys())[0]
            val = list(i.values())[0]
            if val is not None:
                val = val[0]
                if val < initValus()[0]["onlineTerm"] * 60:
                    user = DBase.getUserRow(int(key))
                    email = user["email"]
                    id = key
                    sendLst.append((email, id))
        if sendLst.__len__() == 0:
            try:
                bot.send_message(message.chat.id, initValus()[1]["thereIsNothing"])
            except:
                pass

        # for i in range(len(sendLst)):
        #     bot.send_message(message.chat.id, initValus()[1]["itsOnline"].format(email=sendLst[i][0], id=sendLst[i][1]))
        #     if sendLst.__len__() > 15:
        #         time.sleep(.1)
        #         if i % 15 == 0:
        #             time.sleep(2)
        snd = ""
        for i in range(len(sendLst)):
            snd += f'{initValus()[1]["itsOnline"].format(email=sendLst[i][0], id=sendLst[i][1])}\n'
        sndLst = [""]
        if snd.__len__() > 4000:
            count = 0
            for i in sup(snd, "\n"):
                sndLst[count] += i + "\n"
                if sndLst[count].__len__() > 4000:
                    sndLst.append("")
                    count += 1
            for i in range(len(sndLst)):
                try:
                    bot.send_message(message.chat.id, f"({i + 1}/{sndLst.__len__()})\n\n" + sndLst[i])
                except:
                    pass

        else:
            for i in range(len(sndLst)):
                try:
                    bot.send_message(message.chat.id, snd)
                except:
                    pass


    def manualOnlineWarning(DBase, message, force=False):
        lst = userOnline()
        log = getLogFile()
        if not "block" in list(log.keys()):
            log["block"] = []
        sendLst = []
        for i in lst:
            key = list(i.keys())[0]
            val = list(i.values())[0]
            user = DBase.getUserRow(int(key))
            if (not int(key) in log["block"] or force) and not bool(user["banned"]):
                if val is not None:
                    val = val[0]
                    if val > initValus()[0]["onlineWarning"] * 86400:
                        email = user["email"]
                        id = key
                        timeUser = round(val / 86400)
                        note = user["remarks"]
                        if note is None:
                            note = ""
                        else:
                            note = "\nNote:\n" + note
                        sendLst.append((timeUser, email, id, note))
                else:
                    user = DBase.getUserRow(int(key))
                    email = user["email"]
                    id = key
                    timeUser = -1
                    note = user["remarks"]
                    if note is None:
                        note = ""
                    else:
                        note = "\nNote:\n" + note
                    sendLst.append((timeUser, email, id, note))
        sendLst.sort(reverse=True)
        sendLst1 = [("-", i[1], i[2], i[3]) for i in sendLst if i[0] == -1]
        sendLst2 = [(i[0], i[1], i[2], i[3]) for i in sendLst if i[0] != -1]
        sendLst = sendLst2 + sendLst1
        count = 0
        if message is not None:
            if sendLst.__len__() == 0:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["thereIsNothing"])
                except:
                    pass

            else:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["duringSending"])
                except:
                    pass

        if not force:
            for i in sendLst:
                adminsMessage("adminOnlineWarning", email=i[1], id=i[2], time=i[0], note=i[3])
                if sendLst.__len__() > 15:
                    timeSystem.sleep(.1)
                    if count % 15 == 0:
                        timeSystem.sleep(2)
                count += 1
        else:
            for i in sendLst:
                try:
                    bot.send_message(message.chat.id,
                                     initValus()[1]["adminOnlineWarning"].format(time=i[0], email=i[1], id=i[2],
                                                                                 note=i[3]),
                                     reply_markup=blockMarkup(i[2]))
                except:
                    pass

                if sendLst.__len__() > 15:
                    timeSystem.sleep(.1)
                    if count % 15 == 0:
                        timeSystem.sleep(2)
                count += 1


    def manualSniRandom(db, message):
        tableRaw = db.getTable(table("v2_server_v2ray"))
        tableInfo = db.getTableInfo(table("v2_server_v2ray"))
        lstDic = []
        for i in range(len(tableRaw)):
            dic = dict()
            for j in range(tableInfo.__len__()):
                dic[tableInfo[j]] = tableRaw[i][j]
            lstDic.append(dic)
        tableRaw = lstDic
        fb = True
        strLst = ""
        for i in tableRaw:
            char = randomChar(initValus()[0]["sniRandomLen"])
            tls = i['tlsSettings']
            try:
                tls = json.loads(tls)
                sni = tls["serverName"]
                if sni is None:
                    net = i["networkSettings"]
                    net = json.loads(net)
                    sni = net["headers"]["Host"]
                if not var.sniShow:
                    tls["serverName"] = char + sni[sni.find("."):]
                    strLst += f'{i["name"]}: {tls["serverName"]}' + "\n"
                    tls = str(tls).replace("'", '"').replace(" ", "")
                    tls = "'" + tls + "'"
                    fb = fb and db.setValue(table("v2_server_v2ray"), "tlsSettings", tls, i["id"])
                else:
                    strLst += f'{i["name"]}: {tls["serverName"]}' + "\n"
            except:
                pass
        if True:  # SNI fb
            if bool(initValus()[0]["sniNotic"]):
                if var.sniShow and message is not None:
                    try:
                        bot.send_message(message.chat.id, f"🔔✅ Admin Report ✅🔔\nSNI updated:\n\n{strLst}")
                    except:
                        pass

                else:
                    for i in db.getAdminTlId():
                        try:
                            bot.send_message(i, f"🔔✅ Admin Report ✅🔔\nSNI updated:\n\n{strLst}")

                        except:
                            pass

        else:
            for i in db.getAdminTlId():
                try:
                    bot.send_message(i, "❌ SNI ERROR ❌\n\nAn Error Raised During Set SNIs, Call Developer..!")

                except:
                    pass


    def manualWarning(db, message, force=False):
        checkLog(db)
        expireIds = getExpireIds(db)
        if expireIds.__len__() != 0:
            if message is not None:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["duringSending"])
                except:
                    pass

            sendWarnings(expireIds, db, force=force)
        else:
            if message is not None:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["thereIsNothing"])
                except:
                    pass

            else:
                adminsMessage("", data=initValus()[1]["thereIsNothing"])
        var.updateAdmin = False
        var.updateRe = False


    def manualNewReport(db, message):
        idList = db.getColumn(table("v2_user"), "id")
        log = getLogFile()
        if not "ids" in log.keys():
            log["ids"] = idList
            setValus(log, "log.json")
            return
        news = list(set(idList).difference(set(log["ids"])))
        if news.__len__() != 0:
            adminsMessage("newAccount", newList=news)
            log["ids"] += news
            setValus(log, "log.json")
        elif message is not None:
            try:
                bot.send_message(message.chat.id, initValus()[1]["thereIsNothing"])

            except:
                pass


    # remind to write orderMarkup(id)
    def sendOrderToAdmin(db, message, idx, admins):
        try:
            mssg = initValus()[1]["sendOrderToAdmin"].format(staff=db.getUserRow(idx["staffId"])["email"], date=idx["time"],
                                                         user=db.getUserRow(idx["id"])["email"], amount=idx["amount"])
            for i in admins:
                try:
                    bot.send_message(i, mssg, reply_markup=orderMarkup(idx["id"]))
                except:
                    pass
        except:
            bot.send_message(message.chat.id, "There is an ERROR, Error code: 5482")

    def manualOrderReport(db, message):
        idList = db.getColumn(table("v2_user"), "id")
        logPay = getPaymentFile()
        adminsTlid = db.getAdminTlId()
        if not "order" in logPay.keys():
            logPay["order"] = {}
            setValus(logPay, "payment.json")
            return
        if logPay["order"].__len__() > 0:
            for i in logPay["order"]:
                sendOrderToAdmin(db, message, i, adminsTlid)
        else:
            if message is not None:
                try:
                    bot.send_message(message.chat.id, initValus()[1]["thereIsNoNewOrder"])
                except:
                    pass
            else:
                for i in adminsTlid:
                    try:
                        bot.send_message(i, initValus()[1]["thereIsNoNewOrder"])
                    except:
                        pass


    # services

    def service():
        def getTimeNow():
            tt = sup(getTehranTime(timeSystem.time())[1], ":")
            tt[0] = ["0" + tt[0] if tt[0].__len__() == 1 else tt[0]][0]
            tt[1] = ["0" + tt[1] if tt[1].__len__() == 1 else tt[1]][0]
            return tt[0] + ":" + tt[1]

        def warningService(DbaseService):
            nowTime = getTimeNow()
            if initValus()[0]["serviceWarningTime"] != "" and bool(initValus()[0]["warningEnable"]):
                serviceTimes = sup(initValus()[0]["serviceWarningTime"], ";")
                if nowTime in serviceTimes:
                    if var.warningServiceUpdated:
                        var.warningServiceUpdated = False
                        manualWarning(DbaseService, None)
                else:
                    var.warningServiceUpdated = True

        def sniChangeService(DbaseService):
            nowTime = getTimeNow()
            if initValus()[0]["serviceSniTime"] != "" and bool(initValus()[0]["sniEnable"]):
                serviceTimes = sup(initValus()[0]["serviceSniTime"], ";")
                if nowTime in serviceTimes:
                    if var.sniUpdate:
                        var.sniUpdate = False
                        manualSniRandom(DbaseService, None)
                else:
                    var.sniUpdate = True

        def onlineService(DbaseService):
            nowTime = getTimeNow()
            if initValus()[0]["serviceOnlineTime"] != "" and bool(initValus()[0]["onlineEnable"]):
                serviceTimes = sup(initValus()[0]["serviceOnlineTime"], ";")
                if nowTime in serviceTimes:
                    if var.onlineUpdate:
                        var.onlineUpdate = False
                        manualOnlineWarning(DbaseService, None)
                else:
                    var.onlineUpdate = True

        def newService(DbaseService):
            nowTime = getTimeNow()
            if initValus()[0]["serviceNewTime"] != "" and bool(initValus()[0]["newEnable"]):
                serviceTimes = sup(initValus()[0]["serviceNewTime"], ";")
                if nowTime in serviceTimes:
                    if var.newUpdate:
                        var.newUpdate = False
                        manualNewReport(DbaseService, None)
                else:
                    var.newUpdate = True

        def orderService(DbaseService):
            nowTime = getTimeNow()
            if initValus()[0]["serviceOrderTime"] != "" and bool(initValus()[0]["orderEnable"]):
                serviceTimes = sup(initValus()[0]["serviceOrderTime"], ";")
                if nowTime in serviceTimes:
                    if var.orderService:
                        var.orderService = False
                        manualOrderReport(DbaseService, None)
                else:
                    var.orderService = True

        DbaseService = dbTools.DB()
        while True:
            # do the things
            counter = int(DbaseService.getTehranTime().timestamp())
            var.updateCounter = counter
            while True:
                timeSystem.sleep(1)
                if int(DbaseService.getTehranTime().timestamp()) - counter > DbaseService.initValus()[0]["serviceTime"]:
                    warningService(DbaseService)
                    sniChangeService(DbaseService)
                    onlineService(DbaseService)
                    newService(DbaseService)
                    orderService(DbaseService)
                    counter = int(DbaseService.getTehranTime().timestamp())
                    var.updateCounter = counter


    while True:
        if sys.argv.__len__() <= 1:
            try:
                thread = threading.Thread(target=service)
                thread.start()
                bot.polling()
            except Exception as e:
                setErrorLog(str(e))
                timeSystem.sleep(.5)
                pass
        else:
            if sys.argv[1] == "debug":
                thread = threading.Thread(target=service)
                thread.start()
                bot.polling()
