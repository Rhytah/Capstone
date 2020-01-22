import { Injectable } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { FlashMessagesService } from 'angular2-flash-messages';

@Injectable({
  providedIn: 'root'
})
export class HandleHttpErrorService {
  message;

  constructor(public flashMsg: FlashMessagesService) { }
  
  handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      console.error('No response error:', error.error.message);
      this.message = 'Network error!';
    } else {
      console.error('Unsuccessful response error:', error);
      this.message = error.error.message;
      if(typeof(this.message) == "object"){
        if(error.status === 401){
        this.message = this.message.error.description;
      }else{
        this.message = this.message.join('<br>');
      }
      }
      console.log(this.message);
      if(error.status === 0){
        this.message = 'Network error';
      }
    }
    this.flashMsg.show(this.message, { cssClass: 'alert-danger', timeout: 10000 });
  }
}
