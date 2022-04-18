import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Bool

import random


class VoiceInterpreter(Node):

    def __init__(self):
        super().__init__('voice_interpreter')
        self.subscription = self.create_subscription(
            String,
            'voice_commands',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.tts_publisher_ = self.create_publisher(String, 'tts', 10)
        self.speech_activation_publisher_ = self.create_publisher(Bool, 'activation', 1)
        self.gen_responses = ["Yes, all systems are a go",
                              "I am here", "Hello", "Yes", "Are you talking to me"]

    #str.startswith(str, beg=0,end=len(string));
    # in
    def publish_to_tts(self):
    	
        msg = String()
        msg.data = tts_message
        self.tts_publisher_.publish(msg)
        
    def start_voice_recognition(self):
        st_msg = Bool()
        st_msg.data = True
        self.speech_activation_publisher_.publish(st_msg)

    def general_response(self, msg):
        valid = False
        if "are you there" in msg:
            valid = True
        elif "can you hear me" in msg:
            valid = True
        elif "are you ready" in msg:
            valid = True
        elif "tr2 hello" in msg:
            valid = True

        if valid:
            global tts_message
            tts_message = random.choice(self.gen_responses)
            self.publish_to_tts()
        return valid

    def my_name(self, msg):
        valid = False
        if "what is your name" in msg:
            valid = True
        elif "what do they call you" in msg:
            valid = True
        elif "what's your name" in msg:
            valid = True
        elif "who are you" in msg:
            valid = True

        if valid:
            global tts_message
            tts_message = "TR2"
            self.publish_to_tts()
        return valid

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        valid = self.general_response(msg.data)
        if valid is False:
            valid = self.my_name(msg.data)
            
            
        #turn on voice recognition if we didn't send anything to TTS
        if valid is False:
            self.start_voice_recognition()


def main(args=None):
    rclpy.init(args=args)

    node = VoiceInterpreter()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
