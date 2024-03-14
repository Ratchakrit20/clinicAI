from gtts import gTTS
from IPython.display import Audio
import subprocess

text = "อาการสำคัญที่ทำให้มาโรงพยาบาล"
tts = gTTS(text,lang='th')
tts.save('output1.mp3')

# audio = Audio('output.mp3', autoplay=True)

#โค้ดนี้จะใช้ subprocess.run เพื่อเรียกใช้คำสั่ง start ใน Windows เพื่อเปิดไฟล์เสียงโดยใช้โปรแกรมเล่นไฟล์เสียงที่ติดตั้งในระบบของคุณ. กรุณาปรับแต่งโค้ดตามระบบปฏิบัติการที่คุณใช้งาน (Windows, macOS, Linux) และโปรแกรมเล่นไฟล์เสียงที่คุณติดตั้ง.
subprocess.run(['start', 'output1.mp3'], shell=True)