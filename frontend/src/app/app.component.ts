import { Component } from '@angular/core';
import { AuthService } from './services/auth.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  title:string = 'Capstone Casting Agency';
  loginURL:string;
  token:string;

  constructor(
    public auth: AuthService
  ) {
    this.loginURL = auth.build_login_link('/');
  }

  ngOnInit() {
    // Perform required auth actions
    this.auth.load_jwts();
    this.auth.check_token_fragment();
    this.token = this.auth.token;
  }

  setTitle = (value: string) => {
    this.title = value;
  }
  
}
