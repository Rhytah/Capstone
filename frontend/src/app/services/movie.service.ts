import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Movie } from '../models/movie';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service'

@Injectable({
  providedIn: 'root'
})
export class MovieService {
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

  getMovies():Observable<any> {
    return this.http.get<any>(`${this.apiServerUrl}/movies`, this.options);
  }

  addMovies(movie: Movie):Observable<any> {
    return this.http.post<any>(`${this.apiServerUrl}/movies`, movie, this.options);
  }

  editMovies(movie: Movie):Observable<any> {
    return this.http.patch<any>(`${this.apiServerUrl}/movies/${movie.id}`, movie, this.options);
  }

  deleteMovies(id: number):Observable<any> {
    return this.http.delete<any>(`${this.apiServerUrl}/movies/${id}`, this.options);
  }

}
