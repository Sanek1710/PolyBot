class Message():
    def __init__(self, id = 0, from_id = 0, to_ids = [], text='', attachments=[], forwards=[], keyboard=None):
        self.id = id
        self.from_id = from_id
        self.to_ids = to_ids
        self.text = text
        self.attachments = attachments
        self.forwards = forwards
        self.keyboard = keyboard
        self.random_id = 0

    def to_forward(self):
        return Message(forwards=[self.id])

    def dump(self):
        
        return {
            'peer_ids': self.to_ids if isinstance(self.to_ids, list) else [self.to_ids],
            'random_id': self.random_id,
            'message': self.text if self.text else '&#13;',
            'attachment': ','.join(self.attachments),
            'forward_messages': self.forwards,
            'keyboard': self.keyboard.get_keyboard() if self.keyboard else None
        }

    def dump_fwd(self):
        return {
            'peer_ids': self.to_ids if isinstance(self.to_ids, list) else [self.to_ids],
            'random_id': self.random_id,
            'forward_messages': self.id
        }

    def send(self, vk, to_ids=None):
        if to_ids:
            self.to_ids = to_ids
        try:
            result = vk.messages.send(**self.dump())
            return result
        except Exception as e:
            print("Error sending message:", e)
            return []

    def forward(self, vk, to_ids=None):
        if to_ids:
            self.to_ids = to_ids
        try:
            vk.messages.send(**self.dump_fwd())
        except Exception as e:
            print("Error sending message:", e)


def upload_attachment(attachment):
    if attachment['type'] in ["photo", "video", "doc"]: 
        attch = attachment[attachment['type']]
        return '{}{}_{}_{}'.format(attachment['type'], attch['owner_id'], attch['id'], attch['access_key'])
    elif attachment['type'] == "audio":
        audio = attachment["audio"]
        return 'audio{}_{}'.format(audio['owner_id'], audio['id'])
    elif attachment['type'] == "wall":
        wall = attachment["wall"]
        return 'wall{}_{}'.format(wall['from_id'], wall['id'])

def load(message : dict):
    msg = Message(id = message['id'], from_id = message['from_id'], to_ids=message['from_id'])

    if message['fwd_messages']:
        msg.forwards = [message['id']]
    else:
        msg.attachments = [upload_attachment(attachment) for attachment in message['attachments']]
        msg.text = message['text'].strip()
    return msg



