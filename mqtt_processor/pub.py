import paho.mqtt.client as mqtt

mqtt = mqtt.Client("python_pub") #Mqtt Client 오브젝트 생성
mqtt.connect("52.194.252.52", 1883) #MQTT 서버에 연결

mqtt.publish("/Seoul/Dongjak/1", "/Seoul/Dongjak/1") #토픽과 메세지 발행
mqtt.publish("/Seoul/Dongjak/2", "/Seoul/Dongjak/2")

mqtt.loop(2)
