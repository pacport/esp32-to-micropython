


endpoint = b'a8mam99my8vlt-ats.iot.ap-northeast-1.amazonaws.com'



SHADOW_TOPIC = '$aws/things/{}/shadow'
SHADOW_TOPIC_GET = SHADOW_TOPIC + '/get'
SHADOW_TOPIC_GET_ACCEPTED = SHADOW_TOPIC_GET + '/accepted'
SHADOW_TOPIC_GET_REJECTED = SHADOW_TOPIC_GET + '/rejected'
SHADOW_TOPIC_GET_DOCUMENT = SHADOW_TOPIC_GET + '/documents'
SHADOW_TOPIC_UPDATE = SHADOW_TOPIC + '/update'
SHADOW_TOPIC_UPDATE_ACCEPTED = SHADOW_TOPIC_UPDATE + '/accepted'
SHADOW_TOPIC_UPDATE_REJECTED = SHADOW_TOPIC_UPDATE + '/rejected'
SHADOW_TOPIC_UPDATE_DELTA =  SHADOW_TOPIC_UPDATE + '/delta'
SHADOW_TOPIC_UPDATE_DOCUMENT = SHADOW_TOPIC_UPDATE + '/documents'


AWS_TOPIC_JOBS_NOTIFY_NEXT = "$aws/things/{}/jobs/notify-next"
AWS_TOPIC_JOBS = "$aws/things/{}/jobs"
AWS_TOPIC_JOBS_GET = AWS_TOPIC_JOBS + "/get"
AWS_TOPIC_JOBS_START_NEXT = AWS_TOPIC_JOBS + '/start-next'
AWS_TOPIC_JOBS_START_NEXT_ACCEPTED = AWS_TOPIC_JOBS_START_NEXT + '/accepted'

AWS_TOPIC_STREAM_DATA = '$aws/things/{}/streams/{}/data/json'
AWS_TOPIC_STREAM_REJECTED = '$aws/things/{}/streams/{}/rejected/json'
AWS_TOPIC_STREAM_GET = '$aws/things/{}/streams/{}/get/json'


AWS_TOPIC_STREAMS_DESCRIBE = '$aws/things/{}/streams/{}/describe/json'
AWS_TOPIC_STREAMS_DESCRIPTION = '$aws/things/{}/streams/{}/description/json'

AWS_TOPIC_LOG = '$aws/{}}/things/{}/logs'
AWS_TOPIC_ERROR_LOG = '$aws/{}}/things/{}/logs/errors'

TOPIC_Directive = 'cmd/PabbitLite/{}/directive'
TOPIC_Event = 'cmd/PabbitLite/{}/event'
