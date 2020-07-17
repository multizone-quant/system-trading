# 2020/07/17
# telegram-bot 만드는 간단한 예제
# xing-api와 연동하는 예제는 다음 주 올릴 예정임
# 자세한 설명 : https://money-expert.tistory.com/19

import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler  
import time

my_token = '텔레그램 봇 토큰'

updater = Updater(my_token, use_context=True)

# 명령어 help가 들어올 때 불리어지는 함수
#def help_command(bot, update) :
def help_command(update, context) :
    # 돌려 줄 text를 알아서 만든다.
    reply_text = "실행가능한 명령어" + "\n" + "/sise code : 현재가를 알려줌"

    # 만든 text를 caller에게 돌려준다.
    update.message.reply_text(reply_text)

# 명령어 sise가 들어올 때 불리어지는 함수
def sise_command(update, context) :
    # args[0]에 첫번째 인자, 복수개 인자를 사용한 경우에는 [1], [2] 이런식으로 구분
    code = context.args[0]
    # 보내줄 현재가, xing api로 값을 얻는다.
    price = 11000
    # 돌려줄 full text, 알아서 만든다.
    reply_text = '현재가 : ' + code + ' ' + str(price)

    # 만든 text를 caller에게 돌려준다.
    update.message.reply_text(reply_text)

# 일반 메세지를 입력할 때 불리어지는 함수
#def get_message(bot, update) :
def get_message(update, context) :
    # 받은 메세지 출력
    print(update.message.text)
    # 응대할 메지를 만들어 보낸다
    res = '받은 메세지: ' + update.message.text
    update.message.reply_text(res)

# 등록되지 않은 명령어에 대응
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# /help 명령어를 위한 handler 등록
updater.dispatcher.add_handler(CommandHandler('help', help_command))

# /sise 명령어를 위한 handler 등록
# /sise 명령어는 코드를 입력을 받아야하므로, pass_args를 Ture로 설정
updater.dispatcher.add_handler(CommandHandler('sise', sise_command, pass_args=True))

# 알 수 없는 명령어가 왔을 때 대응
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

# 일반 메세지를 처리하기 위한 handler 등록 
#   일반 메세지는 / 없이 입력하는 문자열
updater.dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), get_message))

# 3초마다 새 명령어 왔는지 확인하도록 설정
updater.start_polling(timeout=10, clean=True)

# 새 명령어가 올때까지 waiting
print('bot start')
updater.idle()
