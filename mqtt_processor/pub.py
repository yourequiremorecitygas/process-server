import paho.mqtt.client as mqtt

mqtt = mqtt.Client("python_pub") #Mqtt Client 오브젝트 생성
mqtt.connect("52.194.252.52", 1883) #MQTT 서버에 연결

mqtt.publish("topic", "AT") #토픽과 메세지 발행
mqtt.publish("topic", "BT")

mqtt.loop(2)