import sys
from logger import logging

def err_msg_dtls(error,errordetail:sys):
    _,_,exc_tbl=errordetail.exc_info()

    file_name=exc_tbl.tb_frame.f_code.co_filename
    line_num=exc_tbl.tb_lineno
    err=error

    errmsg=f"Error occured in python script name {file_name} line number {line_num} and error message is {err}"
    return errmsg




class CustomException(Exception):
    def __init__(self,err_msg,errordetail:sys):
        super().__init__(err_msg)
        self.err_msg=err_msg_dtls(err_msg,errordetail)

    def __str__(self):
        return self.err_msg
    

if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
        logging.info('Divide by 0 err')
        raise CustomException(e,sys)    
