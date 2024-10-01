from time import sleep
import telebot
import json

class TelegramBot:
    
    def start(self, grupo):
        self.token = "7193505693:AAF39FmfHiTsRLX-gOk40x94lt2QAwApBSc"
        self.grupos = grupo
        self.bot = telebot.TeleBot(self.token, parse_mode=None)
    
    def close(self):
        self.bot.close()
        
    def send_alert(self):
        with open('alerta.txt', 'r', encoding='utf8') as alertFile:
            alert =  alertFile.read()
            alertFile.close()
        list_message_id = []
        for grupo in self.grupos:
            try:
                list_message_id.append(self.get_info(self.bot.send_message(grupo, alert)))
            except:
                continue
            sleep(2)
        return list_message_id

    def send_confirmed(self, aposta, martingale, ultimo):
        with open('confirmacao.txt', 'r', encoding='utf8') as confirmacaoFile:
            confirmacao =  confirmacaoFile.read()
            confirmacaoFile.close()
        empjiUltimo =  "🔵" if ultimo == "Player" else  "🔴"
        emojiAposta = "🔵" if aposta == "Player" else "🔴"
        confirmacao = confirmacao.replace(r'{emoji1}', f"{empjiUltimo}")
        confirmacao = confirmacao.replace(r'{emoji2}', f"{emojiAposta}")
        confirmacao = confirmacao.replace(r'{gales}', f"{martingale}")
        for grupo in self.grupos:
            self.bot.send_message(grupo, confirmacao, parse_mode='HTML', disable_web_page_preview=True)
            
    def result(self, win):
        if win: sticker = "CAACAgEAAxkBAAEL8_NmIp17s6mfmYpU_t5na8y2RAa8ewACVwQAAui7GUWAe-4hmV3OzTQE"
        else: sticker = "CAACAgEAAxkBAAEL8_VmIp2A-Kwvd3_QyBxRAcZ6xPa-IQACqwMAAnwbEEWnaTXH5IfB5zQE"
        for grupo in self.grupos: 
            self.bot.send_sticker(grupo, sticker)
            
    def martingale(self, martingale):
        list_message_id = []
        with open('martingale.txt', 'r', encoding='utf8') as martingaleFile:
            martingaleTexto =  martingaleFile.read()
            martingaleFile.close()
        martingaleTexto = martingaleTexto.replace(r"{gale}", f"{martingale}")
        for grupo in self.grupos:
            list_message_id.append(self.get_info(self.bot.send_message(grupo, martingaleTexto)))
        return list_message_id
    
    def greens_seguidos(self, numero):
        for grupo in self.grupos:
            self.bot.send_message(grupo, f"✅ ESTAMOS A {numero} GREENS SEGUIDOS !")
            
    def delete_messages(self, list_message_id):
        for info in list_message_id:
            self.bot.delete_message(info[0], info[1])
            
    def get_info(self, jsonMessageInfo):
        return [jsonMessageInfo.chat.id,jsonMessageInfo.id]
    
    def placar(self, sinais, greens_contagem, loss_contagem, porcentagem, otherGroup = None):
        for grupo in self.grupos:
            try:
                mensagem = f"✳ Parcial 📈\n✳ Sinais : {sinais}\n✅ Greens : {greens_contagem}\n❎ Loss : {loss_contagem} \n\n🚀 Assertividade : {porcentagem}%"
                try:
                    self.get_info(self.bot.send_message(otherGroup or grupo, mensagem))
                except:
                    continue
            except:
                pass