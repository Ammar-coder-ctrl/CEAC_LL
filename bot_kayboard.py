from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ContextTypes
import os
from constant import *



#Kyeboard_set
admin_main_menu_k = [["DOWNLOAD FILE"],["UPLOAD FILE"],["DELETE FILE"],["SEND FILES DATA"],["HELP"]]
user_main_menu_k = [["DOWNLOAD FILE"],["HELP"]]
year_k = [["FIRST YEAR"],["SECOND YEAR"],["THIRD YEAR"],["FOURTH YEAR"],["FIFTH YEAR"],["MAIN MENU"]]
semester_k = [["FIRST SEMESTER"],["SECOND SEMESTER"],["YEAR","MAIN MENU"]]
Y1S1 = [["رياضيات 1"],["لغة 1"],["مهارات حاسوب 1"],["فيزياء"],["عربي"],["ثقافة"],["خواص"],["SEMESTER","MAIN MENU"]]
Y1S2 = [["رياضيات 2"],["لغة 2"],["مهارات حاسوب 2"],["مدخل الى الحاسوب"],["ورش تخصصية"],["رسم هندسي"],["اسس هندسة كهريائية"],["SEMESTER","MAIN MENU"]]
Y2S1 = [["رياضيات 3"],["لغة 3"],["برمجة 2"],["امن صناعي"],["بحوث عمليات"],["تحليل نظم"],["اسس هندسة ألكترونية"],["SEMESTER","MAIN MENU"]]
Y2S2 = [["رياضيات 4"],["لغة 4"],["خوارزميات و بنى معطيات"],["دارات منطقية"],["دارات الكترونية"],["اتصالات تشابهية"],["ألات كهريائية"],["SEMESTER","MAIN MENU"]]
Y3S1 = [["بنية حاسوب 1"],["تحكم الي 1"],["قواعد بيانات"],["معالجة اشارة"],["اتصالات رقمية"],["رسم باستخدام الحاسب"],["SEMESTER","MAIN MENU"]]
Y3S2 = [["بنية حاسوب 2"],["ذكاء اصطناعي"],["هندسة البرمجيات"],["قياسات الكترونية"],["مهارات ذاتية"],["انظمة التشغيل"],["SEMESTER","MAIN MENU"]]
Y4S1 = [["شبكات 1"],["تحكم الي 2"],["حساسات"],["نظرية المعلومات"],["معالجات صغرية"],["شبكات عصبونية"],["SEMESTER","MAIN MENU"]]
Y4S2 = [["شبكات 2"],["منطق غيمي"],["مترجمات"],["زمن حقيقي"],["نمذجة و محاكات"],["SEMESTER","MAIN MENU"]]
Y5S1 = [["معالجة صورة"],["ياثون"],["أمن المعلومات"],["معالجات تفرعية"],["SEMESTER","MAIN MENU"]]
Y5S2 = [["أدارة مشاريع"],["تحكم منطقي مبرمج"],["وثوقية و معايرة"],["تعرف على النماذج"],["SEMESTER","MAIN MENU"]]
supject_k = [Y1S1,Y1S2,Y2S1,Y2S2,Y3S1,Y3S2,Y4S1,Y4S2,Y5S1,Y5S2]
type_k = [["THEORETICAL","PRACTICAL","OTHER"],["SUPJECT","MAIN MENU"]]
admain_edetor_k = [["ADD ADMIN"],["REMOVE ADMIN"],["ADMIN LIST"],["SEND USERS DATA"],["SEND FILES DATA"],["MAIN MENU"]]





#Kyeboard Function
    #MAIN MENU
async def main_menu_keyboard(update: Update,context : ContextTypes.DEFAULT_TYPE):
    if context.user_data.get(the_user_type,"normel") == "admin":
        keyboard = admin_main_menu_k
    elif context.user_data.get(the_user_type,"normel") == "normel":
        keyboard = user_main_menu_k
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("ماذا تريد ان تفعل ؟ ", reply_markup=reply_markup)
    
    
    #YEAR
async def year_keyboard(update: Update):
    keyboard = year_k
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(" اختر سنتك الدراسية:", reply_markup=reply_markup)
    
    
    #SEMESTER    
async def semester_keyboard(update: Update):
    keyboard = semester_k
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(" اختر فصلك الدراسي:", reply_markup=reply_markup)
    
    
    #SUPJECT
async def supject_keyboard(update: Update,context : ContextTypes.DEFAULT_TYPE):
    year = context.user_data.get(the_year,"FIRST YEAR")
    semester = context.user_data.get(the_semester,"FIRST SEMESTER")
    if year == "FIRST YEAR" and semester == "FIRST SEMESTER":
        keyboard = supject_k[0]
    elif year == "FIRST YEAR" and semester == "SECOND SEMESTER":
        keyboard = supject_k[1]
    elif year == "SECOND YEAR" and semester == "FIRST SEMESTER":
        keyboard = supject_k[2]
    elif year == "SECOND YEAR" and semester == "SECOND SEMESTER":
        keyboard = supject_k[3]
    elif year == "THIRD YEAR" and semester == "FIRST SEMESTER":
        keyboard = supject_k[4]
    elif year == "THIRD YEAR" and semester == "SECOND SEMESTER":
        keyboard = supject_k[5]
    elif year == "FOURTH YEAR" and semester == "FIRST SEMESTER":
        keyboard = supject_k[6]
    elif year == "FOURTH YEAR" and semester == "SECOND SEMESTER":
        keyboard = supject_k[7]
    elif year == "FIFTH YEAR" and semester == "FIRST SEMESTER":
        keyboard = supject_k[8]
    elif year == "FIFTH YEAR" and semester == "SECOND SEMESTER":
        keyboard = supject_k[9]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر المقرر الدراسي:", reply_markup=reply_markup)
    
    
    #TYPE
async def type_keyboard(update: Update):
    keyboard = type_k
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر نوع الملفات:", reply_markup=reply_markup)
    
    
    #FILES
async def files_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    year = context.user_data.get(the_year)
    semester = context.user_data.get(the_semester)
    subject = context.user_data.get(the_supject)
    file_type = context.user_data.get(the_type)
    folder_path = f"./files/{year}/{semester}/{subject}/{file_type}"
    if not os.path.exists(folder_path):
        await update.message.reply_text("لا يوجد ملفات في هذا القسم.")
        return
    files = os.listdir(folder_path)
    files = [f for f in files if not f.startswith(".")]
    if not files:
        await update.message.reply_text("لا توجد ملفات مرفوعة بعد.")
        return
    keyboard = [[file_name] for file_name in files]
    keyboard.append(["TYPE", "MAIN MENU"])
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر الملف:", reply_markup=reply_markup)
    
    #ADMIN
async def admin_edetor_keyboard(update: Update):
    keyboard = admain_edetor_k
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("اختر نوع الملفات:", reply_markup=reply_markup)