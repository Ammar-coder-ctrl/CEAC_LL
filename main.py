from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder , MessageHandler , filters
import os


#TOKEN
TOKEN = "8455470674:AAEhM_jFlFpRhgZ4x9806QMrenXzYTBY5WA"

#CONSTENT
the_command = 'the_command'
the_year = 'the_year'
the_semester = 'the_semester'
the_supject = 'the_supject'
the_type = 'the_type'
upload_file_ok = "upload_file_ok"
dd_file_ok = 'dd_file_ok'


#Kyeboard_set
main_menu_k = [["DOWNLOAD FILE"],["UPLOAD FILE"],["DELETE FILE"],["HELP"],["CONTACT"]]
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
admain_k = [["ADD ADMAIN"],["REMOVE ADMAIN"],["MAIN MENU"]]
user_k = [["DOWNLOAD FILE"],["HELP"],["CONTACT"]]

#Kyeboard Function
    #MAIN MENU
async def main_menu_keyboard(update: Update,context = ContextTypes.DEFAULT_TYPE):
    keyboard = main_menu_k
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
    
    
#Command Function
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await main_menu_keyboard(update)
    restart_data(context)
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📌 *مساعدة البوت التعليمي*:

هذا البوت يساعدك في إدارة ملفات المحاضرات حسب السنة والفصل والمادة ونوع الملف.

🧭 *طريقة الاستخدام*:
1. اختر العملية من القائمة الرئيسية:
   - 📥 DOWNLOAD FILE: لتحميل ملف موجود.
   - 📤 UPLOAD FILE: لرفع ملف جديد.
   - 🗑 DELETE FILE: لحذف ملف موجود.

2. اختر سنتك الدراسية، ثم الفصل، ثم المقرر.

3. اختر نوع الملف:
   - THEORETICAL: ملفات نظرية.
   - PRACTICAL: ملفات عملية.
   - OTHER: ملفات أخرى.

4. في حالة التحميل أو الحذف، اختر اسم الملف من القائمة.

📂 الملفات تُحفظ وتُنظّم تلقائيًا حسب اختياراتك.

🔁 يمكنك العودة في أي وقت إلى القائمة الرئيسية بالضغط على "MAIN MENU".

📞 لأي استفسار إضافي، تواصل مع مسؤول البوت أو المطوّر.
/start

    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="Markdown")
    
    
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = """
📞 *معلومات التواصل مع المطوّر:*

- 💬 Telegram: [@amoshka183]

    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=contact_text, parse_mode="Markdown")

    
async def upload_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get(upload_file_ok,False):
        document = update.message.document
        year = context.user_data.get(the_year)
        semester = context.user_data.get(the_semester)
        subject = context.user_data.get(the_supject)
        file_type = context.user_data.get(the_type)
        folder_path = f"./files/{year}/{semester}/{subject}/{file_type}"
        os.makedirs(folder_path, exist_ok=True)
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(folder_path, document.file_name)
        await file.download_to_drive(file_path)
        await context.bot.send_message(chat_id = update.effective_chat.id,text = "تم حفظ الملف بنجاح")
        context.user_data[upload_file_ok] = False
        return
    else:
        return
    
    
async def DD_file(update: Update,context: ContextTypes.DEFAULT_TYPE):
    file_name = update.message.text
    command = context.user_data.get(the_command)
    year = context.user_data.get(the_year)
    semester = context.user_data.get(the_semester)
    subject = context.user_data.get(the_supject)
    file_type = context.user_data.get(the_type)
    folder_path = f"./files/{year}/{semester}/{subject}/{file_type}"
    file_path = os.path.join(folder_path, file_name)
    if not os.path.isfile(file_path):
        await update.message.reply_text("⚠️ الملف غير موجود.")
        return
    if command == "DOWNLOAD FILE":
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, "rb"))
        await update.message.reply_text("📤 تم إرسال الملف بنجاح.")
        return
    elif command == "DELETE FILE":
        try:
            os.remove(file_path)
            await update.message.reply_text("🗑 تم حذف الملف بنجاح.")
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ أثناء الحذف: {e}")
        return
    context.user_data[dd_file_ok] = False
    
    
async def restart_data(context: ContextTypes.DEFAULT_TYPE):
    context.user_data[the_command] = ""
    context.user_data[the_year] = ""
    context.user_data[the_semester] = ""
    context.user_data[the_supject] = ""
    context.user_data[the_type] = ""
    context.user_data[upload_file_ok] = False
    context.user_data[dd_file_ok] = False


#smart step
async def smart_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    #moving
    if text == "MAIN MENU":
        await main_menu_keyboard(update)
        restart_data(context)
        return
    elif text == "YEAR":
        await year_keyboard(update)
        return
    elif text == "SEMESTER":
        await semester_keyboard(update)
        return
    elif text == "SUPJECT":
        await supject_keyboard(update,context)
        return
    elif text == "TYPE":
        await type_keyboard(update)
        return
    #MAIN MENU
    elif text == "DOWNLOAD FILE":
        context.user_data[the_command] = text
        await year_keyboard(update)
        return
    elif text == "UPLOAD FILE":
        context.user_data[the_command] = text
        await year_keyboard(update)
        return
    elif text == "DELETE FILE":
        context.user_data[the_command] = text
        await year_keyboard(update)
        return
    elif text == "HELP":
        await help_command(update,context)
        return
    elif text == "CONTACT":
        await contact_command(update, context)
        return
    #YEAR
    elif any(text in row for row in year_k):
        context.user_data[the_year] = text
        await semester_keyboard(update)
        return
    #SEMESTER
    elif any(text in row for row in semester_k):
        context.user_data[the_semester] = text
        await supject_keyboard(update,context)
        return
    #SUPJECT
    elif any(text in cell for keyboard in supject_k for row in keyboard for cell in row):
        context.user_data[the_supject] = text
        await type_keyboard(update)
        return
    #TYPE
    elif any(text in row for row in type_k):
        command = context.user_data.get(the_command) 
        context.user_data[the_type] = text
        if command == "UPLOAD FILE":
            await context.bot.send_message(chat_id = update.effective_chat.id,text = "ارسل الملف الان ليتم اضافته")
            context.user_data[upload_file_ok] = True
            return
        elif command == "DOWNLOAD FILE":
            await files_keyboard(update, context)
            context.user_data[dd_file_ok] = True
            return
        elif command == "DELETE FILE":
            await files_keyboard(update, context)
            context.user_data[dd_file_ok] = True
            return
        return
    elif context.user_data[dd_file_ok] == True:
        await DD_file(update,context)
        return
    #END
    else:
        return
#Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    #handlers
    start_command_handler = CommandHandler("start", start_command)
    help_command_handler = CommandHandler("help",help_command)
    smart_step_handler = MessageHandler(filters.TEXT,smart_step)
    upload_file_handler = MessageHandler(filters.Document.ALL,upload_file)
    #Regesters
    app.add_handler(start_command_handler)
    app.add_handler(help_command_handler)
    app.add_handler(smart_step_handler)
    app.add_handler(upload_file_handler)
    app.run_polling()