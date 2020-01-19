import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Actor } from '../models/actor';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service'

@Injectable({
  providedIn: 'root'
})
export class ActorService {
  apiServerUrl:string = environment.apiServerUrl;
  options = {
    headers: new HttpHeaders({
      "content-Type": "application/json",
      Authorization: "Bearer " + this.authService.activeJWT()
    })
  };

  constructor(
    private http:HttpClient,
    private authService:AuthService
  ) { }

  getActors():Observable<any> {
    return this.http.get<any>(`${this.apiServerUrl}/actors`, this.options);
  }

  addActors(actor: Actor):Observable<any> {
    return this.http.post<any>(`${this.apiServerUrl}/actors`, actor, this.options);
  }

  editActors(actor: Actor):Observable<any> {
    return this.http.patch<any>(`${this.apiServerUrl}/actors/${actor.id}`, actor, this.options);
  }

  deleteActors(id: number):Observable<any> {
    return this.http.delete<any>(`${this.apiServerUrl}/actors/${id}`, this.options);
  }

}
