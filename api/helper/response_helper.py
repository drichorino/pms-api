class ResponseHelper:
    
    def success(payload, message):    
    
        return { 
                "payload" : payload, 
                "message" : message 
                }
    
    
    def failed(message):    
    
        return { 
                "message" : message 
                }
