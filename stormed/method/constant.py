FRAME_METHOD         = 1 
FRAME_HEADER         = 2 
FRAME_BODY           = 3 
FRAME_HEARTBEAT      = 8 
FRAME_MIN_SIZE       = 4096 
FRAME_END            = 206 
REPLY_SUCCESS        = 200 
CONTENT_TOO_LARGE    = 311 # soft-error
NO_ROUTE             = 312 # soft-error
NO_CONSUMERS         = 313 # soft-error
ACCESS_REFUSED       = 403 # soft-error
NOT_FOUND            = 404 # soft-error
RESOURCE_LOCKED      = 405 # soft-error
PRECONDITION_FAILED  = 406 # soft-error
CONNECTION_FORCED    = 320 # hard-error
INVALID_PATH         = 402 # hard-error
FRAME_ERROR          = 501 # hard-error
SYNTAX_ERROR         = 502 # hard-error
COMMAND_INVALID      = 503 # hard-error
CHANNEL_ERROR        = 504 # hard-error
UNEXPECTED_FRAME     = 505 # hard-error
RESOURCE_ERROR       = 506 # hard-error
NOT_ALLOWED          = 530 # hard-error
NOT_IMPLEMENTED      = 540 # hard-error
INTERNAL_ERROR       = 541 # hard-error

id2constant = {
       1: "FRAME_METHOD",
       2: "FRAME_HEADER",
       3: "FRAME_BODY",
       8: "FRAME_HEARTBEAT",
    4096: "FRAME_MIN_SIZE",
     206: "FRAME_END",
     200: "REPLY_SUCCESS",
     311: "CONTENT_TOO_LARGE",
     312: "NO_ROUTE",
     313: "NO_CONSUMERS",
     403: "ACCESS_REFUSED",
     404: "NOT_FOUND",
     405: "RESOURCE_LOCKED",
     406: "PRECONDITION_FAILED",
     320: "CONNECTION_FORCED",
     402: "INVALID_PATH",
     501: "FRAME_ERROR",
     502: "SYNTAX_ERROR",
     503: "COMMAND_INVALID",
     504: "CHANNEL_ERROR",
     505: "UNEXPECTED_FRAME",
     506: "RESOURCE_ERROR",
     530: "NOT_ALLOWED",
     540: "NOT_IMPLEMENTED",
     541: "INTERNAL_ERROR",
}
