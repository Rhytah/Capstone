import { Component, OnInit } from '@angular/core';
import { Movie, singleMovie } from 'src/app/models/movie';
import { MovieService } from 'src/app/services/movie.service';
import { FlashMessagesService } from 'angular2-flash-messages';
import { HandleHttpErrorService } from 'src/app/services/handle-http-error.service';

@Component({
  selector: 'app-movie-details',
  templateUrl: './movie-details.component.html',
  styleUrls: ['./movie-details.component.css']
})
export class MovieDetailsComponent implements OnInit {
  movie:singleMovie[];
  id:number;
  title:string;
  release_date:string;
  description:string;
  image_link:string;
  facebook_link:string;
  website:string;
  loading:boolean = false;

  constructor(
    private movieService:MovieService,
    public flashMsg: FlashMessagesService,
    private HandleHttpError: HandleHttpErrorService
  ) { }

  ngOnInit() {
    this.getSingleMovie(this.id)
  }

  update(movie: singleMovie) {
    this.id = movie.id;
    this.title = movie.title;
    this.description = movie.description;
  }

  delete(id: number) {
    this.loading = true;
    this.movieService.deleteMovies(id).subscribe(resp => {
      this.loading = false;
      this.getSingleMovie(id)
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    })
  }

  getSingleMovie(id) {
    this.loading = true;
    this.movieService.getSingleMovie(id).subscribe(movie => {
      this.loading = false;
      console.log("result",movie)
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    });
  }
}