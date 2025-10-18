from telegram import Update
from telegram.ext import CommandHandler, ApplicationBuilder , MessageHandler , filters,ContextTypes
import os
from dotenv import load_dotenv
import threading
from constant import *
from admin_edetor import is_admin,load_admins,add_admin,remove_admin
from bot_kayboard import *
from users_files_db import *
from dummy_server import run_flask

load_dotenv()
create_users_table()
create_files_table()

#KEYS
TOKEN = os.getenv("BOT_TOKEN")
PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_ID  = int(os.getenv("ADMIN_ID"))


#Command Function
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    if user_id == ADMIN_ID or is_admin(user_id):
        context.user_data[the_user_type] = "admin"
    else:
        context.user_data[the_user_type] = "normel"
    user_type = context.user_data.get(the_user_type,"normel")
    user_full_name = update.effective_user.full_name
    context.user_data[the_user_id] =user_id
    context.user_data[the_user_name] =user_name
    context.user_data[the_user_full_name] =user_full_name
    add_user(user_id,user_name,user_full_name,user_type)
    await update_user_data(update,context)
    await restart_data(context)
    await main_menu_keyboard(update,context)
    


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📌 *مساعدة البوت التعليمي*:

هذا البوت يساعدك في إدارة ملفات المحاضرات حسب السنة والفصل والمادة ونوع الملف.

🧭 *طريقة الاستخدام*:
1. اختر العملية من القائمة الرئيسية:
   - 📥 DOWNLOAD FILE: لتحميل ملف موجود.

2. اختر سنتك الدراسية، ثم الفصل، ثم المقرر.

3. اختر نوع الملف:
   - THEORETICAL: ملفات نظرية.
   - PRACTICAL: ملفات عملية.
   - OTHER: ملفات أخرى.

4.🔁 يمكنك العودة في أي وقت إلى القائمة الرئيسية بالضغط على "MAIN MENU".

5.في حال حدوث اي مشكلة او عطل او توقف اثناء استخدام البوت اضغط على الثلاث اشرطة و اختر الامر /start

📞 لأي استفسار إضافي، تواصل مع مسؤول البوت أو المطوّر.
/start

    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text, parse_mode="Markdown")


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = update.effective_user.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text=contact_text, parse_mode="Markdown")



#Function
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
        add_file(document.file_name,subject,file_type,semester,year)
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
            remove_file(file_name,subject,file_type,semester,year)
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
    context.user_data[the_admin_edetor_on] = False
    context.user_data[the_admin_edetor_command] = ""



async def update_user_data(update : Update,context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_full_name = update.effective_user.full_name
    user_type = context.user_data.get(the_user_type,"normel")
    context.user_data[the_user_id] = user_id
    context.user_data[the_user_full_name] = user_full_name
    update_user_info(user_id,user_full_name,user_type)



#smart step
async def smart_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_type = context.user_data.get(the_user_type,"normel")
    #moving
    if text == "MAIN MENU":
        await update_user_data(update,context)
        await restart_data(context)
        await main_menu_keyboard(update,context)
        return
    elif text == "YEAR":
        await update_user_data(update,context)
        await year_keyboard(update)
        return
    elif text == "SEMESTER":
        await update_user_data(update,context)
        await semester_keyboard(update)
        return
    elif text == "SUPJECT":
        await update_user_data(update,context)
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
    elif text == "UPLOAD FILE" and user_type == "admin":
        context.user_data[the_command] = text
        await year_keyboard(update)
        return
    elif text == "DELETE FILE" and user_type == "admin":
        context.user_data[the_command] = text
        await year_keyboard(update)
        return
    elif text == "HELP":
        await help_command(update,context)
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
    elif context.user_data.get(dd_file_ok,False) == True:
        await DD_file(update,context)
        return
    #ADMIN
    elif text == PASSWORD and user_type == "admin":
        context.user_data[the_admin_edetor_on] = True
        await admin_edetor_keyboard(update)
        return
    elif text == "ADMIN LIST" and context.user_data.get(the_admin_edetor_on,False):
        re_text = load_admins()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=re_text, parse_mode="Markdown")
        return
    #DATA
    elif text == "SEND USERS DATA" and context.user_data.get(the_admin_edetor_on,False):
        await send_users_excel(update)
        return
    elif text == "SEND FILES DATA" and context.user_data.get(the_user_type,"normel"):
        await send_files_excel(update)
        return
    elif text in ["ADD ADMIN","REMOVE ADMIN"] and context.user_data.get(the_admin_edetor_on,False):
        context.user_data[the_admin_edetor_command] = text
        return
    elif context.user_data.get(the_admin_edetor_on,False):
        command = context.user_data.get(the_admin_edetor_command)
        if command == "ADD ADMIN":
            add_admin(text)
            return
        elif command == "REMOVE ADMIN":
            remove_admin(text)
            return
    #END
    else:
        return







#Main
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    #handlers
    start_command_handler = CommandHandler("start", start_command)
    help_command_handler = CommandHandler("help",help_command)
    id_command_handler = CommandHandler("id",id_command)
    smart_step_handler = MessageHandler(filters.TEXT & ~filters.COMMAND,smart_step)
    upload_file_handler = MessageHandler(filters.Document.ALL,upload_file)
    #Regesters
    app.add_handler(start_command_handler)
    app.add_handler(help_command_handler)
    app.add_handler(id_command_handler)
    app.add_handler(upload_file_handler)
    app.add_handler(smart_step_handler)
    
    app.run_polling()



if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_bot()
