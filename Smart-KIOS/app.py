from flask import Flask, jsonify, request
import mysql.connector
from transformers import pipeline
import torch
from flask_cors import CORS
from gtts import gTTS
from IPython.display import Audio
import os




app = Flask(__name__)
CORS(app)
# กำหนดค่าการเชื่อมต่อฐานข้อมูล
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'mydb',
}
# ใส่โค้ดส่วนที่ใช้ Transformers ที่นี่
MODEL_NAME = "biodatlab/whisper-th-small-combined"  # specify the model name
lang = "th"  # change to Thai langauge

device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)
pipe.model.config.forced_decoder_ids = pipe.tokenizer.get_decoder_prompt_ids(
  language=lang,
  task="transcribe"
)




# เรียกใช้ฟังก์ชันนี้เพื่อเรียกหน้าเว็บ
@app.route('/python-endpoint', methods=['POST'])
def index():
    data = request.json
    userID = data['userID']
    questionId = data['questionId']
    try:
        # เชื่อมต่อกับฐานข้อมูล
        connection = mysql.connector.connect(**db_config)

        # สร้าง Cursor object เพื่อทำคำสั่ง SQL
        cursor_SELECT = connection.cursor()

        # ทำคำสั่ง SQL ตรวจสอบข้อมูลในฐานข้อมูล
        # ในที่นี้ไม่ได้ใช้ข้อมูลจริง แค่ตัวอย่างเท่านั้น
        cursor_SELECT.execute("SELECT path FROM log WHERE `questionID` = %s AND `userID` = %s AND DATE(`date`) = CURDATE()", (questionId, userID))
        #cursor_SELECT.execute("INSERT INTO `log` (`userID`, `questionID`, `path`) VALUES (?,?,?)")
        # ดึงข้อมูล
        data = cursor_SELECT.fetchall()

        # ปิดการเชื่อมต่อ
        connection.close()

        # ตรวจสอบว่ามีข้อมูลในฐานข้อมูลหรือไม่
        if data:
             # ลิสต์เพื่อเก็บผลลัพธ์ทุกตัว
            print(data)
            results = []
             # ลูปเพื่อนำข้อมูลทุกตัวไปให้ Transformers pipeline
            for item in data:
                audio_path = item[0]  # ตัวอย่างข้อมูลอาจจะอยู่ในคอลัมน์
                print(item[0])
                # ทำต่อไปเพื่อให้ได้ตัวแปร sample ในรูปแบบที่ Transformers ต้องการ
                # นำ audio_path มาใส่ใน Transformers pipeline
                sample = rf'{audio_path}'

                # นำตัวแปร sample ไปให้ Transformers pipeline
                result = pipe(sample)
                print(result["text"])
                results.append(result["text"])
                 # เพิ่มการเชื่อมต่อกับฐานข้อมูล
                connection_insert = mysql.connector.connect(**db_config)
                cursor_INSERT = connection_insert.cursor()

                # ทำคำสั่ง SQL เพื่อ INSERT ข้อมูล result["text"]
                sql_INSERT = "UPDATE log SET text = %s WHERE path = %s AND `questionID` = %s AND `userID` = %s AND DATE(`date`) = CURDATE()"
                cursor_INSERT.execute(sql_INSERT, (result["text"], audio_path,questionId,userID))

                # Commit การเปลี่ยนแปลงและปิดการเชื่อมต่อ
                connection_insert.commit()
                connection_insert.close()
                # ส่งข้อมูลกลับไปยัง JavaScript
                nextpage = {'nextpage': result["text"]}
            # ส่งข้อมูลไปยังหน้าเว็บ
            return jsonify(nextpage)

        else:
            database = {'database': 'Not have data'}
            return jsonify(database)

    except Exception as e:
         # ส่งข้อมูลกลับไปยัง JavaScript ว่ามีข้อผิดพลาด
        error = {'error': str(e)}
        return jsonify(error)
    
@app.route('/python-sound', methods=['POST'])
def index1():
    data = request.json
    text = data['text']
    tts = gTTS(text, lang='th')
    # ให้ไฟล์เสียงถูกบันทึกไว้ในโฟลเดอร์ public/audio
    # filename = 'output1.mp3'
    # filepath = os.path.join('api', 'audio', filename)
    tts.save('output1.mp3')
    # ส่ง URL สาธารณะของไฟล์เสียงกลับ
    return jsonify({'sound': 'output1.mp3'})


if __name__ == '__main__':
    app.run(port=5000,debug=True)
    
    
#ยังไม่สามารถให้flaskรันอัตโนมัติได้