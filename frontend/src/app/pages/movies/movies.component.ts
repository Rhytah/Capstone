import { Component, OnInit } from '@angular/core';
import { Movie } from '../../models/movie';
import { MovieService } from '../../services/movie.service'
import { FlashMessagesService } from 'angular2-flash-messages';
import { HandleHttpErrorService } from '../../services/handle-http-error.service'

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  styleUrls: ['./movies.component.css']
})
export class MoviesComponent implements OnInit {

  movies:Movie[];
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
    this.getMovies()
  }

  onSubmit() {
    const movie = {
      id: this.id,
      title: this.title,
      release_date: this.release_date,
      description: this.description,
      facebook_link:this.facebook_link,
      website:this.website,
      image_link: this.image_link
   
    };

    if(this.id){
      this.loading = true;
      this.movieService.editMovies(movie).subscribe(resp => {
        this.loading = false;
        this.getMovies()
      }, err => {
        this.loading = false;
        this.HandleHttpError.handleError(err)
      })
    }
    else {
      this.loading = true;
      this.movieService.addMovies( movie).subscribe(resp => {
        this.loading = false;
        this.getMovies()
      }, err => {
        this.loading = false;
        this.HandleHttpError.handleError(err)
      })
    }

    this.id = null;
    this.title = null;
    this.release_date = null;
  }

  update(movie: Movie) {
    this.id = movie.id;
    this.title = movie.title;
    this.release_date = movie.release_date;
  }

  delete(id: number) {
    this.loading = true;
    this.movieService.deleteMovies(id).subscribe(resp => {
      this.loading = false;
      this.getMovies()
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    })
  }

  getMovies() {
    this.loading = true;
    this.movieService.getMovies().subscribe(movies => {
      this.loading = false;
      this.movies = movies.movies;
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    });
  }

}
